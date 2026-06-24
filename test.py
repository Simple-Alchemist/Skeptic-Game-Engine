"""Mildly Testing out the classes and methods"""
from src import Session
from src import (
    ItemDistributionCommand, 
    AddPlayerCommand, 
    StartRoundCommand,
    ShotgunLoadCommand,
    ShootCommand,
    TwoFoldItemCommand,
)

from src.bot import BotAbility
session = Session()

result = session.game_command(AddPlayerCommand(id=101, health=10))
result = session.game_command(AddPlayerCommand(id=102, health=10))

result = session.game_command(ShotgunLoadCommand(lives=5, blanks=5))

result = session.game_command(ItemDistributionCommand(max_item=5))

print(result,end="\n")


# print(session.player_turn_manager.all_player)
result = session.game_command(StartRoundCommand())

print(session.player_turn_manager.current_player.inventory, end="\n")
bot_snap = session.export_game_snapshot()


ability = BotAbility(gs=bot_snap,last_result=result)
print(bot_snap)
print()
response = ability.think()

print(response)
result = session.game_command(command=response)
print()
print(result)

print() 

print(session.export_game_snapshot())



