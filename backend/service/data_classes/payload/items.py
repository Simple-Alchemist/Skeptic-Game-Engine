from ._base import ItemBasePayload
from ....core import ItemType
from attrs import define

@define(kw_only=True)
class UTurnPayload(ItemBasePayload):

    item_type: ItemType = ItemType.U_TURN
    direction: int


@define(kw_only=True)
class ShellPayload(ItemBasePayload):
    
    item_type: ItemType
    shell_damage: int


@define(kw_only=True)
class InversePayload(ItemBasePayload):
    
    item_type: ItemType = ItemType.INVERSE_SHELL
    damage_before_inversion: int  
    damage_after_inversion: int  

@define(kw_only=True)
class HandCuffPayload(ItemBasePayload):

    item_type: ItemType = ItemType.HAND_CUFF
    user_id: int
    target_id: int

@define(kw_only=True)
class CharemPayload(ItemBasePayload):

    item_type: ItemType = ItemType.CHAREM
    polnareff_id: int
    victim_id: int

@define(kw_only=True)
class BananaPayload(ItemBasePayload):

    item_type: ItemType = ItemType.BANANA
    initial_health: int 
    final_health: int

@define(kw_only=True)
class BaistaDaustoPayload(ItemBasePayload):

    item_type: ItemType = ItemType.BAISTA_DAUSTO
    yoshikage_id: int
    target_id: int
    total_leap_back: int 
    
   
