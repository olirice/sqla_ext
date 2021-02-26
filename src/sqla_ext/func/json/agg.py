from typing import Any, Dict, Union

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.sql.expression import ColumnClause, TextClause
from sqlalchemy.sql.functions import GenericFunction
from sqlalchemy.types import JSON


class agg(GenericFunction):  # type: ignore
    r"""JSON array aggregation

    :Dialects:
        - mysql
        - postgresql
        - sqlite

    :param expression: A SQL expression, such as a
        :class:`ColumnElement` expression or a :class:`TextClause` with elements
        that are castable as JSON

    :return: :class:`FuntionElement`

    E.g.::

        from sqlalchemy import select, Integer, text, table, column
        from sqla_ext import func as func_ext

        t = table('some_table', column('q', Integer))

        query = select([
            func_ext.json.agg(t.q)
        ])

    The above statement will produce SQL resembling::

        SELECT
            jsonb_agg(some_table.q)
        FROM
            some_table
    """

    type = JSON()
    name = "agg"

    def __init__(self, expression: Union[ColumnClause, TextClause]) -> None:
        super().__init__(expression)


@compiles(agg, "postgresql")
def pg(element: agg, compiler: SQLCompiler, **kw: Dict[str, Any]) -> str:
    return "jsonb_agg(%s)" % compiler.process(element.clauses, **kw)


@compiles(agg, "sqlite")
def sqlite(element: agg, compiler: SQLCompiler, **kw: Dict[str, Any]) -> str:
    return "json_group_array(%s)" % compiler.process(element.clauses, **kw)


@compiles(agg, "mysql")
def mysql(element: agg, compiler: SQLCompiler, **kw: Dict[str, Any]) -> str:
    return "json_arrayagg(%s)" % compiler.process(element.clauses, **kw)
