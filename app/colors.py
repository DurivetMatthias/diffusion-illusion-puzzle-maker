import random


def get_distinct_colors() -> list[tuple[float, float, float]]:
    colors = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),  # Primary colors: Red, Green, Blue
        (1, 1, 0),
        (0, 1, 1),
        (1, 0, 1),  # Secondary colors: Yellow, Cyan, Magenta
    ]

    random_colors = []

    # Generate combinations with varying intensities
    start = 3
    stop = start + 4

    for r in range(start, stop):
        for g in range(start, stop):
            for b in range(start, stop):
                color = (r / stop, g / stop, b / stop)
                if r == g == b:
                    # Skip grayscale colors
                    continue
                random_colors.append(color)

    # Shuffle the list to avoid similar colors being next to each other
    random.shuffle(random_colors)
    return colors + random_colors
