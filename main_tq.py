import numpy as np
import torch
from cuda_test import test_cuda
from pycefl.environment import ChessEnvironment
import agent as agt
from datetime import datetime
import pandas as pd

import plots as pts


EPISODE_COUNT = 6

CHESS_OUTPUT_CLASSIC = 226
CHESS_OUTPUT_REDUCED = 74

BATCH_SIZE = 100


class ChessAgent(agt.DDQNAgent):
    def __init__(self, device='cpu') -> None:
        super().__init__(64, CHESS_OUTPUT_CLASSIC, BATCH_SIZE, device)


def main():
    device = 'cuda:0' if test_cuda(verbose=True) else 'cpu'

    env = ChessEnvironment().reset()
    agent = ChessAgent(device)

    done = False

    thresholds = []
    losses = []
    memory_size = []

    for eps in range(EPISODE_COUNT):
        done = False
        i = 0
        prev_reward = 0.

        while not done:
            success = False
            print(f"Episode {eps + 1}")
            print(f"Player: {i % 2 + 1}\tSubepisode {i + 1}")
            j = 0
            while not success:
                j += 1
                action = agent.select_action(
                    torch.tensor(env.chessboard.numpy_chessboard,
                                 dtype=torch.float32).flatten(),
                    j
                )

                state, state2, reward, done, success = env.step(action.item())

            reward -= prev_reward

            agent.memorize(
                torch.tensor(state, dtype=torch.float32).flatten(),
                action,
                reward,
                torch.tensor(state2, dtype=torch.float32).flatten() if state2 is not None else None)

            agent.step()
            i += 1

            env.flip()
            print(state2)
            print(f"Iteration: {j}\tAction: {action.item()}")
            print(f"Reward: {reward}")
            print(f"Exploration Threshold: {agent.threshold}")
            size = len(agent.memory)
            print(f"Memory Size: {size} / {agent.memory.maxlen}")
            print(f"Loss: {agent.loss}")

            thresholds.append(agent.threshold)
            losses.append(agent.loss)
            memory_size.append(size)

            # agent.plot_durations()
            prev_reward = reward

        env.reset()

    dt = datetime.now().strftime(r'%Y-%m-%d_%H-%M-%s')
    print('Saving the models... ', end='')
    agent.save(dt)

    print('done')

    pts.init_plotting()

    pts.plot_thresholds(thresholds, 'threshold-' + dt, 'tanh')
    pts.plot_losses(losses, 'loss-' + dt, 'Huber')

    pd.Series(thresholds).to_csv(f'./results/thresholds-{dt}.csv')
    pd.Series(losses).to_csv(f'./results/losses-{dt}.csv')
    pd.Series(memory_size).to_csv(f'./results/memory-{dt}.csv')


if __name__ == '__main__':
    main()
