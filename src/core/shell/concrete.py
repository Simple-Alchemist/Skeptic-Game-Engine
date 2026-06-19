from attrs import define, field

from .interface import ShellInterface


@define(frozen=True)
class LiveShell(ShellInterface): 
    
    _damage: int = field(default=1, repr=False, init=False)

    @property 
    def damage(self) -> int:
        return self._damage

@define(frozen=True)
class BlankShell(ShellInterface):

    _damage: int = field(default=0, repr=False, init=False)

    @property 
    def damage(self) -> int:
        return self._damage
 


    
    