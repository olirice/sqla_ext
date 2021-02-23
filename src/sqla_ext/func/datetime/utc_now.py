from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


class utc_now(expression.FunctionElement):
    type = DateTime()


@compiles(utc_now, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@compiles(utc_now, "sqlite")
def sqlite_utcnow(element, compiler, **kw):
    return "datetime('now')"


@compiles(utc_now, "mysql")
def mysql_utcnow(element, compiler, **kw):
    return "utc_timestamp()"
