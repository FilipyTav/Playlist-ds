from structs.MenuStack import MenuStack

from ui import (
    lib_add_song,
    main_menu,
    screen_clear,
    todo_screen,
)

from utils.types import Screen


class MenuManager:
    def __init__(self):
        self.__screen_history: MenuStack = MenuStack()

        self.__is_running: bool = True
        self.__screen_history.push(Screen.MAIN)

        self._dispatch_map = {
            Screen.MAIN: main_menu,
            Screen.ADD_SONG: lib_add_song,
            Screen.TODO: todo_screen,
        }

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
        if handler:
            return handler()

        print(f"Error: No handler for {screen}")
        return Screen.EXIT

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
