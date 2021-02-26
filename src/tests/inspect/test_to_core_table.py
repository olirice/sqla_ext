import pytest
from sqlalchemy import Table
from sqlalchemy.orm import Mapper

from sqla_ext.inspect import to_core_table
from sqla_ext.types import ORMTableProtocol


def test_table_to_core_table(core_table: Table) -> None:
    assert to_core_table(core_table) == core_table


def test_orm_table_to_core_table(
    orm_table: ORMTableProtocol, core_table: Table
) -> None:
    assert to_core_table(orm_table) == core_table


def test_mapper_to_core_table(mapper_table: Mapper, core_table: Table) -> None:
    assert to_core_table(mapper_table) == core_table


def test_callable_to_core_table(core_table: Table) -> None:
    assert to_core_table(lambda: core_table) == core_table  # type: ignore


def test_not_implemented_to_core_table(core_table: Table) -> None:
    with pytest.raises(NotImplementedError):
        to_core_table(1) == core_table  # type: ignore
