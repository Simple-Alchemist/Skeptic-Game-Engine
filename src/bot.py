from attrs import define, field
from statistics import mean, stdev
from typing import cast

from .service.data_classes import (
    GameSnapshot, 
    Result, 
    ActionType,
    ErrorType,
    payload,
    States
)

from .service.commands import *

from .core import ShellInterface, ItemType

@define(kw_only=True)
class BotAbility: 

    _game_snapshot: GameSnapshot = field(alias="gs")
    _last_result: Result = field(alias="last_result")
    _peek_shell: ShellInterface | None = field(init=False, default=None)
    _thread_values: dict[tuple[ItemType,...], int] = field(init=False, factory=dict)
    _competitors: set[int] = field(init=False, factory=set)
    _predators: set[int] = field(init=False, factory=set)
    _preys: set[int] = field(init=False, factory=set)
    _bot_id: int = field(init=False)
    _bot_inventory: tuple[ItemType,...] = field(init=False, factory=tuple)


    def __attrs_post_init__(self):

        self._thread_values.update({ # How can these Item can reduce win rate of bot

                (ItemType.HAND_CUFF,): 20,   
                (ItemType.PEEK_SHOTGUN, ItemType.TWO_FOLD):30 , 
                (ItemType.TWO_FOLD,): 5 ,    
                (ItemType.PEEK_SHOTGUN,):15 ,  
                (ItemType.CHAREM,): 40,  
                (ItemType.BANANA,):  10,      
                (ItemType.BAISTA_DAUSTO,): 45,
                (ItemType.EJECTOR,): 10,
                (ItemType.INVERSE_SHELL,): 10,
                (ItemType.U_TURN,): 10
            })

        

        self._bot_id = self._game_snapshot.turn_data.current_player_id

        self._bot_inventory: tuple[ItemType,...] = tuple()
        for player_data in  self._game_snapshot.player_datas: 
            if player_data.id == self._bot_id: 
                self._bot_inventory = player_data.inventory


    def __inventory_strength(self, inventory: tuple[ItemType,...]) -> int:

        strength_value: int  = 0
        
        for thvs in self._thread_values: 
            
            if set(thvs).issubset(inventory): 
                strength_value += self._thread_values[thvs]

        return strength_value
        
    def __extract_info(self):

        player_health: tuple[int,...] = tuple(player_data.health for player_data in self._game_snapshot.player_datas)

        mean_ = mean(player_health)
        stdev_ = stdev(player_health)

        health_data: tuple[float,float] = ((mean_- stdev_) , (mean_+ stdev_))
        
        for player_data in self._game_snapshot.player_datas: 

            if health_data[0] >= player_data.health >= health_data[1]:
                self._competitors.add(player_data.id)

            elif player_data.health < health_data[0]: 
                self._preys.add(player_data.id)

            elif player_data.health > health_data[1]:
                self._predators.add(player_data.id)

            total_thread_value: int = sum(thread_value for thread_value in self._thread_values.values())
            players_thread_value: float = (self.__inventory_strength(player_data.inventory)*100/total_thread_value)
            if players_thread_value > 75: 
                self._predators.add(player_data.id)

            elif players_thread_value < 25: 
                self._preys.add(player_data.id)

            else: 
                self._competitors.add(player_data.id)         

    def __analysis(self) -> tuple[float, int]: 
        """
        Calculates the bot's perceived winrate (Y-Axis) out of 100 and selects a target.
        Returns: (perceived_winrate, target_player_id)
        """
        self.__extract_info()

        # 1. Determine where the Bot itself sits in the food chain
        is_predator = self._bot_id in self._predators
        is_prey = self._bot_id in self._preys
        
        # Calculate percentage of prey on the board (0 to 100)
        total_players = len(self._game_snapshot.player_datas)
        prey_percentage = (len(self._preys) / total_players) * 100 if total_players > 0 else 0.0

        # Base winrate out of 100 based on status
        winrate = 40.0 # Default (Competitor)
        if is_predator: 
            winrate = 70.0
        elif is_prey: 
            winrate = 20.0

        # Add the percentage of prey to the winrate (Having more prey makes the board easier!)
        # We multiply by 0.5 so a 100% prey board adds +50 to the score without instantly breaking the cap.
        winrate += (prey_percentage * 0.5)

        # 2. Adjust winrate based on the "Hostility" of the board
        # If there are lots of predators, everyone's winrate effectively drops
        num_predators = len(self._predators)
        if not is_predator and num_predators > 0:
            winrate -= (10.0 * num_predators) # High paranoia (subtracts 10 per predator)!

        winrate = max(0.0, min(100.0, winrate)) # Clamp strictly between 0 and 100

        # 3. Choose the smartest Target
        target_id: int = -1
        
        # If Bot is a Predator: Bully the weak (Target Preys)
        if is_predator and self._preys:
            target_id = tuple(self._preys)[0] # Just grab the first prey
            
        # If Bot is Prey or Competitor: Try to take out the biggest threat!
        elif self._predators:
            target_id = tuple(self._predators)[0]
            
        # Fallback: Just target a competitor
        elif self._competitors:
            # Don't target yourself!
            valid_targets = [p for p in self._competitors if p != self._bot_id]
            if valid_targets: target_id = valid_targets[0]

        return winrate, target_id
    

    def think(self) -> interface.CommandInterface:

        item_values: dict[ItemType, float] = dict()
    
        winrate, target_id = self.__analysis()

        # 1. FIX: Prevent Division by Zero
        total_shells = self._game_snapshot.shotgun_data.blanks + self._game_snapshot.shotgun_data.lives

        live_probability: float = 0
        if isinstance(self._last_result.payload, payload.ShellPayload):
            
            if self._last_result.payload.item_type == ItemType.PEEK_SHOTGUN:
                live_probability = self._last_result.payload.shell_damage*100
             
        live_probability = (self._game_snapshot.shotgun_data.lives * 100) / total_shells


        commands: dict[ItemType, type[interface.InGameCommand]] = {

            ItemType.HAND_CUFF: HandCuffItemCommand,   
            ItemType.PEEK_SHOTGUN:PeekItemCommand, 
            ItemType.TWO_FOLD: TwoFoldItemCommand ,    
            ItemType.CHAREM: CharemItemCommand,  
            ItemType.BANANA:  BananaItemCommand,      
            ItemType.BAISTA_DAUSTO: BaistaDaustoItemCommand,
            ItemType.EJECTOR: EjectorItemCommand,
            ItemType.INVERSE_SHELL: RandomInverseShellItemCommand,
            ItemType.U_TURN: UTurnItemCommand
        }
        # 2. FIX: Check if inventory has AT LEAST 1 item
        if not len(self._bot_inventory) > 0: 
            return ShootCommand(target_player_id=target_id)

        item_values[ItemType.HAND_CUFF] = (100 - winrate + live_probability - 100) / 2
        item_values[ItemType.TWO_FOLD] = live_probability
        item_values[ItemType.PEEK_SHOTGUN] = abs(live_probability - 50) + 50
        item_values[ItemType.INVERSE_SHELL] = abs(live_probability - 50) + 49
        item_values[ItemType.EJECTOR] = abs(live_probability - 50) + 48
        item_values[ItemType.BANANA] = 100 - winrate
        item_values[ItemType.BAISTA_DAUSTO] = -winrate + 1
        item_values[ItemType.U_TURN] = (winrate + live_probability) / 2
        item_values[ItemType.CHAREM] = 102 - winrate

        best_item = max(self._bot_inventory, key=lambda item: item_values.get(item, 0))

        final_command = commands[best_item]

        if issubclass(final_command, interface.TargetPlayerCommandInterface):

            return final_command(target_player_id=target_id)
        
        elif issubclass(final_command, interface.ItemCommandInterface):
            return final_command()

        
        return ShootCommand(target_player_id=target_id)


        
        
