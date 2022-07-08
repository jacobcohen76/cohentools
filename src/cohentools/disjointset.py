from typing import (
  Any,
  Generic,
  Hashable,
  Iterable,
  Iterator,
  TypeVar,
)

T = TypeVar("T", bound=Hashable)

class DisjointSet(Generic[T]):
  def __init__(self, nodes: Iterable[T] | None = None) -> None:
    self.parent: dict[T, T]   = {}
    self.size:   dict[T, int] = {}
    if nodes is not None:
      self.update(nodes)

  def add(self, node: T) -> None:
    if node not in self:
      self.parent[node] = node; self.size[node] = 1

  def update(self, nodes: Iterable[T]) -> None:
    for node in nodes:
      self.add(node)

  def find(self, node: T) -> T:
    while self.parent[node] != node:
      self.parent[node] = node = self.parent[self.parent[node]]
    return node

  def union(self, x: T, y: T, *items: T) -> None:
    if (x := self.find(x)) != (y := self.find(y)):
      if self.size[x] < self.size[y]:
        x, y = y, x
      self.parent[y] = x
      self.size[x]  += self.size.pop(y)
    for y in items:
      if x != (y := self.find(y)):
        if self.size[x] < self.size[y]:
          x, y = y, x
        self.parent[y] = x
        self.size[x]  += self.size.pop(y)

  def merge(self, items: Iterable[T]) -> None:
    itr = iter(items)
    try:
      self.union(next(itr), next(itr), *itr)
    finally: ...

  def linked(self, x: T, y: T) -> bool:
    return self.find(x) == self.find(y)

  def groups(self) -> int:
    return len(self.size)

  def groupsize(self, node: T) -> int:
    return self.size[self.find(node)]

  def itergroups(self) -> Iterable[set[T]]:
    table: dict[T, set[T]] = {}
    for node in self:
      group = table.setdefault(self.find(node), set())
      group.add(node)
    return table.values()

  def __len__(self) -> int:
    return len(self.parent)

  def __iter__(self) -> Iterator[T]:
    return iter(self.parent.keys())

  def __contains__(self, item: T) -> bool:
    return item in self.parent

  def __bool__(self) -> bool:
    return bool(len(self))

  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, DisjointSet):
      return NotImplemented
    return sorted(self.itergroups()) == sorted(other.itergroups())

  def __ne__(self, other: Any) -> bool:
    if not isinstance(other, DisjointSet):
      return NotImplemented
    return not self == other

  def __repr__(self) -> str:
    return f"{type(self).__name__}({list(self.itergroups())})"
