
import heapq
from collections import Counter


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):

    frequency = Counter(text)

    heap = [
        Node(char, freq)
        for char, freq in frequency.items()
    ]

    heapq.heapify(heap)

    if not heap:
        return None

    while len(heap) > 1:

        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        new_node = Node(
            None,
            left.freq + right.freq
        )

        new_node.left = left
        new_node.right = right

        heapq.heappush(heap, new_node)

    return heap[0]


def generate_codes(root, code="", codes=None):

    if codes is None:
        codes = {}

    if root is None:
        return codes

    if root.char is not None:
        codes[root.char] = code if code else "0"
        return codes

    generate_codes(root.left, code + "0", codes)
    generate_codes(root.right, code + "1", codes)

    return codes
