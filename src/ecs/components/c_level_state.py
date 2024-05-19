from enum import Enum
import pygame

class CLevelState:
    def __init__(self) -> None:
        self.state = LevelState.READY

class LevelState(Enum):
    READY=0
    READY_DONE=1
    PLAY_TIME=2
    GAME_OVER_RECIEVED=3
    GAME_OVER=4
    GAME_OVER_DONE=5
    RESET=6
    LEVEL_ACHIEVED=7