from music import Music
from structs.Library import MusicLibrary
from structs.MusicNode import SMusicNode


def main():
    song: Music = Music(0, "Test", "Me", "Electronic", 60)
    track1 = Music(1, "Blinding Lights", "The Weeknd", "Synthwave", 171)
    track2 = Music(
        102, "Supercalifragilisticexpialidocious", "Dick Van Dyke", "Musical", 144
    )

    library = MusicLibrary()
    library.push(song)
    library.push(track1)
    library.push(track2)
    library.prepend(track2)

    print(library)
    library.display_library()
    library.display_all_cards()

    # print(song)
    # print(track1)
    # print(track2)
    #
    # print(repr(track1))
    # print(repr(track2))
    # print(repr(song))
    # song.display_card()
    # track1.display_card()
    # track2.display_card()


if __name__ == "__main__":
    main()
