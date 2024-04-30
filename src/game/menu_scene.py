import json
import pygame

from src.create.prefab_creator import create_star_spawner
from src.ecs.systems.s_movement_star import system_movement_star

from src.ecs.systems.s_star_spawner import system_star_spawner
from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand 

class MenuScene(Scene):

    def __init__(self,engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/starfield.json", encoding="utf-8") as window_file:
            self.starfield_cfg = json.load(window_file )  

    
    def do_create(self):

        create_text(self.ecs_world, "PRESS Z TO START", 8, 
                    pygame.Color(255, 0, 0), pygame.Vector2(128, 180), TextAlignment.CENTER)

        
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))
        
        create_star_spawner(self.ecs_world,self.starfield_cfg,self.window_cfg['size']['w'])

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("PLAY_SCENE")
        
    

    def do_update(self,delta_time:float):
        self.ecs_world._clear_dead_entities()
        system_star_spawner(self.ecs_world)
        system_movement_star(self.ecs_world,delta_time,self.window_cfg['size']['h'], self.starfield_cfg["vertical_speed"]["min"],self.starfield_cfg["vertical_speed"]["max"])
    
