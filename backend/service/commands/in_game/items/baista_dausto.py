from typing import TYPE_CHECKING, override

if TYPE_CHECKING: 
    from ....session import Session
    
from attrs import define, field

from ....data_classes import Result, ActionType, ErrorType, BaistaDaustoPayload
from ...interface import ItemCommandInterface, TargetPlayerCommandInterface

from .....core import  ItemType

@define(kw_only=True)
class BaistaDaustoItemCommand(ItemCommandInterface, TargetPlayerCommandInterface):

    _item_type: ItemType = field(init=False, default=ItemType.BAISTA_DAUSTO, repr=False)
    _target_player_id: int = field(alias="target_player_id")
    _number_of_leap: int =field(default=3)

    @property
    @override
    def item_type(self) -> ItemType:
        return self._item_type
    
    @property
    @override
    def target_player_id(self) -> int:
        
        return self._target_player_id

    def execute(self, session: 'Session') -> Result:
        
        if not session.history_span >= self._number_of_leap+1:
            return Result(
                    action_type=ActionType.USE_ITEM,
                    is_success=False,
                    error_type=ErrorType.SHORT_HISTORY
                )        
        

        current_player_id = session.player_turn_manager.current_player.id
        
        target_player_data = session.export_players_snapshot(player_ids=(self._target_player_id,))

        session.leap_back(self._number_of_leap)  
        session.import_players_snapshot(player_snaps=target_player_data)

        current_player = session.player_turn_manager.get_player(player_id=current_player_id)
        
        if self._item_type in current_player.inventory.items_tuple: 
            current_player.inventory.remove_item(item=ItemType.BAISTA_DAUSTO)

        all_player = session.player_turn_manager.all_player

        for i in range(0, session.player_turn_manager.total_player):
            if not self._target_player_id == all_player[i].id: 
                session.player_turn_manager.advance()
            else: 
                break

        return Result(

                action_type=ActionType.USE_ITEM,
                is_success=True,
                payload=BaistaDaustoPayload(
                    
                    yoshikage_id=current_player.id,
                    target_id=self._target_player_id, 
                    total_leap_back=self._number_of_leap
                    
                    )
            )