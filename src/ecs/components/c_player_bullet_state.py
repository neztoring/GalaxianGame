from enum import Enum

class CPlayerBulletState:
    def __init__(self) -> None:
        self.state = PlayerBulletState.IDLE

class PlayerBulletState(Enum):
    IDLE = 0
    READY = 1
    FIRED = 2