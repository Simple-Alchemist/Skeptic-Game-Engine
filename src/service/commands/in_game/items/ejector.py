from typing import TYPE_CHECKING, override

if TYPE_CHECKING: 
    from ....session import Session

from attrs import define, field

from ...interface import ItemCommandInterface
from ....data_classes import Result, ActionType,  ShellPayload
from .....core import ItemType

@define(kw_only=True)
class EjectorItemCommand(ItemCommandInterface):

    _item_type: ItemType = field(default=ItemType.EJECTOR,repr=False, init=False)

    @property
    @override 
    def item_type(self) -> ItemType:
        return self._item_type
    

    def execute(self, session: 'Session') -> Result:
        
        shotgun = session.shotgun
        ejected_shell_damage = shotgun.unload_shell().damage
   
        return Result(

            action_type=ActionType.USE_ITEM,
            is_success=True,
            payload=ShellPayload(item_type=self._item_type,shell_damage=ejected_shell_damage)
           
        )