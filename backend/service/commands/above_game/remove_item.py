from typing import TYPE_CHECKING

from attrs import define,field

if TYPE_CHECKING: 
    from ...session import Session

from ...data_classes import Result, ActionType, ErrorType
from ....core import  ItemType
from ..interface import AboveGameCommand

@define(kw_only=True)
class RemoveItemCommand(AboveGameCommand):

    _player_id: int = field(alias="player_id")
    _items: tuple[ItemType,...] = field(alias="items")

    def execute(self, session: 'Session') -> Result:

        if not session.player_turn_manager.is_player_in_order(player_id=self._player_id):
            return Result(

                action_type= ActionType.REMOVE_ITEM,
                is_success=False,
                error_type=ErrorType.UNKNOWN_PLAYER
                )

        target_player = session.player_turn_manager.get_player(player_id=self._player_id)

        if not set(self._items).issubset(target_player.inventory.items_tuple):

            return Result(

                action_type= ActionType.REMOVE_ITEM,
                is_success=False,
                error_type=ErrorType.ITEM_NOT_IN_INVENTORY
                )
        
        for item in self._items: 

            target_player.inventory.remove_item(item)

        return Result(

            action_type= ActionType.REMOVE_ITEM,
            is_success=True,
            #Adding a Pay load stating what is being added
            )