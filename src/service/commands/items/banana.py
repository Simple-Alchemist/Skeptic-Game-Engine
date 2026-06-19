from attrs import define, field

from ...session import Session
from ...data_classes import ActionResult, ActionType, ErrorType
from interface import CommandInterface

from ....core import  ItemType

@define(kw_only=True)
class BananaItemCommand(CommandInterface):

    _item_type: ItemType = field(init=False, default=ItemType.BANANA, repr=False)

    def execute(self, session: Session) -> ActionResult:
        
        current_player = session.player_turn_manager.current_player

        if not current_player.inventory.is_item_present(item=self._item_type): 

            return ActionResult(
                action_type=ActionType.EATING_BANANA,
                is_success=False,
                error_type=ErrorType.ITEM_NOT_IN_INVENTORY
            )

        current_player.adjust_health(points=+1)
        
        current_player.inventory.remove_item(item=self._item_type)

        return ActionResult(
                action_type=ActionType.EATING_BANANA,
                is_success=True,
                # might need a payload for comparision reason I guess? (or I might be thinking too much)
            )