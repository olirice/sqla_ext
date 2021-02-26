from sqlalchemy import Table

from sqla_ext.inspect import to_schema_name


def test_to_schema_name(core_table: Table) -> None:
    assert to_schema_name(core_table) == "public"
