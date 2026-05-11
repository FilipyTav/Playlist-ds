import os

from utils.strings import clean_string
from utils.types import Screen


def screen_clear():
    os.system("cls" if os.name == "nt" else "clear")


NAV_PROMPT: str = "\n[B] Voltar | [M] Início | [Q] Sair\n> "


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


def main_menu() -> Screen:
    print("\n" + "=" * 40)
    print("\t--- BIBLIOTECA ---")
    print("=" * 40)

    print("\nEscolha uma opção: \n")
    choice = input(NAV_PROMPT).strip().lower()

    # Check global nav first
    nav = handle_global_nav(choice)
    if nav:
        return nav

    match choice:
        case _:
            print("Opção inválida! Escolha 1, 2 ou q.")
            return Screen.MAIN
