import pytest
from sqlalchemy import Column, Integer, MetaData, select, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import Column

from sqla_ext.types.postgresql import CITEXT


def test_citext_concatenate() -> None:
    assert str(Column("field", CITEXT) + "value") == "field || :field_1"  # type: ignore


def test_citext_compare_compare_w_bind_param() -> None:
    str(Column(CITEXT, name="field") == "NON_EXISTING") == "field = :field_1"  # type: ignore


def test_citext_compare_compare_w_literal_bind() -> None:
    comparison = Column(CITEXT, name="field") == "NON_EXISTING"  # type: ignore
    compiled_comparison = comparison.compile(
        dialect=postgresql.dialect(),  # type: ignore
        compile_kwargs={"literal_binds": True},
    )

    assert str(compiled_comparison) == "field = 'NON_EXISTING'"


def test_citext_compare_compare_w_literal_bind_2() -> None:
    stmt = str(
        (Column(CITEXT, name="field") == "NON|'_EXISTING%").compile(  # type: ignore
            dialect=postgresql.dialect(),  # type: ignore
            compile_kwargs={"literal_binds": True},
        )
    )

    assert stmt == "field = 'NON|''_EXISTING%%'"


@pytest.mark.asyncio
async def test_citext_integration(sess: AsyncSession) -> None:
    await sess.execute(text("create extension if not exists citext"))

    Base = declarative_base(metadata=MetaData())

    class MyTable(Base):
        __tablename__ = "citext_table"

        id = Column(Integer(), primary_key=True)
        email = Column(CITEXT)  # type: ignore

        def __repr__(self) -> str:
            return f'MyTable(id={self.id}, email="{self.email}")'

    conn = await sess.connection()
    await conn.run_sync(Base.metadata.create_all)

    row = MyTable(id=1, email="John.Smith@example.com")  # type: ignore

    sess.add(row)  # type: ignore
    await sess.commit()

    # Expunge the row from the session so we don't fetch it from the cache
    # If you don't do this, the retrieved row will come from the local session
    # and will not have any preprocessor rules applied
    sess.expunge(row)  # type: ignore

    from_db = await (
        sess.execute(select(MyTable).where(MyTable.email == "john.smith@example.com"))
    )
    (res,) = from_db.one()
    assert res.id == 1
