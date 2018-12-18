


from EronFine.EndCompute import DDPG
from EronFine.Front import Viewer
from EronFine.evaluator import Evaluator
from copy import deepcopy
from EronFine import util


def train(agent, env, evaluate, validate_steps, output, max_episode_length = None):
    
    agent.is_training = True
    step = episode = episode_steps = 0
    episode_reward = 0.
    observation = None
    num_iterations = 10000
    
    while step < num_iterations:
        
        if observation is None:
            observation = env.reset()
            agent.reset(observation)
        
        if step <= 200:
            action = agent.random_action()
        else:
            action = agent.select_action(observation)
        
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
    
    train(agent, env, evaluate, validate_steps, output, max_episode_length)
    print("train over")
    
    
    
    
    
    
    
    
    
    


