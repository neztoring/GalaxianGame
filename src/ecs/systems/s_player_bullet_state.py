import esper, pygame
from src.create.prefab_creator import spawn_player_bullet
from src.ecs.components.c_player_bullet_state import CPlayerBulletState, PlayerBulletState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_trasform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_player_bullet_state(world: esper.World, player_cfg: dict, player_pos: pygame.Vector2, player_size: pygame.Rect):
    components = world.get_components(CSurface, CTransform, CVelocity, CPlayerBulletState)
    for _, (c_s, c_t, c_v, c_pbst) in components:
        if c_pbst.state == PlayerBulletState.IDLE:
            _do_idle_state(world, c_pbst, player_cfg, player_pos, player_size)
        if c_pbst.state == PlayerBulletState.READY:
            _do_ready_state(c_s, c_t, player_pos, player_size)
        if c_pbst.state == PlayerBulletState.FIRED:
            _do_fired_state(c_v, player_cfg)

def _do_idle_state(world: esper.World, c_pbst: CPlayerBulletState, player_cfg: dict, player_pos: pygame.Vector2, player_size: pygame.Rect):
    spawn_player_bullet(world, player_pos, player_size, player_cfg["bullets"])
    c_pbst.state = PlayerBulletState.READY

def _do_ready_state(c_s: CSurface, c_t: CTransform, player_pos: pygame.Vector2, player_size: pygame.Vector2):
    x_pos = round(player_pos.x + (player_size.w / 2)) -1
    c_t.pos = pygame.Vector2(x_pos, player_pos.y-c_s.area.h + 1)

def _do_fired_state(c_v: CVelocity, player_cfg: dict):
    player_bullet_cfg = player_cfg["bullets"]
    velocity_bullet_cfg = player_bullet_cfg["velocity"]
    c_v.vel = pygame.Vector2(velocity_bullet_cfg["x"], velocity_bullet_cfg["y"])

