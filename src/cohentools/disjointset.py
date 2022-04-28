from typing import Any, Generic, Iterable, Iterator, Optional, TypeVar

from cohentools.utility import group_by

T  = TypeVar("T")

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

    def linked(self, x: T, y: T) -> bool:
        return self.find(x) == self.find(y)

    def groups(self) -> list[set[T]]:
        return list(group_by(self.parent.keys(), self.find, set).values())

    def __len__(self) -> int:
        return len(self.parent)

    def __iter__(self) -> Iterator[T]:
        return iter(self.parent.keys())

    def __contains__(self, item: T) -> bool:
        return item in self.parent

    def __bool__(self) -> bool:
        return bool(self.parent and self.counts)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DisjointSet):
            return NotImplemented
        return {tuple(group) for group in  self.groups()} == \
               {tuple(group) for group in other.groups()}

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, DisjointSet):
            return NotImplemented
        return not self == other

    def __repr__(self) -> str:
        find_table = {node: self.find(node) for node in self}
        return f"{type(self).__name__}({find_table})"

    def __str__(self) -> str:
        groups = self.groups()
        groups.sort(key=len, reverse=True)
        return f"{type(self).__name__}({groups})"
