
from EronFine.EndCompute import *
from EronFine.Front import *


def train(agent, env, num_iterations):
    
    step = episode = episode_steps = 0
    episode_reward = 0.  # 最终所有的奖励
    observation = None  # 避碰中的环境量
    
    while step < num_iterations:
        if observation is None:
            observation = env.reset()
            agent.reset(observation)
        
        action = agent.select_action(observation)
        next_observation, reward, done = env.step(action)
        # 需要存储当前状态    observation, action, reward, next_observation
        
        step += 1
        episode += 1
        episode_reward += reward
        observation = next_observation
        
        if done:  # 一个回合结束
            
            observation = None
            episode_steps = 0
            episode_reward = 0.
            episode += 1
            pass
        

if __name__ == "__main__":
    
    env = Viewer()
    agent = DDPG(5, 4)   # 环境和动作的维度
    num_iterations = 1000
    
    train(agent, env, num_iterations)
    print("train over")
    


