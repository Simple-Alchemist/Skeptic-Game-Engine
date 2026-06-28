from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..session import Session

from . import StateInterface
from random import randint
from ..commands.interface import CommandInterface
from ..data_classes import Result, ActionType, ErrorType, States


class ResolutionState(StateInterface):

    @property
    def name(self) -> States:
        return States.RESOLUTION

    def handle(self, command: CommandInterface, session: 'Session') -> Result:

        return Result(
            action_type=ActionType.CMD_OBJ_PASSED, 
            is_success=False, 
            error_type=ErrorType.CURRENTLY_IN_RESOLUTION_STATE
            )    
    
    def enter(self, session: 'Session') -> None:

        ptm = session.player_turn_manager

        #A bit of clean Up
        # iterate over a copy since we may remove players from the turn order

        before_player_size, after_player_size = ptm.total_player, 0
        for player in ptm.all_player:
            if not player.is_alive: 
                ptm.remove_player(player_id=player.id)
        
        else: 
            after_player_size = ptm.total_player

        #Checking whether the game is over or not
        if not ptm.is_player_sufficient:
    
            session.change_state(new_state_enum=States.GAME_OVER, trigger_enter=False)
            return 
        
        max_skips = len(ptm.all_player)  # Safety: avoid infinite loop
        skips = 0
        # call boolean methods properly
        while skips < max_skips:

            # Scenario A: The NEXT person is cuffed. 
            if ptm.current_player.is_cuffed:
                ptm.current_player.hand_uncuff()
                ptm.advance() 

                skips += 1
            
                continue
            
            break 
        
        has_live = any(s.damage >= 1 for s in session.shotgun.magazine_order)
        has_blank = any(s.damage < 1 for s in session.shotgun.magazine_order)

        if not (has_live and has_blank) or before_player_size > after_player_size: 
            #When there's no Combination of Live-Blank Shell, it will clear out the magazine

            session.shotgun.clear_magazine()
            ptm.reset_pointer()

            ptm.advance(turns=randint(1,ptm.total_player))

            session.change_state(new_state_enum=States.ROUND_MANAGER, trigger_enter=False)
            return

        #Storing a Snapshot of the Game 
        session.save_history()

        #Else -> Continue Transitioning to PlayState
        
        session.change_state(new_state_enum=States.PLAY, trigger_enter=False)


