from dataclasses import dataclass
from enum import Enum, auto

from structs.Library import MusicLibrary


class Screen(Enum):
    # Library
    # ------------------------
    ADD_SONG = auto()
    REMOVE_SONG = auto()
    LIST_SONGS = auto()
    # ------------------------

    # Helpers
    # ------------------------
    MAIN = auto()
    BACK = auto()
    EXIT = auto()
    STAY = auto()
    TODO = auto()
    # ------------------------


@dataclass
class AppState:
    library: MusicLibrary
