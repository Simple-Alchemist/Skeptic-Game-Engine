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

    def load_shells(self, shells: list[ShellInterface]) -> None:
        """
        Load a single shell object into the magazine.

        Param:
            shell (ShellInterface): A shell object to add to the magazine.
        """

        self._magazine.extend(shells)

    def unload_shell(self) -> ShellInterface:  #Will be used for Shooting
        """
        Unloads a single shell from the magazine.

        """
        if len(self._magazine) <=0: 
            raise ShotgunException("Magazine is Empty")
        
        return self._magazine.pop()

    def clear_magazine(self):
        """
        Clears all shells from the magazine.

        """
        self._magazine.clear()
