from typing import Union
import math
import random
import torch
from torch import nn
import matplotlib.pyplot as plt

import q
from memory import ReplayMemory, Transition

BATCH_SIZE = 128
GAMMA = .999                # Discount coefficient
EPS_START = .9
EPS_END = .05
EPS_DECAY = 200
TARGET_UPDATE = 10

LEARNING_RATE = .003
MEMORY_CAPACITY = 12000


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
            q.DQNPolicy(state_count, action_count, device=device)
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

    def select_action(self, state):
        sample = random.random()

        eps_threshold = EPS_END + \
            (EPS_START - EPS_END) * math.exp(-1. * self.step_count / EPS_DECAY)
        self.state_count += 1

        if sample > eps_threshold:
            with torch.no_grad():
                return self.qn_policy(state).max(1)[1].view(1, 1)
        else:
            return torch.tensor([[random.randrange(self.action_count)]], dtype=torch.long, device=self.device)

    def step(self):
        if len(self.memory) < BATCH_SIZE:
            return

        transitions = self.memory.sample(BATCH_SIZE)
        batch = Transition(*zip(*transitions))

        non_final_mask = torch.tensor(
            tuple(map(lambda s: s is not None, batch.state2)),
            dtype=torch.bool,
            device=self.device
        )
        non_final_states2 = torch.cat(
            [s for s in batch.state2 if s is not None]
        )

        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        action_values = self.qn_policy(state_batch).gather(1, action_batch)

        state2_values = torch.zeros(BATCH_SIZE, device=self.device)
        state2_values[non_final_mask] = self.qn_target(
            non_final_states2).max(1)[0].detach()

        # Expected Q values
        expected_action_values = (state2_values * GAMMA) + reward_batch

        loss: torch.Tensor = \
            self.loss_m(action_values, expected_action_values.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()
        for param in self.qn_policy.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

    def plot_durations(self):
        plt.figure(2)
        plt.clf()
        durations_t = torch.tensor(self.episode_durations, dtype=torch.float)
        plt.title('Training...')
        plt.xlabel('Episode')
        plt.ylabel('Duration')
        plt.plot(durations_t.numpy())
        # Take 100 episode averages and plot them too
        if len(durations_t) >= 100:
            means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
            means = torch.cat((torch.zeros(99), means))
            plt.plot(means.numpy())
