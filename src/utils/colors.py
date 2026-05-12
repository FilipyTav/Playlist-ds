from dataclasses import dataclass


@dataclass
class Colors:
    BLUE: str = "\033[94m"
    GOLD: str = "\033[93m"
    CYAN: str = "\033[96m"
    RED: str = "\033[91m"
    MAGENTA: str = "\033[95m"
    YELLOW: str = "\033[93m"
    GREEN: str = "\033[32m"
    LIGHT_GREEN: str = "\033[92m"

    WHITE: str = "\033[97m"
    LIGHT_GRAY: str = "\033[37m"
    DARK_GRAY: str = "\033[90m"
    BLACK: str = "\033[30m"

    # Formatting
    BOLD: str = "\033[1m"
    UNDERLINE: str = "\033[4m"
    ITALIC: str = "\033[3m"
    REVERSE: str = "\033[7m"
    RESET: str = "\033[0m"

    # Background
    BG_RED: str = "\033[41m"
    BG_GREEN: str = "\033[42m"
