import json

import pygame

import esper
from src.create.prefab_creator import create_star_spawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_movement_star import system_movement_star
from src.ecs.systems.s_star_spawner import system_star_spawner
from src.engine.scenes.scene import Scene
from src.game.menu_scene import MenuScene
from src.game.play_scene import PlayScene


class GameEngine:
    def __init__(self) -> None:
        

        self._load_config_files()
        pygame.init()
        pygame.display.set_caption(self._window_cfg["title"])
        self.screen = pygame.display.set_mode((self._window_cfg['size']['w'],self._window_cfg['size']['h']),pygame.SCALED)

        self._clock = pygame.time.Clock()
        self.is_running = False
        self._framerate = self._window_cfg["framerate"]
        self._delta_time = 0
        self._bg_color = pygame.Color(self._window_cfg["bg_color"]["r"],
                                    self._window_cfg["bg_color"]["g"],
                                    self._window_cfg["bg_color"]["b"]
                                    )
        self._scenes:dict[str, Scene] = {}
        self._scenes["MENU_SCENE"] = MenuScene(self)
        self._scenes["PLAY_SCENE"] = PlayScene(self)

        
        self._current_scene:Scene = None
        self._scene_name_to_switch:str = None


    def run(self, start_scene_name:str) -> None:
        self.is_running = True
        self._current_scene = self._scenes[start_scene_name]
        self._create()
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
        self._do_clean()

    def switch_scene(self, new_scene_name:str):
        self._scene_name_to_switch = new_scene_name


    def _create(self):
        self._current_scene.do_create()
        #create_star_spawner(self.ecs_world,self.starfield_cfg,self.window_cfg['size']['w'])


    def _calculate_time(self):
        self._clock.tick(self._framerate)
        self._delta_time = self._clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False



    def _update(self):
        self._current_scene.simulate(self._delta_time)
        #self.ecs_world._clear_dead_entities()
        #system_star_spawner(self.ecs_world)
        #system_movement_star(self.ecs_world,self.delta_time,self.window_cfg['size']['h'], self.starfield_cfg["vertical_speed"]["min"],self.starfield_cfg["vertical_speed"]["max"])

    def _draw(self):
        self.screen.fill(self._bg_color)
        #system_rendering_star(self.ecs_world,self.screen)
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()

    def _handle_switch_scene(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    def _do_action(self, action:CInputCommand):        
        self._current_scene.do_action(action)
        
    def _do_clean(self):
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()




    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self._window_cfg = json.load(window_file)
        with open("assets/cfg/starfield.json", encoding="utf-8") as window_file:
            self._starfield_cfg = json.load(window_file )   