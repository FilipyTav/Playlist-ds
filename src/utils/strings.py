from utils.colors import Colors


def clean_string(string: str):
    return string.strip().lower()


SEPARATOR_WIDTH: int = 45
SEPARATOR: str = "=" * SEPARATOR_WIDTH
SUB_SEPARATOR: str = "-" * SEPARATOR_WIDTH


def print_section_name(name: str, sub: bool = False):
    sep: str = SEPARATOR if not sub else SUB_SEPARATOR

    print(f"\n{Colors.MAGENTA}{Colors.BOLD}" + sep)
    print(f"{Colors.BOLD}{name:^{SEPARATOR_WIDTH}}")
    print(sep + f"{Colors.RESET}")
