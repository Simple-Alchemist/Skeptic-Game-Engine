from .interface import PayLoadInterface
from attrs import define

@define(kw_only=True)
class ShootPayload(PayLoadInterface):
    damage_dealt: int  