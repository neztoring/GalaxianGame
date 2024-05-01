import pygame

from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand
from src.engine.scenes.scene import Scene
import src.engine.game_engine

class PlayScene(Scene):
    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)

    def do_create(self):
        create_text(self.ecs_world, "Started!", 16, 
                    pygame.Color(255, 0, 0), pygame.Vector2(128, 120), TextAlignment.CENTER,0)
      
        

        quit_to_menu_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(quit_to_menu_action,
                                     CInputCommand("QUIT_TO_MENU", pygame.K_ESCAPE))
        
    def do_action(self, action: CInputCommand):
        if action.name == "QUIT_TO_MENU":
            self.switch_scene("MENU_SCENE")
        
