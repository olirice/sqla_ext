from __future__ import annotations

from functools import lru_cache

from sqlalchemy import Table
from sqlalchemy.orm import Mapper

from sqla_ext.types import ORMTableProtocol, TableCoercable


@lru_cache()
def to_core_table(entity: TableCoercable) -> Table:
    r"""Coerces multiple SQLA Table-like entities to a core sqlalcehmy.Table

    :param entity: A sqlalchemy :class:`Table`, :class::`DeclarativeBase` or :class:`Mapper`

    :return: :class:`Table`
    """

    if isinstance(entity, Table):
        return entity

    if isinstance(entity, ORMTableProtocol):
        return entity.__table__

    if isinstance(entity, Mapper):
        # re-wrapping with to_core_table is not necessary
        # but makes type checking happy
        return to_core_table(entity.local_table)

    if callable(entity):
        return to_core_table(entity())

    raise NotImplementedError("to_core_table not implemented for entity type")
