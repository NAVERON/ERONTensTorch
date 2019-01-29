



# 总体调用部件
import time
from tkinter import Tk, Canvas
import numpy as np
from EronFine.Ship import Ship


from EronFine.EndCompute import DDPG
from EronFine.SpecialSen.Evaluator_Set import Evaluator
from EronFine import util


class Viewer():
    
    ships_count = 5
    state_dim = 1+4*(ships_count-1)
    action_dim = 2
    action_bound = [-0.2, 0.2]
    rudder_bound = [-0.5, 0.5]
    speed_bound = [-0.2, 0.2]
    
    train_id = None
    dis = 300
    
    def __init__(self):
        self.tk = Tk()
        
        self.window_width = 1000.0
        self.window_height = 600.0
        
        self.canvas = Canvas(self.tk, width=self.window_width, height=self.window_height)
        self.ships = {}
        self.drawer_ships = []
        self.drawer_velocities = []
        self.canvas.bind("<Button-1>", self.create_things)
        self.canvas.bind("<Button-3>", self.do_begin)
        self.canvas.bind("<ButtonRelease-1>", self.new_things)
        
        self.canvas.pack()
        self.render()
        # 开启总循环
        
    def do_begin(self, event):
        test(self.validate_episodes, self.agent, self, self.evaluate, self.output)
        
        pass
    def create_things(self, event):    # 创建功能作废，手动创建
        self.pressed_x = event.x
        self.pressed_y = event.y
        print("正在创建", self.pressed_x, ", ", self.pressed_y)
        pass
    def new_things(self, event):
        self.released_x = event.x
        self.released_y = event.y
        print("生成新对象", self.released_x, ", ", self.released_y)
        
        x = self.pressed_x
        y = self.window_height-self.pressed_y
        dx = self.released_x - self.pressed_x
        dy = self.pressed_y - self.released_y
        
        temp = Ship(np.array([x, y], dtype = np.float64), np.array([dx, dy], dtype = np.float64), self.window_width, self.window_height)
        self.ships[temp.id] = temp
        print("创建成功", temp)
        pass
    
    def init_train_parameters(self, validate_episodes, agent, env, evaluate, output):
        self.validate_episodes = validate_episodes
        self.agent = agent
        self.evaluate = evaluate
        self.agent = agent
        self.evaluate = evaluate
        self.output = output
        
        self.tk.mainloop()
        pass
    
    def createRandomEntity(self):
        position_list = np.array(np.random.random((1, 2))).flatten()
        position = np.multiply(position_list, 600)         # 范围是   0到600
        
        velocity_list = np.array(-1 + 2*np.random.random((1, 2))).flatten()         #生成的范围时   -1到1
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
            if k == self.train_id:
                self.drawer_ships.append(
                    self.canvas.create_oval(s.position[0]-10, self.window_height-s.position[1]-10, s.position[0]+10, self.window_height-s.position[1]+10, fill="red")
                )
            else:
                self.drawer_ships.append(
                    self.canvas.create_oval(s.position[0]-10, self.window_height-s.position[1]-10, s.position[0]+10, self.window_height-s.position[1]+10, fill=None)
                )
            
            self.drawer_velocities.append(
                self.canvas.create_line(s.position[0], self.window_height-s.position[1], s.position[0]+s.velocity[0]*10, self.window_height-s.position[1]-s.velocity[1]*10, fill="blue")
            )
            # 绘制历史轨迹
            for i in range(len(s.history)):
                his = s.history[i]
                self.canvas.create_text(his[0], self.window_height-his[1], text="*")
            
        self.tk.update()
    
    all_observations = {}  # 以自定形式存储数据   id : observation
    def step(self,  **actions):    # 这里传入每一个对象的动作，每一艘船舶都向前走一步，之后会得到新的环境
        # 这里先做动作，舵角，速度变化等
        # print("在 环境中step打印当前传入的动作   ", actions)
        self.all_observations.clear()
        train_reward = 0
        done = False
        # 根据action做出动作
        for k, v in actions.items():           #  重点：一个是环境获取，一个是惩罚奖励设置函数
            action = actions[k]
            action = np.array([np.clip(action[0], self.rudder_bound[0], self.rudder_bound[1]), np.clip(action[1], self.speed_bound[0], self.speed_bound[1])])
            # print("action id:", k, ", action:", action)
            # action      变向/舵角变化            变速/  航向改变
            # 根据id操作相应的动作，修改数据
            s = self.ships[k]
            if s.isDead:       #  如果已经死亡，则不进行动作指导
                continue
            s.rudderChange(action[0])   #动作1是改变舵角   动作2 是改变速度
            s.speedChange(action[1])
            
            s.goAhead()
            #s.addHistory(s.position)
            #self.all_observations[k] = s.getObservation(self.dis, **self.ships)
            
        # 判断是否碰撞
        for k, v in self.ships.items():
            for in_k, in_v in self.ships.items():
                if v is in_v:
                    continue
                v.isCollision(in_v)
        # 根据碰撞情况制定惩罚奖励  reward
        if self.ships[self.train_id].isDead:
            # 如何造成的碰撞，追究原因，给予惩罚
            speed = self.ships[self.train_id].getSpeed()
            action = actions[self.train_id]
            if  speed > 7:
                train_reward -= speed/3
            
            done = True
        else:
            # 会遇态势，如果遵守规则，奖励多一些，否则给予奖励少一些
