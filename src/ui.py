import os

from music import Music
from structs.HistoryQueue import History
from structs.Library import MusicLibrary
from structs.PlaylistQueue import Playlist, PlaylistInfo
from utils.colors import Colors
from utils.input import get_and_validate_input, get_nav_input, validate_id
from utils.strings import (
    SEPARATOR,
    SEPARATOR_WIDTH,
    SUB_SEPARATOR,
    clean_string,
    format_error,
    print_section_end,
    print_section_name,
)
from utils.types import Screen, ScreenConfig


def screen_clear():
    os.system("cls" if os.name == "nt" else "clear")


# Main
# --------------------------------


def main_menu(registry: list[ScreenConfig]) -> Screen:
    print_section_name("--- BIBLIOTECA ---")
    print("Escolha uma opção: \n")

    # All screens belonging to MAIN
    options: list[ScreenConfig] = [c for c in registry if c.parent == Screen.MAIN]

    # Options
    for i, config in enumerate(options, 1):
        print(f"{Colors.BLUE}{i}{Colors.RESET}. {config.label}")

    print_section_end()
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
    print(SUB_SEPARATOR)

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

        data[key] = val.capitalize()

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
    print_section_name("Montar playlists por humor")
    success: bool = library.fill_playlists()
    if success:
        print("Playlists criadas com sucesso!")
        library.display_playlists()
    else:
        print(format_error("Não foi possível criar as playlists"))

    nav, _ = get_nav_input()
    if nav:
        return nav

    return Screen.BACK


def lib_choose_playlist(library: MusicLibrary) -> str | None:
    screen_clear()
    print_section_name("ESCOLHA UMA PLAYLIST DE HUMOR")

    options: list = list(library.playlists.keys())

    for i, name in enumerate(options, 1):
        p: Playlist = library.playlists[name]
        print(f" {i}. {name.capitalize():<10} ({p.info.humor})")

    def playlist_validator(v: str) -> bool:
        return v.isdigit() and 1 <= int(v) <= len(options)

    choice: str | None = get_and_validate_input(
        prompt="Selecione o número da playlist",
        validator=playlist_validator,
        error_msg=f"Escolha um número entre 1 e {len(options)}",
        cancel_key="B",
    )

    if choice is None:
        return None

    index: int = int(choice) - 1
    selected_key = options[index]

    return selected_key


def lib_play_next(library: MusicLibrary, history: History, selected_key: str) -> Screen:
    screen_clear()
    print_section_name(f"REPRODUZINDO: {selected_key.upper()}")

    playlist: Playlist = library.playlists[selected_key]

    music: Music | None = playlist.dequeue()

    if music is None:
        print(format_error(f"A fila '{selected_key}' está vazia!"))
        print(f"\n{Colors.YELLOW} Monte as filas na opção 5.{Colors.RESET}")
        nav, _ = get_nav_input()
        if nav:
            return nav
        return Screen.BACK

    print(f"\n{Colors.CYAN}{SEPARATOR}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}   > TOCANDO AGORA{Colors.RESET}")
    print(f"{Colors.CYAN}{SEPARATOR}{Colors.RESET}")

    print(f"\n   {Colors.WHITE}Título:  {Colors.BOLD}{music.title}{Colors.RESET}")
    print(f"   {Colors.WHITE}Artista: {Colors.LIGHT_GRAY}{music.artist}{Colors.RESET}")
    print(f"   {Colors.WHITE}Gênero:  {Colors.LIGHT_GRAY}{music.genre}{Colors.RESET}")
    print(f"   {Colors.WHITE}BPM:     {Colors.GOLD}{music.bpm}{Colors.RESET}")

    print(f"\n{Colors.CYAN}{SEPARATOR}{Colors.RESET}")

    history.enqueue(music)

    print(
        f"\n{Colors.DARK_GRAY}Música adicionada ao seu histórico de reprodução.{Colors.RESET}"
    )

    print("[A] Próxima na playlist")
    nav, choice = get_nav_input(False)
    if nav:
        return nav
    if choice == "a":
        return Screen.STAY

    return Screen.BACK


def lib_see_playlist(playlist: Playlist) -> Screen:
    screen_clear()
    playlist.display_for_user()

    print("[A] Exibir novamente")
    nav, choice = get_nav_input(False)
    if nav:
        return nav
    if choice == "a":
        return Screen.STAY

    return Screen.BACK


def lib_see_history(history: History) -> Screen:
    screen_clear()
    print_section_name("--Histórico--")

    history.display_for_user()
    print("[A] Mostrar novamente")
    nav, choice = get_nav_input(False)
    if nav:
        return nav
    if choice == "a":
        return Screen.STAY

    return Screen.BACK


def lib_see_statistics(library: MusicLibrary) -> Screen:
    screen_clear()
    print_section_name("--Estatísticas--")

    total_songs, playlist_sizes = library.get_statistics()

    print(f"{Colors.BOLD}{Colors.CYAN}Total de Músicas: {Colors.RESET}{Colors.LIGHT_GREEN}{total_songs}{Colors.RESET}")
    print(f"{Colors.DARK_GRAY}{SEPARATOR}{Colors.RESET}")

    print(f"{Colors.BOLD}{Colors.GOLD}{'Playlist':<20} | {'Músicas':<10}{Colors.RESET}")
    print(f"{Colors.DARK_GRAY}{SEPARATOR}{Colors.RESET}")

    for name, size in playlist_sizes.items():
        print(f"{Colors.WHITE}{name:<20}{Colors.RESET} | {Colors.BLUE}{size:<10}{Colors.RESET}")
    
    print_section_end()

    print("\n[A] Exibir novamente")
    nav, choice = get_nav_input(False)
    if nav: return nav
    if choice == "a":
        return Screen.STAY

    return Screen.BACK

# --------------------------------


def todo_screen() -> Screen:
    print("Screen yet to be implemented")
    nav, _ = get_nav_input()
    if nav:
        return nav
    return Screen.STAY
