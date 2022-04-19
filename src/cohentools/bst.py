from __future__ import annotations
import dataclasses
from typing import Generic, Iterable, Optional, TypeVar

T = TypeVar("T")

@dataclasses.dataclass
class TreeNode(Generic[T]):
    data:  T
    left:  Optional[TreeNode[T]] = None
    right: Optional[TreeNode[T]] = None

def walk_preorder(root: Optional[TreeNode[T]]) -> Iterable[TreeNode[T]]:
    stack = [root]
    while stack:
        if node := stack.pop():
            yield node
            stack.append(node.right)
            stack.append(node.left)

def walk_inorder(root: Optional[TreeNode[T]]) -> Iterable[TreeNode[T]]:
    stack = []; node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        yield (node := stack.pop())
        node = node.right

def walk_postorder(root: Optional[TreeNode[T]]) -> Iterable[TreeNode[T]]:
    stack = [root]; order = []
    while stack:
        if node := stack.pop():
            order.append(node)
            stack.append(node.left)
            stack.append(node.right)
    return reversed(order)
