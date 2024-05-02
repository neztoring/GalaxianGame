
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform



def system_blink(world:esper.World, delta_time:float):

    components = world.get_components(CTransform,CSurface)

    c_s:CSurface
    for entity, (_,c_s) in components:
          if c_s.blink_rate>0 :
               c_s.timer+=delta_time
               if c_s.timer >= c_s.blink_rate :
                    c_s.timer = 0
                    c_s.visible = not c_s.visible 
          