from random import randint
from statistics import stdev,mean
from typing import TYPE_CHECKING

from attrs import define, field

if TYPE_CHECKING: 
    from ...session import Session

from ...data_classes import Result, ActionType, ErrorType
from ....core import ItemType
from ..interface import AboveGameCommand

@define(kw_only=True)
class ItemDistributionCommand(AboveGameCommand):

    _max_item: int = field(alias="max_item", default=4)
    _except_player_ids: tuple[int,...] | None = field(alias="except_player_ids", default=None)
    _except_items_type: tuple[ItemType,...] | None = field(alias="except_item_type", default=None)

    def execute(self, session: 'Session') -> Result:

        items_available: tuple[ItemType,...] = ItemType.item_available()
        weight_pool: list = list()

        if self._except_items_type is not None: 
            items_available = tuple(
                item for item in items_available if item not in self._except_items_type
            )
        
        all_item_value: tuple[int,...] = tuple( item.value for item in items_available )

        rarity_threshold = mean(data=all_item_value)- stdev(data=all_item_value)
        
        for item in items_available:
            for _ in range(item.value):
                weight_pool.append(item)
                
        if not weight_pool:
            return Result(
                action_type=ActionType.ITEM_DISTRIBUTION,
                is_success=False,
                error_type=ErrorType.EMPTY_WEIGHT_POOL
            )
        for player in session.player_turn_manager.all_player:
            
            if (self._except_player_ids is not None) and (player.id in self._except_player_ids):
                continue

            allocate_counter = 0

            while allocate_counter < self._max_item:

                _random_pointer = randint(0, len(weight_pool)-1)

                item_selected:ItemType = weight_pool[_random_pointer]

                if (item_selected.value < rarity_threshold) and (item_selected in player.inventory.items_tuple):
                    continue 

                player.inventory.add_items((item_selected,))
                allocate_counter +=1

    
        return Result(

            action_type= ActionType.ITEM_DISTRIBUTION,
            is_success=True,
            )