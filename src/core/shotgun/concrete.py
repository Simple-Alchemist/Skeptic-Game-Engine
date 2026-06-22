from attrs import define, field

from ..shell.interface import ShellInterface

from .exception import ShotgunException

@define(kw_only=True)
class Shotgun:
    """
    Represents the shotgun in the game

    """

    _magazine: list[ShellInterface] = field(factory=list, init=False)

    @property
    def magazine_order(self) -> tuple[ShellInterface, ...]: 

        return tuple(self._magazine[::-1])
    
    def is_magazine_empty(self) -> bool: 

        return len(self.magazine_order) <= 0

    def current_loaded_shell(self) -> ShellInterface:

        if self.is_magazine_empty(): 
            raise ShotgunException("Magazine is Empty")
        
        return self.magazine_order[0]

    def load_shells(self, shells: tuple[ShellInterface,...]) -> None:
        """
        Load a single shell object into the magazine.

        Param:
            shell (ShellInterface): A shell object to add to the magazine.
        """

        self._magazine.extend(shells[::-1])

    def unload_shell(self) -> ShellInterface:  #Will be used for Shooting
        """
        Unloads a single shell from the magazine.

        """
        if self.is_magazine_empty(): 
            raise ShotgunException("Magazine is Empty")
        
        return self._magazine.pop()

    def clear_magazine(self):
        """
        Clears all shells from the magazine.

        """
        self._magazine.clear()
