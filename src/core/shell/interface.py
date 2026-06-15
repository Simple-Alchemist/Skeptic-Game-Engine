from typing import Protocol,runtime_checkable


@runtime_checkable
class ShellInterface(Protocol):

    _damage: int 

    @property
    def damage(self) -> int: 
        ...