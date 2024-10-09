from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class maestro:
    action_name: str
    export: bool = True

    def __call__(
        self, 
        action: Any,
        *args: Any, 
        **kwds: Any
    ) -> Any:
        setattr(action, "maestro_meta", self)
        return action
    

@dataclass
class Action:
    action_name: str
    runs: str
    inputs: Dict[str, Any] = None

    