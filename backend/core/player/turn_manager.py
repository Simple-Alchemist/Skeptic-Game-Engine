from attrs import Factory, define, field
from attrs.validators import in_

from . import PlayerException, Player

@define(kw_only=True)
class PlayerTurnManager:

    """Manages the turn order and direction of play for players in the game.
    It is an immutable class; all methods that modify the order or direction
    return a new TurnManager instance.
    """

    _order: list[Player] = field(default=Factory(list), init=False)
    _direction: int = field(
        default=1,
        validator=in_((-1, 1)),
        init=False
    )
    _pointer: int = field(default=0, init=False, repr=False)
    
    @property
    def current_player(self) -> Player:
    
        try:
            return self._order[(self._pointer%len(self._order))]
        
        except (IndexError, ZeroDivisionError):

            raise PlayerException("Couldn't retrieve the current player.")
        
    @property
    def next_player(self) -> Player:

        try: 
            return self._order[((self._pointer+1)%len(self._order))]
        
        except (IndexError, ZeroDivisionError):

            raise PlayerException("Couldn't retrieve the next player.")

    @property
    def all_player(self) -> tuple[Player,...]:
        return tuple(self._order)
    
    @property
    def total_player(self) -> int: 
        return len(self._order)
    
    @property
    def is_player_sufficient(self) -> bool: 
        # Return True when there are enough players (>= 2)
        return len(self._order) >= 2
    
    @property 
    def direction(self) -> int: 
        return self._direction 
    
    @property 
    def pointer(self) -> int: 
        return self._pointer
        

    def is_player_in_order(self, player_id: int) -> bool: 
        
        for player in self._order: 
            if player_id == player.id:
                return True
        else:
            return False
        
    def get_player(self, player_id: int) -> Player: 
        for player in self._order:
            if player_id == player.id:
                return player 
            
        else: 
            raise PlayerException("There is no player with this ID.")

    def remove_player(self, player_id: int) -> None:

        player = self.get_player(player_id=player_id)
        self._order.remove(player)

    def add_player(self, player_obj: Player) -> None:

        if self.is_player_in_order(player_obj.id):
            raise PlayerException("Player is already in the turn order")

        self._order.append(player_obj)

    def advance(self, turns: int = 1) -> None:

        if turns < 0:
           raise PlayerException("Turns Can't be Less than equal 0")

        self._pointer += (turns*self._direction)

    def reverse_order(self) -> None:
 
        self._direction = self._direction * -1

    def reset_pointer(self) -> None: 
        self._pointer = 0

    def clear_reset_order(self) -> None: 

        self._order.clear()
        self._direction = 1
        self._pointer = 0
