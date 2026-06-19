"""This File is under development"""

# from attrs import define, field

# from ...session import Session

# from interface import CommandInterface
# from ...data_classes import ActionResult, ActionType, ErrorType
# from ....core import LiveShell, BlankShell, ItemException, ItemType

# @define(kw_only=True)
# class EjectorItemCommand(CommandInterface):

#     _item_type: ItemType = field(init=False, default=ItemType.EJECTOR, repr=False)

    
#     def execute(self, session: Session) -> ActionResult:
        
#         current_player = session.player_manager.get_player(session.turn_manager.current_player_id)
#         shotgun = session.shotgun

#         if not current_player.inventory.is_item_present(item=self._item_type): 
#             raise ItemException(f"{self._item_type} is not present in {current_player.id}'s inventory")
    
#         ejected_shell = shotgun.unload_shell()
            
#         current_player.inventory.remove_item(item=self._item_type)

#         return ActionResult() # using EjectorPayload