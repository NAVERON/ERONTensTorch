


# 总体调用部件
import time
from tkinter import Tk, Canvas
import numpy as np
from EronFine.Ship import Ship


class Viewer():
    
    state_dim = 4
    action_dim = 5
    action_bound = [-1, 1]
    num_iterations = 10000
    
    def __init__(self):
        self.tk = Tk()
        self.canvas = Canvas(self.tk, width=1000, height=600)
        self.ships = []
        self.drawer_ships = []
        
        for _ in range(10):
            self.ships.append(self.createRandomEntity())
        self.canvas.pack()
        
        self.render()
    
    def createRandomEntity(self):
        position = np.multiply([np.random.rand(), np.random.rand()], 600)
        velocity = np.multiply([np.random.rand(), np.random.rand()], 2)
        entity = Ship(np.array(position), np.array(velocity))
        print(entity.toString())
        time.sleep(0.001)
        return entity
    def getNear(self, this_ship, dis):  # 传入查找对象的引用this_ship，以及距离范围 dis
        near = []
        for item_ship in self.ships:
            if this_ship.id == item_ship.id:
                continue
            if this_ship.distance(item_ship) < dis:
                near.append(item_ship)
        return near
        pass
    
    
    def render(self):  # 根据当前状况绘制
        for entity in self.drawer_ships:
            self.canvas.delete(entity)
        self.drawer_ships.clear()
        
        for s in self.ships:
            self.drawer_ships.append(self.canvas.create_oval(s.position[0]-10, s.position[1]-10, s.position[0]+10, s.position[1]+10, fill="black"))
        
        self.tk.update()
        
    def step(self, action):
        # 这里先做动作，舵角，速度变化等
        self.render()  #渲染当前画面 =====可以在外层调用，也可以直接放在步进合并渲染
        
        for s in self.ships:
            s.goAhead(self.tk)
        
        time.sleep(0.01)
        
        return [0, 0, 0, 0, 0], 0, False
        pass
    def reset(self):  # 重置环境和变量的条件
        
        return [0, 0, 0, 0, 0], 0, False
        pass
    
    def sampleAction(self):
        pass
    def getState(self):
        pass


if __name__ == "__main__":
    
    env = Viewer()
    step = 0
    while step < 1000:
        env.step(0)
        step += 1
        
    
    















