import torch
from torch.nn import Module
import numpy as np


class KRLModel(Module):
    def __init__(self):
        super().__init__()


def main():
    # print(torch.cuda.is_available())

    # t = torch.rand(2, 2).cuda()
    # print(t)
    # print(t.device)
    a = np.zeros([5, 5])
    a[0, 0] = 3
    a[1, 1] = 5
    a[1, 3] = 9
    a[2] = 6
    a[3, 4] = 6

    print(a)
    print(-a[::-1])
    # print(np.flip(a, axis=0))


if __name__ == '__main__':
    main()
