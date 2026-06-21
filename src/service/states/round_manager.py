from typing import TYPE_CHECKING

from .interface import StateInterface
from ..commands.interface import CommandInterface, AboveGameCommand, InGameCommand

if TYPE_CHECKING:
    from ..session import Session

from ..data_classes import Result, ActionType, ErrorType, States


class RoundManagerState(StateInterface):

    @property
    def name(self) -> States:
        return States.ROUND_MANAGER
    
    def handle(self, command: CommandInterface, session: 'Session') -> Result:
        
        if not isinstance(command, AboveGameCommand): 
            
            return Result( 
                action_type=ActionType.CMD_OBJ_PASSED,
                is_success=False, 
                error_type=ErrorType.INCORRECT_COMMAND
            )
   
        
        result = command.execute(session=session)
        
        return result

    def enter(self, session: 'Session'): 
        ...
        

    
        
        
    
