import esper
import pygame

from src.ecs.components.Tags.c_tag_player import CTagPlayer
from src.ecs.components.Tags.c_tag_star import CTagStar
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_star_spawner import CStarSpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator



def create_star(world: esper.World, pos: pygame.Vector2, color: pygame.Vector2,vel: pygame.Vector2,blink_rate:str) -> int:
    star_entity = world.create_entity()
    world.add_component(star_entity,CSurface(size=pygame.Vector2(1,1),color=color))
    world.add_component(star_entity,CTransform(pos=pos))
    world.add_component(star_entity,CVelocity(vel=vel))    
    world.add_component(star_entity, CTagStar())
    world.add_component(star_entity,CBlink(blink_rate=blink_rate) )


    return star_entity


def create_star_spawner(world: esper.World, starfield_cfg: dict,screen_w:str):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CStarSpawner(starfield_cfg,screen_w))
    
def create_sprite(world: esper.World, pos: pygame.Vector2,vel: pygame.Vector2,
                  surface:pygame.Surface)->int:
    sprite_entity= world.create_entity()
    world.add_component(sprite_entity, CTransform(pos))
    world.add_component(sprite_entity, CVelocity(vel))
    world.add_component(sprite_entity,CSurface.from_surface(surface))
    return sprite_entity

def create_player_square(world:esper.World, player_info:dict)->int:
    player_sprite = ServiceLocator.images_service.get(player_info["image"])
    size=player_sprite.get_size()
    pos=pygame.Vector2(player_info['position']['x']-size[0]/2,player_info['position']['y']-size[1]/2)
    vel=pygame.Vector2(0,0)
    player_entity=create_sprite(world, pos,vel, player_sprite)
    world.add_component(player_entity,CTagPlayer())
    return player_entity

def create_input_player(world:esper.World):
    input_left=world.create_entity()
    input_right=world.create_entity()
    input_pause=world.create_entity()

    world.add_component(input_left,CInputCommand("PLAYER_LEFT",pygame.K_LEFT))
    world.add_component(input_right,CInputCommand("PLAYER_RIGHT",pygame.K_RIGHT))
    world.add_component(input_pause,CInputCommand("PAUSE",pygame.K_p))

