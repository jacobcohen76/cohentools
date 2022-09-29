import itertools
from typing import (
  Any,
  Callable,
  Generic,
  Iterable,
  Iterator,
  SupportsIndex,
  TypeVar,
)

T = TypeVar('T')

def make_tree(array: list[T], op: Callable[[T, T], T]) -> list[T]:
  tree = [None] * (2 * len(array))
  for i in range(n := len(array)):
    tree[i + n] = array[i]
  for i in reversed(range(1, n)):
    tree[i] = op(tree[2 * i], tree[2 * i + 1])
  return tree

def update_tree(tree: list[T], op: Callable[[T, T], T], node: int, item: T) -> None:
  tree[node] = item
  while (node := node // 2) > 0:
    tree[node] = op(tree[2 * node], tree[2 * node + 1])

def query_tree(tree: list[T], op: Callable[[T, T], T], lower: int, upper: int, default: T) -> T:
  total = default
  while lower < upper:
    if lower & 1:
      total = op(total, tree[lower]); lower += 1
    if upper & 1:
      upper -= 1; total = op(total, tree[upper])
    lower //= 2; upper //= 2
  return total

class SegTree(Generic[T]):
  def __init__(self, items: Iterable[T], op: Callable[[T, T], T]) -> None:
    self._tree = make_tree(items := list(items), op)
    self._size = len(items)
    self._op   = op

  def query(self, i: int, j: int, default: T) -> T:
    return query_tree(self._tree, self._op, i + len(self), j + len(self), default)

  def __getitem__(self, idx: int) -> T:
    return self._tree[len(self) + idx]

  def __setitem__(self, idx: int, item: T) -> None:
    update_tree(self._tree, self._op, len(self) + idx, item)

  def __len__(self) -> int:
    return self._size

  def __iter__(self) -> Iterator[T]:
    return itertools.islice(self._tree, len(self), len(self._tree))

  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, SegTree):
      return NotImplemented
    return self._op == other._op \
       and all(a == b for a, b in zip(self, other))

  def __repr__(self) -> str:
    items = ", ".join(str(item) for item in self)
    return f"{type(self).__name__}([{items}], {self._op})"
