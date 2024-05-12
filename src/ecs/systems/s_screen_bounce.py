import esper, pygame
from src.ecs.components.Tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_enemy_screen_bounce(world: esper.World, screen: pygame.Surface, level_cfg: dict):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemy)
    c_transform: CTransform
    c_surface: CSurface
    c_velocity: CVelocity
    c_enemy: CTagEnemy
    change_direction = False
    for entity, (c_transform, c_velocity, c_surface, c_enemy) in components:
        cuad_rect = CSurface.get_area_relative(c_surface.area, c_transform.pos)
        if cuad_rect.left < level_cfg["border_space"]["left"] or cuad_rect.right > (screen_rect.width - level_cfg["border_space"]["right"]):
            change_direction = True
            break
    for entity, (c_transform, c_velocity, c_surface, c_enemy) in components:
        cuad_rect = CSurface.get_area_relative(c_surface.area, c_transform.pos)
        if change_direction:
            c_velocity.vel.x *= -1
