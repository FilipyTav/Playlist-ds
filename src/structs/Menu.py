from structs.MenuStack import MenuStack
from utils.types import AppState, Screen, ScreenConfig
from ui import (
    lib_add_song,
    lib_choose_playlist,
    lib_fill_playlists,
    lib_list_songs,
    lib_play_next,
    lib_remove_song,
    lib_search_song,
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
                Screen.CHOOSE_PLAYLIST,
                "Escolhar playlist",
                lambda: lib_choose_playlist(self.state.library),
                Screen.MAIN,
            ),
            # ------------
            ScreenConfig(
                Screen.PLAYER,
                "Reproduzir música",
                # Already handled in __handle_player
                lambda: (),
                None,
            ),
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
            self.__screen_history.print_stack()
            new_sc = self._handle_nav(screen)

            self._navigate(screen, new_sc)

    def _handle_nav(self, screen: Screen) -> Screen:
        """Lookup and execute the handler for the given screen"""

        handler = self._dispatch_map.get(screen)

        if screen == Screen.MAIN:
            return handler(self.registry)  # type: ignore

        elif screen == Screen.CHOOSE_PLAYLIST:
            next_screen, selected_key = handler()  # type: ignore

            if next_screen == Screen.PLAYER and selected_key:
                return self.__handle_player(selected_key)
            return next_screen

        return handler()  # type: ignore

    def _navigate(self, current_sc: Screen, new_sc: Screen) -> None:
        if new_sc == current_sc or new_sc == Screen.STAY:
            return

        if new_sc == Screen.MAIN:
            self.__screen_history.clear()
            self.__screen_history.push(Screen.MAIN)

        elif new_sc == Screen.EXIT:
            print("\nEncerrando o sistema...")
            self.__is_running = False
            self.__screen_history.clear()

        elif new_sc == Screen.BACK:
            self.__screen_history.pop()

        else:
            self.__screen_history.push(new_sc)

    def __handle_player(self, key: str) -> Screen:
        return lib_play_next(self.state.library, self.state.history, key)
