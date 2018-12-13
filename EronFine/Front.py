

import time
import numpy as np
import pandas as pd
import math
import datetime



class Ship():
    
    K = 0.0785
    T = 3.12
    
    def __init__(self, position, velocity):  # 矩阵
        self.id = self.setID()
        self.rudder = 0
        
        self.position = position
        self.velocity = velocity
    
    def setID(self):
        return datetime.datetime.now().strftime("%d%H%M%S%f")
    def courseTurn(self, dc):  # dc代表变化的方向
        # 返回 新的速度矢量，将事例的速度重新设置
        dc_radius = np.radians(dc)  # 转换成弧度
        c, s = np.cos(dc_radius), np.sin(dc_radius)
        R = np.array([ [c, -s], [s, c] ])
        self.velocity = np.dot(R, self.velocity.T).T
        
    def velocityChange(self, dv): # 根据dv  修改原速度矢量
        self.velocity += dv
    
    def getSpeed(self):  # 速度大小
        return np.linalg.norm(self.velocity)
    def getCourse(self): # 运动方向
        return self.calAngle(self.velocity[0], self.velocity[1])
        
    def calAngle(self, dx, dy):   # 计算的角度按照顺时针旋转，正向向上是0度角
        theta = math.atan2(dx, dy)
        angle = math.degrees(theta)
        if angle < 0:
            angle += 360
        return angle
    
    def goAhead(self):
        
        pass
    
    def toString(self):
        return "id:" + self.id + " , position:" + str(self.position[0]) + " , velocity:" + str(self.velocity[0])

# 总体调用部件

from tkinter import *

class Viewer():
    
    def __init__(self):
        self.tk = Tk()
        self.canvas=Canvas(self.tk, width=1000, height=800)
        self.canvas.pack()
        self.canvas.create_oval(20, 20, 50, 50, fill="#476042")
    
    def step(self):
        pass


if __name__ == "__main__":
    ship = Ship( np.array([23, 19]), np.array([0, 10]) )
    ship.courseTurn(45)
    print(ship.velocity)
    env = Viewer()
    env.step()
    
















