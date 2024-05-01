import pygame

class CMovingText:
    def __init__(self, pos_ini:pygame.Vector2, pos_fin:pygame.Vector2) -> None:
        self.pos_ini = pos_ini
        self.pos_fin = pos_fin