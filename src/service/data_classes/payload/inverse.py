from .base import ItemBasePayload
from ....core import ItemType
from attrs import define

@define(kw_only=True)
class InversePayload(ItemBasePayload):
    
    item_type: ItemType = ItemType.INVERSE_SHELL
    previous_shell_damage: int 
    new_shell_damage: int 
