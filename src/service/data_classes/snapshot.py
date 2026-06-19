from attrs import define, field
from ..session import Session

@define(kw_only=True)
class PlayerSnapshot: 

    id: int 
    health: int 
    inventory: tuple[int,...]
    cuffed: bool

@define(kw_only=True)
class GameSnapshot:
    
    session: Session = field(init=True)
    current_state_name: str = field(init=False)
    current_player_id: int = field(init=False)
    player_data: dict[int, PlayerSnapshot] = field(factory=dict,init=False)  
    magazine: tuple[int, ...] = field(factory=tuple, init=False)#convert bullet's name into it's damage
   




