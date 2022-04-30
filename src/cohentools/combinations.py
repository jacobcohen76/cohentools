import math
from typing import (
    Iterable,
    TypeVar,
)

T = TypeVar("T")

def kth_permutation(items: Iterable[T], k: int) -> tuple[T, ...]:
    items = list(items); k %= math.factorial(len(items))
    permutation = []
    while items:
        factorial = math.factorial(len(items) - 1)
        idx  = k // factorial
        k   %= factorial
        permutation.append(items.pop(idx))
    return tuple(permutation)
