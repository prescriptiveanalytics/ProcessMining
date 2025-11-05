import csv
import io
from datetime import datetime
from typing import List
from Domain.Event import Event
from Domain.Trace import Trace

class EventLog:
    def __init__(self,
                 case_identifier="Case ID",
                 event_identifier="Event ID",
                 timestamp_identifier="Timestamp",
                 activity_identifier="Activity",
                 resource_identifier="Resource",
                 cost_identifier="Cost"):
        self.traces = None
        self.split_symbol = ';'
        self.case_identifier = case_identifier
        self.event_identifier = event_identifier
        self.timestamp_identifier = timestamp_identifier
        self.activity_identifier = activity_identifier
        self.resource_identifier = resource_identifier
        self.cost_identifier = cost_identifier

    def from_csv_file(self, file_path: str):
        traces = {}
        with open(file_path, 'r') as file:
            lines = file.readlines()
            header = [h.strip() for h in lines[0].strip().split(self.split_symbol)]

            identifiers = [self.case_identifier,
                           self.event_identifier,
                           self.timestamp_identifier,
                           self.activity_identifier,
                           self.resource_identifier,
                           self.cost_identifier]

            # Create a mapping from identifier to its index in the header
            identifier_to_index = {}
            for identifier in identifiers:
                if identifier in header:
                    identifier_to_index[identifier] = header.index(identifier)
            if len(identifier_to_index) == 0:
                return EventLog()

            for line in lines[1:]:
                reader = csv.reader(io.StringIO(line), delimiter=self.split_symbol)
                parts = []
                for row in reader:
                    # Iterate over each cell in the row
                    for cell in row:
                        parts.append(cell)

                # Create a dictionary of attributes
                attributes = {}
                matched_attributes = []
                non_matched_attributes = {}
                non_matched_headers = []
                faulty_event = False
                for identifier, index in identifier_to_index.items():
                    if index < len(parts):
                        if identifier is self.activity_identifier:
                            if not parts[index]:
                                faulty_event = True
                                break
                        attributes[identifier] = parts[index]
                        matched_attributes.append(identifier)

                if faulty_event:
                    continue

                for index in range(len(header)):
                    if index not in identifier_to_index.items():
                        non_matched_attributes[index] = parts[index]
                        non_matched_headers.append(header[index])


                # Create an Event object with the attributes
                event = Event(attributes=attributes,
                              matched_attributes=matched_attributes,
                              non_matched_attributes=non_matched_attributes,
                              non_matched_headers=non_matched_headers)

                # Use the 'case_identifier' attribute as the case_id for the trace
                case_id = attributes.get(self.case_identifier, 'Unknown')
                if case_id not in traces:
                    traces[case_id] = Trace(case_id=case_id, events=[])
                traces[case_id].events.append(event)
            self.traces = traces
        return None
        


