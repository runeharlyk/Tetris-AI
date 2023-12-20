from game import Tetris
from agent import Agent
from graphics import CVRenderer

env = Tetris(10, 20)

# Initialize training variable
max_episode = 3000
max_steps = 25000

agent = Agent(4)

renderer = CVRenderer()

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

        best_action = None
        for action, state in next_states.items():
            if (best_state == state).all():
                best_action = action
                break

        reward, done = env.step(best_action)
        total_reward += reward

        agent.add_to_memory(current_state, next_states[best_action], reward, done)

        current_state = next_states[best_action]

        renderer.wait(1)
        steps += 1

    agent.replay()

    if agent.epsilon > agent.epsilon_min:
        agent.epsilon -= agent.epsilon_decay

    return total_reward

if __name__ == '__main__':
    run_episodes()