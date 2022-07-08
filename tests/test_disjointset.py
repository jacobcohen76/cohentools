from cohentools import DisjointSet

def test_disjoint_set_eq() -> None:
    disjoint1 = DisjointSet([1, 2, 3, 4, 5, 6, 7, 8])
    disjoint1.union(1, 2, 5, 6, 8)
    disjoint1.union(3, 4)
    disjoint1.union(7, 7)

    disjoint2 = DisjointSet([1, 2, 3, 4, 5, 6, 7, 8])
    disjoint2.union(8, 6, 5, 2, 1)
    disjoint2.union(3, 4)
    disjoint2.union(7, 7)

    assert disjoint1 == disjoint2
