import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.patches as mpatches


def create_plot(data, ax):
    matrix = np.zeros((8, 10))
    thresholds = [35, 40, 50, 60, 70, 80, 90, 100]
    for _, players in data.items():
        levels = [player[1] for player in players if player]
        for i, t in enumerate(thresholds):
            j = sum(level <= t for level in levels)
            if j > 0:
                matrix[i][j - 1] += 1

    matrix = matrix / len(data) * 100

    df = pd.DataFrame(matrix,
                      columns=[i for i in range(1, 11)],
                      index=thresholds)

    total = df.sum(axis=0)
    n = total.astype(bool).sum()
    colours = sns.color_palette('rocket', n)

    handles = []
    for ind, t in enumerate(total.iloc[::-1]):
        if t > 0:
            i = len(df.columns) - ind
            colour = colours[i - 1]
            sns.barplot(x=thresholds, y=df[[*range(1, i + 1)]].sum(axis=1), color=colour, ax=ax)
            handles.append(mpatches.Patch(label=str(i), color=colour))

    ax.legend(handles=handles)
    ax.set_title("Percentage of the amount of low level players per game", fontweight='bold')
    ax.set_xlabel('Level')
    ax.set_ylabel('Percentage of games')
