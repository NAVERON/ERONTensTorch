
import numpy as np
import math
import datetime
import copy

class Ship():  # 训练对象的属性
    
    K = 0.0785
    T = 3.12
    isDead = False
    
    def __init__(self, position=np.array([500, 400], dtype=np.float), velocity=np.array([2, 4], dtype=np.float)):  # 矩阵
        self.id = datetime.datetime.now().strftime("%d%H%M%S%f")
        
        self.rudder = 0
        self.position = position
        self.velocity = velocity
        
        # self.q = queue.Queue(maxsize=10)
        
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
        if self.getSpeed() > 10 or self.getSpeed() < 0:   # 控制速度大小
            self.velocity -= dv
    def rudderChange(self, dr):  # 舵角变化    范围为每次一度， 变化舵角会造成航向的变化
        self.rudder += dr
        if self.rudder > 20 or self.rudder < -20:  # 设定舵角的范围
            self.rudder -= dr
    def getSpeed(self):  # 速度大小
        return np.linalg.norm(self.velocity)
    def getCourse(self): # 运动方向
        return self.calAngle(self.velocity[0], self.velocity[1])
    def distance(self, other_ship):
        return np.linalg.norm(other_ship.position - self.position)
    
    def calAngle(self, dx, dy):   # 计算的角度按照顺时针旋转，正向向上是0度角
        theta = math.atan2(dx, dy)
        angle = math.degrees(theta)
        if angle < 0:
            angle += 360
        # angle = np.float64(angle)
        return angle
    
    def goAhead(self, width, height):
        # 边界判断    设置为不能超越边界
        if self.position[0] < 0:
            self.position[0] = width
        elif self.position[0] > width:
            self.position[0] = 0
        elif self.position[1] < 0:
            self.position = height
        elif self.position[1] > height:
            self.position[1] = 0
        
        delta = self.K * self.rudder * (1 - self.T + self.T * math.exp(-1 / self.T))
        self.courseTurn(delta)
        self.position += self.velocity  # 这样就更新位置了    ====  可以把界面更新放到数据更新里面同步，更好
    
    def isCollision(self, other):
        dis = np.linalg.norm(other.position-self.position)
        if dis < 20:
            self.isDead = True
            other.isDead = True
            
            self.velocity = np.array([0., 0.])
            self.rudder = 0.
            other.velocity = np.array([0., 0.])
            other.rudder = 0.
            return True
        
        return False
    def setDead(self):
        if self.isDead:
            self.velocity = np.array([0., 0.])
            self.rudder = 0.
        pass
    def getObservation(self):
        near_locals = self.warpAxis(self.near)
        up = 0
        right = 0
        down = 0
        left = 0
        for local in near_locals:
            ratio = local.getRatio()
            if ratio > 355 and ratio < 30:
                up += 1
            elif ratio > 30 and ratio < 112.5:
                right += 1
            elif ratio > 112.5 and ratio < 210:
                down += 1
            elif ratio > 210 and ratio < 355:
                left += 1
        
        return [up, right, down, left, self.getCourse(), self.getSpeed()]
        pass
    
    near = []   # 顶层计算后存储现在周边的情况
    def getNear(self, dis, **ships):  # 传入查找对象的引用this_ship，以及距离范围 dis
        self.near.clear()   # 清空之前的数据
        
        for k, v in ships.items():
            item_ship = v
            if self.id == item_ship.id:
                continue
            if self.distance(item_ship) < dis:
                self.near.append(item_ship)
        return self.near
        pass
    def warpAxis(self, near):
        
        near_locals = []
        for ship in near:
            d_pos = ship.position - self.position
            d_pos_radius = -np.radians(-self.getCourse())  # 转换成弧度
            c, s = np.cos(d_pos_radius), np.sin(d_pos_radius)
            R = np.array([ [c, -s], [s, c] ])
            position = np.dot(R, d_pos.T).T
            
            dh = ship.getCourse() - self.getCourse()
            while dh >= 360 or dh < 0:
                if dh >= 360:
                    dh -= 360
                if dh < 0:
                    dh += 360
            
            local_ship = LocalShip(ship.id, position, dh)
            local_ship.setRatio(self.calAngle( position[0], position[1] ))
            near_locals.append(local_ship)
        
        return near_locals
        pass
    
    def toString(self):
        return "id:" + self.id + " , position:" + str(self.position) + " , velocity:" + str(self.velocity)

class LocalShip():
    
    def __init__(self, id, position, velocity):
        self.id = id
        self.position = position
        self.velocity = velocity
        self.ratio = 0
        pass
    
    def setRatio(self, ratio):
        self.ratio = ratio
    def getRatio(self):
        return self.ratio
        pass
















