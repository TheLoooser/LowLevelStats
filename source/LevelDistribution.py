import seaborn as sns
from collections import Counter


def create_plot(data, ax):
    all_levels = []
    for _, players in data.items():
        levels = [player[1] for player in players if player]
        all_levels.extend(levels)

    all_levels.sort()
    freq = Counter((x - 1) // 50 for x in all_levels)

    palette = sns.color_palette("hls", len(freq))
    x = list(freq.keys())
    sns.barplot(x=x, y=list(freq.values()), palette=palette, ax=ax, hue=x)

    labels = [f"{i*50}-{(i+1)*50}" for i in x]
    ax.set_xticks(x, labels, rotation=60)
    ax.set_title("Level distribution", fontweight='bold')
    ax.set_xlabel('Level')
    ax.set_ylabel('Number of players')
    ax.legend_.remove()
