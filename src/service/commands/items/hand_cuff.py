

from attrs import define, field

from ...session import Session
from ...data_classes import ActionResult, ActionType, ErrorType
from interface import CommandInterface
from core import ItemException,ItemType 

@define(kw_only=True)
class HandCuffItemCommand(CommandInterface):

    _target_id: int = field(alias="target_id")
    _item_type: ItemType = field(init=False, default=ItemType.HAND_CUFF, repr=False)

    
    def execute(self, session: Session) -> ActionResult:
        
        current_player = session.player_turn_manager.current_player

        if not current_player.inventory.is_item_present(item=self._item_type): 

            return ActionResult(
                action_type=ActionType.HAND_CUFF_PLAYER,
                is_success=False,
                error_type=ErrorType.ITEM_NOT_IN_INVENTORY
            )
        
        if self._target_id == current_player.id:
            
            return ActionResult(
                action_type=ActionType.HAND_CUFF_PLAYER,
                is_success=False,
                error_type=ErrorType.HAND_CUFFING_YOURSELF
            )
        
        if not session.player_turn_manager.is_player_in_order(player_id=self._target_id): 

            return ActionResult(
                action_type=ActionType.HAND_CUFF_PLAYER,
                is_success=False,
                error_type=ErrorType.UNKNOWN_PLAYER
            )
        
        targeted_player = session.player_turn_manager.get_player(self._target_id)

        if targeted_player.is_cuffed:

            return ActionResult(
                action_type=ActionType.HAND_CUFF_PLAYER,
                is_success=False,
                error_type=ErrorType.ALREADY_CUFFED
            )
            
        targeted_player.hand_cuff() 

        current_player.inventory.remove_item(item=self._item_type)

        return ActionResult(

            action_type=ActionType.HAND_CUFF_PLAYER,
            is_success=True,
            # pay load code to be written
            )

        