from typing import TYPE_CHECKING, override

from attrs import define, field

if TYPE_CHECKING: 
    from ....session import Session

from ....data_classes import Result, ActionType
from ....data_classes.payload.u_turn import UTurnPayload
from ...interface import ItemCommandInterface
from .....core import ItemType


@define(kw_only=True)
class UTurnItemCommand(ItemCommandInterface):

    _item_type: ItemType = field(default=ItemType.U_TURN,repr=False, init=False)

    @property
    @override 
    def item_type(self) -> ItemType: 
         return self._item_type
    
    def execute(self, session: 'Session') -> Result:
        
        session.player_turn_manager.reverse_order()

        return Result(

            action_type=ActionType.USE_ITEM,
            is_success=True,
            payload=UTurnPayload(direction=session.player_turn_manager.direction)
        )