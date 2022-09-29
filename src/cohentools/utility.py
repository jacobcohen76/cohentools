from __future__ import annotations

from typing import (
  Protocol,
  TypeVar,
)

class Comparable(Protocol):
  def __lt__(self, other: Comparable) -> bool: ...
  def __gt__(self, other: Comparable) -> bool: ...

T = TypeVar('T')

def identity_fn(x: T) -> T:
  return x
