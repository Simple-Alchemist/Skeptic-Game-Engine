from attrs import define, field

from ...session import Session
from interface import CommandInterface
from ....core import ItemType, ItemException
from ...data_classes import ActionResult, ActionType, ErrorType, ShellLoadedPayload

@define(kw_only=True)
class PeekItemCommand(CommandInterface):

    _item_type: ItemType = field(init=False, default=ItemType.PEEK_SHOTGUN, repr=False)


    
    def execute(self, session: Session) -> ActionResult:
        
        current_player = session.player_turn_manager.current_player
        
        if not current_player.inventory.is_item_present(item=self._item_type): 

            raise ItemException(f"{self._item_type} is not present in {current_player.id}'s inventory")
        
        if session.shotgun.is_magazine_empty:
            return ActionResult(
                action_type=ActionType.PEEK_LOADED_SHELL,
                is_success=False,
                error_type=ErrorType.EMPTY_MAGAZINE
            )
        loaded_shell_damage = session.shotgun.current_loaded_shell().damage
        
        if not current_player.inventory.is_item_present(item=self._item_type): 

            return ActionResult(
                action_type=ActionType.PEEK_LOADED_SHELL,
                is_success=False,
                error_type=ErrorType.ITEM_NOT_IN_INVENTORY
            )
        current_player.inventory.remove_item(item=self._item_type)

        return ActionResult(
            action_type=ActionType.PEEK_LOADED_SHELL,
            is_success=True,
            payload=ShellLoadedPayload(shell_loaded_damage=loaded_shell_damage)
        )