import itertools
from typing import Any, Callable, Generic, Iterable, Iterator, SupportsIndex, TypeVar

T = TypeVar("T")

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
        self.tree = make_tree(items := list(items), op)
        self.size = len(items)
        self.op   = op

    def query(self, i: int, j: int, default: T) -> T:
        return query_tree(self.tree, self.op, i + len(self), j + len(self), default)

    def __getitem__(self, key: SupportsIndex) -> T:
        if not isinstance(key, SupportsIndex):
            raise TypeError(f"SegTree indices must be integers, not {type(key).__name__}")
        return self.tree[key + len(self)]

    def __setitem__(self, key: SupportsIndex, item: T) -> None:
        if not isinstance(key, SupportsIndex):
            raise TypeError(f"SegTree indices must be integers, not {type(key).__name__}")
        update_tree(self.tree, self.op, key + len(self), item)

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[T]:
        return itertools.islice(self.tree, self.size, len(self.tree))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SegTree):
            return NotImplemented
        return self.op == other.op and \
            all(a == b for a, b in zip(self, other))

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, SegTree):
            return NotImplemented
        return not self == other

    def __repr__(self) -> str:
        items = ", ".join(str(item) for item in self)
        return f"{type(self).__name__}([{items}], {self.op!r})"
