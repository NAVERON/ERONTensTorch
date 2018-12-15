

import time
import numpy as np
import math
import datetime
import queue


class Ship():  # 训练对象的属性
    
    K = 0.0785
    T = 3.12
    
    def __init__(self, position=np.array([500, 400], dtype=np.float), velocity=np.array([2, 4], dtype=np.float)):  # 矩阵
        self.id = self.setID()
        
        self.rudder = 0
        self.position = position
        self.velocity = velocity
        
        self.q = queue.Queue(maxsize=10)
        
    def setID(self):
        return datetime.datetime.now().strftime("%d%H%M%S%f")
    def courseTurn(self, dc):  # dc代表变化的方向
        # 返回 新的速度矢量，将事例的速度重新设置
        dc_radius = np.radians(-dc)  # 转换成弧度
        c, s = np.cos(dc_radius), np.sin(dc_radius)
        R = np.array([ [c, -s], [s, c] ])
        # print(R)
        self.velocity = np.dot(R, self.velocity.T).T
        
        #print(self.id, "id:", self.velocity)
        
    def velocityChange(self, dv): # 根据dv  修改原速度矢量
        self.velocity += dv
    def rudderChange(self, dr):  # 舵角变化    范围为每次一度
        self.rudder += dr
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
    
    def goAhead(self, viewer):
        # 边界判断    设置为不能超越边界
        if self.position[0] < 0:
            self.position[0] = viewer.winfo_width()
        elif self.position[0] > viewer.winfo_width():
            self.position[0] = 0
        elif self.position[1] < 0:
            self.position = viewer.winfo_height()
        elif self.position[1] > viewer.winfo_height():
            self.position[1] = 0
        
        if self.q.full():  # 如果队列满了，就取出
            self.q.get()
        self.q.put(self.position)
        
        delta = self.K * self.rudder * (1 - self.T + self.T * math.exp(-1 / self.T))
        self.courseTurn(delta)
        self.position += self.velocity  # 这样就更新位置了    ====  可以把界面更新放到数据更新里面同步，更好
        
    def isCollision(self, other):
        dis = np.linalg.norm(other.position-self.position)
        if dis < 30:
            return False
        
        return True
    
    
    def toString(self):
        return "id:" + self.id + " , position:" + str(self.position) + " , velocity:" + str(self.velocity)

# 总体调用部件

from tkinter import *


class Viewer():
    
    running = True
    
    def __init__(self):
        self.tk = Tk()
        self.canvas = Canvas(self.tk, width=1000, height=600)
        self.ships = []
        for _ in range(10):
            self.ships.append(self.createRandomEntity())
        self.canvas.pack()
        
        self.render()
        self.tk.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        self.running = False
        self.tk.update()
        time.sleep(0.01)
        #self.tk.destroy()
    
    def createRandomEntity(self):
        position = np.multiply([np.random.rand(), np.random.rand()], 600)
        velocity = np.multiply([np.random.rand(), np.random.rand()], 2)
        entity = Ship(np.array(position), np.array(velocity))
        time.sleep(0.001)
        return entity
    
    drawer_ships = []
    def render(self):  # 根据当前状况绘制
        for entity in self.drawer_ships:
            self.canvas.delete(entity)
        self.drawer_ships.clear()
        
        for s in self.ships:
            self.drawer_ships.append(self.canvas.create_oval(s.position[0]-10, s.position[1]-10, s.position[0]+10, s.position[1]+10, fill="black"))
        
        self.tk.update()
        
    def step(self, action):
        # 这里先做动作，舵角，速度变化等
        self.render()  #渲染当前画面
        
        for s in self.ships:
            s.goAhead(self.tk)
        time.sleep(0.01)
        
        return 0, 0, False
        pass
    def reset(self):  # 重置环境和变量的条件
        return 0
        pass
    
    def sampleAction(self):
        pass
    def getState(self):
        pass


if __name__ == "__main__":
    
    view = Viewer()
    
    while view.running:
        view.step(0)
        
    
    















