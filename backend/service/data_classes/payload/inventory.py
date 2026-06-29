from ._base import BasePayload
from attrs import define
from ....core import ItemType


@define(kw_only=True, frozen=True)
class AddItemPayload(BasePayload):
    
    player_id: int
    items_added: tuple[ItemType,...]


@define(kw_only=True,frozen=True)
class RemoveItemPayload(BasePayload):
    
    player_id: int
    items_removed: tuple[ItemType,...]

@define(kw_only=True, frozen=True)
class ItemDistributionPayload(BasePayload): 

    distribution: dict[int, tuple[ItemType,...]] # id: inventory
