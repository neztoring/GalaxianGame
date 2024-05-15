from enum import Enum

class CPlayerState:
    def __init__(self) -> None:
        self.state = PlayerState.IDLE

class PlayerState(Enum):
    IDLE = 0
    ALIVE = 1
    DEAD = 2
    GAME_OVER = 3