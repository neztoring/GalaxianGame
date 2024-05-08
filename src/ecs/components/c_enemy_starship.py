import pygame

class CEnemyStarship:
    def __init__(self, enemy_starships_data: dict) -> None:
        self.enemy_starship_data: list[EnemyStarshipMatrixData] = []
        for starship_enemy in enemy_starships_data["enemy_starships"]:
            self.enemy_starship_data.append(EnemyStarshipMatrixData(starship_enemy, enemy_starships_data["pivot_position_ship"]))
        

class EnemyStarshipMatrixData:
    def __init__(self, starship_data: dict, pivot_position:dict) -> None:
        self.enemy_starship_type = starship_data['starship_type']
        self.enemy_starships: list[list] = []
        for i in range(starship_data["starship_quantity"]["rows"]):
            enemy_columns: list = []
            for j in range(starship_data["starship_quantity"]["columns"]):
                enemy_columns.append(EnemyStarshipData(starship_data['separation_space'], pivot_position))
            if (len(enemy_columns) > 0):
                self.enemy_starships.append(enemy_columns)

class EnemyStarshipData:
    def __init__(self, separation_space: dict, pivot_position:dict) -> None:
        self.position: pygame.Vector2 = pygame.Vector2(
            pivot_position["x"], pivot_position["y"]
        )
        self.separation_space_x = separation_space["x"]
        self.separation_space_y = separation_space["y"]