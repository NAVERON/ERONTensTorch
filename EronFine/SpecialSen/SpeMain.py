



from EronFine.EndCompute import DDPG
from EronFine.SpecialSen.Ui_Set import Viewer
from EronFine.evaluator import Evaluator
from EronFine import util

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
    validate_steps = 2000   # 每一个回合最大步数，验证需要的步数
    
    output = "../output"   # 输出文件夹==========================================新建的场景目录发生变化，那么输出文件也应该变化一下
    max_episode_length = 500   # 每一个回合最大步数
    
    env = Viewer()
    agent = DDPG(env.state_dim, env.action_dim)   # 环境和动作的维度
    evaluate = Evaluator(validate_episodes, validate_steps, output, max_episode_length)
    
    
    # test(validate_episodes, agent, env, evaluate, output)
    print("test over")
    
    
    
   



























