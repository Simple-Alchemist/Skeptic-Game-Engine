from ..core import ItemType
from ..service.commands import *
from ..service.commands.interface import CommandInterface

class InGameCommandFactory:

    @staticmethod
    def manufacture_item_command(item_type: ItemType, **kwargs) -> CommandInterface:

        commands: dict[ItemType, type[CommandInterface]] = {

                ItemType.HAND_CUFF: HandCuffItemCommand,    #target_player_id
                ItemType.PEEK_SHOTGUN: PeekItemCommand, 
                ItemType.TWO_FOLD: TwoFoldItemCommand,    
                ItemType.CHAREM: CharemItemCommand,  
                ItemType.BANANA: BananaItemCommand,      
                ItemType.BAISTA_DAUSTO: BaistaDaustoItemCommand, #target_player_id
                ItemType.EJECTOR: EjectorItemCommand,
                ItemType.INVERSE_SHELL: RandomInverseShellItemCommand,
                ItemType.U_TURN: UTurnItemCommand
            }

        concrete_command: CommandInterface = PeekItemCommand()

        command_type: type[CommandInterface] = commands[item_type] 

        if item_type == ItemType.HAND_CUFF or item_type== ItemType.BAISTA_DAUSTO: 

            try: 

                target_player_id: int = kwargs["target_player_id"]


                if issubclass(command_type, (HandCuffItemCommand, BaistaDaustoItemCommand)): 

                    concrete_command: CommandInterface = command_type(target_player_id=target_player_id)

            except KeyError: 

                raise Exception("target_player_id wasn't passed")
            
        else: 

            concrete_command: CommandInterface = command_type()

        return concrete_command

    @staticmethod
    def manufacture_shoot_command(target_player_id: int) -> CommandInterface: 

        return ShootCommand(target_player_id=target_player_id)
