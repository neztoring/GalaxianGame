import random
import esper
from src.ecs.components.Tags.c_tag_star import CTagStar
from src.ecs.components.Tags.c_tag_text_mov import CTagTextMov
from src.ecs.components.c_moving_text import CMovingText
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_movement_text(world:esper.World, delta_time:float,screen_h:str):

    components = world.get_components(CTransform,CVelocity,CSurface,CMovingText)

    c_t:CTransform
    c_v:CVelocity
    for entity, (c_t,c_v,_,c_mt) in components:
        direction = 0 
        if c_mt.pos_ini.y < c_mt.pos_fin.y  and c_mt.pos_fin.x == c_mt.pos_ini.x:
            direction = 1
        elif c_mt.pos_fin.y < c_mt.pos_ini.y and c_mt.pos_fin.x == c_mt.pos_ini.x:
            direction = 2


        if direction == 0:
            c_v.vel.y = 0

        if direction == 1:
            if c_v.vel.y > 0 :
                c_t.pos.y += c_v.vel.y * delta_time 
                if  c_t.pos.y >= c_mt.pos_fin.y:
                    c_v.vel.y = 0

        if direction == 2:
            if c_v.vel.y > 0 :
                c_t.pos.y -= c_v.vel.y * delta_time 
                if  c_t.pos.y <= c_mt.pos_fin.y:
                    c_v.vel.y = 0

       