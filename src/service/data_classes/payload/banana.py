from .interface import ItemPayloadInterface
from ....core import ItemType
from attrs import define

@define(kw_only=True)
class BananaPayload(ItemPayloadInterface):

    item_type: ItemType = ItemType.BANANA
    initial_health: int 
    final_health: int
    ... # code to be written
