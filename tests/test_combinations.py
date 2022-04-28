import itertools
from typing import Iterable, TypeVar

import pytest

from cohentools import combinations

T = TypeVar("T")

@pytest.mark.parametrize("seq", [
    [1, 2, 3, 4, 5],
    "abcdefg",
])
def test_kth_permutation(seq: Iterable[T]) -> None:
    for k, permutation in enumerate(itertools.permutations(seq)):
        assert combinations.kth_permutation(seq, k) == permutation
