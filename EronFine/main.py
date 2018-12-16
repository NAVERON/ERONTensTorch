
from EronFine.EndCompute import DDPG, Actor, Critic
from EronFine.Front import Viewer
from EronFine.evaluator import Evaluator

evaluate = Evaluator(20, 2000, "output", 500)

def train(agent, env):
    
    agent.is_training = True
    step = episode = episode_steps = 0
    episode_reward = 0.
    observation = None
    num_iterations = 10000
    
    while step < num_iterations:
        # reset if it is the start of episode
        if observation is None:
            observation = env.reset()
            agent.reset(observation)

        action = agent.select_action(observation)
        
        # env response with next_observation, reward, terminate_info
        observation2, reward, done = env.step(action)
        if episode_steps >= 100:
            done = True
        
        agent.observe(reward, observation2, done)
        agent.update_policy()
        
        # [optional] evaluate
        if step % 50 == 0:
            policy = lambda x: agent.select_action(x, decay_epsilon=False)
            evaluate(env, policy, debug=False, visualize=False)
            
        # [optional] save intermideate model
        if step % int(num_iterations/3) == 0:
            agent.save_model("output")
        
        # update
        step += 1
        episode_steps += 1
        episode_reward += reward
        observation = observation2
        
        if done: # end of episode
            
            agent.memory.append(
                observation,
                agent.select_action(observation),
                0., False
            )

            # reset
            observation = None
            episode_steps = 0
            episode_reward = 0.
            episode += 1
        

if __name__ == "__main__":
    
    env = Viewer()
    agent = DDPG(5, 4)   # 环境和动作的维度
    
    train(agent, env)
    print("train over")
    


