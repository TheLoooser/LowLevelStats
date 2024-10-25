import pickle
import seaborn as sns
import matplotlib.pyplot as plt

from source.RiotApi import get_information
from source.Metrics import calculate_metrics
from source.Parameters import get_parser_args
import source.LowLevelPercentages
import source.LevelDistribution
import source.RankLevelRelation
import source.LevelPerRole


# summoner_name = 'TheŁoooser'


if __name__ == '__main__':
    args = get_parser_args()
    summoner_name = args.summoner_name
    tag_line = args.tag_line
    queue_type = args.queue_type
    queue_mapping = {'RANKED_SOLO_5x5': 'Solo/Duo', 'RANKED_FLEX_SR': 'Flex'}

    summoner_info, matches = get_information(summoner_name, tag_line, queue_type)

    with open(f'data/{summoner_name}.pickle', 'wb') as handle:
        pickle.dump(summoner_info, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(f'data/{summoner_name}_matches.pickle', 'wb') as handle:
        pickle.dump(matches, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(f'data/{summoner_name}.pickle', 'rb') as handle:
        s_info = pickle.load(handle)

    with open(f'data/{summoner_name}_matches.pickle', 'rb') as handle:
        data = pickle.load(handle)

    metrics = calculate_metrics(data)

    sns.set(style="darkgrid")
    fig, axs = plt.subplots(2, 2, figsize=(18, 14))
    source.LowLevelPercentages.create_plot(data, axs[0, 0])
    source.LevelDistribution.create_plot(data, axs[0, 1])
    source.RankLevelRelation.create_plot(data, axs[1, 0])
    source.LevelPerRole.create_plot(data, axs[1, 1])
    fig.suptitle(f'{summoner_name.upper()}\n\n', fontsize=30, fontweight='bold', fontfamily='Times New Roman')
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.95,
                        top=0.85,
                        wspace=0.1,
                        hspace=0.3)
    fig.text(0.5, 0.94, f"Level: {s_info['level']}, Rank: {s_info['rank']} {s_info['division']}, LP: {s_info['lp']}, "
                        f"Queue: {queue_mapping[queue_type]}, No. of games: {s_info['games']}, Win-%: {s_info['win']:.2f}",
             fontsize=18, ha='center', fontweight='bold', fontfamily='Times New Roman')
    fig.text(0.5, 0.90, f"Level-Statistics: Min: {metrics['min']}, Max: {metrics['max']}, "
                        f"Avg: {metrics['avg']:.2f}, Median: {metrics['median']}", fontsize=18, ha='center')
    plt.savefig(f'results/{summoner_name}.png')
