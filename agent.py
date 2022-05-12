from typing import Union
import math
import random
import numpy as np
import torch
from torch import nn
import numpy as np
from datetime import datetime

import q
from memory import ReplayMemory, Transition

GAMMA = .96                # Discount coefficient

TARGET_UPDATE = 10

EX_THRES_START = .03
EX_THRES_END = .95
EX_THRES_RATE = .005

LEARNING_RATE = .003
MEMORY_CAPACITY = 12000

SAVE_PATH = './models/ddqn-{0}-.pt'
T_SAVE_PATH = './models/ddqn-target-{0}-.pt'


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

        # Use RMSprop rather than Adam
        self.optimizer = torch.optim.RMSprop(
            self.qn_policy.parameters(),
            lr=LEARNING_RATE,
        )

        self.loss_m = nn.SmoothL1Loss()

        self.memory = ReplayMemory(MEMORY_CAPACITY)
        self.step_count = 0

        self.episode_durations = []
        self.threshold = 0
        self.loss = 0

    def select_action(self, state) -> torch.Tensor:
        self.threshold = threshold = EX_THRES_START + \
            (EX_THRES_END - EX_THRES_START) * \
            np.tanh(self.step_count * EX_THRES_RATE)

        if random.random() > threshold:
            with torch.no_grad():
                return self.qn_policy(state).argmax()
        else:
            return torch.tensor(random.randrange(self.action_count), dtype=torch.int64, device=self.device)

    def memorize(self, *args):
        self.memory.push(*args)

    def step(self):
        if len(self.memory) < self.batch_size:
            return

        transitions = self.memory.sample(self.batch_size)
        batch_dict = Transition(*zip(*transitions))

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
        expected_action_values = torch.tensor(
            (state2_values * GAMMA) + reward_batch, requires_grad=True, device=self.device
        )

        self.loss = loss = self.loss_m(
            action_values, expected_action_values.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.step_count += 1

    def save(self):
        d_str = datetime.now().strftime(r'%Y-%m-%d_%H-%M-%s')

        torch.save(self.qn_policy, SAVE_PATH.format(d_str))
        torch.save(self.qn_target, T_SAVE_PATH.format(d_str))
