from game import Tetris
from agent import Agent
from Renderer.InvincibleRenderer import InvincibleRenderer
from Renderer.CVRenderer import CVRenderer
from Renderer.PyGameRenderer import PyGameRenderer
from plot import ScatterPlot

# https://github.com/andreanlay/tetris-ai-deep-reinforcement-learning/tree/master

height, width = 20, 10

env = Tetris(width, height)

plot = ScatterPlot("", "", "") 
# Initialize training variable
max_episode = 1500
max_steps = 25000

# model_path = f'model_{width}_{height}.pt'

agent = Agent(4)

renderer = PyGameRenderer()

def run_episodes():
    rewards = [run_episode(i) for i in range(max_episode)]
    return rewards

def run_episode(episode):
    current_state = env.reset()
    score = 0
    total_reward = 0
    done = False
    max_steps = 25000
    steps = 0

    while not done and steps < max_steps:
        renderer.render(env, score) 

        next_states = env.get_next_states()

        if not next_states: break

        best_action = agent.act(next_states)

        state, score, cleared_lines, done = env.step(best_action)
        reward = agent.costCalc.calculate(state, cleared_lines, done)
        total_reward += reward

        agent.add_to_memory(current_state, next_states[best_action], reward, done)

        current_state = next_states[best_action]

        renderer.wait(1)
        steps += 1

    agent.replay()

    if agent.epsilon > agent.epsilon_min:
        agent.epsilon -= agent.epsilon_decay

    print(f'Run episode {episode:02d}\t score:{score} \t total_reward:{total_reward}')
    plot.add_point(episode, score, True)
    return score

if __name__ == '__main__':
    try:
        run_episodes()
    finally:
        # agent.save(model_path)
        # plot.update()
        plot.freeze()