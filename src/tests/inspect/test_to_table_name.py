from sqlalchemy import Table

from sqla_ext.inspect import to_table_name


def test_to_table_name(core_table: Table) -> None:
    assert to_table_name(core_table) == "some_tab"
