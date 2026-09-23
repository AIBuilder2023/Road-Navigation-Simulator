"""
This is the road generation algorithm following real-life traffic situation
the model will be similar to a tiled map
Some attributes:
Average 3 road per node
for each node:
1 way - 18%
3 way - 62%
4 way - 19%-21%
"""
from dataclasses import dataclass
from attributes import *
import math
import random
import networkx as nx

UP = [0,1]
DOWN = [0,-1]
LEFT = [-1,0]
RIGHT = [1,0]
#x+y*2
DIRECTIONS = {
    -1:2, #left
    1:0, #right
    2:1, #up
    -2:3 #down
}
INDEX_TO_DIR = [[1,0],[0,1],[-1,0],[0,-1]]

@dataclass
class Node:
    id: int
    pos: list
    tiled_pos: list
    #connection [right,up,left,down] n=connected to node id n  None=not
    #NOTE: None is used instead of 0, because node 0 is a valid node id
    connection: list
    degrees: int=0

@dataclass
class Road:
    ptA: int
    ptB: int
    length: float

def default_road(road_cfg:Config_road_generator):
    """the road generation algorithm following real-life traffic situation
    returns a networkx Graph, a drop-in replacement of core.road.create_road_graph"""
    ''' step 1 - initialization '''
    ''' the expected attributes will be calculated '''

    exp = [int(road_cfg.num_nodes*0.18),int(road_cfg.num_nodes*0.62),int(road_cfg.num_nodes*0.2)]
    origin = Node(0,[0,0],[0,0],[None,None,None,None])
    num = 1
    occupied_pos = [[0,0]]
    nodes = [origin]
    roads = []
    #degrees 0..4, so 5 buckets are needed
    nodes_degrees = [[],[],[],[],[]]

    def new_road(a:Node,b:Node):
        road = Road(a.id,b.id, math.dist(a.pos,b.pos))
        roads.append(road)
        a.degrees += 1
        b.degrees += 1

    def has_edge(a:Node,b:Node):
        """whether a road between a and b already exists"""
        return any({r.ptA,r.ptB} == {a.id,b.id} for r in roads)

    def new_node(id:int,father:Node,direction:list):
        nonlocal num

        #mark the father nodes connection as CONNECTED
        direction_index = DIRECTIONS[direction[0]+direction[1]*2]
        father.connection[direction_index] = id

        #calculate the position of the node
        angle = math.pi*(direction_index/2) + (random.random()*road_cfg.angle_variation*2-road_cfg.angle_variation)
        distance = road_cfg.exp_road_length * (1 + random.random()*road_cfg.var_road_length*2-road_cfg.var_road_length)
        x = father.pos[0]+math.cos(angle)*distance
        y = father.pos[1]+math.sin(angle)*distance
        tx = father.tiled_pos[0]+direction[0]
        ty = father.tiled_pos[1]+direction[1]

        #set the connection status
        conn = [None,None,None,None]
        conn[(direction_index + 2) % 4] = father.id

        #create node and push in to the list
        node = Node(id, [x, y], [tx, ty], conn, 0)
        nodes.append(node)
        new_road(father,node)

        #update variables
        occupied_pos.append([tx,ty])
        num += 1

    #start randomly generate nodes
    for i in range(road_cfg.num_nodes):
        #choose a random existed node
        while True:
            father = random.choice(nodes)
            founded = False
            direction = random.randint(0,3)
            for _ in range(4):
                if father.connection[direction] is None:
                    if not [father.tiled_pos[0]+INDEX_TO_DIR[direction][0],father.tiled_pos[1]+INDEX_TO_DIR[direction][1]] in occupied_pos:
                        founded = True
                        break
                direction = (direction+1)%4
            if founded:
                break
        new_node(num,father,INDEX_TO_DIR[direction])

    #calculate the number of nodes having specific degrees
    for i in nodes:
        nodes_degrees[i.degrees].append(i)
    max_d = road_cfg.exp_road_length * (1+road_cfg.var_road_length)

    targets = {1: exp[0], 3: exp[1], 4: exp[2]}
    for deg, target in targets.items():
        while sum(1 for n in nodes if n.degrees == deg) < target:
            pool = [n for n in nodes if n.degrees == deg - 1]
            if not pool:
                break
            a = random.choice(pool)
            cand = [b for b in nodes if b is not a and b.degrees < 4
                    and math.dist(a.pos, b.pos) <= max_d
                    and not has_edge(a, b)]
            if not cand:
                break
            #NOTE: these extra roads are not aligned to the tiled grid, so they
            #are NOT written into node.connection (only into the roads list)
            new_road(a, random.choice(cand))

    ''' step 3 - turn the generator output into the Graph the simulation uses '''
    G = nx.Graph()
    for n in nodes:
        #x/y are the real coordinates, tiled_pos is the grid cell of the node
        G.add_node(n.id,
                   pos=(n.pos[0], n.pos[1]),
                   x=n.pos[0],
                   y=n.pos[1],
                   tiled_pos=(n.tiled_pos[0], n.tiled_pos[1]),
                   degrees=n.degrees,
                   connection=tuple(n.connection))
    for r in roads:
        lanes = random.randint(1, road_cfg.max_lanes)
        #length is the real geometric distance, so the A* heuristic stays consistent
        G.add_edge(r.ptA, r.ptB,
                   weight=1 / r.length,
                   length=r.length,
                   lanes=lanes,
                   capacity=r.length * lanes,
                   congestion=0.0,
                   cars=0,
                   congestion_logs=[])

    return G