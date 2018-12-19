

import torch
import torch.nn as nn
from torch.optim import Adam
import numpy as np

from EronFine.memory import SequentialMemory
from EronFine import util
from EronFine import random_process


class DDPG(object):
    
    def __init__(self, states_dim, actions_dim):
        self.states_dim = states_dim
        self.actions_dim = actions_dim
        
        hidden1 = 300
        hidden2 = 200
        init_w = 0.003
        net_cfg = {
            'hidden1':hidden1, 
            'hidden2':hidden2, 
            'init_w':init_w
        }
        self.actor = Actor(self.states_dim, self.actions_dim, **net_cfg)
        self.actor_target = Actor(self.states_dim, self.actions_dim, **net_cfg)
        self.actor_optim  = Adam(self.actor.parameters(), lr=0.001)
        
        self.critic = Critic(self.states_dim, self.actions_dim, **net_cfg)
        self.critic_target = Critic(self.states_dim, self.actions_dim, **net_cfg)
        self.critic_optim  = Adam(self.critic.parameters(), lr=0.001)
        # 确认网络中参数是一样的，再DDPG网络中，会有两套网络，一个现实，一个虚拟
        util.hard_update(self.actor_target, self.actor) # Make sure target is with the same weight
        util.hard_update(self.critic_target, self.critic)
        
        #Create replay buffer
        self.memory = SequentialMemory(limit=6000000, window_length=1)
        self.random_process = random_process.OrnsteinUhlenbeckProcess(size=self.actions_dim, theta=0.15, mu=0.0, sigma=0.2)
        # Hyper-parameters
        self.batch_size = 64
        self.tau = 0.001
        self.discount = 0.99
        self.depsilon = 1.0 / 50000  # 微分
        
        self.epsilon = 1.0
        self.s_t = None # Most recent state
        self.a_t = None # Most recent action
        self.is_training = True
        pass
    
    def update_policy(self):
        # Sample batch
        state_batch, action_batch, reward_batch, next_state_batch, terminal_batch = self.memory.sample_and_split(self.batch_size)
        
        # Prepare for the target q batch
        next_q_values = self.critic_target([
            util.to_tensor(next_state_batch, volatile=True),
            self.actor_target( util.to_tensor(next_state_batch, volatile=True) )
        ])
        next_q_values.volatile=False
        
        target_q_batch = util.to_tensor(reward_batch) + self.discount* util.to_tensor(terminal_batch.astype(np.float))*next_q_values

        # Critic update
        self.critic.zero_grad()

        q_batch = self.critic([ util.to_tensor(state_batch), util.to_tensor(action_batch) ])
        
        value_loss = nn.MSELoss(q_batch, target_q_batch)
        value_loss.backward()
        self.critic_optim.step()

        # Actor update
        self.actor.zero_grad()

        policy_loss = -self.critic([
            util.to_tensor(state_batch),
            self.actor( util.to_tensor(state_batch) )
        ])

        policy_loss = policy_loss.mean()
        policy_loss.backward()
        self.actor_optim.step()
        
        # Target update
        util.soft_update(self.actor_target, self.actor, self.tau)
        util.soft_update(self.critic_target, self.critic, self.tau)

    def eval(self):
        self.actor.eval()
        self.actor_target.eval()
        self.critic.eval()
        self.critic_target.eval()

    def observe(self, r_t, s_t1, done):
        if self.is_training:
            self.memory.append(self.s_t, self.a_t, r_t, done)
            self.s_t = s_t1

    def random_action(self):
        action = np.random.uniform(-1.,1., self.actions_dim)   # 在均匀分布上取size个数   在-1 和 1之间取值
        self.a_t = action
        return action

    def select_action(self, s_t, decay_epsilon=True):
        action = util.to_numpy(
            self.actor( util.to_tensor( np.array([s_t]) ) )    # 向Actor网络中发输入当前的状态量
        ).squeeze(0)     #  从数组的形状中删除单维度条目，即把shape中为1的维度去掉
        
        action += self.is_training * max(self.epsilon, 0) * self.random_process.sample()  # 这里的布尔值可以运算，当作1   有随即动作的成分
        action = np.clip(action, -1., 1.)
        
        if decay_epsilon:  # 衰退
            self.epsilon -= self.depsilon
        
        self.a_t = action
        return action

    def reset(self, obs):
        self.s_t = obs
        self.random_process.reset_states()

    def load_weights(self, output):
        if output is None: return

        self.actor.load_state_dict(
            torch.load('{}/actor.pkl'.format(output))
        )

        self.critic.load_state_dict(
            torch.load('{}/critic.pkl'.format(output))
        )
    
    def save_model(self,output):
        torch.save(
            self.actor.state_dict(),
            '{}/actor.pkl'.format(output)
        )
        torch.save(
            self.critic.state_dict(),
            '{}/critic.pkl'.format(output)
        )

    def seed(self,s):
        torch.manual_seed(s)
    
def fanin_init(size, fanin=None):
    fanin = fanin or size[0]
    v = 1. / np.sqrt(fanin)
    return torch.Tensor(size).uniform_(-v, v)

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
    
class Critic(nn.Module):
    
    def __init__(self, states_dim, actions_dim, hidden1=400, hidden2=300, init_w=3e-3):
        super(Critic, self).__init__()
        self.fc1 = nn.Linear(states_dim, hidden1)
        self.fc2 = nn.Linear(hidden1 + actions_dim, hidden2)
        self.fc3 = nn.Linear(hidden2, 1)
        self.relu = nn.ReLU()
        self.init_weights(init_w)
    
    def init_weights(self, init_w):
        self.fc1.weight.data = fanin_init(self.fc1.weight.data.size())
        self.fc2.weight.data = fanin_init(self.fc2.weight.data.size())
        self.fc3.weight.data.uniform_(-init_w, init_w)
    
    def forward(self, xs):
        x, a = xs
        out = self.fc1(x)
        out = self.relu(out)
        print("out:", out)
        print("a:", a)
        # debug()
#         out = self.fc2(torch.cat( [out, a], 1) )  # 按列拼接
#         out = self.fc2()
#         out = self.relu(out)
#         out = self.fc3(out)
        return out


    
    
















