import random
import networkx as nx
from attributes import *
def create_road_graph(road_cfg:Config_road_generator):
    """ create road graph randomly"""
    G = nx.Graph()
    G.add_nodes_from(range(road_cfg.num_nodes))
    G.add_node()
    #make sure all nodes are connected together
    nodes = list(G.nodes)
    for i in range(1,road_cfg.num_nodes):
        length = random.randint(1, 7)
        capacity = length * random.randint(1, road_cfg.max_lanes)
        G.add_edge(i, i-1,
                   weight=1/ length,
                   length=length,
                   capacity=capacity,
                   congestion=0.0,
                   cars=0,
                   congestion_logs=[])

    #ring
    if road_cfg.ring:
        length = random.randint(1, 7)
        capacity = length * random.randint(1, road_cfg.max_lanes)
        G.add_edge(0, road_cfg.num_nodes-1,
                   weight=1 / length,
                   length=length,
                   capacity=capacity,
                   congestion=0.0,
                   cars=0,
                   congestion_logs=[])

    #random connection
    for i in range(road_cfg.num_nodes):
        for j in range(i + 1, road_cfg.num_nodes):
            if random.random() < road_cfg.edge_prob:
                if G.degree[i] < road_cfg.max_degree and G.degree[j] < road_cfg.max_degree \
                    and abs(i-j)<=road_cfg.connection_limit \
                    and not i in road_cfg.force_single_road\
                    and not j in road_cfg.force_single_road:
                    length = random.randint(1, 7)
                    capacity = length*random.randint(1, road_cfg.max_lanes)
                    G.add_edge(i, j,
                               weight=1/length,
                               length=length,
                               capacity=capacity,
                               congestion=0.0,
                               cars=0,
                               congestion_logs=[])

    return G