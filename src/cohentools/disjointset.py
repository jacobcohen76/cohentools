from typing import Generic, Iterable, Optional, TypeVar

T = TypeVar("T")

class DisjointSet(Generic[T]):
    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self.parent = dict[T, T]()
        self.counts = dict[T, int]()
        for item in items or []:
            self.add(item)

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
