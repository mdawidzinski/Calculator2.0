import math

class Rounding:
    def __int__(self, value, decimals=0):
        self.value = value
        self.decimals = decimals

    def round_half_up(self, n, decimals):  # solution from: https://realpython.com/python-rounding/,
        multiplier = 10 ** decimals
        return math.floor(n * multiplier + 0.5) / multiplier

    def round_half_down(self, n, decimals):
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier - 0.5) / multiplier

    def result(self, n, decimals=14):
        result = 0
        if n <= 0:
            result += self.round_half_down(n, decimals)
        else:
            result += self.round_half_up(n, decimals)
        if result == int(result):
            return str(int(result))
        else:
            return str(result)
