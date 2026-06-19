from typing import Protocol, runtime_checkable 

from ..commands import CommandInterface
from ..session import Session

@runtime_checkable
class StateInterface(Protocol): 

    def handle(self, command: CommandInterface, session: Session) -> str: 
        ...

    # in the handle method, always check whether the current player is hand-cuffed? or dead? 



