""" Record the logs of the simulation and store it into logs/reports directory """
from road_generation.classes import Road,Node
Nodes = []
Roads = []
def record_map(node:list[Node],road:list[Road]):
    for i in node:
        Nodes.append(i.asdict())
    for j in road:
        Roads.append(j.asdict())
    print(Nodes)
    print(Roads)
def restore_map(node:list[dict],road:list[dict]):
    Nodes = []
    Roads = []
    for i in node:
        Nodes.append(Node(i['id'],i['pos'],i['tiled_pos'],i['connection'],i['degrees']))
    for j in road:
        Roads.append(Road(j['ptA'],j['ptB'],j['length'],j['lanes']))
    return Nodes,Roads