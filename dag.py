from __future__ import annotations

from typing import Set, List, Optional, TypedDict


def _ancestors(key: str, nodes: TypedDict[str, List[str]]):
    ancestors = {key}
    if key in nodes:
        for value in nodes[key]:
            ancestors = ancestors.union(_ancestors(value, nodes))
    return ancestors


class DAG:
    """Directed Acyclic Graph"""
    graph: TypedDict[str, List[str]]
    inverted: TypedDict[str, List[str]]
    ancestors: TypedDict[str, List[str]]

    def __init__(self, edges: List[(str, Optional[str])]):
        """Initializes a DAG.

        Args:
            edges:
                A list of (child, parents) tuples.

        Examples:
            [
                ('A', []),
                ('B', ['A']),
                ('C', ['B'])
            ]

            [
                ('A', []),
                ('B', ['A']),
                ('C', ['B']),
                ('D', []),
                ('E', ['D']),
                ('F', ['C', 'E']),
                ('G', ['F']),
                ('H', ['G']),
            ]

        Raises:
            RuntimeError: If the input list in not topologically sorted.
        """
        self.graph = {}
        self.inverted = {}
        self.ancestors = {}
        for child, parents in edges:
            self.graph[child] = []
            self.inverted[child] = []
            for parent in parents:
                if parent not in self.graph:
                    raise RuntimeError("Invalid Input")
                self.graph[child].append(parent)
                self.inverted[parent].append(child)

    def get_leaves(self) -> Set[str]:
        """Collects all leaf nodes from the graph.

        A node is considered a leaf node if it has no children.

        Returns:
            A set of leaf nodes
        """
        leaves = set()
        for parent, children in self.inverted.items():
            if len(children) == 0:
                leaves.add(parent)
        return leaves

    def get_ancestors(self, value: str) -> Set[str]:
        """Collects ancestors for the provided node.

        Args:
            value: A node.

        Returns:
            A set of ancestors.

        """
        if value not in self.ancestors:
            self.ancestors[value] = _ancestors(value, self.graph)
        return self.ancestors[value]

    def get_bisect(self):
        """Determines the bisector nodes for the DAG.

        Returns:
            A set of bisector nodes.

        """
        n = len(self.graph.keys())
        minimums = {}
        maximum = 0
        for value in self.graph.keys():
            a = len(self.get_ancestors(value))
            minimum = min(a, n - a)
            values = minimums.get(minimum, set())
            values.add(value)
            minimums[minimum] = values
            if minimum > maximum:
                maximum = minimum
        return minimums[maximum]
