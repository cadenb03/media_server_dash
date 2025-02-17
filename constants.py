class Colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class FG:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

        def rgb(r: int,g: int,b: int):
            return f'\033[38;2;{r};{g};{b}m'

    class BG:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

        def rgb(r: int,g: int,b: int):
            return f'\033[48;2;{r};{g};{b}m'

class Terminal:
    clear = '\033[2J'
    reset = '\033[0;0H'

    def move(self, line, col):
        return f'\033[{line};{col}H'

class Weather:
    sunny = '\U000f0599'
    cloudy = '\U000f0590'
    partly = '\U000f0595'
    rain = '\U000f0596'
    snow = '\U000f0598'
