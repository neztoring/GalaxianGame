from enum import Enum
import json
import time
import pygame, esper

from src.create.prefab_creator import create_enemy_starship, create_flag, create_player_bullet, create_input_player, create_player_square, create_starship_enemies
from src.create.prefab_creator_interface import TextAlignment, create_level_state, create_text, create_text_score
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_level_state import CLevelState, LevelState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_bullet_player import system_collision_bullet_player
from src.ecs.systems.s_enemy_fire import system_enemy_fire
from src.ecs.systems.s_level_state import system_level_state
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_bullet_delete import system_bullet_delete
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_rendering_debug import system_rendering_debug
from src.ecs.systems.s_screen_bounce import system_enemy_screen_bounce
from src.ecs.systems.s_screen_player import system_screen_player
from src.engine.scenes.scene import Scene
import src.engine.game_engine
from src.engine.service_locator import ServiceLocator

class DebugView(Enum):
    NONE = 0
    RECTS = 1

class PlayScene(Scene):
    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:

        with open("assets/cfg/player.json", encoding="utf-8") as player_file:
            self.player_cfg = json.load(player_file)   
        with open("assets/cfg/enemies.json", encoding="utf-8") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/level_01.json", encoding="utf-8") as level_file:
            self.level_cfg = json.load(level_file)
        with open("assets/cfg/window.json", encoding="utf-8") as level_file:
            self.windows_cfg = json.load(level_file)
        with open("assets/cfg/explosion.json", encoding="utf-8") as explosion_file:
            self.explosion_cfg = json.load(explosion_file)
        super().__init__(engine)
        self.level=1
        

    def do_create(self):
        self.current_time=0
        self.debug_mode = DebugView.NONE
        self.pause=False
        self.player_entity=create_player_square(self.ecs_world, self.player_cfg)
        self.player_c_v=self.ecs_world.component_for_entity(self.player_entity, CVelocity)
        self.player_c_t=self.ecs_world.component_for_entity(self.player_entity, CTransform)
        self.player_c_s=self.ecs_world.component_for_entity(self.player_entity, CSurface)
        self.ready=create_text(self.ecs_world, "GAME START", 8, 
                    pygame.Color(255, 255, 255), pygame.Vector2(128, 120), TextAlignment.CENTER, 0)
        ServiceLocator.sounds_service.play(self.player_cfg["sound_intro"])
      
        quit_to_menu_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(quit_to_menu_action,
                                     CInputCommand("QUIT_TO_MENU", pygame.K_ESCAPE))
        
        create_input_player(self.ecs_world)
        create_flag(self.ecs_world,pygame.Vector2(200,10))
        create_text(self.ecs_world,"0"+str(self.level), 8, pygame.Color(255, 255, 255), pygame.Vector2(210, 15), TextAlignment.LEFT, 0)
        create_text(self.ecs_world,"1UP", 8, pygame.Color(255, 0, 0 ), pygame.Vector2(18, 10), TextAlignment.LEFT, 0)
        create_text_score(self.ecs_world, "00" , 8, pygame.Color(255, 255, 255), pygame.Vector2(58, 18), TextAlignment.RIGHT, 0)
        self.level_entity=create_level_state(self.ecs_world)
        self.level_state=self.ecs_world.component_for_entity(self.level_entity, CLevelState)
        
    def do_action(self, action: CInputCommand):
        if action.name == "QUIT_TO_MENU":
            self.switch_scene("MENU_SCENE")
        if action.name=='PLAYER_LEFT':
            if action.phase == CommandPhase.START:
                self.player_c_v.vel.x -= self.player_cfg['input_velocity']
            elif action.phase == CommandPhase.END:
                self.player_c_v.vel.x += self.player_cfg['input_velocity']
        if action.name=='PLAYER_RIGHT':
            if action.phase == CommandPhase.START:
                self.player_c_v.vel.x += self.player_cfg['input_velocity']
            elif action.phase == CommandPhase.END:
                self.player_c_v.vel.x -= self.player_cfg['input_velocity']
        if action.name=="PLAYER_FIRE" and self.level_state.state==LevelState.PLAY_TIME and action.phase == CommandPhase.START:
                create_player_bullet(self.ecs_world, self.player_c_t.pos, self.player_c_s.surf.get_rect(), self.player_cfg["bullets"])
        if action.name=="PLAYER_FIRE" and self.level_state.state==LevelState.GAME_OVER_DONE and action.phase == CommandPhase.START:    
            self.switch_scene("MENU_SCENE")
        if action.name=='PAUSE' and self.level_state.state==LevelState.READY:
            if action.phase == CommandPhase.START:          
                if not self.pause:  
                    ServiceLocator.sounds_service.play(self.player_cfg["game_paused"])
                    self.pause_text=create_text(self.ecs_world, "PAUSED", 8, 
                                            pygame.Color(255, 0, 0 ), pygame.Vector2(128, 120), TextAlignment.CENTER, 0.5)
                else:
                    self.ecs_world.delete_entity(self.pause_text)
                self.pause = not self.pause
        if action.name=="DEBUG" and action.phase == CommandPhase.START:
            if self.debug_mode == DebugView.NONE:
                self.debug_mode = DebugView.RECTS
            elif self.debug_mode == DebugView.RECTS:
                self.debug_mode = DebugView.NONE
    
    def do_update(self,delta_time:float):
        
        self.current_time+=delta_time 
        
        if(self.level_state.state==LevelState.LEVEL_ACHIEVED):
            self.level+=1
            self.clean()
            self.do_create()

        self.ecs_world._clear_dead_entities()      
        system_level_state(self.ecs_world, self.level_entity, self.current_time, self.player_cfg)
        system_blink(self.ecs_world,delta_time)
        
        if not self.pause:
            system_movement(self.ecs_world, delta_time)
            system_animation(self.ecs_world, delta_time)
            system_bullet_delete(self.ecs_world, self._game_engine.screen)
            system_enemy_screen_bounce(self.ecs_world, self._game_engine.screen, self.level_cfg)
            system_screen_player(self.ecs_world, self._game_engine.screen, self.level_cfg) 
            system_enemy_fire(self.ecs_world, delta_time ,self.level_cfg["enemy_bullet"])
            system_collision_bullet_enemy(self.ecs_world, self.explosion_cfg["enemy"])   
            system_collision_bullet_player(self.ecs_world, self.player_cfg, self.explosion_cfg["player"], delta_time)

            if self.level_state.state==LevelState.READY_DONE: 
                self.ecs_world.delete_entity(self.ready)
                create_enemy_starship(self.ecs_world, self.level_cfg)
                create_starship_enemies(self.ecs_world, self.enemies_cfg)
                self.level_state.state=LevelState.PLAY_TIME
            if self.level_state.state==LevelState.GAME_OVER:          
                create_text(self.ecs_world, "GAME OVER", 8, 
                            pygame.Color(255, 255, 255), pygame.Vector2(128, 120), TextAlignment.CENTER, 0)
                ServiceLocator.sounds_service.play(self.player_cfg["sound_over"])
                self.level_state.state=LevelState.GAME_OVER_DONE
                
    
    def do_draw(self, screen):
        if self.debug_mode == DebugView.RECTS:
            system_rendering_debug(self.ecs_world, screen)
        else:
            system_rendering(self.ecs_world, screen)
                
                

      
        