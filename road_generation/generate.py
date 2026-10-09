import networkx as nx
import random

from road_generation.classes import Node,Road

def generate_graph(nodes:list[Node],roads:list[Road]):
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
        #length is the real geometric distance, so the A* heuristic stays consistent
        G.add_edge(r.ptA, r.ptB,
                   weight=1 / r.length,
                   length=r.length,
                   lanes=r.lanes,
                   capacity=r.length * r.lanes,
                   congestion=0.0,
                   cars=0,
                   congestion_logs=[])
    return G