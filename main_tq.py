import torch
from cuda_test import test_cuda
from pycefl.environment import ChessEnvironment
import agent as agt


EPISODE_COUNT = 100

CHESS_OUTPUT_CLASSIC = 226
CHESS_OUTPUT_REDUCED = 74

BATCH_SIZE = 12


class ChessAgent(agt.DDQNAgent):
    def __init__(self, device='cpu') -> None:
        super().__init__(64, CHESS_OUTPUT_CLASSIC, BATCH_SIZE, device)


def main():
    device = 'cuda:0' if test_cuda(verbose=True) else 'cpu'

    env = ChessEnvironment().reset()
    agent = ChessAgent(device)

    done = False

    for eps in range(EPISODE_COUNT):
        done = False
        i = 0
        while not done:
            success = False
            print(f"Episode {eps + 1}")
            print(f"Player: {i % 2 + 1}; Subepisode {i + 1}")
            j = 0
            while not success:
                j += 1
                action = agent.select_action(
                    torch.tensor(env.chessboard.numpy_chessboard,
                                 dtype=torch.float32).flatten()
                )

                state, state2, reward, done, success = env.step(action.item())

            env.flip()
            print(f"Iteration: {j}\tAction: {action.item()}")
            print(f"Reward: {reward}")
            print(f"Exploration Threshold: {agent.threshold}")
            print(state2)

            agent.memorize(
                torch.tensor(state, dtype=torch.float32).flatten(),
                action,
                reward,
                torch.tensor(state2, dtype=torch.float32).flatten()) if state2 is not None else None
            agent.step()
            i += 1

            # agent.plot_durations()
        env.reset()
    agent.save()


if __name__ == '__main__':
    main()
