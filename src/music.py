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
        """Nice card for visualization"""
        width: int = 40
        line: str = "─" * (width + 2)

        def format_row(label, value):
            content = f"{label}: {value}"

            if len(content) > width:
                content = content[: width - 3] + "..."

            return f"│ {content:<{width}} │"

        print(f"┌{line}┐")
        print(format_row("ID", self.id))
        print(format_row("Title", self.title))
        print(format_row("Artist", self.artist))
        print(format_row("Genre", self.genre))
        print(format_row("Tempo", f"{self.bpm} BPM"))
        print(f"└{line}┘")
