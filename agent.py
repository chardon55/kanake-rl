from typing import Union
import random
import numpy as np
import torch
from torch import nn
import numpy as np

import q
from memory import ReplayMemory, Transition

GAMMA = .96                # Discount coefficient

TARGET_UPDATE = 10

EX_THRES_START = .03
EX_THRES_END = .95
EX_THRES_RATE = .005

OFFSET_LAMBDA = -7.8
PACE_EITA = .13
LOSS_SCALE = 80

LEARNING_RATE = .003
MEMORY_CAPACITY = 68000

SAVE_PATH = './models/ddqn-{0}.pt'
T_SAVE_PATH = './models/ddqn-target-{0}.pt'


class DDQNAgent:
    def __init__(self,
                 state_count: int, action_count: int, batch_size: int,
                 device: Union[torch.device, str] = 'cpu') -> None:
        super(DDQNAgent, self).__init__()
        self.state_count = state_count
        self.action_count = action_count
        self.batch_size = batch_size

        self.device = device

        # Double DQN
        self.qn_policy: q.DQNPolicy = \
            q.DQNPolicy(state_count, action_count).to(device)
        self.qn_target: q.DQNPolicy = \
            q.DQNPolicy(state_count, action_count).to(device)
        self.qn_target.load_state_dict(self.qn_policy.state_dict())
        self.qn_target.eval()

        self.optimizer = torch.optim.RMSprop(
            self.qn_policy.parameters(),
            lr=LEARNING_RATE,
        )

        self.loss_m = nn.HuberLoss()

        self.memory = ReplayMemory(MEMORY_CAPACITY)

        self.episode_durations = []
        self.threshold = 0.
        self.loss = 1.

    def __threshold_func(self, rate, episode, loss, memory_size) -> float:
        raw_thres = EX_THRES_START + (EX_THRES_END - EX_THRES_START) * (
            np.tanh(PACE_EITA * memory_size * rate + OFFSET_LAMBDA) + 1) / 2

        return min(raw_thres, EX_THRES_END)

    def select_action(self, state, episode=None, force_explore=False) -> torch.Tensor:
        threshold =\
            self.__threshold_func(EX_THRES_RATE, episode,
                                  self.loss, len(self.memory))

        self.threshold = threshold

        if not force_explore and random.random() < threshold:
            with torch.no_grad():
                return self.qn_policy(state)
        else:
            r = random.randrange(self.action_count)
            return torch.tensor([(1 if i == r else 0) for i in range(self.action_count)], dtype=torch.float64, device=self.device)

    def memorize(self, *args):
        self.memory.push(*args)

    def step(self):
        if len(self.memory) < self.batch_size:
            return

        batch_dict = Transition(*zip(*self.memory.sample(self.batch_size)))
        reward_batch = torch.tensor(batch_dict.reward, device=self.device)

        actions = [self.qn_policy(state) for state in batch_dict.state]
        action_values = torch.tensor(
            [item.max().detach() for item in actions], requires_grad=True, device=self.device)

        state2_values = torch.zeros(self.batch_size, device=self.device)

        for i, state2 in enumerate(batch_dict.state2):
            if state2 is None:
                continue

            state2_values[i] = self.qn_target(state2).max().detach()

        # Expected Q values
        expected_action_values = (
            (state2_values * GAMMA) + reward_batch
        ).detach().requires_grad_(True)

        loss = self.loss_m(action_values, expected_action_values.unsqueeze(1))
        self.loss = loss.item()

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.memory.is_full:
            self.memory.dropout(.06)
        # r = random.random()
        # if r < len(self.memory) / self.memory.maxlen:
        #     self.memory.dropout(.01)

    def save(self, id: str):
        torch.save(self.qn_policy, SAVE_PATH.format(id))
        torch.save(self.qn_target, T_SAVE_PATH.format(id))


class LoadedAgent:
    def __init__(self, qn_path, action_count, device='cpu') -> None:
        self.qn_policy = torch.load(qn_path).to(device)
        self.device = device
        self.action_count = action_count

    def select_action(self, state, explore=False) -> torch.Tensor:
        if not explore:
            with torch.no_grad():
                return self.qn_policy(state)
        else:
            r = random.randrange(self.action_count)
            return torch.tensor([(1 if i == r else 0) for i in range(self.action_count)], dtype=torch.float64, device=self.device)
