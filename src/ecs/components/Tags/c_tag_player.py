from src.ecs.components.c_player_state import PlayerState


class CTagPlayer:
    def __init__(self) -> None:
        self.collisioned = False
        self.time_recover = 0

