import esper, pygame

from src.create.prefab_creator import explode_animation
from src.ecs.components.Tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.Tags.c_tag_player import CTagPlayer
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.engine.service_locator import ServiceLocator

def system_collision_bullet_player(world: esper.World, player_conf: dict, explosion_conf: dict, player_info: dict):

    player_components = world.get_components(CSurface, CTransform, CTagPlayer)
    bullet_components = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    animations_components = world.get_component(CAnimation)

    p_s: CSurface
    p_t: CTransform
    for player_entity, (p_s, p_t, p_e) in player_components:
        player_rect = CSurface.get_area_relative(p_s.area, p_t.pos)
        for bullet_entity, (b_s, b_t, _) in bullet_components:
            bullet_rect = b_s.surf.get_rect(topleft = b_t.pos)
            if player_rect.colliderect(bullet_rect):
                explode_animation(world, explosion_conf, p_t.pos, player_entity)
                world.delete_entity(bullet_entity)
                new_p_s = CSurface(pygame.Vector2(0,0),pygame.Color(0,0,0), 0)
                p_e.collisioned = True
                world.remove_component(player_entity, CSurface)
                world.add_component(player_entity, new_p_s)

    for player_entity, (p_s, p_t, p_e) in player_components:
        active_animation = False
        for _, c_animation in animations_components:
            if c_animation.entity == player_entity:
                active_animation = True
        if not active_animation and p_e.collisioned:
            p_e.collisioned = False
            player_rect = CSurface.get_area_relative(p_s.area, p_t.pos)
            size = player_rect.size
            p_t.pos = pygame.Vector2(player_conf['position']['x'] - size[0]/2, player_conf['position']['y'] - size[1]/2)
            player_sprite = ServiceLocator.images_service.get(player_info["image"])
            world.remove_component(player_entity, CSurface)
            world.add_component(player_entity, CSurface.from_surface(player_sprite))
                

    
                