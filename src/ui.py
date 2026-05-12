import os

from music import Music
from structs.Library import MusicLibrary
from utils.colors import Colors
from utils.errors import EmptyValueError, NegativeNumberError
from utils.input import get_and_validate_input
from utils.strings import (
    SEPARATOR_WIDTH,
    SUB_SEPARATOR,
    clean_string,
    print_section_name,
)
from utils.types import Screen, ScreenConfig


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


def main_menu(registry: list[ScreenConfig]) -> Screen:
    print_section_name("--- BIBLIOTECA ---")
    print("\nEscolha uma opção: ")

    # All screens belonging to MAIN
    options: list[ScreenConfig] = [c for c in registry if c.parent == Screen.MAIN]

    # Options
    for i, config in enumerate(options, 1):
        print(f"{i}. {config.label}")

    choice: str = input(NAV_PROMPT).strip().lower()

    nav = handle_global_nav(choice)
    if nav:
        return nav

    # Choice for main options
    try:
        idx: int = int(choice) - 1
        if 0 <= idx < len(options):
            return options[idx].id
    except ValueError:
        pass

    print(f"{Colors.RED}[!] Opção inválida!{Colors.RESET}")
    return Screen.STAY


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

    print(SUB_SEPARATOR)
    print(
        f"{Colors.LIGHT_GREEN} Música '{title}' adicionada com sucesso!{Colors.RESET}"
    )

    choice = input(NAV_PROMPT).strip().lower()
    nav = handle_global_nav(choice)
    if nav:
        return nav

    return Screen.BACK


def lib_list_songs(library: MusicLibrary) -> Screen:
    screen_clear()
    library.display_all_cards()

    print("[A] Listar novamente", end="")
    choice = clean_string(input(f"{NAV_PROMPT}"))
    nav = handle_global_nav(choice)
    if nav:
        return nav
    if choice == "a":
        return Screen.STAY

    return Screen.BACK


def lib_remove_song(library: MusicLibrary) -> Screen:
    screen_clear()
    library.display_all_cards()

    if library.is_empty():
        choice = input(f"{NAV_PROMPT}").strip().lower()
        nav = handle_global_nav(choice)
        if nav:
            return nav

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
        print(SUB_SEPARATOR)
        print(
            f"{Colors.LIGHT_GREEN} Música '{rm_song.title}' removida com sucesso!{Colors.RESET}"
        )
    else:
        print(f"Algo deu errado. Não foi possível remover {rm_song.title}")

    choice = input(f"\n [A] Remover outra | {NAV_PROMPT[1:]}").strip().lower()
    nav = handle_global_nav(choice)
    if nav:
        return nav
    match clean_string(choice):
        case "a":
            return Screen.STAY

    return Screen.BACK


def lib_search_song(library: MusicLibrary) -> Screen:
    screen_clear()
    print_section_name("PROCURAR MÚSICA")

    if library.is_empty():
        print(SUB_SEPARATOR)
        print("A biblioteca está vazia!")
        choice = input(f"{NAV_PROMPT}").strip().lower()
        nav = handle_global_nav(choice)
        if nav:
            return nav

    def validate_op(v) -> bool:
        try:
            a: int = int(v)
            return a in [1, 2]
        except ValueError:
            return False

    op: str | None = get_and_validate_input(
        "Buscar por ID[1] ou nome[2]?", validate_op, "Escolha uma das opções", "B"
    )

    if not op:
        return Screen.BACK

    choice = input(f"{NAV_PROMPT}").strip().lower()
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
