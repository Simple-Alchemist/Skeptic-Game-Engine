from ._base import ItemBasePayload
from ....core import ItemType
from attrs import define

@define(kw_only=True)
class InversePayload(ItemBasePayload):
    
    item_type: ItemType = ItemType.INVERSE_SHELL
    damage_before_inversion: int  
    damage_after_inversion: int  