import attributes
import imageio
from io import BytesIO


def congestion_calculation(G,cars):
    edges = G.edges()
    for edge in edges:
        G[edge[0]][edge[1]]['cars'] = 0
    for i in cars:
        if not i.destination:
            G[i.route[i.progress]][i.route[i.progress + 1]]['cars'] += 1
    for edge in edges:
        if G[edge[0]][edge[1]]['cars'] <= G[edge[0]][edge[1]]['capacity'] / G[edge[0]][edge[1]]['length']:
            G[edge[0]][edge[1]]['congestion'] = 0
        else:
            G[edge[0]][edge[1]]['congestion'] = G[edge[0]][edge[1]]['cars'] / G[edge[0]][edge[1]]['capacity']
        G[edge[0]][edge[1]]['congestion_logs'].append(G[edge[0]][edge[1]]['congestion'])

def cars_run(G,cars,SPEED):
    for i in cars:
        if not i.destination:
            if G[i.route[i.progress]][i.route[i.progress + 1]]['congestion'] <= 0.1:
                i.distance += SPEED / G[i.route[i.progress]][i.route[i.progress + 1]]['length']
                i.tot_distance += SPEED / G[i.route[i.progress]][i.route[i.progress + 1]]['length']
            elif G[i.route[i.progress]][i.route[i.progress + 1]]['congestion'] <= 0.4:
                i.distance += SPEED / 2 / G[i.route[i.progress]][i.route[i.progress + 1]]['length']
                i.tot_distance += SPEED / 2 / G[i.route[i.progress]][i.route[i.progress + 1]]['length']
            elif G[i.route[i.progress]][i.route[i.progress + 1]]['congestion'] <= 0.6:
                i.distance += SPEED / 3 / G[i.route[i.progress]][i.route[i.progress + 1]]['length']
                i.tot_distance += SPEED / 3 / G[i.route[i.progress]][i.route[i.progress + 1]]['length']
            else:
                i.distance += SPEED / 4 / G[i.route[i.progress]][i.route[i.progress + 1]]['length']
                i.tot_distance += SPEED / 4 / G[i.route[i.progress]][i.route[i.progress + 1]]['length']

            if i.distance >=1:
                i.progress += 1
                i.distance = 0

            i.time_cost += 1

def cars_finish(cars):
    for i in cars:
        if i.route[i.progress] == i.endPt and not i.destination:
            i.destination = True

def whole_process(G,cars,SPEED):
    congestion_calculation(G,cars)
    cars_run(G,cars,SPEED)
    cars_finish(cars)