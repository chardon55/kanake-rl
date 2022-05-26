from collections import deque, namedtuple
import random

# Transition <- <s,a,r,s'>
Transition = namedtuple('Transition', (
    'state',
    'action',
    'reward',
    'state2',
))


class ReplayMemory:
    def __init__(self, capacity=None) -> None:
        self.m = deque([])
        self.__capacity = capacity

    def push(self, *args):
        self.m.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.m, batch_size)

    def dropout(self, frac: float):
        count = int(len(self.m) * frac)
        for _ in range(count):
            del self.m[random.randrange(count)]

    def __len__(self):
        return len(self.m)

    @property
    def maxlen(self):
        return self.__capacity

    @property
    def is_full(self):
        return len(self.m) >= self.maxlen
