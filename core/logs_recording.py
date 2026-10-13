""" Record the logs of the simulation and store it into logs/reports directory """
from time import time,localtime,strftime
from road_generation.classes import Road,Node
import networkx as nx

import json

Nodes = []
Roads = []
Cars = []
Congestion = []
def record_map(node:list[Node],road:list[Road]):
    for i in node:
        Nodes.append(i.asdict())
    for j in road:
        Roads.append(j.asdict())
    print("nodes:",Nodes)
    print("roads:",Roads)
def restore_map(node:list[dict],road:list[dict]):
    Nodes = []
    Roads = []
    for i in node:
        Nodes.append(Node(i['id'],i['pos'],i['tiled_pos'],i['connection'],i['degrees']))
    for j in road:
        Roads.append(Road(j['ptA'],j['ptB'],j['length'],j['lanes']))
    return Nodes,Roads
def record_congestion(G:nx.Graph):
    for i in G.edges():
        c = {"endpoints":i,"congestion_logs":G[i[0]][i[1]]["congestion_logs"]}
        Congestion.append(c)
def record_car_logs(cars):
    for i in cars:
        Cars.append(i.asdict())
def save_logs():
    report = {"nodes":Nodes,"roads":Roads,"congestion":Congestion,"car_logs":Cars}
    with open(f"logs/reports/report-{strftime('%Y%m%d-%H%M%S',localtime(time()))}.json",'w') as f:
        json.dump(report,f)

