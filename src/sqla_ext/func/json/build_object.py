from typing import Any, Dict

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.types import JSON


class build_object(FunctionElement):  # type: ignore
    r"""JSON object creation

    :Dialects:
        - mysql
        - postgresql
        - sqlite

    :param expression: A SQL expression, such as a
        :class:`ColumnElement` expression or a :class:`TextClause` with elements
        that are castable as JSON

    :return: :class:`FuntionElement`

    E.g.::

        from sqlalchemy import select
        from sqla_ext import func as func_ext

        query = select([
            func_ext.json.build_object("first_key", "first_value", "second_key", 2)
        ])

    The above statement will produce SQL resembling::

        SELECT
            jsonb_build_object('first_key', 'first_value', 'second_key', 2)
    """

    type = JSON()
    name = "jsonb_build_object"


@compiles(build_object, "postgresql")
def pg_build_object(
    element: build_object, compiler: SQLCompiler, **kw: Dict[str, Any]
) -> str:
    return "jsonb_build_object(%s)" % compiler.process(element.clauses, **kw)


@compiles(build_object, "sqlite")
@compiles(build_object, "mysql")
def other_build_object(
    element: build_object, compiler: SQLCompiler, **kw: Dict[str, Any]
) -> str:
    return "json_object(%s)" % compiler.process(element.clauses, **kw)
