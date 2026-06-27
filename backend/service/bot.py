"""
    Alright I admit that this is a bit of a mess. But it works
    This is a bot algorithm which is not well developed, it's just a spagetti code 
    with few mathematical operations to make the bot move
    After all, it works
    
"""

from attrs import define, field

from .data_classes import (
    GameSnapshot, 
    Result, 
    payload,

)

from .commands.interface import CommandInterface

from ..core import ShellInterface, ItemType


@define(kw_only=True)
class BotAlgorithm: 

    _game_snapshot: GameSnapshot = field(alias="gs")
    _last_result: Result | None = field(alias="last_result", default=None)

    _peek_shell: ShellInterface | None = field(init=False, default=None)

    _bot_id: int = field(init=False)
    _bot_inventory: tuple[ItemType,...] = field(init=False, factory=tuple)
    _bot_health_contri: float = field(init=False)
    _bot_relative_strength: float = field(init=False)

    _preys: list = field(factory=list)
    _predators: list = field(factory=list)

    def __attrs_post_init__(self):

        self._bot_id = self._game_snapshot.turn_data.current_player_id

        self._bot_inventory: tuple[ItemType,...] = tuple()

        for player_data in  self._game_snapshot.player_datas: 
            if player_data.id == self._bot_id: 
                self._bot_inventory = player_data.inventory

    def __inventory_strength(self, inventory: tuple[ItemType,...]) -> float:

        item_weight_sum: int = sum(item.weight for item in ItemType.item_available()) 
        # lesser the weight, the more strength the inventory holds
        given_inventory_weight: int = sum(item.weight for item in inventory)

        return 100-((given_inventory_weight*100)/item_weight_sum)
    
    def __players_analysis(self) -> tuple[int,...]: 

        players_health: tuple[int,...] = tuple(player_data.health for player_data in self._game_snapshot.player_datas)

        player_strength_dict: list[tuple[float, int]] = list()
        total_strength_list: list[float] = list() 

    
        for player_data in self._game_snapshot.player_datas: 
            
            
            player_inventory_strength: float = self.__inventory_strength(inventory=player_data.inventory)
            player_health_contri: float = (player_data.health*100)/sum(players_health)

            player_strength: float = (player_inventory_strength + player_health_contri)/2
            bot_strength: float = 0.0

            if player_data.id == self._bot_id: 
        
                bot_strength = player_strength
                self._bot_health_contri = player_health_contri
                continue
            
            player_strength_dict.append((player_strength, player_data.id))
            total_strength_list.append(player_strength)

            self._bot_relative_strength = bot_strength/sum(total_strength_list)

            player_strength_dict.sort(key=lambda x: x[0], reverse=True)

        return tuple(x[1] for x in player_strength_dict)
        

    def think(self) -> CommandInterface:

        # 1. Target Analysis
        players_spectrum: tuple[int,...] = self.__players_analysis()

        target_enemy = players_spectrum[0] 
        target_weakest = players_spectrum[-1] 

        # 2. Base Probability Calculation
        total_shells = self._game_snapshot.shotgun_data.blanks + self._game_snapshot.shotgun_data.lives
        live_probability: float = (self._game_snapshot.shotgun_data.lives * 100) / total_shells 
        
        force_shoot = False

        if isinstance(self._last_result, Result):
            payload_data = self._last_result.payload
            
            if isinstance(payload_data, payload.ShellPayload):
                if payload_data.item_type == ItemType.TWO_FOLD:
                    force_shoot = True
                
    
            if isinstance(payload_data, payload.ShellPayload):
                if payload_data.item_type == ItemType.PEEK_SHOTGUN:
                    live_probability = 100.0 if payload_data.shell_damage >= 1 else 0.0

        item_values: dict[ItemType, float] = {}
        

        if len(self._bot_inventory) > 0:
            # Converting inventory to a set so we evaluate items we actually own (getting rid of duplication)
            inventory_set = set(self._bot_inventory)

            if ItemType.INVERSE_SHELL in inventory_set:

                if 25 >= live_probability >= 75:
                    force_shoot = True

                else: 

                    item_values[ItemType.INVERSE_SHELL] = 90

                
            if ItemType.EJECTOR in inventory_set:
                
                if 25 >= live_probability >= 75:
                    force_shoot=  True

                elif live_probability > 50: 
                    item_values[ItemType.EJECTOR] = 100-live_probability

                elif live_probability < 50: 
                    item_values[ItemType.EJECTOR] = live_probability

                else: 
                    item_values[ItemType.EJECTOR] = 100
                
            if ItemType.HAND_CUFF in inventory_set:

                item_values[ItemType.HAND_CUFF] = 100
                
            if ItemType.TWO_FOLD in inventory_set:

                item_values[ItemType.TWO_FOLD] = live_probability 
                
            if ItemType.PEEK_SHOTGUN in inventory_set:
                
                item_values[ItemType.PEEK_SHOTGUN] = 0 if (live_probability == 100 or live_probability == 0) else 100
                
            if ItemType.BANANA in inventory_set:

                item_values[ItemType.BANANA] = 100

            if ItemType.U_TURN in inventory_set:
                item_values[ItemType.U_TURN] = (100 - self._bot_relative_strength+ live_probability) / 2 # this is some random calculation ._.
                
            if ItemType.CHAREM in inventory_set:

                if self._bot_relative_strength < 50:
                    item_values[ItemType.CHAREM] = 100 - self._bot_relative_strength

        else: 

            force_shoot = True


        from ..api import InGameCommandFactory  
        if not force_shoot :

                                
            best_item = max(self._bot_inventory, key=lambda item: item_values.get(item, 0))
            
            final_command = InGameCommandFactory.manufacture_item_command(item_type=best_item, target_player_id =target_enemy )
            return final_command
            
        else:
            
            if live_probability >= 50: 
                return InGameCommandFactory.manufacture_shoot_command(target_player_id=target_weakest)

            else:  
                return InGameCommandFactory.manufacture_shoot_command(target_player_id=self._bot_id)