#             ob = self.ships[self.train_id].getObservation(self.dis, **self.ships)
#             if ob[0] > 1 and actions[self.train_id]>0:
#                 train_reward += 1
#             elif ob[0] > 1 and actions[self.train_id]<0:
#                 train_reward += 4
#             else:
#                 train_reward += 2
            
            if actions[self.train_id][1] > 0:
                train_reward += 1
            train_reward += 1
        
        for k, v in self.ships.items():
            self.all_observations[v.id] = v.getObservation(self.dis, **self.ships)
        self.render()  #渲染当前画面 =====可以在外层调用，也可以直接放在步进合并渲染
        time.sleep(0.001)
        
        return self.all_observations, train_reward, done   # 观察值， 奖励， 一个回合是否完成
        pass
    
    def saveAllShips(self):
        for id, ship in self.ships.items():
            ship.storeTrajectories()
        pass
    def reset(self):  # 重置环境和变量的条件
        print("一个回合结束，重新生成新的环境")
        self.train_id = None
        
        self.ships.clear()
        self.canvas.delete("all")
        self.drawer_ships.clear()
        self.drawer_velocities.clear()
        # 重新生成一个新的环境
#         for _ in range(self.ships_count):
#             temp = self.createRandomEntity()
#             self.ships[temp.id] = temp
        
        # 对遇态势
        temp = Ship(np.array([500.0, 100.0]), np.array([0.0, 2.0]), width=self.window_width, height=self.window_height)
        self.ships[temp.id] = temp
        time.sleep(0.01)
        
        temp = Ship(np.array([500.0, 500.0]), np.array([0.0, -2.0]), width=self.window_width, height=self.window_height)
        self.ships[temp.id] = temp
        time.sleep(0.01)
        #  对遇和 左舷交叉相遇     3 无人艇会遇
        temp = Ship(np.array([200.0, 300.0]), np.array([1.2, -1.0]), width=self.window_width, height=self.window_height)
        self.ships[temp.id] = temp
        time.sleep(0.01)
        #  四无人艇   会遇
        temp = Ship(np.array([700.0, 450.0]), np.array([-2.0, -3.0]), width=self.window_width, height=self.window_height)
        self.ships[temp.id] = temp
        time.sleep(0.01)
        #再来一个追越
        temp = Ship(np.array([600.0, 20.0]), np.array([-2.0, 1.0]), width=self.window_width, height=self.window_height)
        self.ships[temp.id] = temp
        time.sleep(0.01)
        
        # 随机生成避碰环境
#         for _ in range(self.ships_count):
#             temp = self.createRandomEntity()
#             self.ships[temp.id] = temp
        
        self.all_observations.clear()
        for k, v in self.ships.items():
            s = v
            if self.train_id is None:
                self.train_id = k
            self.all_observations[s.id] = s.getObservation(self.dis, **self.ships)
        
        #print("本次训练的id号码是:", self.train_id)
        return self.all_observations
        pass




#   在gym环境中observation观测变量   3个值
#   动作是一个值
#   具体参考      https://www.jianshu.com/p/af3a7853268f

def test(validate_episodes, agent, env, evaluate, model_path):
    
    agent.load_weights(model_path)
    agent.is_training = False
    agent.eval()
    policy = lambda x: agent.select_action(x, decay_epsilon=False)  # 不衰减  decay_epsilon
    
    for i in range(validate_episodes):
        validate_reward = evaluate(env, policy, debug=True, save=False)
        util.prYellow('[Evaluate] #{}: mean_reward:{}'.format(i, validate_reward))
    
    pass

if __name__ == "__main__":
    
    validate_episodes = 10    # 回合，一整个回合
    validate_steps = 1000   # 每一个回合最大步数，验证需要的步数
    
    output = "../output"   # 输出文件夹==========================================新建的场景目录发生变化，那么输出文件也应该变化一下
    max_episode_length = 500   # 每一个回合最大步数
    
    env = Viewer()
    agent = DDPG(env.state_dim, env.action_dim)   # 环境和动作的维度
    evaluate = Evaluator(validate_episodes, validate_steps, output, max_episode_length)
    
    env.init_train_parameters(validate_episodes, agent, env, evaluate, output)
    #test(validate_episodes, agent, env, evaluate, output)
    print("test over")
        
    
    








































