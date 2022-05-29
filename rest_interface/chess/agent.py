import numpy as np
import torch
from agent import LoadedAgent

from model import get_latest_model
from cuda_test import test_cuda
from pycefl.environment import Environment
from pycefl.ceil import CEIL


interpreter = CEIL()


def init_latest_agent():
    return LoadedAgent(get_latest_model(), 226, 'cuda' if test_cuda() else 'cpu')


def check_rule(state: np.ndarray, state2: np.ndarray, env: Environment):
    delta: np.ndarray = state2 - state
    am = delta.argmax()

    r = int(am / state2.shape[0])
    c = am % state2.shape[0]

    is_src = state[r, c] > 0
    if is_src:
        source = (r, c)
    else:
        destination = (r, c)

    delta[r, c] = 0

    am = delta.argmax()

    r = int(am / state2.shape[0])
    c = am % state2.shape[0]

    if is_src:
        destination = (r, c)
    else:
        source = (r, c)

    return env.chessboard._check_rule(source, destination)


def interpret_action(action_rank: torch.Tensor, env: Environment):
    sorted = action_rank.sort(descending=True)

    result_state = None

    for action in sorted.indices:
        _, state2, _, _, success = env.step(
            int(action))

        if success:
            result_state = state2
            break

    if result_state is None:
        return None

    return interpreter.generate(result_state)
