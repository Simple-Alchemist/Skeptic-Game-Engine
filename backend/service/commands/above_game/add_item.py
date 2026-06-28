from typing import TYPE_CHECKING

from attrs import define,field

if TYPE_CHECKING: 
    from ...session import Session

from ...data_classes import Result, ActionType, ErrorType
from ....core import  ItemType
from ..interface import AboveGameCommand

@define(kw_only=True)
class AddItemCommand(AboveGameCommand):

    _player_id: int = field(alias="player_id")
    _items: tuple[ItemType,...] = field(alias="items")

    def execute(self, session: 'Session') -> Result:

        if not session.player_turn_manager.is_player_in_order(player_id=self._player_id):
            return Result(

                action_type= ActionType.ADD_ITEM,
                is_success=False,
                error_type=ErrorType.UNKNOWN_PLAYER
                #Adding a Pay load stating what is being added
                )

        target_player = session.player_turn_manager.get_player(player_id=self._player_id)

        if target_player.inventory.reached_limit: 
            return Result(

                action_type= ActionType.ADD_ITEM,
                is_success=False,
                error_type=ErrorType.REACHED_INVENTORYS_LIMIT
                )

        target_player.inventory.add_items(self._items)

        return Result(

            action_type= ActionType.ADD_ITEM,
            is_success=True,
            #Adding a Pay load stating what is being added
            )