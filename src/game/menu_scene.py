import json
import pygame

from src.create.prefab_creator import create_logo, create_star_spawner
from src.ecs.components.Tags.c_tag_text_mov import CTagTextMov
from src.ecs.components.c_move_to import CMoveTo
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_movement_star import system_movement_star
import src.engine.game_engine

from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_movement_to import system_movement_to
from src.ecs.systems.s_star_spawner import system_star_spawner
from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase 

class MenuScene(Scene):

    def __init__(self,engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/starfield.json", encoding="utf-8") as window_file:
            self.starfield_cfg = json.load(window_file )  

    
    def do_create(self):

        self._textpress=create_text(self.ecs_world, "PRESS Z TO START", 8, 
                    pygame.Color(255, 0, 0), pygame.Vector2(128, (self.window_cfg['size']['h'])+150), TextAlignment.CENTER,0.5)
        self.ecs_world.add_component(self._textpress,CVelocity(vel=pygame.Vector2(self.window_cfg['text_speed']['min'],self.window_cfg['text_speed']['max'])) )
        self.ecs_world.add_component(self._textpress,CMoveTo( (pygame.Vector2(128,(self.window_cfg['size']['h'])+150)),pygame.Vector2(128,150) )) 
 


        self._text_hi_score=create_text(self.ecs_world, "1UP         HI-SCORE", 8, 
                    pygame.Color(255, 0, 0), pygame.Vector2(20, (self.window_cfg['size']['h'])), TextAlignment.LEFT,0)
        self.ecs_world.add_component(self._text_hi_score,CVelocity(vel=pygame.Vector2(self.window_cfg['text_speed']['min'],self.window_cfg['text_speed']['max'])) )
        self.ecs_world.add_component(self._text_hi_score,CMoveTo( (pygame.Vector2(128,(self.window_cfg['size']['h'])+20)),pygame.Vector2(128,10) ))
        
        self._textup=create_text(self.ecs_world, "   00", 8, 
                    pygame.Color(255, 255, 255), pygame.Vector2(20, (self.window_cfg['size']['h'])+10), TextAlignment.LEFT,0)
        self.ecs_world.add_component(self._textup,CVelocity(vel=pygame.Vector2(self.window_cfg['text_speed']['min'],self.window_cfg['text_speed']['max'])) )
        self.ecs_world.add_component(self._textup,CMoveTo( (pygame.Vector2(128,(self.window_cfg['size']['h'])+20)),pygame.Vector2(128,20) )) 

        self._textscore=create_text(self.ecs_world, "               5000", 8, 
                    pygame.Color(51, 51, 255), pygame.Vector2(20, (self.window_cfg['size']['h'])+10), TextAlignment.LEFT,0)
        self.ecs_world.add_component(self._textscore,CVelocity(vel=pygame.Vector2(self.window_cfg['text_speed']['min'],self.window_cfg['text_speed']['max'])) )
        self.ecs_world.add_component(self._textscore,CMoveTo( (pygame.Vector2(128,(self.window_cfg['size']['h'])+20)),pygame.Vector2(128,20) ))  

        self._logo=create_logo(self.ecs_world,pygame.Vector2(60, (self.window_cfg['size']['h'])+40),pygame.Vector2(self.window_cfg['text_speed']['min'],self.window_cfg['text_speed']['max']))
        self.ecs_world.add_component( self._logo,CMoveTo( (pygame.Vector2(60,(self.window_cfg['size']['h'])+60)),pygame.Vector2(60,50) )) 

        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))
        
        create_star_spawner(self.ecs_world,self.starfield_cfg,self.window_cfg['size']['w'],self.window_cfg['size']['h'])

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME" and action.phase == CommandPhase.START:
            self.switch_scene("PLAY_SCENE")
        
    

    def do_update(self,delta_time:float):
        self.ecs_world._clear_dead_entities()
        system_movement_to(self.ecs_world,delta_time)
        system_star_spawner(self.ecs_world)
        system_movement_star(self.ecs_world,delta_time,self.window_cfg['size']['h'], self.starfield_cfg["vertical_speed"]["min"],self.starfield_cfg["vertical_speed"]["max"])
        system_blink(self.ecs_world,delta_time)
        
    
