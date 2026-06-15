from typing import Protocol, runtime_checkable

@runtime_checkable
class ItemInterface(Protocol):
    
    _id: int 
    _desc: str 

    @property
    def id(self): 
        ...

    @property
    def desc(self):
        ...