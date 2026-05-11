from music import Music
from structs.Library import MusicLibrary
from structs.PlaylistQueue import Playlist


def main():
    song: Music = Music("Test", "Me", "Electronic", 60)
    track1 = Music("Blinding Lights", "The Weeknd", "Synthwave", 171)
    track2 = Music(
        "Supercalifragilisticexpialidocious", "Dick Van Dyke", "Musical", 144
    )

    library = MusicLibrary()
    library.push(song)
    library.push(track1)
    library.prepend(track2)
    # a = library.find_by_name("Supercalifragilisticexpialidocious")

    # print(library)
    # library.display_library()
    # library.display_all_cards()

    list1: Playlist = Playlist()
    list1.enqueue(song)
    list1.enqueue(track1)
    list1.enqueue(track2)

    print(list1)
    list1.display_playlist()
    list1.display_all_cards()


if __name__ == "__main__":
    main()
