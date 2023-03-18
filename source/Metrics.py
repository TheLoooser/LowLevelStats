def calculate_metrics(data):
    avg_level_per_match = []
    max_level_per_match = []
    min_level_per_match = []
    all_levels = []
    for _, players in data.items():
        levels = [player[1] for player in players if player]
        avg_level = sum(levels) / len(levels)
        avg_level_per_match.append(avg_level)

        max_level = max(levels)
        max_level_per_match.append(max_level)

        min_level = min(levels)
        min_level_per_match.append(min_level)

        all_levels.extend(levels)

    min_ = min(min_level_per_match)
    max_ = max(max_level_per_match)
    avg = sum(avg_level_per_match) / len(avg_level_per_match)
    index = int(len(all_levels) / 2)
    median = all_levels[index] if len(all_levels) % 2 == 0 else (all_levels[index] + all_levels[index + 1]) / 2

    return {'min': min_, 'max': max_, 'avg': avg, 'median': median}