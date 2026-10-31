# algorithms/structures.py

class MaxHeap:
    """Custom Binary Max-Heap implemented from scratch for ADSA evaluation."""
    def __init__(self):
        self.heap = []

    def _parent(self, i):
        return (i - 1) // 2

    def _left_child(self, i):
        return (2 * i) + 1

    def _right_child(self, i):
        return (2 * i) + 2

    def insert(self, transaction):
        """Inserts a transaction and bubbles it up to maintain heap property O(log N)."""
        self.heap.append(transaction)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        """Helper to move the element up if it's larger than its parent."""
        parent_idx = self._parent(i)
        while i > 0 and self.heap[i].amount > self.heap[parent_idx].amount:
            # Swap
            self.heap[i], self.heap[parent_idx] = self.heap[parent_idx], self.heap[i]
            i = parent_idx
            parent_idx = self._parent(i)

    def get_highest_expense(self):
        """Instantly returns the highest spending transaction O(1)."""
        if not self.heap:
            return None
        return self.heap[0]  # Root of the max-heap is always the maximum