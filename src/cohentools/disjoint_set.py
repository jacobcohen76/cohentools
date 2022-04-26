from typing import Generic, Optional, TypeVar

T = TypeVar("T")

class DisjointSet(Generic[T]):
    def __init__(self, parent: Optional[dict[T, T]]   = None,
                       counts: Optional[dict[T, int]] = None) -> None:
        self.parent = parent or {}
        self.counts = counts or {}

    def add(self, node: T) -> None:
        self.parent.setdefault(node, node)
        self.counts.setdefault(node, 1)

    def find(self, node: T) -> T:
        while self.parent[node] != node:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, x: T, y: T) -> None:
        x = self.find(x); y = self.find(y)
        if self.counts[x] < self.counts[y]:
            x, y = y, x
        self.parent[y]  = x
        self.counts[y] += self.counts[x]
