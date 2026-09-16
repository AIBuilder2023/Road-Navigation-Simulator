from core.road import *
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


cfg_road = Config_road_generator(100,5,4,0.2,[],10,True)
cfg_car = Config_car_generator(100,0.2)

G = create_road_graph(cfg_road)
pos = nx.spring_layout(G, seed=114514,weight="weight")

edges = G.edges()
nodes = G.nodes()
#print(edges)
cars = []
num_cars = 0
for i in range(NUM_CARS_INITIALLY):
    cars.append(car.car(cfg_road.num_nodes,pos))
    astarRes = astar.astar(G,cars[i].startPt, cars[i].endPt,pos)
    cars[i].route = astarRes
    num_cars += 1

frames = []
for t in tqdm(range(FRAMES+1)):
    processing.whole_process(G,cars,SPEED)
    if SHOW_MID_PROCESS and t%FRAMES_PER_OUTPUT==0:
        visualize.draw(G,cars,t,frames)
    if random.random() < NEW_CAR_PROB:
        cars.append(car.car(cfg_road.num_nodes, pos))
        astarRes = astar.astar(G, cars[num_cars].startPt, cars[num_cars].endPt, pos)
        cars[num_cars].route = astarRes
        num_cars += 1

passed = 0
tot_time = 0
tot_avg_speed = 0
for i in cars:
    if i.destination:
        passed += 1
        tot_time += i.time_cost / FPS
        tot_avg_speed += i.tot_distance / i.time_cost * FPS
avg_time = tot_time/passed
avg_speed = tot_avg_speed / passed
result_congestion.draw(G,passed,avg_time,avg_speed)
if GENERATE_GIF:
    imageio.mimsave(f"logs/gif/traffic{strftime('%Y%m%d-%H%M%S',localtime(time()))}.gif", frames, fps=FPS)