import math

import matplotlib.pyplot as plt

from app.jigsaw_classes import Connector, SimpleConnector
from app.jigsaw_classes import Piece
from app.colors import get_distinct_colors

color_spectrum = get_distinct_colors()


def get_color_for_connector(connector: Connector):
    if isinstance(connector, SimpleConnector):
        return color_spectrum[(abs(connector.id) - 1) % len(color_spectrum)]
    return "black"


def draw_piece(piece: Piece, offset_x=0, offset_y=0):
    print("offset_x:", offset_x)
    print("offset_y:", offset_y)
    print("[0 + offset_x, 0 + offset_y]:", [0 + offset_x, 0 + offset_y])
    print("[0 + offset_x, 1 + offset_y]:", [0 + offset_x, 1 + offset_y])
    # south
    plt.plot(
        [0 + offset_x, 0 + offset_x],
        [0 + offset_y, 1 + offset_y],
        color=get_color_for_connector(piece.north),
    )
    # east
    plt.plot(
        [0 + offset_x, 1 + offset_x],
        [1 + offset_y, 1 + offset_y],
        color=get_color_for_connector(piece.east),
    )
    # north
    plt.plot(
        [1 + offset_x, 1 + offset_x],
        [1 + offset_y, 0 + offset_y],
        color=get_color_for_connector(piece.south),
    )
    # west
    plt.plot(
        [1 + offset_x, 0 + offset_x],
        [0 + offset_y, 0 + offset_y],
        color=get_color_for_connector(piece.west),
    )


def show_piece(piece: Piece):
    draw_piece(piece)

    plt.axis("equal")
    plt.show()


def show_pieces(pieces, spacing=1):
    num_pieces = len(pieces)
    grid_size = math.ceil(math.sqrt(num_pieces))

    for index, piece in enumerate(pieces):
        row = index // grid_size
        col = index % grid_size
        offset_x = col + (col * spacing)
        offset_y = row + (row * spacing)
        draw_piece(piece, offset_x, offset_y)

    plt.axis("equal")
    plt.show()
