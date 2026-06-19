from attrs import define, field

from ..session import Session
from ..data_classes import ActionResult, ActionType, ErrorType, ShootPayload
from .interface import CommandInterface

@define(kw_only=True)
class ShootCommand(CommandInterface):

    _target_id: int = field(alias="target_id")

    def execute(self, session: Session) -> ActionResult:
        
        shotgun = session.shotgun 

        if shotgun.is_magazine_empty(): 

           return ActionResult(
                    action_type=ActionType.SHOOT,
                    is_success=False,
                    error_type=ErrorType.EMPTY_MAGAZINE
                    )
        
        ptm = session.player_turn_manager

        if not ptm.is_player_in_order(player_id=self._target_id): 

            return ActionResult(
                action_type=ActionType.SHOOT,
                is_success=False,
                error_type=ErrorType.UNKNOWN_PLAYER
            )
        
        fired_shell = session.shotgun.unload_shell()

        targeted_player = ptm.get_player(self._target_id)

        if targeted_player.health < fired_shell.damage:
            targeted_player.adjust_health(targeted_player.health)

        targeted_player.adjust_health(-fired_shell.damage)

        return ActionResult(

            action_type= ActionType.SHOOT,
            is_success=True,
            payload=ShootPayload(damage_dealt=fired_shell.damage)

            )


        


        


