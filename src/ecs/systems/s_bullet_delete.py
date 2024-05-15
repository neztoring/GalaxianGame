import esper, pygame 
from src.create.prefab_creator import spawn_player_bullet
from src.ecs.components.Tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.Tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform


def system_bullet_delete(world: esper.World, screen: pygame.Surface, player_cfg: dict):
    screen_rect = screen.get_rect()
    c_t: CTransform
    c_s: CSurface

    player_bullet_components = world.get_components(CSurface, CTransform, CTagPlayerBullet)
    for bullet_entity, (c_s, c_t, _) in player_bullet_components:
        cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width or cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            world.delete_entity(bullet_entity)
            spawn_player_bullet(world, c_t.pos, c_s.surf.get_rect(), player_cfg["bullets"])


    enemy_bullet_components = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    for bullet_entity, (c_s, c_t, _) in enemy_bullet_components:
        cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width or cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            world.delete_entity(bullet_entity)