from enum import Enum
import pygame
import esper

from src.ecs.components.Tags.c_tag_score import CTagScore
from src.ecs.components.c_changing_text import CChangingText
from src.ecs.components.c_surface import CSurface

from src.ecs.components.c_trasform import CTransform
from src.engine.service_locator import ServiceLocator

class TextAlignment(Enum):
    LEFT = 0,
    RIGHT = 1
    CENTER = 2

def create_text(world:esper.World, txt:str, size:int, 
                color:pygame.Color, pos:pygame.Vector2, alignment:TextAlignment,blink_rate:float) -> int:
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(txt, font, color,blink_rate))
    txt_s = world.component_for_entity(text_entity, CSurface)

    # De acuerdo al alineamiento, determia el origine de la superficie
    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx

    world.add_component(text_entity,
                        CTransform(pos + origin))
    return text_entity

def create_text_score(world:esper.World, txt:str, size:int, 
                      color:pygame.Color, pos:pygame.Vector2, alignment:TextAlignment,blink_rate:float) -> int:
    text_entity=create_text(world,txt, size, color, pos, alignment, blink_rate)
    world.add_component(text_entity, CChangingText(txt, ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", size)))
    world.add_component(text_entity, CTagScore(int(txt)))
    return text_entity
