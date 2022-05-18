from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    Optional,
    TypeVar,
)

T = TypeVar("T")

class DisjointSet(Generic[T]):
    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self._parent = dict[T, T]()
        self._rank   = dict[T, int]()
        for item in items or ():
            self.add(item)

    def add(self, node: T) -> None:
        self._parent.setdefault(node, node)
        self._rank.setdefault(node, 0)

    def find(self, node: T) -> T:
        while self._parent[node] != node:
            self._parent[node] = self._parent[self._parent[node]]
            node = self._parent[node]
        return node

    def union(self, x: T, y: T, *items: T) -> None:
        x = self.find(x)
        for y in (y, *items):
            y = self.find(y)
            if self._rank[x] < self._rank[y]:
                x, y = y, x
            self._parent[y] = x
            self._rank[x]  += self._rank[x] == self._rank[y]

    def linked(self, x: T, y: T) -> bool:
        return self.find(x) == self.find(y)

    def groups(self) -> list[tuple[T, ...]]:
        table = dict[T, list[T]]()
        for node in self:
            group = table.setdefault(self.find(node), [])
            group.append(node)
        return [tuple(group) for group in table.values()]

    def __len__(self) -> int:
        return len(self._parent)

    def __iter__(self) -> Iterator[T]:
        return iter(self._parent.keys())

    def __contains__(self, item: T) -> bool:
        return item in self._parent

    def __bool__(self) -> bool:
        return bool(self._parent)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DisjointSet):
            return NotImplemented
        return set(self.groups()) == set(other.groups())

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, DisjointSet):
            return NotImplemented
        return not self == other

    def __repr__(self) -> str:
        groups = self.groups(); groups.sort(key=len, reverse=True)
        groups = [sorted(group, key=lambda x: (-self._rank[x], x)) for group in self.groups()]
        groups = ", ".join("{" + ", ".join(f"{item}" for item in group) + "}" for group in groups)
        return f"{type(self).__name__}([{groups}])"
