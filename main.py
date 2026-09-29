import networkx as nx
from road_generation.Default import default_road
import core.car as car
import algorithm.astar as astar
import visualize.road_draw as visualize
import visualize.result_congestion as result_congestion
import core.car_simulation as processing
from attributes import *

from time import time,localtime,strftime
import random
from tqdm import tqdm
import imageio

''' CONFIG '''
cfg_road = Config_road_generator(
    num_nodes=30 ,
    max_lanes=5,
    max_degree=4,
    edge_prob=0.2,
    force_single_road=[],
    connection_limit=10,
    ring=True,
    exp_road_length=10,
    var_road_length=0.2,
    angle_variation=0.1)
cfg_car = Config_car_generator(
    num_cars_initially=40*200,
    new_car_prob=1,
)
cfg_simulation = Config_simulator(
    standard_speed=80
)

''' CREATE GRAPH '''
G = default_road(cfg_road)
#the coordinates come from the generator itself, no spring_layout needed
pos = nx.get_node_attributes(G, "pos")
edges = G.edges()
nodes = G.nodes()
print(G[0][1],G[1][0])
print(pos)
print(edges)
print(nodes)
''' GENERATE FIRST CROWD OF CARS '''
cars = []
num_cars = 0
for i in range(cfg_car.num_cars_initially):
    cars.append(car.car(cfg_road.num_nodes,pos))
    astarRes = astar.astar(G,cars[i].startPt, cars[i].endPt,pos)
    cars[i].route = astarRes
    num_cars += 1
''' PROCESSING '''
frames = []

for t in tqdm(range(FRAMES+1)):
    processing.whole_process(G,cars,cfg_car,cfg_simulation)
    if SHOW_MID_PROCESS and t%FRAMES_PER_OUTPUT==0:
        visualize.draw(G,cars,t,frames,cfg_simulation.standard_speed)
    if random.random() < cfg_car.new_car_prob:
        cars.append(car.car(cfg_road.num_nodes, pos))
        astarRes = astar.astar(G, cars[num_cars].startPt, cars[num_cars].endPt, pos)
        cars[num_cars].route = astarRes
        num_cars += 1

''' CALCULATE RESULTS'''
passed = 0
tot_time = 0
tot_avg_speed = 0
for i in cars:
    if i.destination:
        passed += 1
        tot_time += i.time_cost
        tot_avg_speed += i.tot_distance / i.time_cost
avg_time = tot_time/passed
avg_speed = tot_avg_speed/num_cars
result_congestion.draw(G,passed,avg_time,avg_speed,cfg_simulation.standard_speed)
if GENERATE_GIF:
    imageio.mimsave(f"logs/gif/traffic{strftime('%Y%m%d-%H%M%S',localtime(time()))}.gif", frames, fps=FPS)