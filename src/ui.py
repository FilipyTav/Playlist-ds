import os

from music import Music
from structs.Library import MusicLibrary
from utils.errors import EmptyValueError, NegativeNumberError
from utils.input import get_and_validate_input
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


# Main
# --------------------------------


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

        case "4":
            return Screen.LIST_SONGS

        case _:
            print("Opção inválida!")
            return Screen.MAIN


# --------------------------------

# Library
# --------------------------------


def lib_add_song(library: MusicLibrary) -> Screen:
    screen_clear()

    print("=" * 40)
    print(f"{'ADICIONAR NOVA MÚSICA':^40}")
    print("=" * 40)
    print(" Preencha os campos abaixo:")
    print("-" * 40)

    title: str = get_and_validate_input(
        "Título", error_msg="O título não pode estar vazio"
    )

    artist: str = get_and_validate_input(
        "Artista", error_msg="O artista não pode estar vazio"
    )

    genre: str = get_and_validate_input(
        "Gênero", error_msg="O gênero não pode estar vazio"
    )

    def validate_bpm(v):
        try:
            return int(v) >= 0
        except ValueError:
            return False

    bpm_str: str = get_and_validate_input(
        "BPM", validator=validate_bpm, error_msg="BPM deve ser um número positivo"
    )

    bpm = int(bpm_str)

    library.append(Music(title, artist, genre, bpm))

    print("-" * 40)
    print(f"\033[92mMúsica '{title}' adicionada com sucesso!\033[0m")
    input("\nPressione Enter para continuar...")

    return Screen.BACK


def lib_list_songs(library: MusicLibrary) -> Screen:
    screen_clear()
    library.display_all_cards()

    input("\nPressione Enter para continuar...")
    return Screen.BACK


# --------------------------------


def todo_screen() -> Screen:
    print("Screen yet to be implemented")
    choice = input(NAV_PROMPT).strip().lower()

    nav = handle_global_nav(choice)
    if nav:
        return nav
    return Screen.STAY
