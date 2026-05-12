from music import Music
from structs.Library import MusicLibrary
from structs.Menu import MenuManager
from utils.types import AppState


def main():
    songs: list[Music] = [
        Music("Test", "Me", "Electronic", 60),
        Music("Blinding Lights", "The Weeknd", "Synthwave", 171),
        Music("Supercalifragilisticexpialidocious", "Dick Van Dyke", "Musical", 144),
        #
        Music("Heal the World", "Michael Jackson", "Pop Ballad", 81),
        Music("Chicago", "Michael Jackson", "Contemporary R&B", 101),
        Music("The Way You Make Me Feel", "Michael Jackson", "Pop", 114),
        Music("Wanna Be Startin' Somethin'", "Michael Jackson", "Post-Disco", 122),
        Music("Bad", "Michael Jackson", "Dance-Pop", 133),
        Music("Speed Demon", "Michael Jackson", "Funk Rock", 146),
        #
        Music("Test", "Me", "Electronic", 200),
    ]

    library = MusicLibrary()
    for s in songs:
        library.append(s)
    # library.append(track1)
    # library.prepend(track2)
    # a = library.find_by_name("Supercalifragilisticexpialidocious")

    menu: MenuManager = MenuManager(AppState(library))
    menu.run()


if __name__ == "__main__":
    main()
