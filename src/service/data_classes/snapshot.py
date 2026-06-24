from typing import TYPE_CHECKING
from attrs import define


if TYPE_CHECKING:
    from ..data_classes import States   
from ...core import ItemType

@define(kw_only=True,frozen=True)
class PlayerSnapshot: 

    id: int 
    health: int 
    inventory: tuple[ItemType,...]
    is_cuffed: bool

@define(kw_only=True,frozen=True)
class TurnSnapshot:
    current_player_id: int 
    direction: int
    pointer: int

@define(kw_only=True, frozen=True)
class ShotgunSnapshot: 
    lives: int 
    blanks: int

@define(kw_only=True, frozen=True)
class GameSnapshot:
    
    current_state_name: "States" 
    turn_data: TurnSnapshot
    player_datas: tuple[PlayerSnapshot,...] 
    shotgun_data: ShotgunSnapshot
   




