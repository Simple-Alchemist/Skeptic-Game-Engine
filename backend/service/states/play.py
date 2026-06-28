from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..session import Session

from . import StateInterface
from ..commands.interface import CommandInterface, ItemCommandInterface, TargetPlayerCommandInterface, InGameCommand
from ..data_classes import Result, ActionType, ErrorType, States, ShootPayload

class PlayState(StateInterface):

    @property
    def name(self) -> States:
        return States.PLAY_STATE

    def handle(self, command: CommandInterface , session: 'Session') -> Result:

        current_player = session.player_turn_manager.current_player 

        if not isinstance(command,InGameCommand):
                
                return Result(
                        action_type=ActionType.CMD_OBJ_PASSED,
                        is_success=False,
                        error_type=ErrorType.CURRENTLY_IN_PLAY_STATE 
                    )  

        if isinstance(command, TargetPlayerCommandInterface):
            if not session.player_turn_manager.is_player_in_order(player_id=command.target_player_id): 

                return Result(
                        action_type=ActionType.VERIFY_TARGET_PLAYER,
                        is_success=False,
                        error_type=ErrorType.UNKNOWN_PLAYER
                    )   
    
        if isinstance(command, ItemCommandInterface):

            if not current_player.inventory.is_item_present(item=command.item_type): 

                return Result( 

                    action_type=ActionType.USE_ITEM,
                    is_success=False,
                    error_type=ErrorType.ITEM_NOT_IN_INVENTORY
                )
        
        result = command.execute(session=session)

        if result.is_success:

            if isinstance(command, ItemCommandInterface):
                
                current_player.inventory.remove_item(item=command.item_type)

            if isinstance(result.payload, ShootPayload):
                   
                if result.payload.advance_turn:
                    session.player_turn_manager.advance() 
                
            session.change_state(new_state_enum=States.RESOLUTION_STATE, trigger_enter=True)

        return result


    def enter(self, session: 'Session'):

        ...
        
        

    
        
        
    
