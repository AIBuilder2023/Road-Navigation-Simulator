import random
from attributes import *

class car():
    def __init__(self,id,NUM_NODES,pos):
        self.id = id
        self.startPt = random.randint(0,NUM_NODES-1)
        self.endPt = self.startPt
        while self.startPt == self.endPt:
            self.endPt = random.randint(0,NUM_NODES-1)
        #self.startPt = pos[self.startPt]
        #self.endPt = pos[self.endPt]
        self.route = []
        self.distance = 0
        self.progress = 0
        self.time_cost = 0
        self.destination = False
        self.tot_distance = 0
        self.logs = []

    def asdict(self):
        return {'id':self.id,'startPt':self.startPt,'endPt':self.endPt,'route':self.route,'time_cost':self.time_cost,'total_distance':self.tot_distance,'logs':self.logs}
