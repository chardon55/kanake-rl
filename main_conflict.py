import numpy as np
import torch
from cuda_test import test_cuda
from pycefl.environment import ChessEnvironment
import agent as agt
from datetime import datetime
import pandas as pd

import plots as pts


EPISODE_COUNT = 40

CHESS_OUTPUT_CLASSIC = 226
CHESS_OUTPUT_REDUCED = 74

BATCH_SIZE = 100


class LoadAgent(agt.LoadedAgent):
    def __init__(self, device='cpu') -> None:
        super().__init__('./models/ddqn-2022-05-23_22-23-1653315809-.pt',
                         CHESS_OUTPUT_CLASSIC, device)


class ChessAgent(agt.DDQNAgent):
    def __init__(self, device='cpu') -> None:
        super().__init__(64, CHESS_OUTPUT_CLASSIC, BATCH_SIZE, device)


def main():
    device = 'cuda:0' if test_cuda(verbose=True) else 'cpu'

    env = ChessEnvironment().reset()
    agent = ChessAgent(device)
    loaded = LoadAgent(device)

    done = False

    thresholds = []
    losses = []
    memory_size = []
    win_loss = []
    prev_reward = 0

    for eps in range(EPISODE_COUNT):
        done = False
        i = 0

        while not done:
            success = False
            print(f"Episode {eps + 1}")
            print(f"Subepisode {i + 1}")
            j = 0
            while not success:
                j += 1
                actions = agent.select_action(
                    torch.tensor(env.chessboard.numpy_chessboard,
                                 dtype=torch.float32).flatten(),
                    j
                )

                action_df = pd.DataFrame(data={
                    'value': list(actions.to('cpu')),
                })
                action_df.sort_values('value', ascending=False, inplace=True)

                k = 0
                for action, _ in action_df.iterrows():
                    state, state2, reward, done, success = env.step(
                        action.item())
                    if not success:
                        reward = -1.
                    else:
                        if prev_reward >= 1:
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

            if not done:
                env.flip()
                explore = False
                success1 = False
                while not success1:
                    j += 1
                    actions1 = loaded.select_action(torch.tensor(env.chessboard.numpy_chessboard,
                                                                 dtype=torch.float32).flatten(), explore=explore)

                    action_df1 = pd.DataFrame(data={
                        'value': list(actions1.to('cpu')),
                    })
                    action_df1.sort_values(
                        'value', ascending=False, inplace=True)

                    success1 = False
                    for action_, _ in action_df1.iterrows():
                        state_, state2_, reward1, done1, success1 = env.step(
                            action_.item())

                    explore = not success1

                env.flip()

                reward -= reward1

            print(state2)
            print(state2_) if not done else None
            print(f"Iteration: {j}\tAction: {action}")
            print(f"Reward: {reward}")
            print(f"Exploration Threshold: {agent.threshold}")
            size = len(agent.memory)
            print(f"Memory Size: {size} / {agent.memory.maxlen}")
            print(f"Loss: {agent.loss}")

            thresholds.append(agent.threshold)
            losses.append(agent.loss)
            memory_size.append(size)

            if done:
                win_loss.append(1)
            elif done1:
                done = True
                win_loss.append(-1)
            # agent.plot_durations()
            # prev_reward = reward

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
    pd.Series(win_loss).to_csv(f'./results/win_loss-{dt}.csv')


if __name__ == '__main__':
    main()
