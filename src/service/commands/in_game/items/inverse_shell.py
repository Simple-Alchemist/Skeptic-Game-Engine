from typing import TYPE_CHECKING, override

if TYPE_CHECKING: 
    from ....session import Session

from attrs import define,field

from ...interface import ItemCommandInterface
from ....data_classes import Result, ActionType, InversePayload
from .....core import LiveShell, BlankShell, ItemType

@define(kw_only=True)
class InverseShellItemCommand(ItemCommandInterface):

    _item_type: ItemType = field(default=ItemType.INVERSE_SHELL,repr=False, init=False)

    @property
    @override 
    def item_type(self) -> ItemType:
        return self._item_type
    
    def execute(self, session: 'Session') -> Result:

        shotgun = session.shotgun
        
        previous_shell = shotgun.unload_shell()

        new_shell = BlankShell() if previous_shell.damage >= 1 else LiveShell() 

        shotgun.load_shells((new_shell,))


        return Result(

            action_type=ActionType.USE_ITEM,
            is_success=True,
            payload=InversePayload(item_type=self._item_type, previous_shell_damage=previous_shell.damage, new_shell_damage=new_shell.damage)
          
        )

        