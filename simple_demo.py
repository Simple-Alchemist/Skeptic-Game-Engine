"""Testing PlayGround"""

import time 
from random import randint

from backend.api import Session, BotAlgorithm, InGameCommandFactory, Result
from backend.api.commmands import AddPlayerCommand, ItemDistributionCommand,ShotgunLoadCommand, StartRoundCommand
from backend.api.enum_type import States, ItemType
from backend.api.payload import ShellPayload, ShootPayload

session = Session()


item_map: dict[str, ItemType] = {

    "hand cuff": ItemType.HAND_CUFF,    #target_player_id
    "peek":ItemType.PEEK_SHOTGUN, 
    "two fold":ItemType.TWO_FOLD,    
    "charem":ItemType.CHAREM,  
    "banana":ItemType.BANANA,
    "baista_dausto":ItemType.BAISTA_DAUSTO, #target_player_id
    "ejector":ItemType.EJECTOR,
    "inverse shell":ItemType.INVERSE_SHELL,
    "U Turn":ItemType.U_TURN
    }


bot_result: Result | None = None
lives,blanks = 0,0


for i in range(1,4):
    session.game_command(command=AddPlayerCommand(id=i, health=3))

while session.current_state_name != States.GAME_OVER:

    if session.current_state_name == States.ROUND_MANAGER:
        
        print("Loading Shells...")
        time.sleep(2)
        lives,blanks = randint(4,6),randint(3,5)
        result = session.game_command(ShotgunLoadCommand(lives=lives,blanks=blanks))
        print("Distributing Items...")
        time.sleep(2)
        session.game_command(command=ItemDistributionCommand(max_item=4,except_item_type=(ItemType.BAISTA_DAUSTO, ItemType.U_TURN)))
    

        print("Starting the round")
        time.sleep(2)
        result = session.game_command(command=StartRoundCommand()) 

        if not result.is_success:
            print(result)
            break


    for player in session.player_turn_manager.all_player:
        print(f"Players - id: {player.id}", end= "\n")
        print(f"        - health: {player.health*"🔋"}", end= "\n")
        print(f"        - inventory: {tuple(item.name.lower().replace("_", " ") for item in player.inventory.items_tuple)}")

    lives = sum(shell.damage >= 1 for shell in session.shotgun.magazine_order)
    blanks = sum(shell.damage < 1 for shell in session.shotgun.magazine_order)

    time.sleep(5)
    print(f"shotgun: {lives*"🔴"}{blanks*"🟢"} ", end= "\n\n")
    time.sleep(2)
    
    if session.player_turn_manager.current_player.id == 1: 

        print("You are player with ID: 0")
        
        while True: 
            prompt = input("Do you want to use an 'Item' or you better off 'shoot'?: ")

            if prompt == "item": 

                item_prompt = input("type your item choice: ")

                if item_map.get(item_prompt, 0) == 0:
                    
                    print("Please choose a valid item")
                    continue
                    
                extra_prompt: int = 0

                if item_map[item_prompt] == ItemType.HAND_CUFF: 
                    extra_prompt = int(input("Enter you target: "))

                
                command =InGameCommandFactory.manufacture_item_command(item_type=item_map[item_prompt], target_player_id = extra_prompt)

                user_result = session.game_command(command)

            elif prompt == "shoot": 

                extra_prompt:int  = int(input("Enter you target: "))
                user_result = session.game_command(InGameCommandFactory.manufacture_shoot_command(target_player_id=extra_prompt))

                if not user_result.is_success: 
                    print("Enter correct id")
                    continue

            else: 
                print("Please write 'shoot' or 'item'")
                continue

            if not user_result.is_success: 
                print("Something went wrong, please de-bug")
                print(f"{user_result}")

            if isinstance(user_result.payload, ShellPayload):
                if user_result.payload.item_type == ItemType.PEEK_SHOTGUN:
                    print(f"Peeked!? current shell loaded is {user_result.payload.shell_damage}")

            if isinstance(user_result.payload,ShootPayload):
                print(f"Shell shooted: {user_result.payload.damage_dealt}")

            break


        
        
    else: 

        gs = session.export_game_snapshot() 
        # print(bot_result)
        bot = BotAlgorithm(gs=gs, last_result=bot_result)

        print(f"{session.player_turn_manager.current_player.id} is Thinking hard....")
        time.sleep(5)

        bot_response = bot.think() 

        print(f"bot response: {bot_response}")
        time.sleep(2)

        bot_result = session.game_command(bot_response)

        if not bot_result.is_success: 
            print("Something went wrong, please de-bug")
            print(f"{bot_result}")
                
    print()

else: 

    print(f"this user: {session.player_turn_manager.current_player.id} is a goat! it won this match")