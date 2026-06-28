from ._base import ItemBasePayload
from ....core import ItemType
from attrs import define

@define(kw_only=True)
class BananaPayload(ItemBasePayload):

    item_type: ItemType = ItemType.BANANA
    initial_health: int 
    final_health: int
