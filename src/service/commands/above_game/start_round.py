from typing import TYPE_CHECKING


from attrs import define, field

if TYPE_CHECKING: 
    from ...session import Session
    
from ...data_classes import Result, ActionType, States
from ..interface import AboveGameCommand


@define(kw_only=True)
class StartRoundCommand(AboveGameCommand):

    def execute(self, session: 'Session') -> Result:

        session.change_state(new_state_enum=States.RESOLUTION_STATE, trigger_enter=True)

        return Result(

            action_type= ActionType.ATTEMPT_TO_PLAYSTATE,
            is_success=True,
            )