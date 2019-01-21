


"""
Deep Deterministic Policy Gradient
Implemented using DM Control Suite in PyTorch
Author: Sameera Lanka
Website: https://sameera-lanka.com
"""

from ddpg import DDPG
from dm_control import suite
import torch
import os
import numpy as np
import matplotlib.pyplot as plt
# matplotlib inline


ENVNAME = 'reacher'
TASKNAME = 'hard'
NUM_EPISODES = 100000

if __name__=="__main__":
    env = suite.load(ENVNAME, TASKNAME, visualize_reward=True )
    agent = DDPG(env)
    #agent.loadCheckpoint(Path to checkpoint)
    agent.train()
    

# For Plots
fig = plt.figure(figsize=(50,20))
plt.plot(agent.rewardgraph)
plt.xlabel('Episode number')
plt.ylabel('Episode reward')
plt.show()

avgreward = np.convolve(agent.rewardgraph, np.ones((50,))/50, mode='valid')
plt.xlabel('Episode number')
plt.ylabel('100-Episode reward')
fig = plt.figure(figsize=(50,20))
plt.plot(avgreward)
plt.show()












