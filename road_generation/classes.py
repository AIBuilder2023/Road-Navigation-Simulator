from dataclasses import dataclass

@dataclass
class Node:
    id: int
    pos: list
    tiled_pos: list
    #connection [right,up,left,down] n=connected to node id n  None=not
    #NOTE: None is used instead of 0, because node 0 is a valid node id
    connection: list
    degrees: int=0
    def asdict(self):
        return {'id':self.id,"pos":self.pos,"tiled_pos":self.tiled_pos,"connection":self.connection,"degrees":self.degrees}

@dataclass
class Road:
    ptA: int
    ptB: int
    length: float
    lanes: int
    def asdict(self):
        return {"ptA":self.ptA,"ptB":self.ptB,"length":self.length}