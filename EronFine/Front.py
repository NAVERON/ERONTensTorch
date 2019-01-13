


# 总体调用部件
import time
from tkinter import Tk, Canvas
import numpy as np
from EronFine.Ship import Ship


class Viewer():
    
    state_dim = 6
    action_dim = 2
    action_bound = [-2, 2]
    # num_iterations = 10000
    train_id = None
    dis = 300
    ships_count = 10
    
    def __init__(self):
        self.tk = Tk()
        
        self.window_width = 1000
        self.window_height = 600
        
        self.canvas = Canvas(self.tk, width=self.window_width, height=self.window_height)
        self.ships = {}
        self.drawer_ships = []
        self.drawer_velocities = []
        
#         for _ in range(10):
#             self.ships.append(self.createRandomEntity())
        self.canvas.pack()
        self.render()
    
    def createRandomEntity(self):
        position_list = np.array(np.random.random((1, 2))).flatten()
        position = np.multiply(position_list, 600)
        
        velocity_list = np.array(-1 + 2*np.random.random((1, 2))).flatten()
        velocity = np.multiply(velocity_list, 2)
        entity = Ship(position, velocity, self.window_width, self.window_height)
        #print(entity.toString())  ###############################################################################3
        time.sleep(0.01)
        return entity
    #  获取周边放到了Ship中，方便逻辑调用
    def render(self):  # 根据当前状况绘制
        self.canvas.delete("all")
        self.drawer_ships.clear()
        self.drawer_velocities.clear()
        
        for k, v in self.ships.items():
            s = v
            self.drawer_ships.append(
                self.canvas.create_oval(s.position[0]-10, self.window_height-s.position[1]-10, s.position[0]+10, self.window_height-s.position[1]+10, fill="black")
            )
            self.drawer_velocities.append(
                self.canvas.create_line(s.position[0], self.window_height-s.position[1], s.position[0]+s.velocity[0]*10, self.window_height-s.position[1]-s.velocity[1]*10, fill="blue")
            )
            # 绘制历史轨迹
            i = 0
            for his in s.q:
                self.canvas.create_text(his[0], self.window_height-his[1], text=str(i))
                i += 1
            
        self.tk.update()
    
    all_observations = {}  # 以自定形式存储数据   id : observation
    def step(self,  **actions):    # 这里传入每一个对象的动作，每一艘船舶都向前走一步，之后会得到新的环境
        # 这里先做动作，舵角，速度变化等
        # print("在 环境中step打印当前传入的动作   ", actions)
        self.all_observations.clear()
        train_reward = 0
        done = False
        # 根据action做出动作
        for k, v in actions.items():
            action = actions[k]
            action = np.clip(action, self.action_bound[0], self.action_bound)
            # print("action id:", k, ", action:", action)
            # action      变向/舵角变化            变速/  航向改变
            # 根据id操作相应的动作，修改数据
            s = self.ships[k]
            if s.isDead:       #  如果已经死亡，则不进行动作指导
                continue
            s.rudderChange(action[0])   #动作1是改变舵角   动作2 是改变速度
            s.speedChange(action[1])
            
            s.goAhead()
            self.all_observations[k] = s.getObservation(self.dis, **self.ships)
            
        # 根据动作判断动作后的后果，是好还是坏
        for k, v in self.ships.items():
            for in_k, in_v in self.ships.items():
                if v is in_v:
                    continue
                if v.isCollision(in_v):
                    #train_reward -= 1   # 如果撞上了，则惩罚一次
                    break
        # 根据碰撞情况制定惩罚奖励  reward
        if self.ships[self.train_id].isDead:
            ob = self.ships[self.train_id].getObservation(self.dis, **self.ships)
            if ob[0] > 1 and actions[self.train_id]>0:
                train_reward -= 1
            elif ob[0] > 1 and actions[self.train_id]<0:
                train_reward -= 4
            else:
                train_reward -= 2
            done = True
        else:
            train_reward += 2
        
#         for k, v in self.ships.items():
#             s = v
#             self.all_observations[s.id] = s.getObservation(self.dis, **self.ships)
        self.render()  #渲染当前画面 =====可以在外层调用，也可以直接放在步进合并渲染
        time.sleep(0.01)
        
        return self.all_observations, train_reward, done   # 观察值， 奖励， 一个回合是否完成
        pass
    
    def reset(self):  # 重置环境和变量的条件
        print("一个回合结束，重新生成新的环境")
        self.train_id = None
        
        self.ships.clear()
        self.canvas.delete("all")
        self.drawer_ships.clear()
        self.drawer_velocities.clear()
        # 重新生成一个新的环境
        for _ in range(self.ships_count):
            temp = self.createRandomEntity()
            self.ships[temp.id] = temp
        
        self.all_observations.clear()
        for k, v in self.ships.items():
            s = v
            if self.train_id is None:
                self.train_id = k
            self.all_observations[s.id] = s.getObservation(self.dis, **self.ships)
        
        #print("本次训练的id号码是:", self.train_id)
        return self.all_observations
        pass


if __name__ == "__main__":
    
    env = Viewer()
    observatyions = env.reset()
    step = 0
    dic = {}
    while step < 1000:
        c, d, e = env.step(**dic)
        step += 1
        
    
    















