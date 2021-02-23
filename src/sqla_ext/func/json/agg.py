import sqlalchemy
from sqlalchemy import func, select
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.dialects import sqlite, postgresql, mysql
from sqlalchemy.types import JSON

class agg(FunctionElement):
    type = JSON()
    name = "agg"


@compiles(agg, "postgresql")
def pg_agg(element, compiler, **kw):
    return "jsonb_agg(%s)" % compiler.process(element.clauses, **kw)


@compiles(agg, "sqlite")
def sqlite_agg(element, compiler, **kw):
    return "json_group_array(%s)" % compiler.process(element.clauses, **kw)


@compiles(agg, "mysql")
def mysql_agg(element, compiler, **kw):
    return "json_arrayagg(%s)" % compiler.process(element.clauses, **kw)
