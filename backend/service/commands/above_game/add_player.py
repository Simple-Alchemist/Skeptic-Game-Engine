from typing import TYPE_CHECKING

from attrs import define,field

if TYPE_CHECKING: 
    from ...session import Session

from ...data_classes import Result, ActionType
from ....core import Player
from ..interface import AboveGameCommand

@define(kw_only=True)
class AddPlayerCommand(AboveGameCommand):

    _id: int = field(alias="id")
    _health: int = field(alias="health")
    _inventory_limit: int = field(alias="inventory_limit")

    def execute(self, session: 'Session') -> Result:

        session.player_turn_manager.add_player(

            player_obj=Player(

                id=self._id, 
                health=self._health, 
                inventory_limit=self._inventory_limit)
            )

        return Result(

            action_type= ActionType.ADD_PLAYER,
            is_success=True,

        )