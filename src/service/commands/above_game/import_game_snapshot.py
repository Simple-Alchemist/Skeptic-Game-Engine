from typing import TYPE_CHECKING

from attrs import define,field

if TYPE_CHECKING: 
    from ...session import Session

from ...data_classes import Result, ActionType, ErrorType
from ....core import  ItemType
from ..interface import AboveGameCommand

@define(kw_only=True)
class ImportGameSnapshotCommand(AboveGameCommand):


    def execute(self, session: 'Session') -> Result:

       ...

        # return Result(

            
        #     #Adding a Pay load stating what is being added
        #     )

@define(kw_only=True) 
class ImportPlayerSnapshotCommand(AboveGameCommand): 
    ... 

    def execute(self, sesssion: 'Session') -> Result: 
        ...