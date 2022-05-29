from collections import deque
import numpy as np
import torch
from cuda_test import test_cuda
from pycefl.environment import ChessEnvironment
import agent as agt
from datetime import datetime
import pandas as pd

import plots as pts


EPISODE_COUNT = 20

CHESS_OUTPUT_CLASSIC = 226
CHESS_OUTPUT_REDUCED = 74

BATCH_SIZE = 200


class ChessAgent(agt.DDQNAgent):
    def __init__(self, device='cpu') -> None:
        super().__init__(64, CHESS_OUTPUT_CLASSIC, BATCH_SIZE, device)


prev_actions = deque(maxlen=24)


def check_nasheq(length):
    if len(prev_actions) < 3 * length:
        return False

    for i in range(length):
        if prev_actions[2 * i] != prev_actions[2 * length + 2 * i]:
            return False

    return True


def is_nasheq():
    return check_nasheq(2) or check_nasheq(3) or check_nasheq(4) or check_nasheq(5) or check_nasheq(6)


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
            j = 0
            is_equilibrium = is_nasheq()

            if is_equilibrium:
                print('#### Equilibrium ####')

            while not success:
                j += 1
                actions = agent.select_action(
                    torch.tensor(env.chessboard.numpy_chessboard,
                                 dtype=torch.float32).flatten(),
                    j,
                    force_explore=is_equilibrium
                )
                sorted = actions.sort(descending=True)

                k = 0
                for action in sorted.indices:
                    value = sorted.values[action]
                    if k == 1 and value.item() == 0:
                        break

                    state, state2, reward, done, success = env.step(
                        int(action))

                    if success and prev_reward >= 1:
                        reward -= prev_reward

                    if k == 0 or success:
                        agent.memorize(
                            torch.tensor(state, dtype=torch.float32).flatten(),
                            torch.tensor(action),
                            reward,
                            torch.tensor(state2, dtype=torch.float32).flatten() if state2 is not None else None)
                    if success:
                        break
                    k += 1

            agent.step()
            i += 1

            if i % 2:
                env.flip()
            print(f"Epoch: {eps + 1}")
            print(f"Player: {i % 2 + 1}\tTurns: {i + 1}")
            print(env.chessboard.numpy_chessboard)
            print(f"Iteration: {j}\tAction: {action}")
            print(f"Reward: {reward}")
            print(f"Exploration Threshold: {agent.threshold}")
            size = len(agent.memory)
            print(f"Memory Size: {size} / {agent.memory.maxlen}")
            print(f"Loss: {agent.loss}")

            prev_actions.append(action)

            if not i % 2:
                env.flip()

            thresholds.append(agent.threshold)
            losses.append(agent.loss)
            memory_size.append(size)

            if i > 1000:
                print('Turns out')
                break

            # agent.plot_durations()
            prev_reward = reward
            print()

        env.reset()

    dt = datetime.now().strftime(r'%Y-%m-%d_%H-%M-%S')
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
