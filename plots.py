import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


FIGURE_ROOT = Path('./figures')


def init_plotting():
    sns.set_theme(style='darkgrid', palette='deep')


def plot(x, y, x_name='x', y_name='y', save_to=None, title: str = None):
    df = pd.DataFrame(
        data={
            x_name: x,
            y_name: y,
        },
    )

    sns.lineplot(
        data=df,
        x=x_name,
        y=y_name,
    )
    if title is not None:
        plt.title(title)

    if save_to is not None:
        plt.savefig(save_to)

    plt.show()


def plot_thresholds(thresholds, file_name: str = None, title_addition: str = None):
    plot(
        list(range(1, len(thresholds) + 1)),
        thresholds,
        x_name='Episode',
        y_name='Threshold',
        save_to=FIGURE_ROOT / (file_name + '.png'),
        title=f'Thresholds{"" if title_addition is None else f" ({title_addition})"}',
    )


def plot_losses(losses, file_name: str = None, title_addition: str = None, episodes=None):
    plot(
        list(range(1, len(losses) + 1)) if episodes is None else episodes,
        losses,
        x_name='Episode',
        y_name='Loss',
        save_to=FIGURE_ROOT /
        (file_name + '.png') if file_name is not None else None,
        title=f'Loss{"" if title_addition is None else f" ({title_addition})"}',
    )


def plot_memory(memory, file_name: str = None, title_addition: str = None, episodes=None):
    plot(
        list(range(1, len(memory) + 1)) if episodes is None else episodes,
        memory,
        x_name='Episode',
        y_name='Memory',
        save_to=FIGURE_ROOT /
        (file_name + '.png') if file_name is not None else None,
        title=f'Memory{"" if title_addition is None else f" ({title_addition})"}',
    )


def plot_elo(ratings, file_name: str = None, title_addition: str = None, episodes=None):
    plot(
        list(range(1, len(ratings) + 1)) if episodes is None else episodes,
        ratings,
        x_name='Episode',
        y_name='Linear Elo',
        save_to=FIGURE_ROOT /
        (file_name + '.png') if file_name is not None else None,
        title=f'Average Ratings{"" if title_addition is None else f" ({title_addition})"}',
    )


SLICES = 34


def main():
    # df = pd.read_csv('./results/losses-2022-05-23_21-34-1653312871.csv')
    df = pd.read_csv('./results/memory-2022-05-23_22-23-1653315809.csv')
    # print(df)

    # length = len(df)
    # slices = int(length / SLICES)

    # avgs = []
    # for i in range(SLICES - 1):
    #     avgs.append(df[slices*i:slices*(i+1)]['0'].mean())

    # print(avgs)
    init_plotting()
    # plot_losses(avgs, episodes=[i * slices for i in range(SLICES - 1)])
    plot_memory(df['0'].to_list())


if __name__ == '__main__':
    main()
