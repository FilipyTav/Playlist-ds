from utils.colors import Colors
from utils.strings import clean_string, NAV_PROMPT
from utils.types import Screen


def get_and_validate_input(
    prompt: str,
    validator=None,
    error_msg="Entrada inválida",
    cancel_key: str = "",
) -> str | None:
    """Input while/try/except logic."""
    while True:
        if cancel_key:
            print(f"\n[{cancel_key}] para cancelar")

        value: str = clean_string(input(f"> {prompt}: "))

        if value == clean_string(cancel_key):
            return None

        is_valid = validator(value) if validator else clean_string(value)

        if is_valid:
            return value

        print(f"    {Colors.RED} [!] {error_msg} [!] {Colors.RESET}")


def handle_global_nav(choice: str) -> Screen | None:
    match clean_string(choice):
        case "b":
            return Screen.BACK
        case "m":
            return Screen.MAIN
        case "q":
            return Screen.EXIT
        case _:
            return None


def get_nav_input(has_nls: bool = True) -> tuple[Screen | None, str]:
    choice: str = clean_string(input(NAV_PROMPT if has_nls else NAV_PROMPT[1:]))
    nav: Screen | None = handle_global_nav(choice)

    return nav, choice
