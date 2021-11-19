from enum import Enum


class LandType(Enum):
    LAND = 0
    SEA = 1
    ICE = 2
    FOREST = 3
    CITY = 4


class Altitude(Enum):
    FLAT = 0
    LOW = 1
    HIGH = 2


class WindDirection(Enum):
    NONE = 0
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class Clouds(Enum):
    NO = 0
    YES = 1


class Rain(Enum):
    NO = 0
    YES = 1


class Pollution(Enum):
    NONE = 0
    POLLUTED = 1


# Temperature
cellHealth = {'cold': 'white', 'normal': 'lightgreen', 'water': 'blue', 'warm': 'yellow', 'hot': 'red',
              'mountain': 'green', 'clouds': 'lightgray'}
