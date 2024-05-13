import esper
import pygame

from src.engine.service_locator import ServiceLocator
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.c_surface import CSurface

def system_rendering_debug(world:esper.World, screen:pygame.Surface):
    fnt = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 2)
    debug_font:pygame.Surface = fnt.render("DEBUG_VIEW: RECTS", False, pygame.Color(255, 100, 100))
    pos = pygame.Vector2(20, 20)
    screen.blit(debug_font, pos)

    components = world.get_components(CTransform, CSurface)
    for _, (c_t, c_s) in components:
        if not c_s.visible:
            continue
        
        final_rect = pygame.Rect(c_t.pos, c_s.area.size)
        pygame.draw.rect(screen, pygame.Color(10, 255, 10), final_rect, 1, 2)
        pygame.draw.circle(screen, pygame.Color(255, 255, 255), final_rect.topleft, 2, 2)