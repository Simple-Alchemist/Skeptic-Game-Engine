from typing import Protocol, runtime_checkable

from ..session import Session
from ..data_classes import ActionResult


@runtime_checkable
class CommandInterface(Protocol):

    def execute(self, session: Session) -> ActionResult:
        ...
    

    
    