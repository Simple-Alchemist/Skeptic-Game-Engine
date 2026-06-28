from typing import TYPE_CHECKING

from attrs import define,field

if TYPE_CHECKING: 
    from ...session import Session

from ...data_classes import Result, ActionType,  GameSnapshot, PlayerSnapshot
from ..interface import AboveGameCommand

@define(kw_only=True)
class ImportGameSnapshotCommand(AboveGameCommand):

    _game_snapshot: GameSnapshot 

    def execute(self, session: 'Session') -> Result:

        session.import_game_snapshot(self._game_snapshot)

        return Result(
            action_type=ActionType.IMPORT_GAME,
            is_success=True
            )

@define(kw_only=True) 
class ImportPlayerSnapshotCommand(AboveGameCommand): 
    
    _player_snapshots: tuple[PlayerSnapshot,...] 


    def execute(self, session: 'Session') -> Result: 
        
        session.import_players_snapshot(player_snaps=self._player_snapshots)

        return Result(
            action_type=ActionType.IMPORT_PLAYERS, 
            is_success=True
            )