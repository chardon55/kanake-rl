import torch
from torch import nn
import numpy as np

import q
from memory import Memory


class Agent(nn.Module):
    def __init__(self, state_count: int, action_count: int, batch_size: int) -> None:
        super(Agent, self).__init__()
        self.state_count = state_count
        self.action_count = action_count
        self.batch_size = batch_size

        # Double DQN
        self.qn = q.DQNPolicy(state_count, action_count)
        self.qn_target = q.DQNPolicy(state_count, action_count)

        self.optimizer = torch.optim.Adam(self.qn.parameters(), lr=0.003)
