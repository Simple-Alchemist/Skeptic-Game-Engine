"""Mildly Testing out the classes and methods"""
# from src import Session
# from src import (
#     ItemDistributionCommand, 
#     AddPlayerCommand, 
#     StartRoundCommand,
#     ShotgunLoadCommand,
#     ShootCommand,
#     TwoFoldItemCommand,
    
# )

# session = Session()

# result = session.game_command(AddPlayerCommand(id=101, health=10))
# result = session.game_command(AddPlayerCommand(id=102, health=10))

# result = session.game_command(ShotgunLoadCommand(lives=5, blanks=5))

# result = session.game_command(ItemDistributionCommand(max_item=4))

# if not result.is_success:
#     print("something went wrong")

# # print(session.player_turn_manager.all_player)
# result = session.game_command(StartRoundCommand())

# result = session.game_command(command=TwoFoldItemCommand())
# result = session.game_command(command=ShootCommand(target_player_id=102))

# test = session.export_snapshot()

# result = session.game_command(command=ShootCommand(target_player_id=102))

# # print(result)

# session.import_snapshot(test)
