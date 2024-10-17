from app.jigsaw_classes import EdgeConnector
from app.jigsaw_classes import SimpleConnector
from app.jigsaw_classes import Piece

used_ids = []


def get_unique_id():
    new_id = max(used_ids, default=0) + 1
    used_ids.append(new_id)
    return new_id


def make_distinct_simple_connector():
    return SimpleConnector(get_unique_id())


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


def make_distinct_corner_piece():
    edge_a = EdgeConnector()
    edge_b = EdgeConnector()
    connector_a = make_distinct_simple_connector()
    connector_b = make_distinct_simple_connector()
    return Piece(
        north=connector_a,
        east=connector_b,
        south=edge_a,
        west=edge_b,
    )


def make_distinct_edge_piece():
    edge_a = EdgeConnector()
    connector_a = make_distinct_simple_connector()
    connector_b = make_distinct_simple_connector()
    connector_c = make_distinct_simple_connector()
    return Piece(
        north=connector_a,
        east=connector_b,
        south=connector_c,
        west=edge_a,
    )


def make_distinct_piece():
    connector_a = make_distinct_simple_connector()
    connector_b = make_distinct_simple_connector()
    connector_c = make_distinct_simple_connector()
    connector_d = make_distinct_simple_connector()
    return Piece(
        north=connector_a,
        east=connector_b,
        south=connector_c,
        west=connector_d,
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


def make_puzzle(width, height):
    outlined_grid = LinkedGrid(width + 2, height + 2)

    # Create an outline of pieces that have flat edges on all sides.
    # Inside this outline we can then place the regular puzzle pieces.
    current_cell = outlined_grid.get_cell(0, 0)
    while current_cell.east:
        current_cell.piece = make_outline_piece()
        current_cell = current_cell.east
    while current_cell.north:
        current_cell.piece = make_outline_piece()
        current_cell = current_cell.north
    while current_cell.west:
        current_cell.piece = make_outline_piece()
        current_cell = current_cell.west
    while current_cell.south:
        current_cell.piece = make_outline_piece()
        current_cell = current_cell.south
