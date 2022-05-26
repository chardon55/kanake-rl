import pandas as pd

import plots


RATING = 1000


def elo_linear(opponent_rating, win, loss, total, draw=0):
    return opponent_rating + 400 * ((win + draw / 2) - (loss + draw / 2)) / total


def main():
    df = pd.read_csv('./results/win_loss-2022-05-23_22-58-1653317887.csv')

    ratings = []
    wins = 0
    losses = 0
    draws = 0
    total = len(df)

    s = df['0']
    for i in range(total):
        if s[i] > 0:
            wins += 1
        elif s[i] < 0:
            losses += 1
        else:
            draws += 1

        x = i - 4
        if x > 0:
            ratings.append(elo_linear(RATING, wins, losses, x, draws))

    plots.init_plotting()
    plots.plot_elo(ratings)


if __name__ == '__main__':
    main()
