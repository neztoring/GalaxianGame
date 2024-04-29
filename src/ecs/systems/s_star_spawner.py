import esper

from src.create.prefab_creator import create_star
from src.ecs.components.c_star_spawner import CStarSpawner, SpawnEventData

def system_star_spawner(world:esper.World):
    components = world.get_component(CStarSpawner)
    c_spw:CStarSpawner
    for _,  c_spw in components:
        spw_evt:SpawnEventData
        for spw_evt in c_spw.spawn_event_data:
                if spw_evt.generated == False:
                    create_star(world,spw_evt.position,spw_evt.color,spw_evt.velocity,spw_evt.blink_rate)
                spw_evt.generated = True    
    