from attrs import define

from ....core import ItemType


@define(kw_only=True, frozen=True)
class BasePayload: 

    ...

@define(kw_only=True,frozen=True)
class ItemBasePayload(BasePayload): 

    item_type: ItemType