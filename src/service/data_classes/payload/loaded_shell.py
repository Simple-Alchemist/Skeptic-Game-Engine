from .interface import PayLoadInterface
from attrs import define

@define(kw_only=True)
class ShellLoadedPayload(PayLoadInterface):
    shell_loaded_damage: int
