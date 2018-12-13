

import time
from tkinter import *
import numpy as np
import pandas as pd
import math
import datetime


class Ship():
    
    K = 0.0785
    T = 3.12
    
    def __init__(self, position, velocity):  # 以字典形式传入数据
        self.id = self.setID()
        self.rudder = 0
        
        self.position = position
        self.velocity = velocity
    
    def setID(self):
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    def getVelocity(self):
        return self.velocity
    
    def getSpeed(self):
        return math.sqrt(self.velocity.x * self.velocity.x + self.velocity.y * self.velocity.y)
    
    def calAngle(self, dx, dy):   # 计算的角度按照顺时针旋转，正向向上是0度角
        theta = math.atan2(dx, dy)
        angle = math.degrees(theta)
        if angle < 0:
            angle += 360
        return angle
    
    def toString(self):
        return "id:" + self.id + " , position:" + str(self.position["x"]) + " , velocity:" + str(self.velocity["vx"])
    
class Env():
    def __init__(self):
        pass
    
    def step(self):
        pass


if __name__ == "__main__":
    ship = Ship( {"x":23, "y":19}, {"vx":2, "vy":5} )
    print( ship.toString() )
    print(ship.calAngle(-1, 100))

















