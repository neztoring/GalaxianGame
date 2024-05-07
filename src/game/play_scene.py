import json
import time
import pygame, esper

from src.create.prefab_creator import create_player_bullet, create_input_player, create_player_square
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_bullet_delete import system_player_bullet_delete
from src.ecs.systems.s_screen_player import system_screen_player
from src.engine.scenes.scene import Scene
import src.engine.game_engine
from src.engine.service_locator import ServiceLocator

class PlayScene(Scene):
    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:
        self.start_time = pygame.time.get_ticks()      
        self.pause = False
        self.play_time = False
        self.game_over = False
        self.game_ready_deleted = False
        self.game_over_released = False
        with open("assets/cfg/player.json", encoding="utf-8") as player_file:
            self.player_cfg = json.load(player_file)   
        super().__init__(engine)

    def do_create(self):
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
        if action.name=="PLAYER_FIRE":
            if action.phase == CommandPhase.START:
                create_player_bullet(self.ecs_world, self.player_c_t.pos, self.player_c_s.surf.get_rect(), self.player_cfg["bullets"])
        if action.name=='PAUSE' and self.play_time:
            if action.phase == CommandPhase.START:
                if not self.pause:  
                    self.pause_text=create_text(self.ecs_world, "PAUSED", 8, 
                                            pygame.Color(255, 0, 0 ), pygame.Vector2(128, 120), TextAlignment.CENTER, 0.5)
                else:
                    self.ecs_world.delete_entity(self.pause_text)
                self.pause = not self.pause
    
    def do_update(self,delta_time:float):
        system_player_bullet_delete(self.ecs_world, self._game_engine.screen)
        self.ecs_world._clear_dead_entities()
        self.curret_time=pygame.time.get_ticks()
        self.play_time=self.curret_time-self.start_time>3500
        self.game_over=self.curret_time-self.start_time>8000 #TODO - Cambiar esto a cuando haya colisión con el jugador
        
        
        system_blink(self.ecs_world,delta_time)
        if not self.pause:
            system_movement(self.ecs_world, delta_time)
            system_screen_player(self.ecs_world, self._game_engine.screen)    
            if self.play_time and not self.game_ready_deleted: 
                self.game_ready_deleted=True
                self.ecs_world.delete_entity(self.ready)
            if self.game_over:         
                if not self.game_over_released:
                    create_text(self.ecs_world, "GAME OVER", 8, 
                                pygame.Color(255, 255, 255), pygame.Vector2(128, 120), TextAlignment.CENTER, 0)
                    ServiceLocator.sounds_service.play(self.player_cfg["sound_over"])
                    self.game_over_time=self.curret_time
                    self.ecs_world.delete_entity(self.player_entity)
                    self.game_over_released=True
                elif self.curret_time-self.game_over_time>3500:
                    self.switch_scene("MENU_SCENE")
                
                

      
        