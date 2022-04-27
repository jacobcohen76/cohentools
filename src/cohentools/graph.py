import dataclasses
import math
from typing import Callable, Generic, Optional, TypeVar
from cohentools.disjointset import DisjointSet

VT = TypeVar("VT")
WT = TypeVar("WT")

@dataclasses.dataclass
class Graph(Generic[VT]):
    nodes: set[VT]
    edges: set[tuple[VT, VT]]

def dag_outgoing_degree(graph: Graph[VT]) -> dict[VT, int]:
    outgoing_degree = {node: 0 for node in graph}
    for (src, dst) in graph.edges:
        outgoing_degree[src] += 1
    return outgoing_degree

def dag_incoming_degree(graph: Graph[VT]) -> dict[VT, int]:
    incoming_degree = {node: 0 for node in graph.nodes}
    for (src, dst) in graph.edges:
        incoming_degree[dst] += 1
    return incoming_degree

def dag_outgoing_adj(graph: Graph[VT]) -> dict[VT, list[VT]]:
    outgoing_adj = {node: [] for node in graph.nodes}
    for (src, dst) in graph.edges:
        outgoing_adj[src].append(dst)
    return outgoing_adj

def dag_incoming_adj(graph: Graph[VT]) -> dict[VT, list[VT]]:
    incoming_adj = {node: [] for node in graph.nodes}
    for (src, dst) in graph.edges:
        incoming_adj[dst].append(src)
    return incoming_adj

def topsort(dag: Graph[VT]) -> Optional[list[VT]]:
    incoming = dag_incoming_degree(dag)
    outgoing = dag_outgoing_adj(dag)
    stack    = [node for node in dag.nodes
                if incoming[node] == 0]
    order    = []
    while stack:
        node = stack.pop()
        for child in outgoing[node]:
            incoming[child] -= 1
            if incoming[child] == 0:
                stack.append(child)
        order.append(node)
    if len(order) == len(dag.nodes):
        return order

def kruskals(graph: Graph[VT], weight: Callable[[VT, VT], WT]) -> set[tuple[VT, VT]]:
    mst = set(); disjoint = DisjointSet(graph.nodes)
    for (u, v) in sorted(graph.edges, key=lambda edge: weight(*edge)):
        find_u = disjoint.find(u)
        find_v = disjoint.find(v)
        if find_u != find_v:
            mst |= {(u, v), (v, u)}
            disjoint.union(find_u, find_v)
    return mst

def djikstras(graph: Graph[VT], src: VT, weight: Callable[[VT, VT], WT], *,
              zero: WT = 0, inf: WT = math.inf) -> tuple[dict[VT, WT], dict[VT, Optional[VT]]]:
    outgoing = dag_outgoing_adj(graph)
    dist     = {node: inf  for node in graph.nodes}
    prev     = {node: None for node in graph.nodes}
    fringe   = {src}; dist[src] = zero
    while fringe:
        node = min(fringe, key=dist.__getitem__)
        for adj in outgoing[node]:
            alt = dist[node] + weight(node, adj)
            if alt < dist[adj]:
                dist[adj] = alt
                prev[adj] = node
        fringe.remove(node)
    return dist, prev
