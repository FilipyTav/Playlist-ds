from music import Music
from structs.MusicNode import SMusicNode


def main():
    song: Music = Music(0, "Test", "Me", "Electronic", 60)
    librarynode: SMusicNode = SMusicNode(song)
    print(librarynode.next)


if __name__ == "__main__":
    main()
