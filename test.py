from src.service.session import Session
from src.service.commands.items.twofold import TwoFoldItemCommand
from src.service.commands.shoot import ShootCommand
from src.core import Player, LiveShell, BlankShell, ItemType

session = Session()

session.player_turn_manager.add_player(player_obj=Player(id=101, health=5))
session.player_turn_manager.add_player(player_obj=Player(id=102, health=5))

session.shotgun.load_shells([LiveShell(), BlankShell(), LiveShell(), BlankShell()])
session.player_turn_manager.current_player.inventory.add_item(item=ItemType.TWO_FOLD)

itemcmd = TwoFoldItemCommand()
shootcmd= ShootCommand(target_id=session.player_turn_manager.current_player.id)

result_one = itemcmd.execute(session=session)
result_two = shootcmd.execute(session=session)

print(result_one)
print(result_two)

print(session.shotgun.magazine_order)
print(session.player_turn_manager.all_player)

