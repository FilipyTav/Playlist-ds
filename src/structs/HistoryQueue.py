from structs.Music import Music
from structs.MusicNode import SMusicNode
from utils.colors import Colors
from utils.strings import SEPARATOR_WIDTH, centered_msg, format_error, truncate_string


# Classe Fila
class History:
    def __init__(self):
        self.__head: SMusicNode | None = None
        self.__tail: SMusicNode | None = None
        self.__count: int = 0

    def enqueue(self, m: Music) -> bool:
        new_node: SMusicNode = SMusicNode(m)

        if self.is_empty():
            self.__head = new_node
            self.__tail = new_node
        else:
            assert self.__tail
            self.__tail.next = new_node

            self.__tail = new_node

        self.__count += 1
        return True

    def dequeue(self) -> Music | None:
        if self.is_empty():
            return None

        assert self.__head
        music: Music = self.__head.data

        self.__head = self.__head.next

        if not self.__head:
            self.__tail = None

        self.__count -= 1
        return music

    def is_empty(self) -> bool:
        return not (self.__head and self.__tail)

    def len(self) -> int:
        return self.__count

    def clear(self) -> None:
        self.__head = None
        self.__tail = None
        self.__count = 0

    def __str__(self) -> str:
        return f"Histórico(Size: {self.len()}, Head: {self.__head.data.title if self.__head else 'None'})"

    def display_for_admin(self):
        """Visual chain"""
        if self.is_empty():
            print("\nEmpty Playlist.")
            return

        print(f"\n--- Fila Histórico ({self.len()} Tracks) ---")

        current = self.__head
        chain = []

        while current:
            chain.append(f"[{current.data.title}]")
            current = current.next

        visual_chain = " ⇄ ".join(chain)

        print(f"HEAD ➔ {visual_chain} ➔ TAIL")
        print("-" * 40)

    def display_for_user(self):
        """Display table"""
        if self.is_empty():
            print(centered_msg("Histórico vazio"))
            return

        header: str = (
            f"{Colors.BOLD}{Colors.CYAN}{'ID':<6} {'TÍTULO':<25} {'ARTISTA':<20} {'BPM':<8}{Colors.RESET}"
        )
        print(header)
        print(f"{Colors.DARK_GRAY}{'—' * 60}{Colors.RESET}")

        current = self.__head
        while current:
            m: Music = current.data

            ca: str = truncate_string(m.artist, 18)
            ct: str = truncate_string(m.title, 23)

            print(f"{Colors.GOLD}{m.id:<6}{Colors.RESET}", end="")
            print(f"{Colors.WHITE}{ct:<25}{Colors.RESET}", end="")
            print(f"{Colors.LIGHT_GRAY}{ca:<20}{Colors.RESET}", end="")
            print(f"{Colors.CYAN}{m.bpm:^8}{Colors.RESET}")

            current = current.next

        # 3. Footer
        print(f"{Colors.DARK_GRAY}{'—' * 60}{Colors.RESET}")
        print(f"{Colors.MAGENTA}Total: {self.len()} música(s){Colors.RESET}")

    def display_all_cards(self):
        """Prints every song in the playlist."""
        current = self.__head
        while current:
            current.data.display_card()
            current = current.next
