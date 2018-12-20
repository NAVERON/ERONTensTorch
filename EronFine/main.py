


from EronFine.EndCompute import DDPG
from EronFine.Front import Viewer
from EronFine.evaluator import Evaluator
from copy import deepcopy
from EronFine import util

#   在gym环境中observation体哦那是   3个值
#   动作是一个值
#   具体参考      https://www.jianshu.com/p/af3a7853268f

def train(agent, env, evaluate):
    validate_episodes = evaluate.interval
    output = evaluate.save_path
    
    agent.is_training = True  # 是不是训练状态
    step = episode = episode_steps = 0
    episode_reward = 0.  # 每一个回合的奖励总和
    num_iterations = 1000  # 一共训练多少回合
    max_episode_length = 500   # 每一个回合最大步进长度
    
    observation = None  # 环境状态，观察值
    
    while step < num_iterations:
        
        if observation is None:  # 初始化环境状态  和  智能体的 初始状态，一个新的回合
            observation = env.reset()
            agent.reset(observation)
        
        if step <= 200:  # steop表示已经训练了多少回合    在一定的回合中采用随即动作填充刚开始的网络
            action = agent.random_action()
        else:
            action = agent.select_action(observation)   # 对于每一个Ship都要输入环境并计算出动作Action
        
        next_observation, reward, done = env.step(action)
        next_observation = deepcopy(next_observation)
        if max_episode_length and episode_steps >= max_episode_length - 1:
            done = True
        
        agent.observe(reward, next_observation, done)
        if step > 100:
            agent.update_policy()
        
        # [optional] evaluate
        if evaluate is not None and validate_steps > 0 and step % validate_steps == 0:
            policy = lambda x: agent.select_action(x, decay_epsilon=False)
            validate_reward = evaluate(env, policy, debug=False, visualize=False)
            if True: util.prYellow('[Evaluate] Step_{:07d}: mean_reward:{}'.format(step, validate_reward))
        
        # [optional] save intermideate model
        if step % int(num_iterations/3) == 0:
            agent.save_model(output)
        
        # update
        step += 1
        episode_steps += 1
        episode_reward += reward
        observation = next_observation
        
        if done: # end of episode
            if True: util.prGreen('#{}: episode_reward:{} steps:{}'.format(episode,episode_reward,step))
            agent.memory.append(
                observation,
                agent.select_action(observation),
                0., False
            )
            
            # reset
            observation = None
            episode_steps = 0
            episode_reward = 0.
            episode += 1  #   总体的循环


if __name__ == "__main__":
    
    validate_episodes = 20
    validate_steps = 2000
    output = "output"
    max_episode_length = 500
    
    env = Viewer()
    agent = DDPG(env.state_dim, env.action_dim)   # 环境和动作的维度
    evaluate = Evaluator(validate_episodes, validate_steps, output, max_episode_length)
    
    train(agent, env, evaluate)
    print("train over")
    
    
    
    
    
    
    
    
    
    


