from cohentools import combinations

import itertools
from typing import Iterable, TypeVar

import pytest

T = TypeVar("T")

@pytest.mark.parametrize("seq", [
    [1, 2, 3, 4, 5],
    "abcdefg",
])
def test_kth_permutation(seq: Iterable[T]) -> None:
    for k, permutation in zip(itertools.count(), itertools.permutations(seq)):
        assert combinations.kth_permutation(seq, k) == permutation
