from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..session import Session

from . import StateInterface
from random import randint
from ..commands.interface import CommandInterface
from ..data_classes import Result, ActionType, ErrorType, States, ResolutionPayload


class ResolutionState(StateInterface):

    @property
    def enum(self) -> States:
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

        players_removed: list[int] = list()

        before_player_size, after_player_size = ptm.total_player, 0
        for player in ptm.all_player:
            if not player.is_alive: 
                ptm.remove_player(player_id=player.id)
                players_removed.append(player.id)
        
        else: 
            after_player_size = ptm.total_player

        players_removed_tuple: tuple[int,...] = tuple(players_removed)

        #Checking whether the game is over or not
        if not ptm.is_player_sufficient:
    
            session.change_state(new_state_enum=States.GAME_OVER, trigger_enter=False)

            session.save_resultion_event(
                Result(
                    action_type=ActionType.TRANSITIONING_TO_GAMEOVER_STATE, 
                    is_success=True,
                    payload=ResolutionPayload(
                        players_removed=players_removed_tuple,
                        current_player_id=ptm.current_player.id
                        )
                )
            )

            return 

        players_uncuffed: list[int] = list()
        max_skips = len(ptm.all_player)  # Safety: avoid infinite loop
        skips = 0
        # call boolean methods properly
        while skips < max_skips:

            # Scenario A: The NEXT person is cuffed. 
            if ptm.current_player.is_cuffed:
                ptm.current_player.hand_uncuff()
                players_uncuffed.append(ptm.current_player.id)
                ptm.advance() 

                skips += 1
            
                continue
            
            break 
        
        players_uncuffed_tuple: tuple[int,...] = tuple(players_uncuffed)
        
        
        
        has_live = any(s.damage >= 1 for s in session.shotgun.magazine_order)
        has_blank = any(s.damage < 1 for s in session.shotgun.magazine_order)

        change_in_player:bool = before_player_size > after_player_size
        if not (has_live and has_blank) or change_in_player: 
            #When there's no Combination of Live-Blank Shell, it will clear out the magazine

            if change_in_player: 
                
                ptm.reset_pointer()
                ptm.advance(turns=randint(1,ptm.total_player))

            session.shotgun.clear_magazine()

            session.change_state(new_state_enum=States.ROUND_MANAGER, trigger_enter=False)

            session.save_resultion_event(
                Result(
                    action_type=ActionType.TRANSITIONING_TO_ROUNDMANAGER_STATE, 
                    is_success=True,
                    payload=ResolutionPayload(
                        players_removed=players_removed_tuple,
                        players_uncuffed=players_uncuffed_tuple,
                        current_player_id=ptm.current_player.id,
                        )
                )
            )
            
            return

        #Storing a Snapshot of the Game 
        session.save_history()

        #Else -> Continue Transitioning to PlayState
        
        session.change_state(new_state_enum=States.PLAY, trigger_enter=False)

        session.save_resultion_event(
                Result(
                    action_type=ActionType.TRANSITIONING_TO_PLAYSTATE, 
                    is_success=True,
                    payload=ResolutionPayload(
                        players_removed=players_removed_tuple,
                        players_uncuffed=players_uncuffed_tuple,
                        current_player_id=ptm.current_player.id,
                        saved_history=True
                        )
                )
            )


        return


