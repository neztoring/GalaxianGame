import esper
import pygame

from src.ecs.components.Tags.c_tag_star import CTagStar
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_moving_text import CMovingText
from src.ecs.components.c_star_spawner import CStarSpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator



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

def create_sprite(world:esper.World,pos:pygame.Vector2,vel:pygame.Vector2,
                  surface:pygame.Surface)->int:
        sprite_entity =world.create_entity()
        world.add_component(sprite_entity,CTransform(pos))
        world.add_component(sprite_entity,CVelocity(vel))
        world.add_component(sprite_entity,CSurface.from_surface(surface))
        return sprite_entity



def create_logo(ecs_world:esper.World, window_json:dict, pos :pygame.Vector2) ->int:
     
        logo_sprite = ServiceLocator.images_service.get("assets/img/invaders_logo_title.png")

        vel = pygame.Vector2(10,10)
        logo_entity = create_sprite(ecs_world,pos,vel,logo_sprite)
        ecs_world.add_component(logo_entity,CMovingText( (pygame.Vector2(60,(window_json['size']['h']))),pygame.Vector2(60,80) )) 

        return logo_entity 