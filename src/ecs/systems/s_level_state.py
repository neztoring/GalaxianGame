import esper
from src.ecs.components.Tags.c_tag_enemy import CTagEnemy
from src.ecs.components.Tags.c_tag_player import CTagPlayer
from src.ecs.components.c_level_state import CLevelState, LevelState

def system_level_state(world: esper.World, level_entity: int, current_time:float, player_conf: dict):
    c_ls = world.component_for_entity(level_entity, CLevelState)
    
    player = world.get_components(CTagPlayer)
    enemies = world.get_components(CTagEnemy)

    if(c_ls.state==LevelState.READY and current_time>player_conf["time_recover"]):
        c_ls.state=LevelState.READY_DONE
    if(c_ls.state==LevelState.PLAY_TIME and player.__len__()==0):
        c_ls.state=LevelState.GAME_OVER
    if(c_ls.state==LevelState.PLAY_TIME and enemies.__len__()==44):
        c_ls.state=LevelState.LEVEL_ACHIEVED