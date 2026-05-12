from music import Music
from utils.types import PlaylistInfo


class DQueueNode:
    def __init__(self, data: Music) -> None:
        self.data: Music = data
        self.next: DQueueNode | None = None
        self.prev: DQueueNode | None = None


# Queue
class Playlist:
    def __init__(self, info: PlaylistInfo):
        self.__head: DQueueNode | None = None
        self.__tail: DQueueNode | None = None
        self.__count: int = 0

        self.info: PlaylistInfo = info

    def enqueue(self, m: Music) -> bool:
        new_node: DQueueNode = DQueueNode(m)

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

    def __str__(self) -> str:
        """Quick summary"""
        return f"Playlist(Size: {self.__count}, Head: {self.__head.data.title if self.__head else 'None'})"

    def display_playlist(self):
        """Visual chain"""
        if self.__count == 0:
            print("\nEmpty Playlist.")
            return

        print(f"\n--- Playlist Queue ({self.__count} Tracks) ---")

        current = self.__head
        chain = []

        while current:
            chain.append(f"[{current.data.title}]")
            current = current.next

        visual_chain = " ⇄ ".join(chain)

        print(f"HEAD ➔ {visual_chain} ➔ TAIL")
        print("-" * 40)

    def display_all_cards(self):
        """Prints every song in the playlist."""
        current = self.__head
        while current:
            current.data.display_card()
            current = current.next
