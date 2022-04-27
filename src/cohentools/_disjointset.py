from typing import Any, Generic, Iterable, Optional, TypeVar

from ._utility import group_by

T  = TypeVar("T")
KT = TypeVar("KT")

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

    def groups(self) -> list[set[T]]:
        return list(group_by(self.parent.keys(), self.find, set).values())

    def __len__(self) -> int:
        return len(self.parent)

    def __iter__(self) -> Iterable[T]:
        return self.parent.keys()

    def __repr__(self) -> str:
        groups = self.groups()
        groups.sort(key=len, reverse=True)
        return f"{self.__class__.__name__}({groups})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DisjointSet):
            return NotImplemented
        return self.parent == other.parent and self.counts == other.counts

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, DisjointSet):
            return NotImplemented
        return not self == other
