import numpy as np
from DataStructures.DirectlyFollowsMatrix import DirectlyFollowsMatrix

class HeuristicMiner(object):
    def __init__(self, event_log):
        self.event_log = event_log
        self.matrix = DirectlyFollowsMatrix(self.event_log)
        self.key_to_index = {header: i for i, header in enumerate(self.matrix.keys)}

    def mine(self, activities=1.0, paths=1.0):

        # Step 1: Flatten the matrix and filter out zeros
        non_zero_values = [val for row in self.matrix.matrix for val in row if val != 0]
        number_of_values = len(non_zero_values)
        # Step 2: Sort the non-zero values and find the threshold for the lowest 50%
        sorted_non_zero = sorted(non_zero_values, reverse=True) #descending 100 50 1
        threshold_index = int(number_of_values * paths)
        if threshold_index < number_of_values:
            threshold = sorted_non_zero[threshold_index]

            # Step 3: Replace values below the threshold (except zeros) with zero
            for i in range(len(self.matrix.matrix)):
                for j in range(len(self.matrix.matrix)):
                    if self.matrix.matrix[i][j] != 0 and self.matrix.matrix[i][j] <= threshold:
                        self.matrix.matrix[i][j] = 0


        activity_count = self.matrix.activity_count_for_name()

        # Step 1: Sort the dictionary by value (ascending or descending)
        sorted_items = sorted(activity_count.items(), key=lambda x: x[1], reverse=True)  # reverse=True for descending

        num_items = len(sorted_items)
        keep_items = int(num_items * activities)
        keep_items = min(keep_items, num_items)

        remove_items = num_items - keep_items
        remove_items = max(remove_items, 0)

        if remove_items > 0:
            removed_half = sorted_items[keep_items:]
            for header, value in removed_half:
                index = self.matrix.keys.index(header)
                del self.matrix.keys[index]
                self.matrix.matrix = [row for idx, row in enumerate(self.matrix.matrix) if idx != index]
                self.matrix.matrix = [row[:index] + row[index+1:] for row in self.matrix.matrix]
