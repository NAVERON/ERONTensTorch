

import time
import numpy as np
import pandas as pd
import math
import datetime



class Ship():  # 训练对象的属性
    
    
    def __init__(self, position=np.array([500, 300], dtype=np.float), velocity=np.array([2, 4], dtype=np.float)):  # 矩阵
        self.id = self.setID()
        self.K = 0.0785
        self.T = 3.12
        self.rudder = 0
        
        self.position = position
        self.velocity = velocity
        
    def setID(self):
        return datetime.datetime.now().strftime("%d%H%M%S%f")
    def courseTurn(self, dc):  # dc代表变化的方向
        # 返回 新的速度矢量，将事例的速度重新设置
        dc_radius = np.radians(-dc)  # 转换成弧度
        c, s = np.cos(dc_radius), np.sin(dc_radius)
        R = np.array([ [c, -s], [s, c] ])
        # print(R)
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
        delta = self.K * self.rudder * (1 - self.T + self.T * math.exp(-1 / self.T))
        self.courseTurn(delta)
        self.position += self.velocity  # 这样就更新位置了
    
    def toString(self):
        return "id:" + self.id + " , position:" + str(self.position) + " , velocity:" + str(self.velocity)

# 总体调用部件

from tkinter import *

class Viewer():
    
    def __init__(self):
        self.tk = Tk()
        self.canvas=Canvas(self.tk, width=1000, height=800)
        self.canvas.pack()
        # 创建好绘制面板后 需要添加Entity实体运动物
        self.ships = []
        for _ in range(10):
            self.ships.append(self.createRandomEntity())
        print("生成随机的10个Ship")
        
    def createRandomEntity(self):
        position = np.multiply([np.random.rand(), np.random.rand()], 600)
        velocity = np.multiply([np.random.rand(), np.random.rand()], 4)
        entity = Ship(np.array(position), np.array(velocity))
        time.sleep(0.001)
        return entity
    
    def step(self):
        for s in self.ships:
            print(s.toString())
            s.goAhead()
            print(s.toString())
        pass

i=0
if __name__ == "__main__":
    ship = Ship( np.array([23, 19], dtype=np.float), np.array([0, 10], dtype=np.float) )
    ship.goAhead()
    
    env = Viewer()
    env.step()
















