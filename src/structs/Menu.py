from structs.MenuStack import MenuStack
from structs.PlaylistQueue import Playlist
from utils.strings import format_error
from utils.types import AppState, Screen, ScreenConfig
from ui import (
    lib_add_song,
    lib_choose_playlist,
    lib_fill_playlists,
    lib_list_songs,
    lib_play_next,
    lib_remove_song,
    lib_search_song,
    lib_see_history,
    lib_see_playlist,
    lib_see_statistics,
    main_menu,
    screen_clear,
    todo_screen,
)


class MenuManager:
    def __init__(self, state: AppState):
        self.__screen_history: MenuStack = MenuStack()

        self.__is_running: bool = True
        self.__screen_history.push(Screen.MAIN)

        self.state: AppState = state
        self.registry = [
            # Main
            # ------------
            ScreenConfig(Screen.MAIN, "Menu Inicial", main_menu, None),
            # ------------
            # Children of MAIN
            # ------------
            ScreenConfig(
                Screen.ADD_SONG,
                "Adicionar música",
                lambda: lib_add_song(self.state.library),
                Screen.MAIN,
            ),
            ScreenConfig(
                Screen.REMOVE_SONG,
                "Remover música",
                lambda: lib_remove_song(self.state.library),
                Screen.MAIN,
            ),
            ScreenConfig(
                Screen.FIND_SONG,
                "Buscar música",
                lambda: lib_search_song(self.state.library),
                Screen.MAIN,
            ),
            ScreenConfig(
                Screen.LIST_SONGS,
                "Listar músicas",
                lambda: lib_list_songs(self.state.library),
                Screen.MAIN,
            ),
            ScreenConfig(
                Screen.FILL_PLS,
                "Montar playlists por humor",
                lambda: lib_fill_playlists(self.state.library),
                Screen.MAIN,
            ),
            ScreenConfig(
                Screen.PLAYER,
                "Reproduzir música",
                # Handled in __handle_player
                self.__handle_player,
                Screen.MAIN,
            ),
            ScreenConfig(
                Screen.SEE_PLAYLIST,
                "Ver playlist",
                self.__handle_see_playlist,
                Screen.MAIN,
            ),
            ScreenConfig(
                Screen.SEE_HISTORY,
                "Ver histórico",
                lambda: lib_see_history(self.state.history),
                Screen.MAIN,
            ),
            ScreenConfig(
                Screen.SEE_STATISTICS,
                "Ver estatísticas",
                lambda: lib_see_statistics(self.state.library, self.state.history),
                Screen.MAIN,
            ),
            # ------------
            ScreenConfig(
                Screen.CHOOSE_PLAYLIST,
                "Escolhar playlist",
                lambda: lib_choose_playlist(self.state.library),
                None,
            ),
            # ------------
            # Placeholder
            # ------------
            ScreenConfig(Screen.TODO, "(Em breve)", todo_screen, None),
            # ------------
        ]
        self._dispatch_map = {config.id: config.handler for config in self.registry}

    def run(self):
        screen: Screen | None = None
        new_sc: Screen = Screen.MAIN

        while self.__is_running and not self.__screen_history.is_empty():
            screen = self.__screen_history.peek()
            if not screen:
                break

            screen_clear()
            # self.__screen_history.print_stack()
            new_sc = self._handle_nav(screen)

            self._navigate(screen, new_sc)

    def _handle_nav(self, screen: Screen) -> Screen:
        """Lookup and execute the handler for the given screen"""

        handler = self._dispatch_map.get(screen)

        if screen == Screen.MAIN:
            return handler(self.registry)  # type: ignore

        elif screen == Screen.CHOOSE_PLAYLIST:
            selected_key: str | None = handler()  # type: ignore

            if selected_key:
                self.state.selected_playlist = selected_key

                return Screen.BACK

            return Screen.MAIN

        return handler()  # type: ignore

    def _navigate(self, current_sc: Screen, new_sc: Screen) -> None:
        if new_sc == current_sc or new_sc == Screen.STAY:
            return

        if new_sc == Screen.MAIN:
            self.__screen_history.clear()
            self.__screen_history.push(Screen.MAIN)
            self.state.selected_playlist = None

        elif new_sc == Screen.EXIT:
            print("\nEncerrando o sistema...")
            self.__is_running = False
            self.__screen_history.clear()

        elif new_sc == Screen.BACK:
            self.__screen_history.pop()
            if self.__screen_history.len() == 1:
                self.state.selected_playlist = None

        else:
            self.__screen_history.push(new_sc)

    def __handle_player(self) -> Screen:
        if not self.state.selected_playlist:
            return Screen.CHOOSE_PLAYLIST

        return lib_play_next(
            self.state.library, self.state.history, self.state.selected_playlist
        )

    def __handle_see_playlist(self) -> Screen:
        if not self.state.selected_playlist:
            return Screen.CHOOSE_PLAYLIST

        p: Playlist | None = self.state.library.playlists.get(
            self.state.selected_playlist
        )

        if not p:
            print(
                format_error(
                    f"Playlist '{self.state.selected_playlist}' não encontrada"
                )
            )
            self.state.selected_playlist = None
            return Screen.MAIN

        return lib_see_playlist(p)
