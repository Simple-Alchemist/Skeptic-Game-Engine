from attrs import define, field

from ..core import Shotgun, PlayerTurnManager

@define(kw_only=True)
class Session:
    
    player_turn_manager: PlayerTurnManager = field(factory=PlayerTurnManager)
    shotgun: Shotgun = field(factory=Shotgun)

    