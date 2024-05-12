import esper, pygame 
from src.ecs.components.Tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.Tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform


def system_bullet_delete(world: esper.World, screen: pygame.Surface):
    player_bullet_components = world.get_components(CSurface, CTransform, CTagPlayerBullet)
    enemy_bullet_components = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    screen_rect = screen.get_rect()

    c_t: CTransform
    c_s: CSurface
    for bullet_entity, (c_s, c_t, _) in player_bullet_components:
        cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width or cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            world.delete_entity(bullet_entity)

    for bullet_entity, (c_s, c_t, _) in enemy_bullet_components:
        cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
        if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width or cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            world.delete_entity(bullet_entity)