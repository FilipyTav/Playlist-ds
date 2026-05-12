from utils.colors import Colors
from utils.strings import clean_string


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
