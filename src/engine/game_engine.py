import json

import pygame

import esper
from src.create.prefab_creator import create_star_spawner
from src.ecs.systems.s_movement_star import system_movement_star
from src.ecs.systems.s_rendering_star import system_rendering_star
from src.ecs.systems.s_star_spawner import system_star_spawner


class GameEngine:
    def __init__(self) -> None:
        

        self._load_config_files()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode((self.window_cfg['size']['w'],self.window_cfg['size']['h']),pygame.SCALED)

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                    self.window_cfg["bg_color"]["g"],
                                    self.window_cfg["bg_color"]["b"]
                                    )
        self.ecs_world = esper.World()

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        create_star_spawner(self.ecs_world,self.starfield_cfg,self.window_cfg['size']['w'])


    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False



    def _update(self):
        self.ecs_world._clear_dead_entities()
        system_star_spawner(self.ecs_world)
        system_movement_star(self.ecs_world,self.delta_time,self.window_cfg['size']['h'], self.starfield_cfg["vertical_speed"]["min"],self.starfield_cfg["vertical_speed"]["max"])

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering_star(self.ecs_world,self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()




    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/starfield.json", encoding="utf-8") as window_file:
            self.starfield_cfg = json.load(window_file )   