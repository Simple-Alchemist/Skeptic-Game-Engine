from random import randint
from typing import TYPE_CHECKING

from attrs import define, field

if TYPE_CHECKING: 
    from ...session import Session

from ...data_classes import Result, ActionType
from ....core import ItemType
from ..interface import AboveGameCommand

@define(kw_only=True)
class ItemDistributionCommand(AboveGameCommand):

    _max_item: int = field(alias="max_item", default=4)
    _except_player_ids: tuple[int,...] | None = field(alias="except_player_ids", default=None)

    def execute(self, session: 'Session') -> Result:

        items_available: tuple[ItemType,...] = ItemType.item_available()
        weight_pool: list = list()

        for item in items_available:
            for _ in range(item.value):
                weight_pool.append(item)

        for player in session.player_turn_manager.all_player:
            
            if (self._except_player_ids is not None) and (player.id in self._except_player_ids):
                continue

            allocate_counter = 0
            while allocate_counter < self._max_item:

                _random_pointer = randint(0, len(weight_pool)-1)

                item_selected = weight_pool[_random_pointer]

                player.inventory.add_item(item=item_selected)
                allocate_counter +=1

    
        return Result(

            action_type= ActionType.ITEM_DISTRIBUTION,
            is_success=True,
            )