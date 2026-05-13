from dataclasses import dataclass
from structs.Music import DMusicNode, Music
from utils.colors import Colors
from utils.strings import format_error, truncate_string


@dataclass
class PlaylistInfo:
    name: str
    humor: str
    min_bpm: int
    max_bpm: int


# Queue
class Playlist:
    def __init__(self, info: PlaylistInfo):
        self.__head: DMusicNode | None = None
        self.__tail: DMusicNode | None = None
        self.__count: int = 0

        self.info: PlaylistInfo = info

    def enqueue(self, m: Music) -> bool:
        new_node: DMusicNode = DMusicNode(m)

        if self.is_empty():
            self.__head = new_node
            self.__tail = new_node
        else:
            new_node.prev = self.__tail

            assert self.__tail
            self.__tail.next = new_node

            self.__tail = new_node

        self.__count += 1
        return True

    def dequeue(self) -> Music | None:
        if self.is_empty():
            print("No element to dequeue - list empty")
            return None

        assert self.__head
        music: Music = self.__head.data

        self.__head = self.__head.next

        if self.__head:
            self.__head.prev = None
        else:
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
        """Quick summary"""
        return f"Playlist(Size: {self.len()}, Head: {self.__head.data.title if self.__head else 'None'})"

    def display_for_admin(self):
        """Visual chain"""
        if self.is_empty():
            print("\nEmpty Playlist.")
            return

        print(f"\n--- Playlist Queue ({self.len()} Tracks) ---")

        current = self.__head
        chain = []

        while current:
            chain.append(f"[{current.data.title}]")
            current = current.next

        visual_chain = " ⇄ ".join(chain)

        print(f"HEAD ➔ {visual_chain} ➔ TAIL")
        print("-" * 40)

    def display_for_user(self):
        """Playlist display with table formatting"""
        if self.is_empty():
            print(format_error(f"Playlist {self.info.name} está vazia"))
            print(f"{Colors.YELLOW} Monte as filas na opção 5.{Colors.RESET}\n")
            return

        print(
            f"\n{Colors.BOLD}{Colors.MAGENTA}>PLAYLIST: {self.info.name.upper()}{Colors.RESET}"
        )

        header: str = (
            f"{Colors.BOLD}{Colors.CYAN}{'ID':<6} {'TÍTULO':<25} {'ARTISTA':<20} {'BPM':<8}{Colors.RESET}"
        )
        print(header)
        print(f"{Colors.DARK_GRAY}{'—' * 60}{Colors.RESET}")

        current = self.__head
        while current:
            m: Music = current.data

            clean_title: str = truncate_string(m.title, 23)
            clean_artist: str = truncate_string(m.artist, 18)

            print(f"{Colors.GOLD}{m.id:<6}{Colors.RESET}", end="")
            print(f"{Colors.WHITE}{clean_title:<25}{Colors.RESET}", end="")
            print(f"{Colors.LIGHT_GRAY}{clean_artist:<20}{Colors.RESET}", end="")
            print(f"{Colors.CYAN}{m.bpm:^8}{Colors.RESET}")

            current = current.next

        # 3. Footer
        print(f"{Colors.DARK_GRAY}{'—' * 60}{Colors.RESET}")
        print(f"{Colors.MAGENTA}Total: {self.len()} músicas{Colors.RESET}\n")

    def display_all_cards(self):
        """Prints every song in the playlist."""
        current = self.__head
        while current:
            current.data.display_card()
            current = current.next
