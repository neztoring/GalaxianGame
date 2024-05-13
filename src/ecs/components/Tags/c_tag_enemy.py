class CTagEnemy:
    def __init__(self, distance_pivot, score) -> None:
        self.distance_pivot = distance_pivot
        self.current_time: float = 0
        self.time_last_fire: float = 0
        self.score: int = score