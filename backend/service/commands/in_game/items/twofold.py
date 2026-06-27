from typing import TYPE_CHECKING, override

from attrs import define, field

if TYPE_CHECKING: 
    from ....session import Session

from ....data_classes import Result, ActionType, ShellPayload
from ...interface import ItemCommandInterface
from .....core import ShellInterface, ItemType


@define(kw_only=True)
class TwoFoldItemCommand(ItemCommandInterface):

    _item_type: ItemType = field(default=ItemType.TWO_FOLD,repr=False, init=False)

    @property
    @override 
    def item_type(self) -> ItemType: 
         return self._item_type
    
    def execute(self, session: 'Session') -> Result:

        if session.shotgun.current_loaded_shell().damage >= 1: 
                session.shotgun.unload_shell()
                session.shotgun.load_shells((DoubleLiveShell(),))
    
        return Result(

            action_type=ActionType.USE_ITEM,
            is_success=True,
            payload=ShellPayload(item_type=self._item_type, shell_damage=session.shotgun.current_loaded_shell().damage)
            # in the payload, show the previous shell 
        )
    
@define(kw_only=True, frozen=True)
class DoubleLiveShell(ShellInterface):

    _damage: int = field(default=2, init=False)

    @property 
    def damage(self) -> int:
        return self._damage
    
