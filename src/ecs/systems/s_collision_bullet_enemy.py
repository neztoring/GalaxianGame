import esper

from src.ecs.components.Tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.Tags.c_tag_enemy import CTagEnemy

def system_collision_bullet_enemy(world: esper.World):

    enemies_components = world.get_components(CSurface, CTransform, CTagEnemy)
    bullet_components = world.get_components(CSurface, CTransform, CTagPlayerBullet)

    e_s: CSurface
    e_t: CTransform
    for enemy_entity, (e_s, e_t, _) in enemies_components:
        enemy_rect = CSurface.get_area_relative(e_s.area, e_t.pos)
        for bullet_entity, (b_s, b_t, _) in bullet_components:
            bullet_rect = b_s.surf.get_rect(topleft = b_t.pos)
            if enemy_rect.colliderect(bullet_rect):
                world.delete_entity(bullet_entity)
                world.delete_entity(enemy_entity)