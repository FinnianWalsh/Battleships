from typing import Any, Optional


class Player:
    instances = 0

    def __init__(self, name: Optional[str] = None):
        assign = super().__setattr__
        assign("name", name)
        Player.instances += 1
        assign("instance", Player.instances)

    def __getattribute__(self, item: str) -> Any:
        value = object.__getattribute__(self, item)

        if value is None:
            raise AttributeError(f"{item} has not been initialized")
        return value

    def __setattr__(self, key: str, value: Any):
        if object.__getattribute__(self, key) is None:
            object.__setattr__(self, key, value)
        else:
            raise AttributeError(f"{key} has already been initialized with {value}")
