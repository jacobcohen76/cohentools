from __future__ import annotations

import dataclasses
from typing import (
  Generic,
  Iterable,
  TypeVar,
)

T = TypeVar('T')

@dataclasses.dataclass
class TreeNode(Generic[T]):
  data:  T
  left:  TreeNode[T] | None = None
  right: TreeNode[T] | None = None

def walk_preorder(root: TreeNode[T] | None) -> Iterable[TreeNode[T]]:
  stack = [] if root is None else [root]
  while stack:
    yield (node := stack.pop())
    if node.right:
      stack.append(node.right)
    if node.left:
      stack.append(node.left)

def walk_inorder(root: TreeNode[T] | None) -> Iterable[TreeNode[T]]:
  stack = []; node = root
  while stack or node:
    while node:
      stack.append(node)
      node = node.left
    yield (node := stack.pop())
    node = node.right

def walk_postorder(root: TreeNode[T] | None) -> Iterable[TreeNode[T]]:
  stack = [] if root is None else [root]
  order = []
  while stack:
    order.append(node := stack.pop())
    if node.left:
      stack.append(node.left)
    if node.right:
      stack.append(node.right)
  return reversed(order)
