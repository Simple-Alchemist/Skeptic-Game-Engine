from typing import Protocol, runtime_checkable

@runtime_checkable
class ItemInterface(Protocol):
    """
    Item Interface Class which allows you to create Concrete Item
    
    
    Attributes:
        _id: int -> Holds a ID 
        _desc: str -> a bit of description of the item
    """
    _id: int 
    _desc: str 

    @property
    def id(self) -> int: 
        """id property, returning the id of the item in integer"""
        ...

    @property
    def desc(self) -> str:
        """desc property, returning the description of the item in string"""
        ...