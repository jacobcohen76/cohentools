from __future__ import annotations

from typing import (
  Protocol,
  TypeVar,
)

T = TypeVar("T")

class _Intersection:
  def __getitem__(self, bases):
    class result(*bases): ...
    return result

Intersection = _Intersection

class Comparable(Protocol):
  def __lt__(self, other: Comparable) -> bool: ...
  def __gt__(self, other: Comparable) -> bool: ...

def identity_fn(x: T) -> T:
  return x
