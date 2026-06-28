from attrs import define, field

from ..core import Shotgun, PlayerTurnManager, Player, PlayerException
from .states import StateInterface, RoundManagerState, ResolutionState, PlayState, GameOverState
from .commands.interface import CommandInterface 
from .commands import ShotgunLoadCommand
from .data_classes import Result, States, GameSnapshot, PlayerSnapshot, TurnSnapshot, ShotgunSnapshot

@define(kw_only=True)
class Session:
    
    player_turn_manager: PlayerTurnManager = field(factory=PlayerTurnManager)
    shotgun: Shotgun = field(factory=Shotgun)
    _state: StateInterface = field(init=False, factory=RoundManagerState) 
    _finite_machine: dict[States, type[StateInterface]] = field(factory=dict, init=False)  

    _history: list[GameSnapshot] = field(factory=list,init=False)

    def __attrs_post_init__(self):

        self._finite_machine.update(
            {
                States.ROUND_MANAGER:RoundManagerState,
                States.RESOLUTION_STATE:ResolutionState,
                States.PLAY_STATE: PlayState,
                States.GAME_OVER: GameOverState,
            }
        )
        
    @property
    def current_state_name(self) -> States:

        return self._state.name
    
    @property 
    def history_span(self) -> int: 
        return len(self._history)

    def change_state(self, new_state_enum: States, trigger_enter: bool) -> None: 

        self._state = self._finite_machine[new_state_enum]()
        
        if trigger_enter:
            self._state.enter(session=self)

    def game_command(self, command: CommandInterface) -> Result:
        
        return self._state.handle(command=command, session=self)

    def export_game_snapshot(self) -> GameSnapshot: 
        
        # Creating tuple of PlaySnapshot
        player_datas = tuple(
            PlayerSnapshot(
                id=p.id,
                health=p.health,
                inventory=p.inventory.items_tuple,
                is_cuffed=p.is_cuffed
            ) for p in self.player_turn_manager.all_player
        )


        return GameSnapshot(
            current_state_name=self.current_state_name,
            turn_data=TurnSnapshot(
                current_player_id=self.player_turn_manager.current_player.id,
                direction=self.player_turn_manager.direction,
                pointer=self.player_turn_manager.pointer
            ),
            player_datas=player_datas,
            shotgun_data=ShotgunSnapshot(
                 lives=sum(shell.damage >= 1 for shell in self.shotgun.magazine_order),
                 blanks=sum(shell.damage < 1 for shell in self.shotgun.magazine_order)
                 )
        )

    def import_game_snapshot(self, snapshot: GameSnapshot) -> None:

        self.change_state(new_state_enum=States.ROUND_MANAGER, trigger_enter=False)

        ptm = self.player_turn_manager
        shotgun = self.shotgun

        #clearing out the current config of order
        ptm.clear_reset_order()

        for player_data in snapshot.player_datas: 
            new_player = Player(

                            id=player_data.id,
                            health=player_data.health
                        )
            
            ptm.add_player(player_obj=new_player)
            
            new_player = ptm.get_player(player_id=player_data.id)

            if player_data.is_cuffed:
                new_player.hand_cuff()
            
            new_player.inventory.add_items(player_data.inventory)

        shotgun.clear_magazine()

        self.game_command(command=ShotgunLoadCommand(
                                        lives=snapshot.shotgun_data.lives,
                                        blanks=snapshot.shotgun_data.blanks
                                        )
                                )

        new_state_enum: States = snapshot.current_state_name
        
        if snapshot.turn_data.direction <= -1:
            ptm.reverse_order()

        #Estimating Pointer of the player
        ptm.advance(turns=abs(snapshot.turn_data.pointer))

        if ptm.current_player.id != snapshot.turn_data.current_player_id:
            raise PlayerException("Import Error: Current Player didn't matched")

        self.change_state(new_state_enum=new_state_enum, trigger_enter=False) 
    
    #Export Multiple Player in Tuple
    def export_players_snapshot(self, player_ids: tuple[int,...]) -> tuple[PlayerSnapshot,...]:
        
        ptm = self.player_turn_manager 

        existing_ids =  {player.id for player in ptm.all_player}
        if not set(player_ids).issubset(existing_ids):
            raise PlayerException(f'{player_ids} are not present in player turn manager')

                        
        return tuple(
                [
                    PlayerSnapshot(
                        id=player.id,
                        health=player.health,
                        inventory=player.inventory.items_tuple,
                        is_cuffed=player.is_cuffed
                        )

                    for player in ptm.all_player if player.id in player_ids
                    
                ]

                )
            
    def import_players_snapshot(self, player_snaps: tuple[PlayerSnapshot,...]) -> None: 
        
        ptm = self.player_turn_manager

        for player_data in player_snaps: 
            
            if not ptm.is_player_in_order(player_id=player_data.id):

                target_player: Player = Player(id=player_data.id, health=player_data.health)
                ptm.add_player(player_obj=target_player)

            target_player = ptm.get_player(player_id=player_data.id) 
    
            target_player.adjust_health(player_data.health-target_player.health)

            if (player_data.is_cuffed) and (not target_player.is_cuffed): 
                target_player.hand_cuff() 

            elif (not player_data.is_cuffed) and (target_player.is_cuffed): 
                target_player.hand_uncuff()

            target_player.inventory.clear()
            target_player.inventory.add_items(player_data.inventory)


    def save_history(self):

        self._history.append(self.export_game_snapshot())

    def clear_history(self): 
        
        self._history.clear()

    def leap_back(self, leap: int = 3):

        if self.history_span <= leap:
            raise Exception("Can't Leap in Mystery") 
        
        self.import_game_snapshot(self._history[-leap])
        self._history = self._history[:-leap]


    


    