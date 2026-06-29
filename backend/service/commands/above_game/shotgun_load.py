from random import shuffle
from typing import TYPE_CHECKING


from attrs import define

if TYPE_CHECKING: 
    from ...session import Session

from ....core import LiveShell, BlankShell
from ...data_classes import Result, ActionType
from ..interface import AboveGameCommand


@define(kw_only=True)
class ShotgunLoadCommand(AboveGameCommand):

    lives: int 
    blanks: int 

    def execute(self, session: 'Session') -> Result:

        magazine_list: list = list()

        for _ in range(0, self.lives): 
            magazine_list.append(LiveShell())

        for _ in range(0, self.blanks):
            magazine_list.append(BlankShell())
       
        shuffle(magazine_list)

        session.shotgun.load_shells(tuple(magazine_list))      

        return Result(

            action_type= ActionType.LOAD_SHELL_RANDOMLY_IN_SHOTGUN,
            is_success=True,

        )