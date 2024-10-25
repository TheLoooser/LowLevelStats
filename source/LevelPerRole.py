import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def create_plot(data, ax):
    data_points = []
    for _, players in data.items():
        points = [[player[1],  # level
                   player[6],  # role
                   ] for player in players if player]
        data_points.extend(points)

    df = pd.DataFrame(data_points, columns=['level', 'role'])
    df = df.groupby('role').mean()
    df = df.reindex(index=['TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY'])

    palette = sns.color_palette("viridis", 5)
    sns.barplot(x=df.index, y=df['level'], palette=palette, hue=df.index)
    ax.tick_params(axis='x', which='major', pad=30)

    def get_position(name):
        path = f"images/ranked-positions/Position_Plat-{name}.png"
        im = plt.imread(path)
        return im

    def offset_image(coord, name, a):
        img = get_position(name)
        im = OffsetImage(img, zoom=0.45)
        im.image.axes = a

        ab = AnnotationBbox(im, (coord, 0), xybox=(0., -18.), frameon=False,
                            xycoords='data', boxcoords="offset points", pad=0)

        a.add_artist(ab)

    for i, c in enumerate(['Top', 'Jungle', 'Mid', 'Bot', 'Support']):
        offset_image(i, c, ax)

    plt.title("Average Level per role", fontweight='bold')
    plt.xlabel('Role')
    plt.ylabel('Avg Lvl')
