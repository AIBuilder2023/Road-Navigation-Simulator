import networkx as nx
from attributes import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from time import time,localtime,strftime



def draw(G,passed,avg_time,avg_speed):
    pos = nx.spring_layout(G, seed=114514,weight="weight")
    edges = G.edges()

    #color
    cmap = cm.RdYlGn_r
    norm = mcolors.Normalize(vmin=0, vmax=1)
    colors = [cmap(norm(sum(G[e[0]][e[1]]["congestion_logs"]) / len(G[e[0]][e[1]]["congestion_logs"]))) for e in edges]

    #label
    edge_labels = nx.get_edge_attributes(G, "length")

    #edge-width
    width = [(G[i[0]][i[1]]["capacity"]/G[i[0]][i[1]]["length"])*2 for i in edges]


    #draw
    fig, ax = plt.subplots(figsize=(15*PIC_SCALE, 11.25*PIC_SCALE))
    #plt.figure(figsize=(15, 11.25))
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,font_size=19)
    nx.draw_networkx_edges(G, pos, width=width, alpha=0.6, edge_color=colors)


    text_font_size = 18*PIC_SCALE

    plt.title("Traffic Simulation Result - Congestion",size=text_font_size)
    plt.axis("off")

    stats = (f"SPEED: {SPEED}\n"
             f"Car passed: {passed}\n"
             f"Avg time cost: {round(avg_time, 3)}({round(avg_time * FPS, 3)}frames)\n"
             f"Avg speed: {round(avg_speed, 3)}")
    fig.text(
        0.02,
        0.05,
        stats,
        fontsize=text_font_size,
        ha="left",
        va="bottom"
    )
    fig.savefig(f"logs/results/congestion-{strftime('%Y%m%d-%H%M%S',localtime(time()))}.png")

    plt.close('all')