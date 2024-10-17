import itertools
import math

from app.jigsaw_classes import EdgeConnector
from app.jigsaw_classes import SimpleConnector
from app.jigsaw_classes import Piece
from app import visualisation


def make_outline_piece():
    edge_a = EdgeConnector()
    edge_b = EdgeConnector()
    edge_c = EdgeConnector()
    edge_d = EdgeConnector()
    return Piece(
        north=edge_a,
        east=edge_b,
        south=edge_c,
        west=edge_d,
    )


class GridCell:
    def __init__(self):
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.piece = None
        self.x = None
        self.y = None


class LinkedGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[GridCell() for _ in range(width)] for _ in range(height)]
        self._link_cells()

    def _link_cells(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                cell.x = x
                cell.y = y
                if y > 0:
                    cell.south = self.grid[y - 1][x]
                if y < self.height - 1:
                    cell.north = self.grid[y + 1][x]
                if x > 0:
                    cell.west = self.grid[y][x - 1]
                if x < self.width - 1:
                    cell.east = self.grid[y][x + 1]

    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else:
            raise IndexError("Cell out of bounds")


def connectors_to_puzzle(
    width,
    height,
    vertical_connector_permutation,
    horizontal_connector_permutation,
):
    pieces = []
    for y in range(height):
        for x in range(width):
            north_connector = None
            east_connector = None
            south_connector = None
            west_connector = None

            if x == 0:
                west_connector = EdgeConnector()
            if x == width - 1:
                east_connector = EdgeConnector()
            if y == 0:
                south_connector = EdgeConnector()
            if y == height - 1:
                north_connector = EdgeConnector()

            if not north_connector:
                north_connector_index = x + (y * width)
                north_connector = SimpleConnector(
                    horizontal_connector_permutation[north_connector_index]
                )

            if not east_connector:
                east_connector_index = x + (y * (width - 1))
                east_connector = SimpleConnector(
                    vertical_connector_permutation[east_connector_index]
                )

            if not south_connector:
                south_connector_index = x + ((y - 1) * width)
                south_connector = SimpleConnector(
                    horizontal_connector_permutation[south_connector_index]
                )

            if not west_connector:
                west_connector_index = (x - 1) + (y * (width - 1))
                west_connector = SimpleConnector(
                    vertical_connector_permutation[west_connector_index]
                )

            piece = Piece(
                north=north_connector,
                east=east_connector,
                south=south_connector,
                west=west_connector,
            )

            pieces.append(piece)
    visualisation.show_pieces(pieces)


def get_amount_of_vertical_connectors(width, height):
    return (width - 1) * height


def get_amount_of_horizontal_connectors(width, height):
    return width * (height - 1)


def make_standard_puzzle(width, height):
    amount_of_vertical_connectors = get_amount_of_vertical_connectors(
        width=width, height=height
    )
    amount_of_horizontal_connectors = get_amount_of_horizontal_connectors(
        width=width, height=height
    )
    amount_of_internal_connectors = (
        amount_of_vertical_connectors + amount_of_horizontal_connectors
    )

    vertical_connector_permutation = list(range(1, amount_of_vertical_connectors + 1))
    horizontal_connector_permutation = list(
        range(amount_of_vertical_connectors + 1, amount_of_internal_connectors + 1)
    )

    return connectors_to_puzzle(
        width,
        height,
        vertical_connector_permutation,
        horizontal_connector_permutation,
    )


def make_diffusion_illusion_puzzle(width, height):
    """
    Creates a puzzle with exactly two solutions.
    This allows a processen known as "diffusion illusion"
    to paint two different images on the same puzzle.
    """

    amount_of_vertical_connectors = get_amount_of_vertical_connectors(
        width=width, height=height
    )
    amount_of_horizontal_connectors = get_amount_of_horizontal_connectors(
        width=width, height=height
    )
    amount_of_internal_connectors = (
        amount_of_vertical_connectors + amount_of_horizontal_connectors
    )
    amount_of_duplicated_connectors = math.ceil(amount_of_internal_connectors / 2)
    all_permutations = list(
        itertools.permutations(range(1, amount_of_duplicated_connectors + 1))
    )
    print("len(all_permutations):", len(all_permutations))
