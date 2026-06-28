from ._base import BasePayload
from ..snapshot import GameSnapshot, PlayerSnapshot
from attrs import define

@define(kw_only=True)
class ExportGameSnapshotPayload(BasePayload):

    snapshot: GameSnapshot
    

@define(kw_only=True)
class ExportPlayerSnapshotPayload(BasePayload):

    snapshots: tuple[PlayerSnapshot,...]
    
