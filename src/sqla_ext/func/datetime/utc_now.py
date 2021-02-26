from typing import Any, Dict

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import DateTime


class utc_now(FunctionElement):
    r"""Current timestamp in UTC timezone

    :Dialects:
        - mysql
        - postgresql
        - sqlite

    :return: :class:`FuntionElement`

    E.g.::

        from sqlalchemy import select
        from sqla_ext import func as func_ext

        query = select([
            func_ext.datetime.utc_now()
        ])

    The above statement will produce SQL resembling::

        SELECT
            timezone('utc', current_timestamp)
    """

    name = "to_array"

    def __init__(self) -> None:
        super().__init__()

    type = DateTime()


@compiles(utc_now, "postgresql")
def pg(element: utc_now, compiler: SQLCompiler, **kw: Dict[str, Any]) -> str:
    return "timezone('utc', current_timestamp)"


@compiles(utc_now, "sqlite")
def sqlite(element: utc_now, compiler: SQLCompiler, **kw: Dict[str, Any]) -> str:
    return "datetime('now')"


@compiles(utc_now, "mysql")
def mysql(element: utc_now, compiler: SQLCompiler, **kw: Dict[str, Any]) -> str:
    return "utc_timestamp()"
