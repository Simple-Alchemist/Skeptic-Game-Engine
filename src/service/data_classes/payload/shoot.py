from .base import BasePayload
from attrs import define

@define(kw_only=True)
class ShootPayload(BasePayload):
    damage_dealt: int
    advance_turn: bool