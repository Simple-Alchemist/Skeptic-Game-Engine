from .base import ItemBasePayload
from ....core import ItemType
from attrs import define

@define(kw_only=True)
class HandCuffPayload(ItemBasePayload):

    item_type: ItemType = ItemType.HAND_CUFF
    target_id : int
