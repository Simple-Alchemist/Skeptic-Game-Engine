from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from ..session import Session

from . import StateInterface
from ..commands.interface import CommandInterface
from ..data_classes import Result, ActionType, ErrorType, States


class GameOverState(StateInterface):
    
    @property
    def name(self) -> States:
        return States.GAME_OVER

    def handle(self, command: CommandInterface , session: 'Session') -> Result:
        
        return Result(
            action_type=ActionType.CMD_OBJ_PASSED,
            is_success=False,
            error_type=ErrorType.GAME_OVER
        ) 
    
    def enter(self, session: 'Session'): 
        ...
        

    