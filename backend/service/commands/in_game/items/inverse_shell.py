from typing import TYPE_CHECKING, override
from random import randint 

if TYPE_CHECKING: 
    from ....session import Session

from attrs import define,field

from ...interface import ItemCommandInterface
from ....data_classes import Result, ActionType, InversePayload
from .....core import LiveShell, BlankShell, ShellInterface, ItemType

@define(kw_only=True)
class RandomInverseShellItemCommand(ItemCommandInterface):

    _item_type: ItemType = field(default=ItemType.INVERSE_SHELL,repr=False, init=False)

    @property
    @override 
    def item_type(self) -> ItemType:
        return self._item_type
    
    def execute(self, session: 'Session') -> Result:

        shotgun = session.shotgun

        random_pointer: int = randint(0, shotgun.mag_size-1)

        random_shell = shotgun.get_shell(position=random_pointer)

        new_shell = BlankShell() if random_shell.damage >= 1 else LiveShell() 

        shotgun.replace_shell(position=random_pointer, shell=new_shell) 


        return Result(

            action_type=ActionType.USE_ITEM,
            is_success=True,
            payload=InversePayload(damage_before_inversion=random_shell.damage,damage_after_inversion=new_shell.damage)
          
        )

        