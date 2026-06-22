from typing import TYPE_CHECKING, override

from attrs import define,field

if TYPE_CHECKING: 
    from ....session import Session

from ...interface import ItemCommandInterface
from .....core import ItemType
from ....data_classes import Result, ActionType, ShellPayload

@define(kw_only=True)
class PeekItemCommand(ItemCommandInterface):

    _item_type: ItemType = field(default=ItemType.PEEK_SHOTGUN,repr=False, init=False)

    @property
    @override 
    def item_type(self) -> ItemType:
        return self._item_type
    
    def execute(self, session: 'Session') -> Result:
        
        loaded_shell_damage = session.shotgun.current_loaded_shell().damage
        
        return Result(
            action_type=ActionType.USE_ITEM,
            is_success=True,
            payload=ShellPayload(item_type=self._item_type,shell_damage=loaded_shell_damage)
        )