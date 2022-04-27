from cohentools import DisjointSet

def test_disjoint_set_repr() -> None:
    disjoint = DisjointSet([1, 2, 3, 4, 5, 6, 7, 8])

    disjoint.union(1, 2)
    disjoint.union(1, 5)
    disjoint.union(1, 6)
    disjoint.union(1, 8)

    disjoint.union(3, 4)

    disjoint.union(7, 7)

    assert repr(disjoint) == "DisjointSet([{1, 2, 5, 6, 8}, {3, 4}, {7}])"
