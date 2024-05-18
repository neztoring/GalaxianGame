import random

import pygame

class CStarSpawner:
    def __init__(self, spawn_events_data:dict,screen_width:str,screen_height:str) -> None:
        self.spawn_event_data:list[SpawnEventData] = []
        for x in range(spawn_events_data["number_of_stars"]):
            self.spawn_event_data.append(SpawnEventData(spawn_events_data,screen_width,screen_height))

class SpawnEventData:
    def __init__(self, event_data:dict,screen_width:str,screen_height:str) -> None:
        colors = random.choice(event_data["star_colors"])
        self.color =  pygame.Color(colors['r'],colors['g'],colors['b'])
        self.position = pygame.Vector2(random.randint(0, screen_width),random.randint(0, screen_height))
        self.velocity =  pygame.Vector2(event_data["vertical_speed"]["min"], event_data["vertical_speed"]["max"])
        self.generated = False
        self.blink_rate = random.uniform(event_data["blink_rate"]["min"], event_data["blink_rate"]["max"])
        
