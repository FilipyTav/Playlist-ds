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

    print("\nEscolha uma opção: ")
    print(
        "1. Adicionar música\n"
        "2. Remover música\n"
        "3. Buscar música\n"
        "4. Listar músicas\n"
        "5. Montar playlists\n"
        "6. Reproduzir próxima\n"
        "7. Exibir Playlist atual\n"
        "8. Exibir histórico\n"
        "9. Estatísticas\n"
    )
    choice = input(NAV_PROMPT).strip().lower()

    # Check global nav first
    nav = handle_global_nav(choice)
    if nav:
        return nav

    match choice:
        case "1":
            return Screen.ADD_SONG

        case _:
            print("Opção inválida!")
            return Screen.MAIN


def lib_add_song() -> Screen:
    return Screen.TODO


def todo_screen() -> Screen:
    print("Screen yet to be implemented")
    choice = input(NAV_PROMPT).strip().lower()

    nav = handle_global_nav(choice)
    if nav:
        return nav
    return Screen.STAY
