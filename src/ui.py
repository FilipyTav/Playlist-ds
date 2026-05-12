import os

from music import Music
from structs.Library import MusicLibrary
from utils.errors import EmptyValueError, NegativeNumberError
from utils.input import get_and_validate_input
from utils.strings import SEPARATOR_WIDTH, clean_string, print_section_name
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
    print_section_name("--- BIBLIOTECA ---")

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

        case "2":
            return Screen.REMOVE_SONG

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

    print_section_name("ADICIONAR NOVA MÚSICA")

    print(" Preencha os campos abaixo:")
    print("-" * SEPARATOR_WIDTH)

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

    choice = input(NAV_PROMPT).strip().lower()
    nav = handle_global_nav(choice)
    if nav:
        return nav

    return Screen.BACK


def lib_list_songs(library: MusicLibrary) -> Screen:
    screen_clear()
    library.display_all_cards()

    choice = input(NAV_PROMPT).strip().lower()
    nav = handle_global_nav(choice)
    if nav:
        return nav
    return Screen.BACK


def lib_remove_song(library: MusicLibrary) -> Screen:
    screen_clear()
    library.display_all_cards()

    print_section_name("REMOVER MÚSICA", sub=True)

    def validate_id(v: str):
        try:
            return clean_string(v) == "b" or int(v) >= 0
        except ValueError:
            return False

    rm_song: Music | None = None
    while not rm_song:
        id_str: str = get_and_validate_input(
            "ID(B para cancelar)",
            validator=validate_id,
            error_msg="ID deve ser um número positivo",
        )

        if id_str == "b":
            return Screen.BACK

        id: int = int(id_str)

        rm_song = library.find_by_id(id)

        if not rm_song:
            print(f"ID ({id}) não existe na biblioteca. Tente novamente.\n")
            continue

    if library.remove_by_id(rm_song.id):
        print("-" * 40)
        print(f"\033[92mMúsica '{rm_song.title}' removida com sucesso!\033[0m")
    else:
        print(f"Algo deu errado. Não foi possível remover {rm_song.title}")

    choice = input(NAV_PROMPT).strip().lower()
    nav = handle_global_nav(choice)
    if nav:
        return nav
    return Screen.BACK


# --------------------------------


def todo_screen() -> Screen:
    print("Screen yet to be implemented")
    choice = input(NAV_PROMPT).strip().lower()

    nav = handle_global_nav(choice)
    if nav:
        return nav
    return Screen.STAY
