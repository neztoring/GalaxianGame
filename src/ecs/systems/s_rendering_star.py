import esper
import pygame

from src.ecs.components.Tags.c_tag_star import CTagStar
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_star_spawner import CStarSpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform



def system_rendering_star(world:esper.World,screen:pygame.Surface):
    components = world.get_components(CTransform,CSurface,CBlink, CTagStar)

    c_t:CTransform
    c_s:CSurface
    c_b:CBlink
    for entity, (c_t,c_s,c_b,_) in components:
        if c_b.visible:
            screen.blit(c_s.surf,c_t.pos)

        