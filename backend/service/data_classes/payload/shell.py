from .base import ItemBasePayload
from ....core import ItemType
from attrs import define

@define(kw_only=True)
class ShellPayload(ItemBasePayload):
    
    item_type: ItemType
    shell_damage: int
