


from EronFine.EndCompute import DDPG
from EronFine.Front import Viewer
from EronFine.evaluator import Evaluator
from copy import deepcopy
from EronFine import util

#   在gym环境中observation观测变量   3个值
#   动作是一个值
#   具体参考      https://www.jianshu.com/p/af3a7853268f

def train(agent, env, evaluate):
    #validate_episodes = evaluate.interval
    output = evaluate.save_path
    validate_steps = 200
    
    agent.is_training = True  # 是不是训练状态
    step = episode = episode_steps = 0   # episode 当前所处的回合       episode_steps 回合步数
    episode_reward = 0.  # 每一个回合的奖励总和
    num_iterations = 10000  # 一共训练多少回合
    max_episode_length = 500   # 每一个回合最大步进长度
    
    all_observations = None  # 环境状态，观察值
    # train_id = None
    
    while step < num_iterations:
        
        # train_id  是指当前回合中训练的对象id
        if all_observations is None:  # 初始化环境状态  和  智能体的初始状态，一个新的回合
            all_observations = env.reset()
            train_observation = all_observations[env.train_id]
            agent.reset(train_observation)
        actions = {}
        if step <= 100:  # steop表示已经训练了多少回合    在一定的回合中采用随机动作填充刚开始的网络
            for k, v in all_observations.items():
                actions[k] = agent.random_action()
        else:
            for k ,v in all_observations.items():
                actions[k] = agent.select_action(v)
        
        next_all_observations, train_reward, done = env.step(**actions)  # 传进去每个对象对应 的动作，返回特定id的学习成果
        next_train_observation = next_all_observations[env.train_id]
        next_train_observation = deepcopy(next_train_observation)
        
        if episode_steps >= max_episode_length - 1:
            done = True
        
        agent.observe(train_reward, next_train_observation, done)   # 存储训练状态
        if step > 100:  #和上面选动作一致
            agent.update_policy()
        
        # [optional] evaluate          这里检测一下当前的训练结果
        if validate_steps > 0 and step % validate_steps == 0:
            policy = lambda x: agent.select_action(x, decay_epsilon=False)
            validate_reward = evaluate(env, policy, debug=False)    #########################这里是阶段性验证，判断是否训练成功
            util.prYellow('[Evaluate] Step_{:07d}: mean_reward:{}'.format(step, validate_reward))
        
        # [optional] save intermideate model
        if step % int(num_iterations/3) == 0:    # 如果训练过了3分之1，则保存模型参数
            agent.save_model(output)
        
        # update
        step += 1
        episode_steps += 1   #在这一回合中前进一步
        episode_reward += train_reward     # 在一个回合中总共的奖励值，越高越好
        all_observations = next_all_observations
        
        if done: # end of episode    当一个回合超过了特定的步数，则认为一个回合完成
            util.prGreen('#{}: episode_reward:{} steps:{}'.format(episode, episode_reward, step))  # 第几个回合  回合奖励  这个回合步数
            agent.memory.append(
                train_observation,
                agent.select_action(train_observation),
                episode_reward, False
            )
            
            # reset
            all_observations = None
            episode_steps = 0
            episode_reward = 0.
            episode += 1  #   总体回合数

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
    
    isTraining = True   # 训练参数/使用训练好的参数计算动作
    
    validate_episodes = 100    # 回合，一整个回合
    validate_steps = 2000   # 每一个回合最大步数，验证需要的步数
    
    output = "output"   # 输出文件夹
    max_episode_length = 500   # 每一个回合最大步数
    
    env = Viewer()
    agent = DDPG(env.state_dim, env.action_dim)   # 环境和动作的维度
    evaluate = Evaluator(validate_episodes, validate_steps, output, max_episode_length)
    
    if isTraining:
        train(agent, env, evaluate)
    else:
        test(validate_episodes, agent, env, evaluate, output)
    print("train over")
    
    
    
   











