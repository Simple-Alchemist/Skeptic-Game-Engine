from typing import TYPE_CHECKING, override

if TYPE_CHECKING: 
    from ...session import Session

from attrs import define, field

from ...data_classes import Result, ActionType, ShootPayload
from ..interface import TargetPlayerCommandInterface

@define(kw_only=True)
class ShootCommand(TargetPlayerCommandInterface):

    _target_player_id: int = field(alias="target_player_id")

    @property
    @override 
    def target_player_id(self) -> int: 
        return self._target_player_id
    

    def execute(self, session: 'Session') -> Result:
        
        shotgun = session.shotgun 
        ptm = session.player_turn_manager
        
        fired_shell = shotgun.unload_shell()

        targeted_player = ptm.get_player(self._target_player_id)

        if targeted_player.health < fired_shell.damage:
            targeted_player.adjust_health(targeted_player.health)
        else: 
            targeted_player.adjust_health(-fired_shell.damage)

        return Result(

            action_type= ActionType.SHOOT,
            is_success=True,
            payload=ShootPayload(
                damage_dealt=fired_shell.damage, 
                target_id=self._target_player_id,
                advance_turn= not (
                    fired_shell.damage <= 0 and self._target_player_id == ptm.current_player.id
                    )
                )

            )


        


        


