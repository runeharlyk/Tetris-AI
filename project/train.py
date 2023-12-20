from game import Tetris
from agent import Agent
from graphics import CVRenderer, InvincibleRenderer
from plot import ScatterPlot

height, width = 20, 10

env = Tetris(width, height)

plot = ScatterPlot("", "", "")
# Initialize training variable
max_episode = 3000
max_steps = 25000

model_path = f'model_{width}_{height}.pt'

agent = Agent(4, model_path)

renderer = InvincibleRenderer()

def run_episodes():
    rewards = [run_episode(i) for i in range(max_episode)]
    print(rewards)
    return rewards

def run_episode(episode):
    print(f'Running episode {episode}')
    current_state = env.reset()
    total_reward = 0
    done = False
    max_steps = 25000
    steps = 0

    while not done and steps < max_steps:
        renderer.render(env, total_reward)

        next_states = env.get_next_states()

        if not next_states: break

        best_state = agent.act(next_states.values())

        best_action = next((action for action, state in next_states.items() if (best_state == state).all()), None)

        reward, done = env.step(best_action)
        total_reward += reward

        agent.add_to_memory(current_state, next_states[best_action], reward, done)

        current_state = next_states[best_action]

        renderer.wait(1)
        steps += 1

    agent.replay()

    if agent.epsilon > agent.epsilon_min:
        agent.epsilon -= agent.epsilon_decay

    print(f'Run episode {episode:02d}, total_reward:{total_reward}')
    plot.add_point(episode, total_reward, True)
    return total_reward

if __name__ == '__main__':
    try:
        run_episodes()
    finally:
        agent.save(model_path)