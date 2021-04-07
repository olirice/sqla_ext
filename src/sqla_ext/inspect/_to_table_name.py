from __future__ import annotations

from functools import lru_cache

from sqla_ext.inspect._to_core_table import to_core_table
from sqla_ext.protocols import TableCoercable


@lru_cache()
def to_table_name(entity: TableCoercable) -> str:
    r"""Get the name of a sqlalchemy table-like entity

    :param entity: A sqlalchemy :class:`Table`, :class:`DeclarativeBase` or :class:`Mapper`

    :return: :class:`str`
    """
    return str(to_core_table(entity).name)
