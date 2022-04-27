from torch import nn


class DQNPolicy(nn.Module):
    def __init__(self, state_count: int, action_count: int):
        super(DQNPolicy, self).__init__()

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

    def forward(self, x):
        return self.seq(x)
