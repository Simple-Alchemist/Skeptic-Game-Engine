from .base import ItemBasePayload
from ....core import ItemType
from attrs import define

@define(kw_only=True)
class BaistaDaustoPayload(ItemBasePayload):

    item_type: ItemType = ItemType.BAISTA_DAUSTO
    target_id: int
    total_leap_back: int 
    
   
