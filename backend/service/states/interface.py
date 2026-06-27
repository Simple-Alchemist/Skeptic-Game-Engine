from typing import Protocol, runtime_checkable , TYPE_CHECKING

from ..commands.interface import CommandInterface
if TYPE_CHECKING:
    from ..session import Session
from ..data_classes import Result, States

@runtime_checkable
class StateInterface(Protocol): 

    @property
    def name(self) -> States:
        ...

    def handle(self, command: CommandInterface, session: 'Session') -> Result: 
        ...

    def enter(self, session: 'Session'): ... # Only for Resolution State



