from structs.MenuStack import MenuStack

from ui import (
    main_menu,
    screen_clear,
)

from utils.types import Screen


class MenuManager:
    def __init__(self):
        self.__screen_history: MenuStack = MenuStack()

        self.__is_running: bool = True
        self.__screen_history.push(Screen.MAIN)

    def run(self):
        screen: Screen | None = None
        new_sc: Screen = Screen.MAIN

        while self.__is_running and not self.__screen_history.is_empty():
            screen = self.__screen_history.peek()
            if not screen:
                break

            screen_clear()
            new_sc = self._handle_nav(screen)

            self._navigate(screen, new_sc)

    def _handle_nav(self, screen: Screen) -> Screen:
        match screen:
            case Screen.MAIN:
                return main_menu()

            #
            # ------------------------
            # ------------------------
            case _:
                return Screen.MAIN

    def _navigate(self, current_sc: Screen, new_sc: Screen) -> None:
        if new_sc == current_sc:
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
