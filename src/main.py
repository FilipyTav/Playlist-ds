from music import Music
from structs.Library import MusicLibrary
from structs.MusicNode import SMusicNode


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

    print(library)
    library.display_library()
    library.display_all_cards()

    a = library.remove_at(0)
    print(a)
    library.display_library()

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
