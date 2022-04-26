from collections import deque, namedtuple
import random

Transition = namedtuple('Transition', (
    'state',
    'action',
    'reward',
    'state2',
))


class Memory:
    def __init__(self, capacity) -> None:
        self.m = deque([], maxlen=capacity)

    def push(self, *args):
        self.m.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.m, batch_size)

    def __len__(self):
        return len(self.m)
