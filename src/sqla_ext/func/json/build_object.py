import sqlalchemy
from sqlalchemy import func, select
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import FunctionElement
from sqlalchemy.dialects import sqlite, postgresql, mysql
from sqlalchemy.types import JSON


class build_object(FunctionElement):
    type = JSON()
    name = "jsonb_build_object"


@compiles(build_object, "postgresql")
def pg_build_object(element, compiler, **kw):
    return compiler.visit_function(element)


@compiles(build_object, "sqlite")
@compiles(build_object, "mysql")
def other_build_object(element, compiler, **kw):
    return "json_object(%s)" % compiler.process(element.clauses, **kw)

