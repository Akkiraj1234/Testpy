
from queue import Queue


class Headless:
    def __init__(self, event_bus: Queue ):
        self.event_bus = event_bus
        
    def run(self):
        pass
