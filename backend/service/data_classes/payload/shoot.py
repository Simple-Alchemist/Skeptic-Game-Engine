from ._base import BasePayload
from attrs import define

@define(kw_only=True,frozen=True)
class ShootPayload(BasePayload):
    
    damage_dealt: int
    shooter_id: int
    target_id: int
    advance_turn: bool


