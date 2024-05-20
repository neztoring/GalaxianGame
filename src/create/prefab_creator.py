import esper
import pygame

from src.ecs.components.Tags.c_tag_enemy import CTagEnemy
from src.ecs.components.Tags.c_tag_flag import CTagFlag
from src.ecs.components.Tags.c_tag_player import CTagPlayer
from src.ecs.components.Tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.Tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.Tags.c_tag_star import CTagStar
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_starship import CEnemyStarship
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_move_to import CMoveTo
from src.ecs.components.c_player_bullet_state import CPlayerBulletState, PlayerBulletState
from src.ecs.components.c_player_state import CPlayerState
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


def create_star_spawner(world: esper.World, starfield_cfg: dict,screen_w:str,screen_y:str):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CStarSpawner(starfield_cfg,screen_w,screen_y))
    
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
    world.add_component(player_entity, CPlayerState())
    spawn_player_bullet(world, pos, player_sprite.get_rect(), player_info["bullets"])
    return player_entity

def create_input_player(world:esper.World):
    input_left=world.create_entity()
    input_right=world.create_entity()
    input_pause=world.create_entity()
    input_player_behavior=world.create_entity()
    input_change_debug_mode=world.create_entity()

    world.add_component(input_left,CInputCommand("PLAYER_LEFT",pygame.K_LEFT))
    world.add_component(input_right,CInputCommand("PLAYER_RIGHT",pygame.K_RIGHT))
    world.add_component(input_player_behavior,CInputCommand("PLAYER_BEHAVIOR",pygame.K_z))
    world.add_component(input_pause,CInputCommand("PAUSE",pygame.K_p))
    world.add_component(input_change_debug_mode,CInputCommand("DEBUG",pygame.K_d))

def create_logo(ecs_world:esper.World,pos :pygame.Vector2,vel :pygame.Vector2) ->int:
     
        logo_sprite = ServiceLocator.images_service.get("assets/img/invaders_logo_title.png")
        logo_entity = create_sprite(ecs_world,pos,vel,logo_sprite)


        return logo_entity 

def create_flag(ecs_world:esper.World, pos:pygame.Vector2) ->int:
     
        flag_sprite = ServiceLocator.images_service.get("assets/img/invaders_level_flag.png")
        flag_entity=create_sprite(ecs_world, pos, pygame.Vector2(0,0), flag_sprite)
        ecs_world.add_component(flag_entity,CTagFlag)
        return flag_entity 

def create_enemy_bullet(world: esper.World, enemy_pos: pygame.Vector2, player_size: pygame.Rect, enemy_bullet_cfg: dict):
    bullets_in_screen = world.get_component(CTagEnemyBullet)
    enemy_pos_copy = enemy_pos.copy()

    if len(bullets_in_screen) < 1:
        size_bullet_cfg = enemy_bullet_cfg["size"]
        color_bullet_cfg = enemy_bullet_cfg["color"]
        velocity_bullet_cfg = enemy_bullet_cfg["velocity"]

        x_pos = enemy_pos_copy.x + (player_size.w / 2)

        bullet_size = pygame.Vector2(size_bullet_cfg["w"], size_bullet_cfg["h"])
        bullet_color = pygame.Color(color_bullet_cfg["r"], color_bullet_cfg["g"], color_bullet_cfg["b"])
        bullet_position = pygame.Vector2(x_pos, enemy_pos_copy.y)
        bullet_velocity = pygame.Vector2(velocity_bullet_cfg["x"], velocity_bullet_cfg["y"])

        bullet_entity = world.create_entity()
        world.add_component(bullet_entity, CSurface(size=bullet_size, color=bullet_color, blink_rate=0))
        world.add_component(bullet_entity, CTransform(pos=bullet_position))
        world.add_component(bullet_entity, CVelocity(vel=bullet_velocity))
        world.add_component(bullet_entity, CTagEnemyBullet())

