from pandocfilters import attributes
import graphviz
import pandas as pd
import numpy as np

def add_to_matrix(self, a, b, activity_identifier):
    key_a = a.attributes[activity_identifier]
    key_b = b.attributes[activity_identifier]
    index_a = self.keys.index(key_a)
    index_b = self.keys.index(key_b)
    self.matrix[index_a][index_b] = self.matrix[index_a][index_b] + 1


class DirectlyFollowsMatrix(object):
    def __init__(self, event_log):
        self.event_log = event_log
        self.keys = []
        self.node_frequencies = {}
        for key, trace in event_log.traces.items():
            for event in trace.events:
                attributes = event.attributes
                key = attributes[event_log.activity_identifier]
                if key not in self.keys:
                    self.keys.append(key)

        n = len(self.keys)
        self.matrix = [[0] * n for _ in range(n)]

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
        df.columns = self.keys
        df.index = self.keys
        return df

    def graph_representation(self) -> graphviz.Digraph:
        np_matrix = np.array(self.matrix)
        max_freq = np_matrix.max()
        if max_freq == 0:
            print("Matrix is empty or contains only zeros. Cannot draw graph.")
            return None

        dot = graphviz.Digraph(comment='Directly-Follows Graph',
                               graph_attr={'rankdir': 'TB'})  # TB for Top to Bottom

        # --- 2. Create Nodes (Activities) ---
        for activity in self.keys:
            dot.node(activity, activity,
                     shape='box',
                     style='rounded, filled',
                     fillcolor='#4A88C1',
                     fontcolor='white')

        # --- 3. Create Edges (Flows) ---
        num_activities = len(self.keys)
        for i in range(num_activities):
            for j in range(num_activities):
                # Accessing elements in a NumPy array
                frequency = np_matrix[i, j]

                if frequency > 0:
                    source_activity = self.keys[i]
                    target_activity = self.keys[j]

                    # Calculate edge thickness proportional to frequency
                    pen_width = str(1 + 4 * (frequency / max_freq))

                    dot.edge(source_activity, target_activity,
                             label=str(frequency),
                             penwidth=pen_width,
                             color='#222222',
                             fontsize='10')
        return dot

    def activity_count_for_name(self):
        activity_count = {}
        np_matrix = np.array(self.matrix)
        key_to_index = {header: i for i, header in enumerate(self.keys)}

        for name, index in key_to_index.items():
            activity_count[name] = np_matrix[index, :].sum() + np_matrix[:, index].sum()

        return activity_count

    def activity_count_for_index(self):
        activity_count = {}
        np_matrix = np.array(self.matrix)
        key_to_index = {header: i for i, header in enumerate(self.keys)}

        for name, index in key_to_index.items():
            activity_count[index] = np_matrix[index, :].sum() + np_matrix[:, index].sum()

        return activity_count