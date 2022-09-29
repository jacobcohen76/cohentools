import collections
from typing import (
  Any,
  Callable,
  Generic,
  Hashable,
  Iterable,
  Iterator,
  TypeVar,
)

KT = TypeVar('KT', bound=Hashable)
VT = TypeVar('VT')

class DisjointSetFold(Generic[KT, VT]):
  def __init__(self, op: Callable[[VT, VT], VT], items: Iterable[tuple[KT, VT]] | None = None) -> None:
    self._op                    = op
    self._parent: dict[KT, KT]  = {}
    self._size:   dict[KT, int] = {}
    self._table:  dict[KT, VT]  = {}
    if items is not None:
      self.update(items)

  def find(self, node: KT) -> KT:
    while node != self._parent[node]:
      self._parent[node] = node = self._parent[self._parent[node]]
    return node

  def union(self, x: KT, y: KT, *nodes: KT) -> None:
    if (x := self.find(x)) != (y := self.find(y)):
      if self._size[x] < self._size[y]:
        x, y = y, x
      self._parent[y] = x; self._size[x] += self._size.pop(y)
      self._table[x]  = self._op(self._table[x], self._table.pop(y))
    for y in nodes:
      if x != (y := self.find(y)):
        if self._size[x] < self._size[y]:
          x, y = y, x
        self._parent[y] = x; self._size[x] += self._size.pop(y)
        self._table[x]  = self._op(self._table[x], self._table.pop(y))

  def merge(self, nodes: Iterable[KT]) -> None:
    itr = iter(items)
    try:
      self.union(next(itr), next(itr), *itr)
    finally: ...

  def linked(self, x: KT, y: KT) -> bool:
    return self.find(x) == self.find(y)

  def groups(self) -> int:
    return len(self._size)

  def groupsize(self, node: KT) -> int:
    return self._size[self.find(node)]

  def itergroups(self) -> Iterable[set[KT]]:
    table = collections.defaultdict(set)
    for node in self:
      table[self.find(node)].add(node)
    return table.values()

  def itergroups_acc(self) -> Iterable[tuple[set[KT], VT]]:
    return ((group, self[next(iter(group))]) for group in self.itergroups())

  def __len__(self) -> int:
    return len(self._parent)

  def __iter__(self) -> Iterator[KT]:
    return iter(self._parent)

  def __contains__(self, key: KT) -> bool:
    return key in self._parent

  def __getitem__(self, key: KT) -> VT:
    return self._table[self.find(key)]

  def __setitem__(self, key: KT, val: VT) -> None:
    if key in self:
      raise KeyError(f'{key} already exists')
    self._parent[key] = key
    self._size[key]   = 1
    self._table[key]  = val

  def update(self, items: Iterable[tuple[KT, VT]]) -> None:
    for key, val in items:
      self[key] = val

  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, DisjointSetFold):
      return NotImplemented
    return self._op == other._op and \
      sorted((sorted(group), acc) for group, acc in  self.itergroups_acc()) == \
      sorted((sorted(group), acc) for group, acc in other.itergroups_acc())

  def __repr__(self) -> str:
    groups_acc = sorted((sorted(group), acc) for group, acc in self.itergroups_acc())
    groups_acc = ', '.join(f'({{{", ".join(f"{item}" for item in group)}}}, {acc})'
                           for group, acc in groups_acc)
    return f'{type(self).__name__}({self._op}, [{groups_acc}])'
