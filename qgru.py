import torch
from torch import nn


class QGRU(nn.Module):
    def __init__(self, state_count: int, action_count: int):
        super(QGRU, self).__init__()

        self.seq = nn.Sequential(
            nn.Linear(state_count, 256),
            nn.LeakyReLU(),
            nn.Linear(256, 620),
            nn.LeakyReLU(),
            nn.Linear(620, 1080),
            nn.LeakyReLU(),
            nn.Linear(1080, 480),
            nn.LeakyReLU(),
            nn.Linear(480, action_count),
        )

        # nn.GRU

        self.__p = nn.Parameter(torch.empty(0))

    def forward(self, x):
        if isinstance(x, torch.Tensor):
            x = x.to(self.__p.device)
            pass

        return self.seq(x)
