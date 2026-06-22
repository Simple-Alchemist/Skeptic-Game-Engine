from attrs import define


from .action_type import ActionType
from .error_type import ErrorType
from .payload.base import BasePayload

@define(kw_only=True)
class Result:

    action_type: ActionType 
    is_success: bool 
    error_type: ErrorType | None = None # 'None' indicates that the status is success
    payload: BasePayload | None = None 



