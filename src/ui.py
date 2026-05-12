import os

from music import Music
from structs.Library import MusicLibrary
from utils.colors import Colors
from utils.input import get_and_validate_input, get_nav_input, validate_id
from utils.strings import (
    SEPARATOR_WIDTH,
    SUB_SEPARATOR,
    clean_string,
    format_error,
    print_section_name,
)
from utils.types import Screen, ScreenConfig


def screen_clear():
    os.system("cls" if os.name == "nt" else "clear")


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

    nav, choice = get_nav_input()
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

    data: dict[str, str] = {}
    fields: list = [
        ("title", "Título", "Título não pode estar vazio!", None),
        ("artist", "Artista", "Artista não pode estar vazio!", None),
        ("genre", "Gênero", "Gênero não pode estar vazio!", None),
        (
            "bpm",
            "BPM",
            "BPM deve ser um número positivo!",
            lambda v: v.isdigit() and int(v) >= 0,
        ),
    ]

    for key, label, e_msg, validator in fields:
        val = get_and_validate_input(
            label, validator=validator, error_msg=e_msg, cancel_key="B"
        )

        if val is None:
            return Screen.BACK

        data[key] = val

    success: bool = library.append(
        Music(data["title"], data["artist"], data["genre"], int(data["bpm"]))
    )

    print(SUB_SEPARATOR)
    if success:
        print(
            f"\n{Colors.LIGHT_GREEN} Música '{data['title']}' adicionada com sucesso!{Colors.RESET}"
        )
    else:
        print(format_error("Erro ao adicionar música"))

    nav, _ = get_nav_input()
    if nav:
        return nav

    return Screen.BACK


def lib_list_songs(library: MusicLibrary) -> Screen:
    screen_clear()
    library.display_all_cards()

    print("[A] Listar novamente", end="")
    nav, choice = get_nav_input()
    if nav:
        return nav
    if choice == "a":
        return Screen.STAY

    return Screen.BACK


def lib_remove_song(library: MusicLibrary) -> Screen:
    screen_clear()
    library.display_all_cards()

    if library.is_empty():
        nav, _ = get_nav_input()
        if nav:
            return nav

    print_section_name("REMOVER MÚSICA", sub=True)

    rm_song: Music | None = None
    while not rm_song:
        id_str: str | None = get_and_validate_input(
            "ID", validate_id, "ID deve ser um número positivo", "B"
        )

        if not id_str:
            return Screen.BACK

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

    print("\n[A] Remover outra")
    nav, choice = get_nav_input(False)
    if nav:
        return nav
    match choice:
        case "a":
            return Screen.STAY

    return Screen.BACK


def lib_search_song(library: MusicLibrary) -> Screen:
    screen_clear()
    print_section_name("PROCURAR MÚSICA")

    if library.is_empty():
        print(SUB_SEPARATOR)
        print("A biblioteca está vazia!")

        nav, _ = get_nav_input()
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

    error_msg: str = ""
    song: Music | None = None
    # TODO: search multiple at the same time
    if op == "1":
        id_str: str | None = get_and_validate_input(
            "Busca por ID", validate_id, "ID deve ser um número positivo!", "B"
        )

        if not id_str:
            return Screen.BACK

        id: int = int(id_str)

        song = library.find_by_id(id)
        error_msg = f"Não foi possível econtrar música (ID:{id}) na biblioteca."
    elif op == "2":
        title: str | None = get_and_validate_input(
            "Busca por nome", None, "Nome não pode estar vazio!", "B"
        )

        if not title:
            return Screen.BACK

        song = library.find_by_name(title)
        error_msg = f"Não foi possível encontrar '{title}' na biblioteca."

    if song:
        msg: str = f" Música '{song.title}' encontrada! "
        border: str = "═" * len(msg)

        print(f"\n{Colors.CYAN}╔{border}╗")
        print(f"║{Colors.BOLD}{Colors.LIGHT_GREEN}{msg}{Colors.RESET}{Colors.CYAN}║")
        print(f"╚{border}╝{Colors.RESET}")

        song.display_card()
    else:
        print(format_error(error_msg))

    print("\n[A] Fazer busca")
    nav, choice = get_nav_input(False)
    if nav:
        return nav

    if choice == "a":
        return Screen.STAY

    return Screen.BACK


def lib_fill_playlists(library: MusicLibrary) -> Screen:
    library.fill_playlists()
    return Screen.TODO


# --------------------------------


def todo_screen() -> Screen:
    print("Screen yet to be implemented")
    nav, _ = get_nav_input()
    if nav:
        return nav
    return Screen.STAY
