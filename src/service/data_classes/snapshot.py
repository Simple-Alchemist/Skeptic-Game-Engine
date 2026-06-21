
from attrs import define, field

from ..data_classes import States
from ...core import ItemType, ShellInterface

@define(kw_only=True)
class PlayerSnapshot: 

    id: int 
    health: int 
    inventory: tuple[ItemType,...]
    is_cuffed: bool

@define(kw_only=True, frozen=True)
class GameSnapshot:
    
    current_state_name: States 
    current_player_id: int 
    turn_order_direction: int
    turn_pointer: int
    player_data: tuple[PlayerSnapshot,...] = field(factory=tuple)  
    magazine: tuple[ShellInterface, ...] = field(factory=tuple)
   




