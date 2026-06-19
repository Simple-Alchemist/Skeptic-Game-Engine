
from attrs import define, field
from .item_type import ItemType

from attrs import define, field

from .exception import  ItemException


@define
class Inventory:

    _items_list: list[ItemType] = field(factory=list, init=False)
    
    @property
    def items_list(self) -> tuple[ItemType,...]:

        return tuple(self._items_list)
    
    def is_item_present(self, item: ItemType):
        
        return item in self._items_list
    
    def add_item(self, item: ItemType) -> None: 

        self._items_list.append(item)

    def remove_item(self, item: ItemType) -> None: 

        try:
            self._items_list.remove(item)

        except ValueError:

            raise ItemException(f"Item of '{item}' isn't present in the inventory")

    def clear_inventory(self) -> None: 

        self._items_list.clear()
        




        
