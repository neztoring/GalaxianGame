import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface

def system_animation(ecs_world: esper.World, delta_time:float):
    components = ecs_world.get_components(CSurface, CAnimation)
    for _, (c_surface, c_animation) in components:
        c_animation.current_animation_time -= delta_time
        if c_animation.current_animation_time <= 0 and c_animation.curr_anim < len(c_animation.animation_list):
            c_animation.current_animation_time = c_animation.animation_list[c_animation.curr_anim].framerate
            c_animation.curr_frame += 1
            if c_animation.curr_frame > c_animation.animation_list[c_animation.curr_anim].end:
                c_animation.curr_frame = c_animation.animation_list[c_animation.curr_anim].start
            rect_surf = c_surface.surf.get_rect()
            c_surface.area.w = rect_surf.w / c_animation.number_frames
            c_surface.area.x = c_surface.area.w * c_animation.curr_frame
            