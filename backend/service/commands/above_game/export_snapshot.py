from typing import TYPE_CHECKING

from attrs import define

if TYPE_CHECKING: 
    from ...session import Session

from ...data_classes import Result, ActionType, ExportGameSnapshotPayload, ExportPlayerSnapshotPayload
from ..interface import AboveGameCommand

@define(kw_only=True)
class ExportGameSnapshotCommand(AboveGameCommand):


    def execute(self, session: 'Session') -> Result:

       game_snapshot = session.export_game_snapshot()

       return Result(
           action_type=ActionType.EXPORT_GAME,
           is_success=True,
           payload=ExportGameSnapshotPayload(snapshot=game_snapshot)
       )

@define(kw_only=True) 
class ExportPlayerSnapshotCommand(AboveGameCommand): 

    player_ids: tuple[int,...] 

    def execute(self, session: 'Session') -> Result: 
        
        player_snapshots = session.export_players_snapshot(player_ids=self.player_ids)

        return Result(
            action_type=ActionType.EXPORT_PLAYERS, 
            is_success=True, 
            payload=ExportPlayerSnapshotPayload(snapshots=player_snapshots)
            )