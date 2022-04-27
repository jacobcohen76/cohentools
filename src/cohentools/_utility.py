from enum import Enum
from typing import Callable, Iterable, MutableSequence, MutableSet, Type, TypeVar, overload

T  = TypeVar("T")
KT = TypeVar("KT")
CT = TypeVar("CT")

@overload
def group_by(items: Iterable[T],
             key_fn: Callable[[T], KT],
             collector: Type[list]) -> dict[KT, list[T]]: ...

@overload
def group_by(items: Iterable[T],
             key_fn: Callable[[T], KT],
             collector: Type[set]) -> dict[KT, set[T]]: ...

def group_by(items: Iterable[T],
             key_fn: Callable[[T], KT],
             collector: Type[CT] = list) -> dict[KT, CT]:
    if issubclass(collector, MutableSequence):
        insert_fn = collector.append
    elif issubclass(collector, MutableSet):
        insert_fn = collector.add
    else:
        raise Exception("collector must be an instance of MutableSequence or MutableSet")
    table = dict[KT, CT]()
    for item in items:
        group = table.setdefault(key_fn(item), collector())
        insert_fn(group, item)
    return table
