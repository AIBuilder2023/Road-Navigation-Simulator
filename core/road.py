import random
import networkx as nx
from attributes import *
def create_road_graph(cfg:Config_road_generator):
    """ create road graph randomly"""
    G = nx.Graph()
    G.add_nodes_from(range(cfg.num_nodes))

    #make sure all nodes are connected together
    nodes = list(G.nodes)
    for i in range(1,cfg.num_nodes):
        length = random.randint(1, 7)
        capacity = length * random.randint(1, MAX_LANES)
        G.add_edge(i, i-1,
                   weight=1/ length,
                   length=length,
                   capacity=capacity,
                   congestion=0.0,
                   cars=0,
                   congestion_logs=[])

    #ring
    if RING:
        length = random.randint(1, 7)
        capacity = length * random.randint(1, MAX_LANES)
        G.add_edge(0, cfg.num_nodes-1,
                   weight=1 / length,
                   length=length,
                   capacity=capacity,
                   congestion=0.0,
                   cars=0,
                   congestion_logs=[])

    #random connection
    for i in range(cfg.num_nodes):
        for j in range(i + 1, cfg.num_nodes):
            if random.random() < EDGE_PROB:
                if G.degree[i] < cfg.max_degree and G.degree[j] < cfg.max_degree \
                    and abs(i-j)<=CONNECTION_LIMIT \
                    and not i in cfg.force_single_road\
                    and not j in cfg.force_single_road:
                    length = random.randint(1, 7)
                    capacity = length*random.randint(1, MAX_LANES)
                    G.add_edge(i, j,
                               weight=1/length,
                               length=length,
                               capacity=capacity,
                               congestion=0.0,
                               cars=0,
                               congestion_logs=[])

    return G