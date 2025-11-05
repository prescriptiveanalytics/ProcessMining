from typing import List
from Domain.Event import Event

class Trace:
    case_id: str
    events: List[Event]

    def __init__(self, case_id: str, events: List[Event]):
        self.case_id = case_id
        self.events = events

    def __repr__(self):
        return f"Trace({self.case_id}, {len(self.events)} events)"