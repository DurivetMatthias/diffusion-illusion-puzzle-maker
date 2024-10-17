from app.jigsaw_classes import EdgeConnector
from app.jigsaw_classes import OvalConnector
from app.jigsaw_classes import SimpleConnector
from app.jigsaw_classes import Piece
from app import jigsaw_maker
from app import visualisation
from app import colors


def test_edge_connector():
    edge_a = EdgeConnector()
    edge_b = EdgeConnector()
    assert edge_a == edge_b
    assert edge_a == -edge_b


def test_oval_connector():
    tab_a = OvalConnector(skew=1, width=1, height=1)
    tab_b = OvalConnector(skew=2, width=2, height=2)
    assert tab_a != tab_b

    blank_a = OvalConnector(skew=-1, width=1, height=-1)
    blank_b = OvalConnector(skew=-2, width=2, height=-2)
    assert blank_a != blank_b

    assert tab_a == -blank_a
    assert tab_b == -blank_b


def test_simple_connector():
    tab_a = SimpleConnector(id=1)
    tab_b = SimpleConnector(id=2)
    assert tab_a != tab_b

    blank_a = SimpleConnector(id=-1)
    blank_b = SimpleConnector(id=-2)
    assert blank_a != blank_b

    assert tab_a == -blank_a
    assert tab_b == -blank_b


def test_piece_rotation():
    oval_a = SimpleConnector(id=1)
    oval_b = SimpleConnector(id=2)
    oval_c = SimpleConnector(id=3)
    oval_d = SimpleConnector(id=4)

    piece_a = Piece(oval_a, oval_b, oval_c, oval_d)
    rotated_clockwise_once = piece_a.rotate_clockwise()
    rotated_clockwise_twice = piece_a.rotate_clockwise().rotate_clockwise()
    rotated_clockwise_thrice = (
        piece_a.rotate_clockwise().rotate_clockwise().rotate_clockwise()
    )
    rotated_clockwise_four_times = (
        piece_a.rotate_clockwise()
        .rotate_clockwise()
        .rotate_clockwise()
        .rotate_clockwise()
    )

    rotated_counter_clockwise_once = piece_a.rotate_counter_clockwise()
    rotated_counter_clockwise_twice = (
        piece_a.rotate_counter_clockwise().rotate_counter_clockwise()
    )
    rotated_counter_clockwise_thrice = (
        piece_a.rotate_counter_clockwise()
        .rotate_counter_clockwise()
        .rotate_counter_clockwise()
    )
    rotated_counter_clockwise_four_times = (
        piece_a.rotate_counter_clockwise()
        .rotate_counter_clockwise()
        .rotate_counter_clockwise()
        .rotate_counter_clockwise()
    )

    assert piece_a != rotated_clockwise_once
    assert piece_a != rotated_clockwise_twice
    assert piece_a != rotated_clockwise_thrice
    assert piece_a == rotated_clockwise_four_times

    assert piece_a != rotated_counter_clockwise_once
    assert piece_a != rotated_counter_clockwise_twice
    assert piece_a != rotated_counter_clockwise_thrice

    assert piece_a == rotated_counter_clockwise_four_times
    assert rotated_clockwise_once == rotated_counter_clockwise_thrice
    assert rotated_clockwise_twice == rotated_counter_clockwise_twice
    assert rotated_clockwise_thrice == rotated_counter_clockwise_once
    assert rotated_clockwise_four_times == piece_a


def test_colors():
    assert (
        len(colors.get_distinct_colors()) > 40
    ), f"Expected at least 40 colors, got {len(colors.get_distinct_colors())}"


def test_serialization():
    piece_a = jigsaw_maker.make_distinct_piece()
    piece_a.save_to_json("piece_a")
    piece_b = Piece.load_from_json("piece_a")
    assert piece_a == piece_b, "Expected pieces to be equal after serialization"

    piece_a = jigsaw_maker.make_distinct_edge_piece()
    piece_a.save_to_json("piece_a")
    piece_b = Piece.load_from_json("piece_a")
    assert piece_a == piece_b, "Expected pieces to be equal after serialization"

    piece_a = jigsaw_maker.make_distinct_corner_piece()
    piece_a.save_to_json("piece_a")
    piece_b = Piece.load_from_json("piece_a")
    assert piece_a == piece_b, "Expected pieces to be equal after serialization"


def test_jigsaw_maker():
    jigsaw_maker.make_puzzle(5, 5)


if __name__ == "__main__":
    test_oval_connector()
    test_edge_connector()
    test_piece_rotation()
    test_colors()
    test_serialization()
    test_jigsaw_maker()
