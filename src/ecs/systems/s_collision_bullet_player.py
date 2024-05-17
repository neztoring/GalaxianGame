import copy
import esper, pygame

from src.create.prefab_creator import explode_animation
from src.ecs.components.Tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.Tags.c_tag_player import CTagPlayer
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.engine.service_locator import ServiceLocator

def system_collision_bullet_player(world: esper.World, player_conf: dict,explosion_conf: dict, delta_time: float):

    player_components = world.get_components(CSurface, CTransform, CTagPlayer, CPlayerState)
    bullet_components = world.get_components(CSurface, CTransform, CTagEnemyBullet)

    p_s: CSurface
    p_t: CTransform
    for player_entity, (p_s, p_t, p_p, p_pst) in player_components:
        player_rect = CSurface.get_area_relative(p_s.area, p_t.pos)
        for bullet_entity, (b_s, b_t, _) in bullet_components:
            bullet_rect = b_s.surf.get_rect(topleft = b_t.pos)
            if player_rect.colliderect(bullet_rect):
                explode_animation(world, explosion_conf, p_t.pos, player_entity)
                world.delete_entity(bullet_entity)
                new_p_s = CSurface(pygame.Vector2(0,0),pygame.Color(0,0,0), 0)
                p_pst.state = PlayerState.DEAD
                p_p.time_recover += delta_time
                p_p.collisioned=True
                world.remove_component(player_entity, CSurface)
                world.add_component(player_entity, new_p_s)

    for player_entity, (p_s, p_t, p_p, p_pst) in player_components:
        if p_p.collisioned:
            if p_p.time_recover > player_conf["time_recover"]:
                world.delete_entity(player_entity)
            else:
                p_p.time_recover += delta_time
            
                

    
                