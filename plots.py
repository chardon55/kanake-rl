import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


FIGURE_ROOT = Path('./figures')


def init_plotting():
    sns.set_style('darkgrid')
    sns.color_palette('mako', as_cmap=True)


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


def plot_losses(losses, file_name: str = None, title_addition: str = None):
    plot(
        list(range(1, len(losses) + 1)),
        losses,
        x_name='Episode',
        y_name='Loss',
        save_to=FIGURE_ROOT / (file_name + '.png'),
        title=f'Loss{"" if title_addition is None else f" ({title_addition})"}',
    )
