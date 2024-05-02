import esper, pygame
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.Tags.c_tag_player import CTagPlayer

def system_screen_player(world:esper.World,screen:pygame.Surface):
    src_rect=screen.get_rect()
    components=world.get_components(CTransform,CSurface,CVelocity,CTagPlayer)

    for player_entity, (c_t,c_s,c_v,_) in components:
        player_rect=CSurface.get_area_relative(c_s.area, c_t.pos)
        if not src_rect.contains(player_rect):
            player_rect.clamp_ip(src_rect)
            c_t.pos.xy=player_rect.topleft
