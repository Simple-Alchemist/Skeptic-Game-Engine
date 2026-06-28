
from attrs import define, field
from .item_type import ItemType

from attrs import define, field

from .exception import  ItemException


@define
class Inventory:

    _items_list: list[ItemType] = field(factory=list, init=False)
    _limit: int = field(default=4, alias="limit")
    
    @property
    def items_tuple(self) -> tuple[ItemType,...]:

        return tuple(self._items_list)
    
    @property
    def reached_limit(self) -> bool: 
        return len(self._items_list) >= self._limit
    
    def is_item_present(self, item: ItemType):
        
        return item in self._items_list
    
    def add_items(self, item_tuple: tuple[ItemType,...], forced: bool = False) -> None: 

        if (not forced) and (len(self._items_list) + len(item_tuple) > self._limit):

            raise ItemException("Surpassing Inventory's limit ")
        
        self._items_list.extend(item_tuple)



    def remove_item(self, item: ItemType) -> None: 

        try:
            self._items_list.remove(item)

        except ValueError:

            raise ItemException(f"Item of '{item}' isn't present in the inventory")
        

    def clear(self) -> None: 

        self._items_list.clear()
        




        
