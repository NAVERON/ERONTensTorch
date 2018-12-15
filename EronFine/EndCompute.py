

# Tools LiClipse
# Time 2018
# Author ERON
#                        .::::.
#                      .::::::::.
#                     :::::::::::
#                  ..:::::::::::'
#               '::::::::::::'
#                 .::::::::::
#            '::::::::::::::..
#                 ..::::::::::::.
#               ``::::::::::::::::
#                ::::``:::::::::'        .:::.
#               ::::'   ':::::'       .::::::::.
#             .::::'      ::::     .:::::::'::::.
#            .:::'       :::::  .:::::::::' ':::::.
#           .::'        :::::.:::::::::'      ':::::.
#          .::'         ::::::::::::::'         ``::::.
#      ...:::           ::::::::::::'              ``::.
#     ```` ':.          ':::::::::'                  ::::..
#                        '.:::::'                    ':'````..
#                     美女保佑 永无BUG



import torch
from torch import nn
import time

class DDPG(object):
    
    def __init__(self, states, actions):
        self.states = states
        self.actions = actions
        
        self.s_t = None
        self.a_t = None
        
        self.actor = Actor(self.states, self.actions)
        self.critic = Critic(self.states, self.actions)
        pass
    
    def select_action(self, observation):
        pass
    def reset(self, observation):  # 根据 observation 重置训练模型的变量
        pass
    

class Actor(object):
    
    def __init__(self, states, actions):
        pass
    
    
class Critic(object):
    
    def __init__(self, states, actions):
        pass


class Model():
    
    def __init__(self):
        pass
    
    
















