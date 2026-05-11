from music import Music
from structs.Library import MusicLibrary
from structs.Menu import MenuManager


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

    menu: MenuManager = MenuManager()
    menu.run()


if __name__ == "__main__":
    main()
