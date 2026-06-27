from typing import TYPE_CHECKING, override
from random import randint

if TYPE_CHECKING: 
    from ....session import Session
    
from attrs import define, field

from ....data_classes import Result, ActionType, PlayerSnapshot, CharemPayload
from ...interface import ItemCommandInterface

from .....core import  ItemType

@define(kw_only=True)
class CharemItemCommand(ItemCommandInterface):

    _item_type: ItemType = field(init=False, default=ItemType.CHAREM, repr=False)

    @property
    @override
    def item_type(self) -> ItemType:
        return self._item_type

    def execute(self, session: 'Session') -> Result:

        ptm = session.player_turn_manager
        
        valid_targets = tuple(
            player for player in ptm.all_player 
            if player.id != ptm.current_player.id
        )

        random_pointer = randint(0,len(valid_targets)-1)

        random_player = valid_targets[random_pointer] 


        players_snaps = session.export_players_snapshot(
            player_ids=(random_player.id, ptm.current_player.id)
        )

        # 3. FIX: Convert tuple to a Dictionary keyed by ID!
        snap_dict = {snap.id: snap for snap in players_snaps}
        
        random_player_data = snap_dict[random_player.id]
        current_player_data = snap_dict[ptm.current_player.id]
        
        #Swapping two snapshots
        new_player_snaps = (
            PlayerSnapshot(
                id=ptm.current_player.id, 
                health=random_player_data.health, 
                is_cuffed=random_player_data.is_cuffed, 
                inventory=random_player_data.inventory
            ),
            PlayerSnapshot(
                id=random_player.id, 
                health=current_player_data.health, 
                is_cuffed=current_player_data.is_cuffed,
                inventory=current_player_data.inventory
            )
        )
        
        session.import_players_snapshot(player_snaps=new_player_snaps)

        random_player.inventory.remove_item(item=ItemType.CHAREM)
        ptm.current_player.inventory.add_items(item_tuple=(ItemType.CHAREM,))

        return Result(
            action_type=ActionType.USE_ITEM, 
            is_success=True,
            payload=CharemPayload(victim_id=random_player.id)
        )