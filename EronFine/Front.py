

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
        return datetime.datetime.now().strftime("%d%H%M%S%f")
    
    def getVelocity(self):
        return self.velocity
    
    def getSpeed(self):
        return math.sqrt(self.velocity["vx"] * self.velocity["vx"] + self.velocity["vy"] * self.velocity["vy"])
    
    def calAngle(self, dx, dy):   # 计算的角度按照顺时针旋转，正向向上是0度角
        theta = math.atan2(dx, dy)
        angle = math.degrees(theta)
        if angle < 0:
            angle += 360
        return angle
    
    def toString(self):
        return "id:" + self.id + " , position:" + str(self.position["x"]) + " , velocity:" + str(self.velocity["vx"])

# 总体调用部件


class Env():
    
    def __init__(self):
        self.tk = Tk()
        self.canvas=Canvas(self.tk, width=500, height=500)
        self.canvas.pack()
        self.canvas.create_polygon(10,10,20,10,20,40,10,40)
    
    def step(self):
        for i in range(0,60):    #建立一个60次的循环 ，循环区间[0,59）
            self.canvas.move(1,5,0)    #canvas对象中的编号“1”图形调用移动函数，x轴5个像素点，y轴不变
            self.tk.update()           #更新框架，强制显示改变
            time.sleep(0.01)       #睡眠0.05秒，制造帧与帧间的间隔时间
        for i in range(0,60):
            self.canvas.move(1,0,5)
            self.tk.update()
            time.sleep(0.02)
        for i in range(0,60):
            self.canvas.move(1,-5,0)
            self.tk.update()
            time.sleep(0.02)
        for i in range(0,60):
            self.canvas.move(1,0,-5)
            self.tk.update()
            time.sleep(0.02)


if __name__ == "__main__":
    ship = Ship( {"x":23, "y":19}, {"vx":2, "vy":5} )
    print( ship.toString() )
    print(ship.getSpeed())
    env = Env()
    env.step()

















