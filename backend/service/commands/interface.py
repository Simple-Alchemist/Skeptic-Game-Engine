from typing import Protocol, runtime_checkable, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from ..session import Session
    from ..data_classes import Result

from ...core import ItemType


@runtime_checkable
class CommandInterface(Protocol):

    def execute(self, session: "Session") -> "Result":
        ...

class InGameCommand(ABC): 

    @abstractmethod
    def execute(self, session: "Session") -> "Result": ...

class AboveGameCommand(ABC):

    @abstractmethod
    def execute(self, session: "Session") -> "Result":...

class ItemCommandInterface(InGameCommand):

    @property
    @abstractmethod
    def item_type(self) -> ItemType:
        ...

class TargetPlayerCommandInterface(InGameCommand):

    @property
    @abstractmethod
    def target_player_id(self) -> int:
        ...
