import networkx as nx
from attributes import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import imageio
from io import BytesIO
import sys

def get_car_position_on_graph(G,car):
    #the real coordinates the generator stored in G
    pos = nx.get_node_attributes(G, "pos")
    fromPt = car.route[car.progress]
    toPt = car.route[car.progress+1]
    fromPos = pos[fromPt]
    toPos = pos[toPt]
    return fromPos[0] + car.distance * (toPos[0] - fromPos[0]), fromPos[1]+car.distance * (toPos[1] - fromPos[1])

def draw(G,cars,t,frames,speed):
    #position - the real coordinates the generator stored in G, no spring_layout
    pos = nx.get_node_attributes(G, "pos")
    #pos = nx.shell_layout(G)
    edges = G.edges()

    #color
    cmap = cm.RdYlGn_r
    norm = mcolors.Normalize(vmin=0, vmax=1)
    colors = [cmap(norm(G[e[0]][e[1]]["congestion"])) for e in edges]

    #label - rounded to 1 decimal, the lengths are real distances now
    edge_labels = {e: round(l, 1) for e, l in nx.get_edge_attributes(G, "length").items()}

    #edge-width
    width = [(G[i[0]][i[1]]["capacity"]/G[i[0]][i[1]]["length"])*2 for i in edges]

    #draw-road
    fig, ax = plt.subplots(figsize=(15*PIC_SCALE, 11.25*PIC_SCALE))
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,font_size=19)
    nx.draw_networkx_edges(G, pos, width=width, alpha=0.6, edge_color=colors)

    #cars
    cars_on_road = 0
    cars_passed = 0
    for i in cars:
        if not i.destination and i.route[i.progress] != i.endPt:
            x,y = get_car_position_on_graph(G,i)
            plt.scatter(x,y,color="red",s=50,zorder=10)
            cars_on_road += 1
        else:
            cars_passed += 1

    text_font_size = 18*PIC_SCALE

    plt.title("Traffic Simulation", size=text_font_size)
    plt.axis("off")

    stats = (f"SPEED: {speed}\n"
             f"Frames: {t}\n"
             f"Cars on road: {cars_on_road}\n"
             f"Cars passed: {cars_passed}")
    fig.text(
        0.02,
        0.05,
        stats,
        fontsize=text_font_size,
        ha="left",
        va="bottom"
    )
    #plt.show()



    if GENERATE_GIF:
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        frames.append(imageio.v2.imread(buf))
    else:
        plt.savefig(f"logs/frames/frame{t}.png")

    plt.close('all')