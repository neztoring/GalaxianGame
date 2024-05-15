import esper, pygame
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.engine.service_locator import ServiceLocator


def system_player_state(world: esper.World, player_cfg: dict):
    components = world.get_component(CPlayerState)
    for player_entity, (c_pst) in components:
        if c_pst.state == PlayerState.IDLE:
            _do_idle_state(c_pst)
        if c_pst.state == PlayerState.DEAD:
            _do_dead_state(c_pst)
        if c_pst.state == PlayerState.GAME_OVER:
            _do_game_over_state(world, player_entity, player_cfg)

def _do_idle_state(c_pst: CPlayerState):
    c_pst.state = PlayerState.ALIVE


def _do_dead_state(c_pst: CPlayerState):
    c_pst.state = PlayerState.GAME_OVER

def _do_game_over_state(world: esper.World, player_entity:int, player_cfg: dict):
    create_text(world, "GAME OVER", 8, pygame.Color(255, 255, 255), pygame.Vector2(128, 120), TextAlignment.CENTER, 0)
    ServiceLocator.sounds_service.play(player_cfg["sound_over"])
    world.delete_entity(player_entity)