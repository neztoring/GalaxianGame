import esper, random
from src.create.prefab_creator import create_enemy_bullet
from src.ecs.components.Tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform

def _calculate_time_to_fire(current_time: float, last_fire: float, time_fire: int):
    return current_time - last_fire > time_fire

def system_enemy_fire(world: esper.World, delta_time: float, bullet_conf: dict):
    min_time_fire = bullet_conf["min_time_fire"]
    max_time_fire = bullet_conf["max_time_fire"]
    time_fire = random.uniform(min_time_fire, max_time_fire)
    components_enemy = world.get_components(CSurface, CTransform, CTagEnemy)

    list_enemies = []

    for enemy_entity, (_, _, _) in components_enemy:
        list_enemies.append(enemy_entity)

    if len(list_enemies) > 0:
        random_starship = random.choice(list_enemies)

        c_s: CSurface
        c_t: CTransform
        for enemy_entity, (c_s, c_t, c_e) in components_enemy:
            c_e.current_time += delta_time
            if _calculate_time_to_fire(c_e.current_time, c_e.time_last_fire, time_fire):
                c_e.time_last_fire = c_e.current_time
                if enemy_entity == random_starship:
                    create_enemy_bullet(world, c_t.pos, c_s.surf.get_rect(), bullet_conf)
                    return

