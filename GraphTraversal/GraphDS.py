from math import floor

class graphnode:        
    def __init__(self,name:str, X:int, Y:int, node_width) -> None:
        self.name = name
        self.x = X
        self.y = Y
        self.adjacent = []
        self.node_width = node_width
    
    def set_adjacent(self, adjacent:list['graphedge']) -> None:
        self.adjacent = adjacent

    # Heuristic function
    def get_sld(self, destination:'graphnode') -> int:
        return floor(((destination.x - self.x) ** 2 + (destination.y - self.y) ** 2) ** 0.5)

class graphedge:
    def __init__(self, pointA:graphnode, pointB:graphnode, distance:int):
        self.pointA = pointA
        self.pointB = pointB
        self.distance = distance