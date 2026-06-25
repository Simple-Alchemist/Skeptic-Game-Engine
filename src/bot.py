"""
    Alright I admit that this is a bit of a mess. But it works
    This is a bot algorithm which is not well developed, it's just a spagetti code 
    with few mathematical operations to make the bot move
    After all, it works
    
"""

from attrs import define, field

from .service.data_classes import (
    GameSnapshot, 
    Result, 
    payload,

)

from .service.commands import *

from .core import ShellInterface, ItemType

@define(kw_only=True)
class BotAlgorithm: 

    _game_snapshot: GameSnapshot = field(alias="gs")
    _last_result: Result | None = field(alias="last_result", default=None)

    _peek_shell: ShellInterface | None = field(init=False, default=None)

    _bot_id: int = field(init=False)
    _bot_inventory: tuple[ItemType,...] = field(init=False, factory=tuple)
    _bot_health_contri: float = field(init=False)
    _bot_strength: float = field(init=False)

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

        players_spectrum: list[tuple[float, int]] = list()

    
        for player_data in self._game_snapshot.player_datas: 
            
            
            player_inventory_strength: float = self.__inventory_strength(inventory=player_data.inventory)
            player_health_contri: float = (player_data.health*100)/sum(players_health)

            player_strength: float = (player_inventory_strength + player_health_contri)/2

            if player_data.id == self._bot_id: 
        
                self._bot_strength = player_strength
                self._bot_health_contri = player_health_contri
                continue
            
            players_spectrum.append((player_strength, player_data.id))

            players_spectrum.sort(key=lambda x: x[0], reverse=True)

        return tuple(x[1] for x in players_spectrum)
        

    def think(self) -> interface.CommandInterface:

        players_spectrum: tuple[int,...] = self.__players_analysis()

        item_values: dict[ItemType, float] = dict()
    
        total_shells = self._game_snapshot.shotgun_data.blanks + self._game_snapshot.shotgun_data.lives

        live_probability: float = 0

        
        if isinstance(self._last_result, Result):

            if isinstance(self._last_result.payload, payload.ShellPayload):
                
                if self._last_result.payload.item_type == ItemType.PEEK_SHOTGUN:
                    if self._last_result.payload.shell_damage >= 1:
                        live_probability = 100
                    else:
                        live_probability = 0

        else:
             
            live_probability = (self._game_snapshot.shotgun_data.lives * 100) / total_shells


        commands: dict[ItemType, type[interface.CommandInterface]] = {

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
    
        final_command: interface.CommandInterface = PeekItemCommand() # just for initialization

        if  len(self._bot_inventory) > 0: 

            if 25 < live_probability < 75:

                
                item_values[ItemType.INVERSE_SHELL] = abs(live_probability - 50) + 49
                item_values[ItemType.EJECTOR] = abs(live_probability - 50) + 48
            
            item_values[ItemType.HAND_CUFF] = 100
            item_values[ItemType.TWO_FOLD] = live_probability 
            item_values[ItemType.PEEK_SHOTGUN] = abs(live_probability - 50) + 50
            item_values[ItemType.BANANA] = 100 - self._bot_health_contri

            # This bot couldn't handle the baista dausto
            # item_values[ItemType.BAISTA_DAUSTO] = 101-self._bot_health_contri
            # if isinstance(self._last_result, Result):

            #     if isinstance(self._last_result.payload, payload.BaistaDaustoPayload): 

            #         if not self._last_result.is_success: 
            #             item_values[ItemType.BAISTA_DAUSTO] = 0

            item_values[ItemType.U_TURN] = (100-self._bot_strength + live_probability) / 2
            item_values[ItemType.CHAREM] = 100 - self._bot_strength

            best_item = max(self._bot_inventory, key=lambda item: item_values.get(item, 0))

            final_command_type = commands[best_item]

            if issubclass(final_command_type, BaistaDaustoItemCommand):  

                final_command = final_command_type(target_player_id=players_spectrum[0])
        

            elif issubclass(final_command_type, HandCuffItemCommand): 

                final_command = final_command_type(target_player_id=players_spectrum[-1])

            else: 

                final_command = final_command_type() 

        else: 


            if live_probability >= 50:  
                
                final_command = ShootCommand(target_player_id=players_spectrum[0])
               
            
            elif live_probability < 50:  #shoot itelf
                
                final_command = ShootCommand(target_player_id=self._bot_id)

        return final_command

        
        
