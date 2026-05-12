from dataclasses import dataclass


@dataclass
class Colors:
    BLUE: str = "\033[94m"
    GOLD: str = "\033[93m"
    CYAN: str = "\033[96m"
    RED: str = "\033[91m"
    MAGENTA: str = "\033[95m"
    YELLOW: str = "\033[93m"
    LIGHT_GREEN: str = "\033[92m"

    BOLD: str = "\033[1m"
    RESET: str = "\033[0m"
