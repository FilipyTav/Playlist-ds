import os

from utils.types import Screen


def screen_clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_main_options(back: bool = True, main: bool = True, stop: bool = True) -> None:
    if back:
        print("B. Voltar ao menu anterior")
    if main:
        print("M. Voltar ao menu inicial")
    if stop:
        print("Q. Fechar programa")


def main_menu() -> Screen:
    print("\n" + "=" * 40)
    print("\t--- BIBLIOTECA ---")
    print("=" * 40)

    print()
    print_main_options(back=False, main=False, stop=True)

    choice: str = input("\nEscolha uma opção: ").strip().lower()

    match choice:
        case "q":
            return Screen.EXIT
        case _:
            print("Opção inválida! Escolha 1, 2 ou q.")
            return Screen.MAIN
