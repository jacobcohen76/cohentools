import collections
from typing import (
  Any,
  Generic,
  Hashable,
  Iterable,
  Iterator,
  TypeVar,
)

T = TypeVar('T', bound=Hashable)

class DisjointSet(Generic[T]):
  def __init__(self, nodes: Iterable[T] | None = None) -> None:
    self._parent: dict[T, T]   = {}
    self._size:   dict[T, int] = {}
    if nodes is not None:
      self.update(nodes)

  def add(self, node: T) -> None:
    if node not in self:
      self._parent[node] = node; self._size[node] = 1

  def update(self, nodes: Iterable[T]) -> None:
    for node in nodes:
      self.add(node)

  def find(self, node: T) -> T:
    while node != self._parent[node]:
      self._parent[node] = node = self._parent[self._parent[node]]
    return node

  def union(self, x: T, y: T, *nodes: T) -> None:
    if (x := self.find(x)) != (y := self.find(y)):
      if self._size[x] < self._size[y]:
        x, y = y, x
      self._parent[y] = x; self._size[x] += self._size.pop(y)
    for y in nodes:
      if x != (y := self.find(y)):
        if self._size[x] < self._size[y]:
          x, y = y, x
        self._parent[y] = x; self._size[x] += self._size.pop(y)

  def merge(self, nodes: Iterable[T]) -> None:
    itr = iter(nodes)
    try:
      self.union(next(itr), next(itr), *itr)
    finally: ...

  def linked(self, x: T, y: T) -> bool:
    return self.find(x) == self.find(y)

  def groups(self) -> int:
    return len(self._size)

  def groupsize(self, node: T) -> int:
    return self._size[self.find(node)]

  def itergroups(self) -> Iterable[set[T]]:
    table = collections.defaultdict(set)
    for node in self:
      table[self.find(node)].add(node)
    return table.values()

  def __len__(self) -> int:
    return len(self._parent)

  def __iter__(self) -> Iterator[T]:
    return iter(self._parent.keys())

  def __contains__(self, item: T) -> bool:
    return item in self._parent

  def __bool__(self) -> bool:
    return bool(len(self))

  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, DisjointSet):
      return NotImplemented
    return sorted(sorted(group) for group in  self.itergroups()) \
        == sorted(sorted(group) for group in other.itergroups())

  def __repr__(self) -> str:
    groups = sorted(sorted(group) for group in self.itergroups())
    groups = ', '.join(f'{{{", ".join(f"{item}" for item in group)}}}'
                       for group in groups)
    return f'{type(self).__name__}([{groups}])'
