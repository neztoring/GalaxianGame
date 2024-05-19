import esper, pygame
from src.ecs.components.Tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_movement_player_bullet(world: esper.World, delta_time: float):

    components = world.get_components(CTransform, CVelocity,CTagPlayerBullet)

    c_t: CTransform
    c_v: CVelocity
    for entity, (c_t, c_v,_) in components:
        c_t.pos.x += c_v.vel.x * delta_time
        c_t.pos.y += c_v.vel.y * delta_time
