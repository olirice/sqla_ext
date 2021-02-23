import pytest
from sqlalchemy import Integer, column, table
from sqlalchemy.dialects import mysql, postgresql, sqlite
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.sql.expression import FunctionElement

from sqla_ext import func

t = table("xyz", column("q", Integer()))


@pytest.mark.parametrize(
    "statement,output,dialect",
    [
        # func.json.build_object
        (
            func.json.build_object("key", "value"),
            "jsonb_build_object('key', 'value')",
            postgresql,
        ),
        (func.json.build_object("key", "value"), "json_object('key', 'value')", sqlite),
        (func.json.build_object("key", "value"), "json_object('key', 'value')", mysql),
        # func.json.agg
        (func.json.agg(t.c.q), "jsonb_agg(xyz.q)", postgresql),
        (func.json.agg(t.c.q), "json_group_array(xyz.q)", sqlite),
        (func.json.agg(t.c.q), "json_arrayagg(xyz.q)", mysql),
        # func.datetime.utc_now
        (func.datetime.utc_now(), "timezone('utc', current_timestamp)", postgresql),
        (func.datetime.utc_now(), "datetime('now')", sqlite),
        (func.datetime.utc_now(), "utc_timestamp()", mysql),
    ],
)
def test_json_function(
    statement: FunctionElement, output: str, dialect: SQLCompiler
) -> None:
    compiled = statement.compile(
        dialect=dialect.dialect(), compile_kwargs={"literal_binds": True}
    )
    assert str(compiled) == output
