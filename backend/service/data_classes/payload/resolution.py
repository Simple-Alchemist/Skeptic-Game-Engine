from ._base import BasePayload
from attrs import define



@define(kw_only=True,frozen=True)
class ResolutionPayload(BasePayload):
    
    players_removed: tuple[int,...] = tuple()
    players_uncuffed: tuple[int,...] = tuple()
    current_player_id: int
    saved_history: bool = False

