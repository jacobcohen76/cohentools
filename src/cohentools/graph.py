import dataclasses
from typing import Generic, Iterable, Mapping, TypeVar

VT = TypeVar("VT")

@dataclasses.dataclass
class Graph(Generic[VT]):
    nodes: set[VT]
    edges: set[tuple[VT, VT]]

def dag_outgoing_degree(graph: Graph[VT]) -> dict[VT, int]:
    outgoing_degree = {node: 0 for node in graph}
    for (src, dst) in graph.edges:
        outgoing_degree[src] += 1
    return outgoing_degree

def dag_incoming_degree(graph: Graph[VT]) -> Mapping[VT, int]:
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

def topsort(graph: Graph[VT]) -> Iterable[VT]:
    incoming = dag_incoming_degree(graph)
    outgoing = dag_outgoing_adj(graph)
    stack    = [node for node in graph.nodes
                if incoming[node] == 0]
    while stack:
        node = stack.pop()
        for child in outgoing[node]:
            incoming[child] -= 1
            if incoming[child] == 0:
                stack.append(child)
        yield node
