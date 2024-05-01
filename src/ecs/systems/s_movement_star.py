import random
import esper
from src.ecs.components.Tags.c_tag_star import CTagStar
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_movement_star(world:esper.World, delta_time:float,screen_h:str, vel_mix:str, vel_max:str):

    components = world.get_components(CTransform,CVelocity,CSurface,CTagStar)

    c_t:CTransform
    c_v:CVelocity
    for entity, (c_t,c_v,_,_) in components:
        c_t.pos.y += c_v.vel.y * delta_time
        if  c_t.pos.y> screen_h:
             c_t.pos.y = random.randint(-100, -10) 
             c_t.pos.x = random.randint(0, screen_h)
             c_v.vel.y = random.randint(vel_mix,vel_max) 
        #c_s.timer+=delta_time
        #if c_s.blink_rate>0 and c_s.timer >= c_s.blink_rate :
        #     c_s.timer = 0
        #     c_s.visible = not c_s.visible 
       