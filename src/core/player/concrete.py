from __future__ import annotations

from attrs import define, field,setters
from attrs.validators import ge

from .exception import PlayerException

@define(kw_only=True)
class Player:
    """
    Represents a game player.

    Attributes
    ----------
    _id : int
        Unique identifier for the player.
    _health : int
        Current health value. Must be greater than or equal to 0.
    _cuffed : bool
        Indicates whether the player is currently restrained.

    """
    _id: int = field(on_setattr=setters.frozen, validator=ge(0), alias="id")
    _health: int = field(alias="health")
    _cuffed: bool = field(default=False, init=False)

    def __attrs_post_init__(self):
        """Making sure that the Health Value passed is not less or equal to zero"""
        if self._health == 0: 
            
            raise ValueError("Health Can not be initialized as '0'")
        
        elif self._health < 0:

            raise ValueError("Health cannot be negative")
    

    @property
    def id(self) -> int:
        """
        Returns ID of the player
        """
        return self._id 
    
    @property
    def health(self) -> int: 

        """Return Health of the Player"""

        return self._health 
    
    def is_alive(self) -> bool: 
        """Return Whether the Player is Alive or not"""
        return self._health > 0 

    def is_cuffed(self) -> bool: 

        """Return Whether the Player is Cuffed or not"""

        return  self._cuffed
    
    def adjust_health(self, points: int): 
        
        """
        Adjust's Player health by passing positive | negative points to Increase | Decrease

        Raises: 
            PlayerException -> If the decreasing point is greater than the current health (Health can't go negative)
                            -> When the Player hits Zero Health, it can regain points since it's not Alive
        """
        if self.health <=0: 
            
            raise PlayerException("Player is Dead, can't adjust it's health")
        
        elif self._health + points < 0:

            raise PlayerException("Player's Health can't get below 0")
        
        
        self._health+=points

    def hand_cuff(self) -> None: 

        """
        Hand Cuffing the Player

        """

        if self._cuffed: 
            raise PlayerException("The Player is Already Cuffed")

        self._cuffed = True 

    def hand_uncuff(self) -> None:

        """
        Hand UnCuffing the Player

        """
        
        if not self._cuffed: 
            raise PlayerException("The Player is not Cuffed")

        self._cuffed = False




