from pandocfilters import attributes
import pandas as pd

def add_to_matrix(self, a, b, activity_identifier):
    key_a = a.attributes[activity_identifier]
    key_b = b.attributes[activity_identifier]
    index_a = self.keys.index(key_a)
    index_b = self.keys.index(key_b)
    if self.matrix[index_a][index_b] is None:
        self.matrix[index_a][index_b] = "→"
    elif self.matrix[index_a][index_b] == "←":
        self.matrix[index_a][index_b] = "↔"

    if self.matrix[index_b][index_a] is None:
        self.matrix[index_b][index_a] = "←"
    elif self.matrix[index_b][index_a] == "→":
        self.matrix[index_b][index_a] = "↔"


class CausalDependencyMatrix:
    def __init__(self, event_log):
        self.event_log = event_log
        self.keys = []
        for key, trace in event_log.traces.items():
            for event in trace.events:
                attributes = event.attributes
                key = attributes[event_log.activity_identifier]
                if key not in self.keys:
                    self.keys.append(key)

        n = len(self.keys)
        self.matrix = [[None] * n for _ in range(n)]

        for key, trace in event_log.traces.items():
            for a, b in zip(trace.events, trace.events[1:]):
                add_to_matrix(self, a, b, event_log.activity_identifier)


    def __repr__(self):
        res = ""
        for key in self.keys:
            res += f"{key}\t"
        res += "\n"
        for row in self.matrix:
            for col in row:
                res += f"{col}\t"
            res += "\n"
        return res

    def data_frame_representation(self) -> pd.DataFrame:
        df = pd.DataFrame(self.matrix)
        df_display = df.fillna("")
        df_display.columns = self.keys
        df_display.index = self.keys
        return df_display
