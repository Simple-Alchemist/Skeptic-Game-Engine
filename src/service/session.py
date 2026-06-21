from attrs import define, field

from ..core import Shotgun, PlayerTurnManager, Player
from .states import StateInterface, RoundManagerState, ResolutionState, PlayState, GameOverState
from .commands.interface import CommandInterface 
from .data_classes import Result, States, GameSnapshot, PlayerSnapshot

@define(kw_only=True)
class Session:
    
    player_turn_manager: PlayerTurnManager = field(factory=PlayerTurnManager)
    shotgun: Shotgun = field(factory=Shotgun)
    _state: StateInterface = field(init=False, factory=RoundManagerState) 
    _finite_machine: dict[States, type[StateInterface]] = field(factory=dict, init=False)  

    _history: list[GameSnapshot] = field(factory=list,init=False) #Under work

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

    def export_snapshot(self) -> GameSnapshot: 

        player_data: list[PlayerSnapshot] = list()

        for player in self.player_turn_manager.all_player:

            player_data.append(PlayerSnapshot(
                                            id=player.id,
                                            health=player.health,
                                            inventory=player.inventory.items_tuple,
                                            is_cuffed=player.is_cuffed
                                            ) 
                                        )
        return GameSnapshot(
            current_state_name=self.current_state_name,
            current_player_id=self.player_turn_manager.current_player.id,
            turn_order_direction=self.player_turn_manager.direction,
            turn_pointer=self.player_turn_manager.pointer,
            player_data=tuple(player_data),
            magazine=self.shotgun.magazine_order)


    def import_snapshot(self, snapshot: GameSnapshot) -> None:
        
        new_ptm: PlayerTurnManager = PlayerTurnManager()
        for player in snapshot.player_data: 
            
            new_ptm.add_player(
                player_obj=Player(
                    id=player.id,
                    health=player.health
                    )
                )
            
            new_player = new_ptm.get_player(player_id=player.id)

            if player.is_cuffed:
                new_player.hand_cuff()
            
            for data_player_item in player.inventory:
                new_player.inventory.add_item(data_player_item)

        new_shotgun: Shotgun = Shotgun()

        new_shotgun.load_shells(snapshot.magazine)

        new_state_enum: States = snapshot.current_state_name
        

        if snapshot.turn_order_direction <= -1:
            new_ptm.reverse_order()

        #Estimating Pointer of the player
        new_ptm.advance(turns=abs(snapshot.turn_pointer))

        if new_ptm.current_player.id != snapshot.current_player_id:
            raise Exception("Current Player didn't matched")

        self.player_turn_manager = new_ptm

        self.shotgun = new_shotgun

        self.change_state(new_state_enum=new_state_enum, trigger_enter=False) 
    
    def save_history(self):

        self._history.append(self.export_snapshot())

    def leap_back(self, leap: int = 3):

        if len(self._history) <= leap:
            raise Exception("Can't Leap in Mystery") 
        
        self.import_snapshot(self._history[-leap])
        self._history = self._history[:-leap]


    


    