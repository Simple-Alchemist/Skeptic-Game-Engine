from random import shuffle
from typing import TYPE_CHECKING


from attrs import define

if TYPE_CHECKING: 
    from ...session import Session

from ....core import LiveShell, BlankShell
from ...data_classes import Result, ActionType, ErrorType
from ..interface import AboveGameCommand


@define(kw_only=True)
class ShotgunLoadCommand(AboveGameCommand):

    lives: int 
    blanks: int 
    random: bool = True

    def execute(self, session: 'Session') -> Result:

        magazine_list: list = list()

        for _ in range(0, self.lives): 
            magazine_list.append(LiveShell())

        for _ in range(0, self.blanks):
            magazine_list.append(BlankShell())

        if self.random: 
            shuffle(magazine_list)

        session.shotgun.load_shells(tuple(magazine_list))
        

        return Result(

            action_type= ActionType.LOAD_SHELL,
            is_success=True,
            )