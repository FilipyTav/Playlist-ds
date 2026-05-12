from utils.colors import Colors


def clean_string(string: str, lcase: bool = True):
    return string.strip().lower() if lcase else string.strip()


NAV_PROMPT: str = "\n[B] Voltar | [M] Início | [Q] Sair\n> "

SEPARATOR_WIDTH: int = 45
SEPARATOR: str = "=" * SEPARATOR_WIDTH
SUB_SEPARATOR: str = "-" * SEPARATOR_WIDTH


def print_section_name(name: str, sub: bool = False) -> None:
    sep: str = SEPARATOR if not sub else SUB_SEPARATOR

    print(f"\n{Colors.MAGENTA}{Colors.BOLD}" + sep)
    print(f"{Colors.BOLD}{name:^{SEPARATOR_WIDTH}}")
    print(sep + f"{Colors.RESET}")


def format_error(msg: str) -> str:
    return f"  {Colors.RED}[!] {msg} [!]{Colors.RESET}"
