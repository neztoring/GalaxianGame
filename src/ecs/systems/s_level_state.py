import pygame
import esper
from src.create.prefab_creator import create_enemy_starship, create_starship_enemies
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.Tags.c_tag_enemy import CTagEnemy
from src.ecs.components.Tags.c_tag_player import CTagPlayer
from src.ecs.components.c_level_state import CLevelState, LevelState
from src.engine.service_locator import ServiceLocator

def system_level_state(world: esper.World, level_entity: int, current_time:float, player_conf: dict, level_cfg: dict, enemies_cfg: dict, ready: int):
    c_ls = world.component_for_entity(level_entity, CLevelState)
    
    player = world.get_components(CTagPlayer)
    enemies = world.get_components(CTagEnemy)
    if(c_ls.state==LevelState.READY and current_time>player_conf["time_recover"]):
        c_ls.state = LevelState.READY_DONE
    elif(c_ls.state==LevelState.READY_DONE):
       _do_ready_done_state(c_ls, world, level_cfg, enemies_cfg, ready)
    elif(c_ls.state==LevelState.PLAY_TIME and player.__len__()==0):
        c_ls.state = LevelState.GAME_OVER
    elif(c_ls.state==LevelState.PLAY_TIME and enemies.__len__()==0):
        c_ls.state = LevelState.LEVEL_ACHIEVED
    elif(c_ls.state==LevelState.GAME_OVER):
        _do_game_over_state(c_ls, world, player_conf)

def _do_ready_done_state(c_ls: CLevelState, world: esper.World, level_cfg: dict, enemies_cfg: dict, ready: int):
    world.delete_entity(ready)
    create_enemy_starship(world, level_cfg)
    create_starship_enemies(world, enemies_cfg)
    c_ls.state=LevelState.PLAY_TIME  

def _do_game_over_state(c_ls: CLevelState, world: esper.World, player_cfg: dict):
    create_text(world, "GAME OVER", 8, pygame.Color(255, 255, 255), pygame.Vector2(128, 120), TextAlignment.CENTER, 0)
    ServiceLocator.sounds_service.play(player_cfg["sound_over"])
    c_ls.state=LevelState.GAME_OVER_DONE
