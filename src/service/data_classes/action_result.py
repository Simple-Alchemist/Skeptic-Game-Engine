from typing import Literal

from attrs import define, field
from .action_type import ActionType
from .error_type import ErrorType
from .payload.interface import PayLoadInterface

@define(kw_only=True)
class ActionResult:

    action_type: ActionType 
    is_success: bool 
    error_type: ErrorType | None = None # 'None' indicates that the status is success
    payload: PayLoadInterface| None = None 



