import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy.signal import savgol_filter


def elo_linear(opponent_rating, win, loss, total, draw=0):
    return opponent_rating + 400 * ((win + draw / 2) - (loss + draw / 2)) / total


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


SLICES = 80


def smooth(input):
    if input is pd.Series:
        input = input.to_list()

    return savgol_filter(input, 525, 4, mode='nearest')


def smooth2(input):
    if input is pd.Series:
        input = input.to_list()

    return savgol_filter(input, 17, 4, mode='nearest')


def loss_comp():
    # Stochastic Gradient Descent
    df_sgd = pd.read_csv('./results/losses-2022-05-26_16-07-1653552474.csv')
    # Root Mean Square Propagation
    df_rmsprop = pd.read_csv(
        './results/losses-2022-05-26_16-25-1653553534.csv')
    # Adaptive Moment Estimation
    df_adam = pd.read_csv('./results/losses-2022-05-26_16-48-1653554907.csv')

    split_end = min(len(df_sgd['0']), len(df_rmsprop['0']), len(df_adam['0']))

    # df = pd.read_csv('./results/memory-2022-05-23_22-23-1653315809.csv')
    # print(df)

    # length = len(df)
    # slices = int(length / SLICES)

    # avgs = []
    # for i in range(SLICES - 1):
    #     avgs.append(df[slices*i:slices*(i+1)]['0'].mean())

    df = pd.DataFrame({
        'episode': list(range(1, split_end + 1)),
        'SGD': smooth(df_sgd['0'][:split_end]),
        'RMSprop': smooth(df_rmsprop['0'][:split_end]),
        'Adam': smooth(df_adam['0'][:split_end]),
    }).melt(('episode'), ('SGD', 'RMSprop', 'Adam'), value_name='loss', var_name='optimizer')

    print(df)

    # print(avgs)
    init_plotting()
    # plot_losses(avgs, episodes=[i * slices for i in range(SLICES - 1)])
    # plot_losses(savgol_filter(df['0'].to_list(), 545, 4, mode='nearest'))
    sns.lineplot(
        data=df,
        x='episode',
        y='loss',
        hue='optimizer',
    )
    plt.title('Loss Comparison')
    plt.savefig(FIGURE_ROOT / 'loss_comparison.png')
    plt.show()
    # plot_memory(df['0'].to_list())


def elorating():
    win_loss = pd.read_csv(
        './results/win_loss-2022-05-23_22-58-1653317887.csv')['0']

    ratings = []
    wins = 0
    losses = 0
    draws = 0
    total = len(win_loss)

    s = win_loss
    for i in range(total):
        if s[i] > 0:
            wins += 1
        elif s[i] < 0:
            losses += 1
        else:
            draws += 1

        x = i - 4
        if x > 0:
            ratings.append(elo_linear(1000, wins, losses, x, draws))

    df = pd.DataFrame({
        'episode': list(range(1, len(ratings) + 1)),
        'rating_smooth': smooth2(ratings),
        'raw_rating': ratings,
    }).melt(id_vars='episode', value_vars=['raw_rating', 'rating_smooth'], var_name='rating_type', value_name='rating')

    init_plotting()
    sns.lineplot(
        data=df,
        x='episode',
        y='rating',
    )
    plt.title('Elo Rating')
    plt.savefig(FIGURE_ROOT / 'elo_rating.png')
    plt.show()


def main():
    # loss_comp()
    elorating()


if __name__ == '__main__':
    main()
