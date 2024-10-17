import json


class Connector:
    def __neg__(self):
        """
        The built-in negation operator will be used to create the counterpart of a connector.
        For two connectors to fit together, one must be the negation of the other.
        """
        pass

    def __eq__(self, value):
        """
        The built-in equality operator will be used to compare two connectors.
        Two connectors are equal if they are the same type and have the same properties.
        """
        pass

    def connects_to(self, other):
        """
        This method will be used to check if two connectors fit together.
        """
        return self == -other

    def to_dict(self):
        """
        This method will be used to serialize a connector to a dictionary.
        This way results can be saved to a JSON file and loaded later.
        """
        class_name = self.__class__.__name__
        return {
            "class_name": class_name,
            "data": self.__dict__,
        }

    @staticmethod
    def from_dict(data: dict):
        """
        This method will be used to deserialize a connector from a dictionary.
        This way results can be saved to a JSON file and loaded later.
        """
        class_name = data["class_name"]
        if class_name == "EdgeConnector":
            return EdgeConnector()
        elif class_name == "OvalConnector":
            return OvalConnector(**data["data"])
        elif class_name == "SimpleConnector":
            return SimpleConnector(**data["data"])


class EdgeConnector(Connector):
    def __eq__(self, value):
        return isinstance(value, EdgeConnector)

    def __neg__(self):
        return EdgeConnector()

    def __hash__(self):
        return 0


class OvalConnector(Connector):
    def __init__(self, skew: int, width: int, height: int):
        self.skew = skew
        self.width = width
        self.height = height

    def __neg__(self):
        return OvalConnector(-self.skew, self.width, -self.height)

    def __hash__(self):
        return hash((self.skew, self.width, self.height))

    def __eq__(self, value):
        is_oval = isinstance(value, OvalConnector)
        properties_match = hash(self) == hash(value)
        return is_oval and properties_match


class SimpleConnector(Connector):
    def __init__(self, id: int):
        self.id = id

    def __neg__(self):
        return SimpleConnector(-self.id)

    def __hash__(self):
        return self.id

    def __eq__(self, value):
        is_same_class = isinstance(value, SimpleConnector)
        has_same_id = self.id == value.id
        return is_same_class and has_same_id


class Piece:
    def __init__(
        self,
        north: Connector,
        east: Connector,
        south: Connector,
        west: Connector,
    ):
        self.north = north
        self.east = east
        self.south = south
        self.west = west

    def rotate_clockwise(self):
        return Piece(self.west, self.north, self.east, self.south)

    def rotate_counter_clockwise(self):
        return Piece(self.east, self.south, self.west, self.north)

    def __eq__(self, value):
        return (
            self.north == value.north
            and self.east == value.east
            and self.south == value.south
            and self.west == value.west
        )

    def save_to_json(self, name: str):
        data = {
            "north": self.north.to_dict(),
            "east": self.east.to_dict(),
            "south": self.south.to_dict(),
            "west": self.west.to_dict(),
        }
        data_folder = "json_pieces"
        with open(f"{data_folder}/{name}.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_from_json(name: str):
        data_folder = "json_pieces"
        with open(f"{data_folder}/{name}.json", "r") as file:
            data = json.load(file)
        north = Connector.from_dict(data["north"])
        east = Connector.from_dict(data["east"])
        south = Connector.from_dict(data["south"])
        west = Connector.from_dict(data["west"])
        return Piece(north, east, south, west)


class Puzzle:
    def __init__(self, pieces: list[Piece]):
        self.pieces = pieces
