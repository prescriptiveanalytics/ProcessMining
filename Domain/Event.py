from dataclasses import dataclass
from datetime import datetime

class Event:
    def __init__(self, attributes, matched_attributes = None, non_matched_attributes = None, non_matched_headers = None):
        self.attributes = attributes
        self.matched_attributes = matched_attributes
        self.non_matched_attributes = non_matched_attributes
        self.non_matched_headers = non_matched_headers

    def __repr__(self):
        return f"Event({self.attributes})"

