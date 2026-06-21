from .interface import ItemPayloadInterface
from ....core import ItemType
from attrs import define

@define(kw_only=True)
class BaistaDaustoPayload(ItemPayloadInterface):

    item_type: ItemType = ItemType.BAISTA_DAUSTO
    
   
