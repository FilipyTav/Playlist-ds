from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable

from structs.HistoryQueue import History
from structs.Library import MusicLibrary


class Screen(Enum):
    # Library
    # ------------------------
    ADD_SONG = auto()
    REMOVE_SONG = auto()
    LIST_SONGS = auto()
    FIND_SONG = auto()
    FILL_PLS = auto()
    PLAYER = auto()
    CHOOSE_PLAYLIST = auto()
    SEE_PLAYLIST = auto()
    SEE_HISTORY = auto()
    SEE_STATISTICS = auto()
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
    history: History
    selected_playlist: str | None = None


@dataclass
class ScreenConfig:
    id: Screen
    label: str
    handler: Callable
    parent: Screen | None = None
