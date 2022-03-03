import torch
from torch import cuda


def test_cuda(verbose=False) -> bool:
    cuda_available = cuda.is_available()
    if not verbose:
        return cuda_available

    print("CUDA supported?: " + 'Yes' if cuda_available else 'No')
    print("Current CUDA version: " + torch.version.cuda if cuda_available else "n/a")
    print("-" * 20)

    if cuda_available:
        for i in range(cuda.device_count()):
            dp = cuda.get_device_properties(i)
            print(f"GPU {i}:\t{dp.name}")
            print(f"\t\tMinimal CUDA version: {dp.major}.{dp.minor}")

    return cuda_available


def main():
    test_cuda(verbose=True)


if __name__ == '__main__':
    main()
