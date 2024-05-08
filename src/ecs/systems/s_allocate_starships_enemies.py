import pygame, esper
from src.create.prefab_creator import create_enemy
from src.ecs.components.c_enemy_starship import CEnemyStarship

def system_allocate_starship_enemies(world: esper.World, enemies_config: dict):
    components = world.get_component(CEnemyStarship)
    c_es: CEnemyStarship
    acum = 1
    for _, (c_es) in components:
        for i, matrix_starship in enumerate(c_es.enemy_starship_data):
            for row_starship in matrix_starship.enemy_starships:
                for z, column_starship in enumerate(row_starship):
                    size_x = enemies_config[matrix_starship.enemy_starship_type]['size']['x']
                    size_y = enemies_config[matrix_starship.enemy_starship_type]['size']['y']
                    position_updated = pygame.Vector2(column_starship.position.x 
                                                      + ((size_x + column_starship.separation_space_x) * (i + 1)) 
                                                      + ((size_x + column_starship.separation_space_x) * (z + 1)), 
                                                      column_starship.position.y - ((size_y + column_starship.separation_space_y) * (acum + 1)))
                    if i == len(c_es.enemy_starship_data) - 1 and z > 0:
                        position_updated.x = position_updated.x + (size_x + column_starship.separation_space_x) * 2
                    create_enemy(world, enemies_config[matrix_starship.enemy_starship_type],position_updated)
                acum += 1