

# Tools LiClipse
# Time 2018
# Author ERON




import torch
import torch.nn as nn
import time


class DDPG(object):
    
    def __init__(self, states_dim, actions_dim):
        self.states_dim = states_dim
        self.actions_dim = actions_dim
        
        self.s_t = None
        self.a_t = None
        
        self.actor = Actor(self.states_dim, self.actions_dim)
        self.critic = Critic(self.states_dim, self.actions_dim)
        pass
    
    def select_action(self, observation):
        return 0
        pass
    def reset(self, observation):  # 根据 observation 重置训练模型的变量
        pass
    

class Actor(nn.Module):
    
    def __init__(self, states_dim, actions_dim, hidden1=400, hidden2=300, init_w=3e-3):
        super(Actor, self).__init__()
        self.fc1 = nn.Linear(states_dim, hidden1)
        self.fc2 = nn.Linear(hidden1, hidden2)
        self.fc3 = nn.Linear(hidden2, actions_dim)
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()
        self.init_weights(init_w)
    
    def init_weights(self, init_w):
        self.fc1.weight.data = fanin_init(self.fc1.weight.data.size())
        self.fc2.weight.data = fanin_init(self.fc2.weight.data.size())
        self.fc3.weight.data.uniform_(-init_w, init_w)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.fc3(out)
        out = self.tanh(out)
        return out
    
class Critic(object):
    
    def __init__(self, states_dim, actions_dim, hidden1=400, hidden2=300, init_w=3e-3):
        super(Critic, self).__init__()
        self.fc1 = nn.Linear(states_dim, hidden1)
        self.fc2 = nn.Linear(hidden1+actions_dim, hidden2)
        self.fc3 = nn.Linear(hidden2, 1)
        self.relu = nn.ReLU()
        self.init_weights(init_w)
    
    def init_weights(self, init_w):
        self.fc1.weight.data = fanin_init(self.fc1.weight.data.size())    # 实现在model里面
        self.fc2.weight.data = fanin_init(self.fc2.weight.data.size())
        self.fc3.weight.data.uniform_(-init_w, init_w)
    
    def forward(self, xs):
        x, a = xs
        out = self.fc1(x)
        out = self.relu(out)
        # debug()
        out = self.fc2(torch.cat([out,a],1))
        out = self.relu(out)
        out = self.fc3(out)
        return out

class Model():
    
    def __init__(self):
        pass
    
    
















