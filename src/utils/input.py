from utils.strings import clean_string


def get_and_validate_input(
    prompt: str, validator=None, error_msg="Entrada inválida"
) -> str:
    """Input while/try/except logic."""
    while True:
        value = input(f"> {prompt}: ").strip()

        is_valid = validator(value) if validator else clean_string(value)

        if is_valid:
            return value

        print(f"    \033[91m[!] {error_msg} [!]\033[0m")
