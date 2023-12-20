from game import Tetris
from agent import Agent
from graphics import CVRenderer

env = Tetris(10, 20)

agent = Agent()

if __name__ == '__main__':

renderer = CVRenderer()
    current_state = env.reset()
    total_reward = 0
    done = False
    max_steps = 25000
    steps = 0

    while not done and steps < max_steps:
        renderer.render(env, total_reward)

        next_states = env.get_next_states()

        if not next_states: break

        best_state = agent.get_best_state(next_states.values())

        best_action = None
        for action, state in next_states.items():
            if (best_state == state).all():
                best_action = action
                break

        reward, done = env.step(best_action)
        total_reward += reward

        current_state = next_states[best_action]

        renderer.wait(1)
        steps += 1
    print(total_reward)