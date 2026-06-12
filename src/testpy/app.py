from __future__ import annotations
from queue import Queue
from typing import Any


class TestpyApp:
    def __init__(
        self, 
        config: dict[str, Any], 
        event_bus: Queue,
        args
    ) -> None:
        self.config = config
        self.event_bus = event_bus
        self.args = args

    def run(self) -> None:
        pass
