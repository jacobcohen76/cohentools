import math

from cohentools import SegTree

def test_segtree() -> None:
    tree = SegTree(array := [1, 2, 3, 4, 5], min)
    for i in range(len(array)):
        for j in range(i, len(array) + 1):
            assert min(array[i:j], default=math.inf) == tree.query(i, j, default=math.inf)
