from enum import IntEnum

class Color(IntEnum):
    EMPTY = 0
    RED = 1
    BLUE = -1

class Result(IntEnum):
    DRAW = 0
    RED = 1
    BLUE = -1
    INPROGRESS = 4

color_to_result = {
    Color.RED: Result.RED,
    Color.BLUE: Result.BLUE
    }