def spawn_player_bullet(world: esper.World, player_pos: pygame.Vector2, player_size: pygame.Rect, player_bullet_cfg: dict) -> int:
    world._clear_dead_entities()
    bullets_in_screen = world.get_component(CTagPlayerBullet)
    if len(bullets_in_screen) < 1:
        bullet_entity = world.create_entity()

        size_bullet_cfg = player_bullet_cfg["size"]
        color_bullet_cfg = player_bullet_cfg["color"]
        x_pos = round(player_pos.x + (player_size.w / 2)) -1

        bullet_size = pygame.Vector2(size_bullet_cfg["w"], size_bullet_cfg["h"])
        bullet_color = pygame.Color(color_bullet_cfg["r"], color_bullet_cfg["g"], color_bullet_cfg["b"])
        bullet_position = pygame.Vector2(x_pos, player_pos.y-size_bullet_cfg["h"]+ 1)

        world.add_component(bullet_entity, CSurface(size=bullet_size, color=bullet_color, blink_rate=0))
        world.add_component(bullet_entity, CTransform(pos=bullet_position))
        world.add_component(bullet_entity, CTagPlayerBullet())
        world.add_component(bullet_entity, CVelocity(vel=pygame.Vector2(0,0)))
        world.add_component(bullet_entity, CPlayerBulletState())
        

def fire_player_bullet(world: esper.World, player_bullet_cfg: dict):
    bullets_in_screen = world.get_component(CPlayerBulletState)
    if len(bullets_in_screen) > 0:
        (_, c_pbst) = bullets_in_screen[0]
        if c_pbst.state != PlayerBulletState.FIRED:
            ServiceLocator.sounds_service.play(player_bullet_cfg["sound"])
        c_pbst.state = PlayerBulletState.FIRED
        
        
def create_enemy_starship(world: esper.World, level_data: dict):
    starship_entity = world.create_entity()
    world.add_component(starship_entity, CEnemyStarship(level_data))


def create_enemy(world:esper.World, enemy_starship_conf: dict, position: pygame.Vector2, distance_pivot: float, velocity: int):
    starship_sprite = ServiceLocator.images_service.get(enemy_starship_conf['image'])
    size = starship_sprite.get_size()
    size = [size[0] / enemy_starship_conf['animations']["number_frames"], size[1]]
    velocity = pygame.Vector2(velocity, 0)
    starship_entity = create_sprite(world,position,velocity,starship_sprite)
    world.add_component(starship_entity, CAnimation(enemy_starship_conf['animations']))
    world.add_component(starship_entity, CTagEnemy(distance_pivot, enemy_starship_conf['score']))
    
def create_starship_enemies(world: esper.World, enemies_config: dict):
    components = world.get_component(CEnemyStarship)
    c_es: CEnemyStarship
    acum = 1
    for _, (c_es) in components:
        for i, matrix_starship in enumerate(c_es.enemy_starship_data):
            for row_starship in matrix_starship.enemy_starships:
                for z, column_starship in enumerate(row_starship):
                    size_x = enemies_config[matrix_starship.enemy_starship_type]['size']['x']
                    size_y = enemies_config[matrix_starship.enemy_starship_type]['size']['y']
                    position_updated = pygame.Vector2(column_starship.position.x 
                                                      + ((size_x + column_starship.separation_space_x) * (i + 1)) 
                                                      + ((size_x + column_starship.separation_space_x) * (z + 1)), 
                                                      column_starship.position.y - ((size_y + column_starship.separation_space_y) * (acum + 1)))
                    if i == len(c_es.enemy_starship_data) - 1 and z > 0:
                        position_updated.x = position_updated.x + (size_x + column_starship.separation_space_x) * 2
                    distance_pivot = position_updated.x - row_starship[-1].position.x
                    create_enemy(world, enemies_config[matrix_starship.enemy_starship_type],position_updated, distance_pivot, enemies_config['velocity_enemies'])
                acum += 1


def explode_animation(world: esper.World, explosion_info: dict, last_position: pygame.Vector2, entity: int):
    explode_surface = ServiceLocator.images_service.get(explosion_info["image"])
    pos = last_position.copy()
    vel = pygame.Vector2(0,0)
    explode_entity = create_sprite(world, pos, vel, explode_surface)
    world.add_component(explode_entity, CAnimation(explosion_info["animations"], True, entity))

    c_surf = world.component_for_entity(explode_entity, CSurface)
    c_surf.area.w = explode_surface.get_width() / explosion_info["animations"]["number_frames"]

    ServiceLocator.sounds_service.play(explosion_info["sound"])