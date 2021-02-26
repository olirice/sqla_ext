import pytest
from sqlalchemy import Column, Integer, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapper, mapper

from sqla_ext.types import ORMTableProtocol


@pytest.fixture(scope="function")
def core_table() -> Table:
    return Table(
        "some_tab", MetaData(), Column("q", Integer, primary_key=True), schema="public"
    )


@pytest.fixture(scope="function")
def orm_table(core_table: Table) -> ORMTableProtocol:

    Meta = MetaData()
    Base = declarative_base(metadata=Meta)

    class SomeTable(Base):
        __table__ = core_table

    return SomeTable  # type: ignore


@pytest.fixture(scope="function")
def mapper_table(core_table: Table) -> Mapper:
    class SomeTable:
        def __init__(self, q: int):
            self.q = q

    return mapper(SomeTable, core_table)
