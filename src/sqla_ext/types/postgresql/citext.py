from typing import Callable

import sqlalchemy.types as types
from sqlalchemy.dialects.postgresql.base import PGDialect, ischema_names


class CITEXT(types.Concatenable, types.UserDefinedType):
    r"""Case Insensitive Text Type

    :Dialects:
        - postgresql

    https://www.postgresql.org/docs/current/citext.html

    E.g.::

        from sqlalchemy import Column, Integer
        from sqlalchemy.orm import declarative_base
        from sqla_ext.types.postgresql import CITEXT


        class User(Base):
            __tablename__ = 'user'
            id = sa.Column(Integer, primary_key=True)
            email = sa.Column(CITEXT())


        user = User(id=1, email='John.Smith@example.com')
        session.add(user)
        session.commit()

        # Note: query email is lowercase
        user = (
            session.query(User)
            .filter(User.email == 'john.smith@example.com')
            .one()
        )
        assert user.id == 1
    """

    def literal_processor(self, dialect: PGDialect) -> Callable:
        def process(value: str) -> str:
            value = value.replace("'", "''")

            if dialect.identifier_preparer._double_percents:
                value = value.replace("%", "%%")

            return "'%s'" % value

        return process

    def get_col_spec(self) -> str:
        return "CITEXT"

    def bind_processor(self, dialect: PGDialect) -> Callable:
        def process(value: str) -> str:
            return value

        return process

    def result_processor(self, dialect: PGDialect, coltype: int) -> Callable:
        def process(value: str) -> str:
            return value

        return process


# Register CIText to SQLAlchemy's Postgres reflection subsystem.
ischema_names["citext"] = CITEXT
