import torch


def main():
    print(torch.cuda.is_available())

    t = torch.rand(2, 2).cuda()
    print(t)
    print(t.device)


if __name__ == '__main__':
    main()
