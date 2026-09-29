import attributes
import imageio
from io import BytesIO
from attributes import Config_simulator, Config_car_generator

def speed_calculation(road:dict,cfg_simulation:Config_simulator):
    if road['cars'] == 0:
        v = cfg_simulation.standard_speed
    else:
        v = max(cfg_simulation.minimum_speed, min(
            cfg_simulation.standard_speed, max(
                0, ((road['lanes'] * road['length'] / road[
                    'cars'] - cfg_simulation.car_length - cfg_simulation.minimum_distance) / cfg_simulation.reaction_time)
            )))
    return v

def congestion_calculation(G,cars,cfg_simulation:Config_simulator):
    edges = G.edges()
    for edge in edges:
        G[edge[0]][edge[1]]['cars'] = 0
    for i in cars:
        if not i.destination:
            G[i.route[i.progress]][i.route[i.progress + 1]]['cars'] += 1
    for edge in edges:
        road = G[edge[0]][edge[1]]
        v = speed_calculation(road,cfg_simulation)
        road['congestion'] = 1-v/cfg_simulation.standard_speed
        road['congestion_logs'].append(road['congestion'])


def cars_run(G,cars,cfg_car:Config_car_generator,cfg_simulation:Config_simulator):
    for i in cars:
        if not i.destination:
            road = G[i.route[i.progress]][i.route[i.progress + 1]]
            v = speed_calculation(road,cfg_simulation)
            v /= attributes.FPS
            i.distance += v
            i.tot_distance += v
            #print(i.distance, road['length'], i.progress)

            if i.distance >= road['length']:
                i.progress += 1
                i.distance = 0
            i.time_cost += 1/attributes.FPS
            if i.route[i.progress] == i.endPt:
                i.destination = True


def whole_process(G,cars,cfg_car,cfg_simulation):
    cars_run(G,cars,cfg_car,cfg_simulation)
    congestion_calculation(G, cars,cfg_simulation)