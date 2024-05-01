import esper
import pygame

from src.ecs.components.Tags.c_tag_star import CTagStar
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_star_spawner import CStarSpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.c_velocity import CVelocity



def create_star(world: esper.World, pos: pygame.Vector2, color: pygame.Vector2,vel: pygame.Vector2,blink_rate:str) -> int:
    star_entity = world.create_entity()
    world.add_component(star_entity,CSurface(size=pygame.Vector2(1,1),color=color,blink_rate=blink_rate))
    world.add_component(star_entity,CTransform(pos=pos))
    world.add_component(star_entity,CVelocity(vel=vel))    
    world.add_component(star_entity, CTagStar())



    return star_entity


def create_star_spawner(world: esper.World, starfield_cfg: dict,screen_w:str):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CStarSpawner(starfield_cfg,screen_w))

