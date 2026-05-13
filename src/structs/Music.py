from utils.colors import Colors


class Music:
    __next_id: int = 0

    def __init__(self, title: str, artist: str, genre: str, bpm: int) -> None:
        self.title: str = title
        self.artist: str = artist
        self.genre: str = genre
        self.bpm: int = bpm

        self.id: int = Music.__next_id
        Music.__next_id += 1

    def __str__(self) -> str:
        """User display"""
        return f"'{self.title}' by {self.artist} [{self.genre}, {self.bpm} BPM]"

    def __repr__(self) -> str:
        """Debugging"""
        return f"Music(id={self.id}, title='{self.title}')"

    def display_card(self):
        """Card for visualization"""
        width: int = 40
        line: str = "─" * (width + 2)

        def format_row(label, value):
            val_str: str = str(value)
            EXTRA_LEN: int = len(": ")

            max_val_len: int = width - len(label) - EXTRA_LEN

            # Truncate value
            if len(val_str) > max_val_len:
                val_str = val_str[: max_val_len - 3] + "..."

            colored_label: str = f"{Colors.GOLD}{Colors.BOLD}{label}{Colors.RESET}"
            colored_value: str = f"{Colors.CYAN}{val_str}{Colors.RESET}"

            visible_length: int = len(label) + EXTRA_LEN + len(val_str)
            padding: str = " " * (width - visible_length)

            return f"{Colors.BLUE}│{Colors.RESET} {colored_label}: {colored_value}{padding} {Colors.BLUE}│{Colors.RESET}"

        print(f"{Colors.BLUE}┌{line}┐{Colors.RESET}")
        print(format_row("ID", self.id))
        print(format_row("Title", self.title))
        print(format_row("Artist", self.artist))
        print(format_row("Genre", self.genre))
        print(format_row("Tempo", f"{self.bpm} BPM"))
        print(f"{Colors.BLUE}└{line}┘{Colors.RESET}")


class DMusicNode:
    def __init__(self, data: Music) -> None:
        self.data: Music = data
        self.next: DMusicNode | None = None
        self.prev: DMusicNode | None = None
