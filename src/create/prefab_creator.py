import esper
import pygame

from src.ecs.components.Tags.c_tag_player import CTagPlayer
from src.ecs.components.Tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.Tags.c_tag_star import CTagStar
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_enemy_starship import CEnemyStarship, EnemyStarshipData
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_move_to import CMoveTo
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
    input_player_fire=world.create_entity()

    world.add_component(input_left,CInputCommand("PLAYER_LEFT",pygame.K_LEFT))
    world.add_component(input_right,CInputCommand("PLAYER_RIGHT",pygame.K_RIGHT))
    world.add_component(input_player_fire,CInputCommand("PLAYER_FIRE",pygame.K_z))
    world.add_component(input_pause,CInputCommand("PAUSE",pygame.K_p))

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
        ecs_world.add_component(logo_entity,CMoveTo( (pygame.Vector2(60,(window_json['size']['h']))),pygame.Vector2(60,80) )) 

        return logo_entity 

def create_player_bullet(world: esper.World, player_pos: pygame.Vector2, player_size: pygame.Rect, player_bullet_cfg: dict):
    bullets_in_screen = world.get_component(CTagPlayerBullet)
    if len(bullets_in_screen) < player_bullet_cfg["max_bullets"]:

        size_bullet_cfg = player_bullet_cfg["size"]
        color_bullet_cfg = player_bullet_cfg["color"]
        velocity_bullet_cfg = player_bullet_cfg["velocity"]

        x_pos = player_pos.x + (player_size.w / 2)

        bullet_size = pygame.Vector2(size_bullet_cfg["w"], size_bullet_cfg["h"])
        bullet_color = pygame.Color(color_bullet_cfg["r"], color_bullet_cfg["g"], color_bullet_cfg["b"])
        bullet_position = pygame.Vector2(x_pos, player_pos.y)
        bullet_velocity = pygame.Vector2(velocity_bullet_cfg["x"], velocity_bullet_cfg["y"]) #todo que venga del archivo

        bullet_entity = world.create_entity()
        world.add_component(bullet_entity, CSurface(size=bullet_size, color=bullet_color, blink_rate=0))
        world.add_component(bullet_entity, CTransform(pos=bullet_position))
        world.add_component(bullet_entity, CVelocity(vel=bullet_velocity))
        world.add_component(bullet_entity, CTagPlayerBullet())
        
def create_enemy_starship(world: esper.World, level_data: dict):
    starship_entity = world.create_entity()
    world.add_component(starship_entity, CEnemyStarship(level_data))


def create_enemy(world:esper.World, enemy_starship_conf: dict, position: pygame.Vector2):
    starship_sprite = ServiceLocator.images_service.get(enemy_starship_conf['image'])
    size = starship_sprite.get_size()
    size = [size[0] / enemy_starship_conf['animations']["number_frames"], size[1]]
    velocity = pygame.Vector2(0, 0)
    starship_entity = create_sprite(world,position,velocity,starship_sprite)
    world.add_component(starship_entity, CAnimation(enemy_starship_conf['animations']))
