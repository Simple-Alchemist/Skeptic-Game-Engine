from typing import TYPE_CHECKING, override

if TYPE_CHECKING: 
    from ....session import Session
    
from attrs import define, field

from ....data_classes import Result, ActionType, ErrorType
from ...interface import ItemCommandInterface

from .....core import  ItemType

@define(kw_only=True)
class BaistaDaustoItemCommand(ItemCommandInterface):

    _item_type: ItemType = field(init=False, default=ItemType.BAISTA_DAUSTO, repr=False)
    _number_of_leap: int =field(default=3)

    @property
    @override
    def item_type(self) -> ItemType:
        return self._item_type

    def execute(self, session: 'Session') -> Result:
        
        if not session.history_span >= self._number_of_leap+1:
            return Result(
                    action_type=ActionType.USE_ITEM,
                    is_success=False,
                    error_type=ErrorType.SHORT_HISTORY
                )        

        session.leap_back(self._number_of_leap)  
        
        return Result(
                action_type=ActionType.USE_ITEM,
                is_success=True,
                #Will be working on the payload 
            )