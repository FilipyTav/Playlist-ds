from utils.colors import Colors


def clean_string(string: str):
    return string.strip().lower()


SEPARATOR_WIDTH: int = 45
SEPARATOR: str = "=" * SEPARATOR_WIDTH


def print_section_name(name: str):
    print(f"\n{Colors.MAGENTA}{Colors.BOLD}" + SEPARATOR)
    print(f"{Colors.BOLD}{name:^{SEPARATOR_WIDTH}}")
    print(SEPARATOR + f"{Colors.RESET}")
