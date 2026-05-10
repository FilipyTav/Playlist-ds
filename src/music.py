class Music:
    def __init__(self, id: int, title: str, artist: str, genre: str, bpm: int) -> None:
        self.id: int = id
        self.title: str = title
        self.artist: str = artist
        self.type: str = genre
        self.bpm: int = bpm
