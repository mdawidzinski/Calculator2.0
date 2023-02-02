import math
from typing import Union

class RoundingMethod:  # rounding method that help solve floating point number error to some degree
    @staticmethod
    def round_away_from_zero(value: Union[int, float], decimals: int = 13) -> float:
        multiplier = 10 ** decimals
        if value > 0:
            return math.floor(value * multiplier + 0.5) / multiplier
        else:
            return math.ceil(value * multiplier - 0.5) / multiplier

    @staticmethod
    def result(value: float)-> Union[int, float]:  # function that take float as input and return int if possible
        rounded_value = RoundingMethod.round_away_from_zero(value)
        if rounded_value == int(rounded_value):
            return int(rounded_value)
        else:
            return rounded_value
