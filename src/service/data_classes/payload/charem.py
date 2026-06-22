from .base import ItemBasePayload
from ....core import ItemType
from attrs import define

@define(kw_only=True)
class CharemPayload(ItemBasePayload):

    item_type: ItemType = ItemType.CHAREM
