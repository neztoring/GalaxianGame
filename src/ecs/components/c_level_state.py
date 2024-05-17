from enum import Enum
import pygame

class CLevelState:
    def __init__(self) -> None:
        self.state = LevelState.READY

class LevelState(Enum):
    READY=0
    READY_DONE=1
    PLAY_TIME=2
    GAME_OVER=3
    GAME_OVER_DONE=4
    RESET=5
    LEVEL_ACHIEVED=6