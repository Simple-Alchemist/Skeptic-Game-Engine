from ._base import ItemBasePayload
from ....core import ItemType
from attrs import define

@define(kw_only=True)
class UTurnPayload(ItemBasePayload):

    item_type: ItemType = ItemType.U_TURN
    direction: int