"""Change the attributes of the program here"""
from dataclasses import dataclass

""" ROAD GENERATION """
@dataclass
class Config_road_generator:
    # Number of nodes in the diagram
    num_nodes: int
    # Maximum lanes a road can have
    # The capacity of the road = length * lanes
    max_lanes: int
    # The maximum nodes a node can connect to
    max_degree: int
    # The probability of generating a connection to other nodes
    edge_prob: float
    # The ID of a list of nodes forcing to have a maximum degree of 2
    force_single_road: list
    # The connection limit of a node
    # e.g. if it is 4, then node 12 cannot connect with node 20 as is it too far apart
    connection_limit: int
    # whether to make a ring connection.
    # this will force to create a connection between the first node and the last node
    ring: bool
    #expected average road length
    exp_road_length: float
    #variance of road length [0.00,1.00)
    var_road_length: float
    #variation of the angle [-pi/4,pi/4]
    angle_variation: float

""" CARS """
@dataclass
class Config_car_generator:
    # Number of cars generated when the simulation starts
    num_cars_initially: int
    # The probability of generating a car every FRAME
    new_car_prob: float
    #maximum speed of a car to run if there is no congestion(km/h)
    speed: int
#Number of cars generated when the simulation starts
NUM_CARS_INITIALLY = 200
#The probability of generating a car every FRAME
NEW_CAR_PROB = 0.4

#pic
#Frame per second
#Also representing frame per hour simulated in the program
#This will affect the speed of car per frame and the generation of GIF file
FPS = 240

#The total frames in the simulatiom
FRAMES = 24*60*30
#The scale of every PNG file generated
PIC_SCALE = 2
#Whether generate pictures of the mid-process in the simulation
SHOW_MID_PROCESS = False
#The frequency of generating mid-process pictures
#This will only be effective when SHOW_MID_PROCESS is True
FRAMES_PER_OUTPUT = 30
#Whether automatically generate GIF file when the simulating
#This will only be effective when SHOW_MID_PROCESS is True
#If it is true, the mid-process pictures will not be generated
GENERATE_GIF = False
