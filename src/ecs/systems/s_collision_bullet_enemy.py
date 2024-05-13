import pygame
import esper

from src.ecs.components.Tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.Tags.c_tag_score import CTagScore
from src.ecs.components.c_changing_text import CChangingText
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.Tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator

def system_collision_bullet_enemy(world: esper.World):

    enemies_components = world.get_components(CSurface, CTransform, CTagEnemy)
    bullet_components = world.get_components(CSurface, CTransform, CTagPlayerBullet)
    score_label = world.get_components(CChangingText, CTagScore, CSurface, CTransform)
    
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 8)
    e_s: CSurface
    e_t: CTransform
    c_c: CChangingText
    c_ts: CTagScore
    c_s: CSurface
    c_t: CTransform
    
    for enemy_entity, (e_s, e_t, e_te) in enemies_components:
        enemy_rect = CSurface.get_area_relative(e_s.area, e_t.pos)
        for bullet_entity, (b_s, b_t, _) in bullet_components:
            bullet_rect = b_s.surf.get_rect(topleft = b_t.pos)
            if enemy_rect.colliderect(bullet_rect):
                for entity, (c_c, c_ts, c_s, c_t) in score_label:
                    old_area= c_s.surf.get_rect().topright[0]
                    c_ts.score+=e_te.score
                    c_c.text=str(c_ts.score)
                    c_s.surf=CSurface.from_text(c_c.text, font, c_s.color, c_s.blink_rate)
                    c_s.area = c_s.surf.surf.get_rect()

                    print(c_t.pos, " ", c_s.area.width)

                    origin = pygame.Vector2(0, 0)
                    origin.x -= c_s.area.width-old_area
                    c_t.pos=c_t.pos + origin

                world.delete_entity(bullet_entity)
                world.delete_entity(enemy_entity)