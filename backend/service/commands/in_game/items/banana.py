from typing import TYPE_CHECKING, override

if TYPE_CHECKING: 
    from ....session import Session
    
from attrs import define, field

from ....data_classes import Result, ActionType, BananaPayload
from ...interface import ItemCommandInterface

from .....core import  ItemType

@define(kw_only=True)
class BananaItemCommand(ItemCommandInterface):

    _item_type: ItemType = field(init=False, default=ItemType.BANANA, repr=False)

    @property
    @override
    def item_type(self) -> ItemType:
        return self._item_type

    def execute(self, session: 'Session') -> Result:
        
        current_player = session.player_turn_manager.current_player
        
        initial_health = current_player.health
        current_player.adjust_health(points=+1)
        final_health = current_player.health
        
        return Result(
            
                action_type=ActionType.USE_ITEM,
                is_success=True,
                payload=BananaPayload(initial_health=initial_health, final_health=final_health)
            )