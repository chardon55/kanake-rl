import torch
from torch import cuda


def test_cuda(verbose=False, rand_test=False) -> torch.device:
    cuda_available = cuda.is_available()
    available_device = torch.device("cuda" if cuda_available else "cpu")

    if verbose:
        print("CUDA supported?: " + 'Yes' if cuda_available else 'No')
        print("Current CUDA version: " +
              torch.version.cuda if cuda_available else "n/a")
        print("-" * 20)

        if cuda_available:
            for i in range(cuda.device_count()):
                dp = cuda.get_device_properties(i)
                print(f"GPU {i}:\t{dp.name}")
                print(f"\t\tCUDA compatibility: {dp.major}.{dp.minor}")

    if rand_test:
        print("Generating a 5x5 tensor... ", end='')
        gr = torch.rand(5, 5, device='cuda')
        print("done")
        print(gr)

    return available_device


def main():
    test_cuda(verbose=True, rand_test=True)


if __name__ == '__main__':
    main()
