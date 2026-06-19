"""This File is under development"""

# from attrs import define, field

# from ...session import Session
# from ..interface import CommandInterface
# from ...data_classes import ActionResult, ActionType, ErrorType
# from ....core import LiveShell, BlankShell, ItemException, ItemType

# @define(kw_only=True)
# class InverseShellItemCommand(CommandInterface):

#     _item_type: ItemType = field(init=False, default=ItemType.INVERSE_SHELL, repr=False)

    
#     def execute(self, session: Session) -> ActionResult:
        
#         current_player = session.player_turn_manager.current_player

#         shotgun = session.shotgun

#         if not current_player.inventory.is_item_present(item=self._item_type): 
#            ...
        
#         if shotgun.magazine_order[0].damage >= 1: 
#             shotgun.unload_shell()
#             shotgun.load_shells([BlankShell()])

#         elif shotgun.magazine_order[0].damage <= 0: 
#             shotgun.unload_shell()
#             shotgun.load_shells([LiveShell()])
        
#         current_player.inventory.remove_item(item=self._item_type)

        