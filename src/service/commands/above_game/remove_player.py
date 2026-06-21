from typing import TYPE_CHECKING

from attrs import define,field

if TYPE_CHECKING: 
    from ...session import Session

from ...data_classes import Result, ActionType
from ....core import Player
from ..interface import AboveGameCommand

@define(kw_only=True)
class RemovePlayerCommand(AboveGameCommand):

    _id: int = field(alias="id")

    def execute(self, session: 'Session') -> Result:

        session.player_turn_manager.remove_player(player_id=self._id)

        return Result(

            action_type= ActionType.ADD_PLAYER,
            is_success=True,
            )