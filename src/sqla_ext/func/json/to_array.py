# pylint: disable= unsubscriptable-object
from __future__ import annotations

from typing import Any, Dict, Union

from sqlalchemy import func as sqla_func
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import cast
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.sql.expression import ColumnClause, TextClause
from sqlalchemy.sql.functions import GenericFunction
from sqlalchemy.sql.type_api import TypeEngine


class to_array(GenericFunction):  # type: ignore
    r"""Cast a json array to a native array

    :Dialects:
        - postgresql

    :param expression: A SQL expression, such as a
        :class:`ColumnElement` expression or a :class:`TextClause` that can be coerced into a JSONB array

    :param type\_: A :class:`.TypeEngine` class or instance indicating
        the type to ``CAST`` elements of the native array as.

    :return: :class:`FuntionElement`

    E.g.::

        from sqlalchemy import select, Integer, text
        from sqla_ext import func as func_ext

        query = select([
            func_ext.json.to_array(text("'[1,2,3,4]'::jsonb"), Integer)
        ])

    The above statement will produce SQL resembling::

        SELECT
            array_agg(CAST(anon_1 AS INTEGER)) AS array_agg_1
        FROM
            jsonb_array_elements(CAST('[1,2,3,4]'::jsonb AS JSONB)) AS anon_1
    """

    name = "to_array"

    def __init__(
        self, expression: Union[ColumnClause, TextClause], type_: TypeEngine
    ) -> None:
        super().__init__(expression, type_)


function = to_array


@compiles(function, "postgresql")
def pg(element: function, compiler: SQLCompiler, **kw: Dict[str, Any]) -> str:

    args = iter(element.clauses)  # type: ignore
    json_field = next(args)  # type: ignore
    type_bind_param = next(args)  # type: ignore
    type_: TypeEngine = type_bind_param.value  # type: ignore

    assert isinstance(type_, TypeEngine) or issubclass(type_, TypeEngine)

    select_from = sqla_func.jsonb_array_elements(cast(json_field, JSONB)).table_valued(
        "value"
    )
    statement = select([sqla_func.array_agg(cast(select_from.column, type_))])

    return compiler.process(statement, **kw)
