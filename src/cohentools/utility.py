from typing import Callable, Iterable, MutableSequence, MutableSet, overload, Type, TypeVar

T  = TypeVar("T")
KT = TypeVar("KT")
CT = TypeVar("CT")

def identity_fn(x: T) -> T:
    return x

@overload
def group_by(items: Iterable[T],
             key: Callable[[T], KT],
             collector: Type[list]) -> dict[KT, list[T]]: ...

@overload
def group_by(items: Iterable[T],
             key: Callable[[T], KT],
             collector: Type[set]) -> dict[KT, set[T]]: ...

def group_by(items: Iterable[T],
             key: Callable[[T], KT] = identity_fn,
             collector: Type[CT] = list) -> dict[KT, CT]:
    if issubclass(collector, MutableSequence):
        insert_fn = collector.append
    elif issubclass(collector, MutableSet):
        insert_fn = collector.add
    else:
        raise TypeError(f"collector must be a subclass of MutableSequence or MutableSet not {collector.__name__}")
    table = dict[KT, CT]()
    for item in items:
        group = table.setdefault(key(item), collector())
        insert_fn(group, item)
    return table
