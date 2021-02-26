from __future__ import annotations

from functools import lru_cache

from sqla_ext.types import TableCoercable

from .to_core_table import to_core_table


@lru_cache()
def to_table_name(entity: TableCoercable) -> str:
    r"""Get the name of a sqlalchemy table-like entity

    :param entity: A sqlalchemy :class:`Table`, :class::`DeclarativeBase` or :class:`Mapper`

    :return: :class:`str`
    """
    return str(to_core_table(entity).name)
