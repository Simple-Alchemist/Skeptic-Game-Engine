from typing import TYPE_CHECKING, override

if TYPE_CHECKING: 
    from ....session import Session

from attrs import define, field

from ....data_classes import Result, ActionType, ErrorType, HandCuffPayload
from ...interface import TargetPlayerCommandInterface, ItemCommandInterface
from .....core import ItemType 

@define(kw_only=True)
class HandCuffItemCommand(ItemCommandInterface, TargetPlayerCommandInterface): 
    #this item demands a lot

    _target_player_id: int = field(alias="target_player_id")
    _item_type: ItemType = field(init=False, default=ItemType.HAND_CUFF, repr=False)

    @property
    @override 
    def item_type(self) -> ItemType:
        return self._item_type
    
    @property
    @override 
    def target_player_id(self) -> int: 
        return self._target_player_id
    
    def execute(self, session: 'Session') -> Result:
        
        current_player = session.player_turn_manager.current_player

        if self._target_player_id == current_player.id:
            
            return Result(
                action_type=ActionType.USE_ITEM,
                is_success=False,
                error_type=ErrorType.HAND_CUFFING_YOURSELF
            )
        
        targeted_player = session.player_turn_manager.get_player(self._target_player_id)

        if targeted_player.is_cuffed:

            return Result(
                action_type=ActionType.USE_ITEM,
                is_success=False,
                error_type=ErrorType.ALREADY_CUFFED
            )
            
        targeted_player.hand_cuff() 

        return Result(

            action_type=ActionType.USE_ITEM,
            is_success=True,
            payload=HandCuffPayload(
                user_id = current_player.id,
                target_id=self._target_player_id)

            )

        