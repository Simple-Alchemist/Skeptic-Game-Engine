from attrs import define, field

from ...session import Session
from ...data_classes import ActionResult, ActionType, ErrorType, ShellLoadedPayload
from ..interface import CommandInterface
from ....core import ShellInterface, ItemType


@define(kw_only=True)
class TwoFoldItemCommand(CommandInterface):

    _item_type: ItemType = field(init=False, default=ItemType.TWO_FOLD, repr=False)
    
    def execute(self, session: Session) -> ActionResult:
        
        current_player = session.player_turn_manager.current_player

        if session.shotgun.is_magazine_empty():
           
           return ActionResult(

                    action_type=ActionType.LOADING_DOUBLE_DAMAGE_SHELL,
                    is_success=False,
                    error_type=ErrorType.EMPTY_MAGAZINE
                    )
        
        if session.shotgun.current_loaded_shell().damage >= 1: 
                session.shotgun.unload_shell()
                session.shotgun.load_shells([DoubleLiveShell()])

        if not current_player.inventory.is_item_present(item=self._item_type): 
             return ActionResult( 
                  action_type=ActionType.LOADING_DOUBLE_DAMAGE_SHELL,
                  is_success=False,
                  error_type=ErrorType.ITEM_NOT_IN_INVENTORY
             )
             
        current_player.inventory.remove_item(item=self._item_type)

        return ActionResult(

            action_type=ActionType.LOADING_DOUBLE_DAMAGE_SHELL,
            is_success=True,
            payload=ShellLoadedPayload(shell_loaded_damage=session.shotgun.current_loaded_shell().damage)
            # in the payload, show the previous shell 
        )
    
@define(kw_only=True, frozen=True)
class DoubleLiveShell(ShellInterface):

    _damage: int = field(default=2, init=False)

    @property 
    def damage(self) -> int:
        return self._damage
    
