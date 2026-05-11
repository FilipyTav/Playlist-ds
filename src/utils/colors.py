from dataclasses import dataclass


@dataclass
class Colors:
    BLUE: str = "\033[94m"
    GOLD: str = "\033[93m"
    CYAN: str = "\033[96m"

    BOLD: str = "\033[1m"
    RESET: str = "\033[0m"
