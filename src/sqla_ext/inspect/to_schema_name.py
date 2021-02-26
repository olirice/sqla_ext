from __future__ import annotations

from functools import lru_cache
from typing import Optional

from sqla_ext.types import TableCoercable

from .to_core_table import to_core_table


@lru_cache()
def to_schema_name(entity: TableCoercable) -> Optional[str]:
    r"""Get the schema of a sqlalchemy table-like entity

    :param entity: A sqlalchemy :class:`Table`, :class::`DeclarativeBase` or :class:`Mapper`

    :return: :class:`Optional[str]`
    """

    schema_name = to_core_table(entity).schema
    return str(schema_name) if schema_name is not None else None
