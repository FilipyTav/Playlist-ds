from structs.Music import Music
from structs.MusicNode import SMusicNode
from utils.colors import Colors
from utils.strings import (
    SEPARATOR,
    SEPARATOR_WIDTH,
    clean_string,
    format_error,
    print_section_name,
)
from structs.PlaylistQueue import Playlist, PlaylistInfo


class MusicLibrary:
    def __init__(self):
        self.__head: SMusicNode | None = None
        self.__tail: SMusicNode | None = None
        self.__count: int = 0

        self.playlists: dict[str, Playlist] = {
            "relaxar": Playlist(PlaylistInfo("Relaxar", "Tranquilo", 0, 80)),
            "focar": Playlist(PlaylistInfo("Focar", "Concentração", 81, 120)),
            "animar": Playlist(PlaylistInfo("Animar", "Agitado", 121, 160)),
            "treinar": Playlist(PlaylistInfo("Treinar", "Intenso", 161, 99999)),
        }

        # Avoids repetition
        self.__registered: dict[str, set[str]] = {}

    def insert_at(self, pos: int, m: Music) -> bool:
        """Insert at pos"""
        if self.has_song(m.title, m.artist):
            print("\n" + format_error("Música já presente na biblioteca"))
            return False

        if pos < 0 or pos > self.__count:
            print(f"Index out of range: {pos}, the list has {self.__count} element(s)")
            return False

        new_node: SMusicNode = SMusicNode(m)

        # Empty
        if self.is_empty():
            self.__head = self.__tail = new_node

        # new_node is now the head
        elif pos == 0:
            new_node.next = self.__head

            self.__head = new_node
        # new_node is now the tail
        elif pos == self.__count:
            if self.__tail:
                self.__tail.next = new_node
            self.__tail = new_node
        else:
            current: SMusicNode | None = self.__head

            for _ in range(pos - 1):
                if not current:
                    return False
                current = current.next

            # Because LSP
            assert current is not None
            assert current.next is not None

            new_node.next = current.next
            current.next = new_node

        ac: str = clean_string(m.artist)
        tc: str = clean_string(m.title)

        if ac not in self.__registered:
            self.__registered[ac] = set()

        self.__registered[ac].add(tc)

        self.__count += 1
        return True

    def is_empty(self) -> bool:
        return not (self.__head and self.__tail)

    def __len__(self) -> int:
        return self.__count

    def append(self, m: Music) -> bool:
        """Add to end"""
        return self.insert_at(self.__len__(), m)

    def prepend(self, m: Music) -> bool:
        """Add to start"""
        return self.insert_at(0, m)

    def find_by_name(self, name: str) -> Music | None:
        if self.is_empty():
            print("Lista vazia.")
            return None

        current: SMusicNode | None = self.__head
        while current:
            if clean_string(current.data.title) == clean_string(name):
                return current.data

            current = current.next

        return None

    def find_by_id(self, id: int) -> Music | None:
        if self.is_empty() or id < 0:
            return None

        current: SMusicNode | None = self.__head
        while current:
            if current.data.id == id:
                return current.data

            current = current.next

        return None

    def remove_at(self, pos: int) -> bool:
        """Remove at pos"""
        if pos < 0 or pos >= self.__count:
            print(f"Index out of range: {pos}, the list has {self.__count} element(s)")
            return False

        if self.is_empty():
            return False

        if pos == 0:
            self.__head = self.__head.next  # type: ignore
            self.__count -= 1
            return True

        current: SMusicNode | None = self.__head
        index: int = 0
        while current:
            if index + 1 == pos:
                assert current.next
                current.next = current.next.next
                self.__count -= 1
                return True

            current = current.next
            index += 1

        return False

    def remove_by_id(self, id: int) -> bool:
        """Remove music by id"""
        if id < 0 or self.is_empty():
            return False

        assert self.__head
        m: Music
        # Removes the head
        if self.__head.data.id == id:
            m = self.__head.data
            self.__remove_from_registered(m.title, m.artist)
            self.__head = self.__head.next
            self.__count -= 1

            if self.__count == 0:
                self.__tail = None

            return True

        current: SMusicNode | None = self.__head
        index: int = 0
        # Avoids searching tail
        while current and current.next:
            if current.next.data.id == id:
                m = current.next.data
                self.__remove_from_registered(m.title, m.artist)
                node_to_remove: SMusicNode = current.next

                if node_to_remove == self.__tail:
                    self.__tail = current

                current.next = node_to_remove.next

                self.__count -= 1
                return True

            current = current.next
            index += 1

        return False

    def has_song(self, title: str, artist: str) -> bool:
        t: str = clean_string(title)
        a: str = clean_string(artist)
        sl: set[str] | None = self.__registered.get(a)
        return t in sl if sl else False

    def __remove_from_registered(self, title: str, artist: str) -> bool:
        tc: str = clean_string(title)
        ac: str = clean_string(artist)

        if ac in self.__registered:
            self.__registered[ac].discard(tc)

            if not self.__registered[ac]:
                del self.__registered[ac]

            return True

        return False

    def fill_playlists(self) -> bool:
        if self.is_empty():
            return False

        self.clear_playlists()

        current: SMusicNode | None = self.__head
        while current:
            song: Music = current.data
            for k, v in self.playlists.items():
                min: int = v.info.min_bpm
                max: int = v.info.max_bpm

                if min <= song.bpm <= max:
                    self.playlists[k].enqueue(song)
                    break
            current = current.next

        return True

    def clear_playlists(self) -> None:
        for p in self.playlists.values():
            p.clear()

    def display_playlists(self) -> None:
        if not self.playlists:
            print(format_error("Nenhuma playlist encontrada"))
            return

        print_section_name("MINHAS PLAYLISTS", True)

        for p in self.playlists.values():
            p.display_for_user()
            print("\n" + "━" * SEPARATOR_WIDTH)

    def __str__(self) -> str:
        """Quick summary"""
        return f"MusicLibrary(Size: {self.__count}, Head: {self.__head.data.title if self.__head else 'None'})"

    def display_library(self) -> None:
        """Visual chain"""
        if self.is_empty() == 0:
            print("The library is currently empty.")
            return

        print(f"\n--- My Music Library ({self.__count} Tracks) ---")

        current: SMusicNode | None = self.__head
        chain = []

        while current:
            chain.append(f"[{current.data.title}]")
            current = current.next

        print("(HEAD)" + " ➔ ".join(chain) + "(TAIL)")
        print("-" * 40)

    def display_all_cards(self) -> None:
        """Prints every song in the library."""

        if self.is_empty():
            print(
                f"\n{Colors.YELLOW} A biblioteca está vazia no momento.{Colors.RESET}"
            )
            return

        print_section_name(f"BIBLIOTECA ({self.__len__()} FAIXAS)")

        current: SMusicNode | None = self.__head
        index: int = 1

        while current:
            # print(
            #     f"\n{Colors.YELLOW}Track {index:02d}/{self.__count:02d}{Colors.RESET}"
            # )

            current.data.display_card()

            # if current.next:
            #     print(f"{Colors.MAGENTA}x{Colors.RESET}")

            current = current.next
            index += 1

        print(f"\n{Colors.MAGENTA}{Colors.BOLD}" + SEPARATOR + f"{Colors.RESET}")

    def get_statistics(self) -> tuple[int, dict[str, int]]:
        """Returns [Total songs, playlist_sizes],"""
        total_songs: int = self.__len__()
        playlist_sizes: dict[str, int] = {}
        for k, v in self.playlists.items():
            playlist_sizes[k.capitalize()] = v.len()
        return (total_songs, playlist_sizes)
