from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..session import Session

from . import StateInterface
from ...core import LiveShell, BlankShell
from ..commands.interface import CommandInterface
from ..data_classes import Result, ActionType, ErrorType, States


class ResolutionState(StateInterface):

    @property
    def name(self) -> States:
        return States.RESOLUTION_STATE

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
        for player in list(ptm.all_player):
               if not player.is_alive: 
                   ptm.remove_player(player_id=player.id)
        
        #Checking whether the game is over or not
        if not ptm.is_player_sufficient:
    
            session.change_state(new_state_enum=States.GAME_OVER, trigger_enter=False)
            return 
        
        #Storing a Snapshot of the Game 
        session.save_history()

        #Condition for Moving to RoundManagerState - 1
        if session.shotgun.is_magazine_empty(): 
           
           
            for player in session.player_turn_manager.all_player:
               player.inventory.clear()

            session.change_state(new_state_enum=States.ROUND_MANAGER, trigger_enter=False)
            return
        
        has_live = any(s.damage >= 1 for s in session.shotgun.magazine_order)
        has_blank = any(s.damage < 1 for s in session.shotgun.magazine_order)
        if not (has_live and has_blank): 
            #When there's no Combination of Live-Blank Shell, it will clear out the magazine

            session.shotgun.clear_magazine()
           
            for player in session.player_turn_manager.all_player:
               player.inventory.clear()

            session.change_state(new_state_enum=States.ROUND_MANAGER, trigger_enter=False)
            return

        #Else -> Continue Transitioning to PlayState

        max_skips = len(ptm.all_player)  # Safety: avoid infinite loop
        skips = 0
        # call boolean methods properly
        while skips < max_skips and ptm.current_player.is_cuffed:
            ptm.current_player.hand_uncuff()
            ptm.advance()
            skips += 1

        
        session.change_state(new_state_enum=States.PLAY_STATE, trigger_enter=False)


