from __future__ import annotations

from typing import Callable, Union

from sqlalchemy import Table
from sqlalchemy.orm import Mapper
from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class ORMTableProtocol(Protocol):
    __table__: Table


TableCoercable = Union[
    Table, ORMTableProtocol, Mapper, Callable[[], Union[ORMTableProtocol, Table]]
]
