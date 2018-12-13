
import time
from tkinter import *
import numpy as np
import pandas as pd
import math
import datetime


class Ship():
    
    K = 0.0785, T = 3.12
    
    def __init__(self, id, position, velocity):
        self.id = self.setID()
        self.rudder = 0
        
        self.position = position
        self.velocity = velocity
        
    def setID(self):
        return datetime.datetime.now().strftime("%Y%m%d")
    
    def getVelocity(self):
        return self.velocity
    
    def getSpeed(self):
        return math.sqrt(self.velocity.x * self.velocity.x + self.velocity.y * self.velocity.y)
    
    def calAngle(self, dx, dy):
        theta = math.atan2(dy, dx)
        angle = math.degrees(theta)
        return angle
    
    def toString(self):
        return "id:" + self.id + ", position" + self.position + ", velocity" + self.velocity

class Env():
    def __init__(self):
        pass
    
    def step(self):
        pass





















