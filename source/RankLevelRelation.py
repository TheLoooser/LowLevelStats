import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

TIERS = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
DIVISIONS = ['IV', 'III', 'II', 'I']
COLOUR = {
    'IRON': (161, 157, 148),
    'BRONZE': (176, 141, 87),
    'SILVER': (170, 169, 173),
    'GOLD': (255, 213, 0),
    'PLATINUM': (0, 230, 230),
    'EMERALD': (100, 160, 70),
    'DIAMOND': (51, 85, 255),
    'MASTER': (153, 85, 187),
    'GRANDMASTER': (255, 51, 85),
    'CHALLENGER': (255, 255, 128)
}


def get_rank(tier, div, lp):
    return TIERS.index(tier) * 4 + DIVISIONS.index(div) + (lp / 100)


def create_plot(data, ax):
    data_points = []
    for _, players in data.items():
        points = [[player[1],  # level
                   get_rank(player[2], player[3], player[4]),  # rank
                   players[2], tuple(c/255 for c in COLOUR[player[2]])  # tier, colour
                   ] for player in players if player]
        data_points.extend(points)

    df = pd.DataFrame(data_points, columns=['level', 'rank', 'tier', 'colour'])

    ax.scatter(x=df['level'], y=df['rank'], c=df['colour'], s=20)
    y_tick_min, y_tick_max = int(ax.get_yticks()[0]), int(ax.get_yticks()[-1])
    ticks = list(range(y_tick_min, y_tick_max))

    division = {0: 'IV', 1: 'III', 2: 'II', 3: 'I'}
    labels = [division[t % 4] for t in ticks]
    ax.set_yticks(ticks, labels, fontfamily='Times New Roman')

    def get_emblem(name):
        path = f"images/ranked-emblem/emblem-{name}.png"
        im = plt.imread(path)
        return im

    def offset_image(coord, name, a):
        img = get_emblem(name)
        im = OffsetImage(img, zoom=0.3)
        im.image.axes = a

        ab = AnnotationBbox(im, (0, (coord + 1) * 4 + 2), xybox=(-80., 0.), frameon=False,
                            xycoords='data', boxcoords="offset points", pad=0)
        a.add_artist(ab)

    for i, c in enumerate(['bronze', 'silver', 'gold', 'platinum', 'diamond', 'master', 'grandmaster', 'challenger']):
        offset_image(i, c, ax)

    ax.set_title("Rank-Level relation", fontweight='bold')
    ax.set_xlabel('Level')
