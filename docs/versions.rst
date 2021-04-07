=========
Changelog
=========

.. automodule:: sqla_ext

0.0.0
-----

* Added func.json.build_object for building json objects in the database
* Added func.json.agg for aggregating data as json on the database
* Added func.datetime.utc_now as a unified interface for current timestamp in UTC timezone across dbms


0.0.1
-----

* Test all dialects of `func` functions
* Minimal docstrings
* Initail RTD documentation


0.0.2
-----

* Added func.json.to_array for casting json/jsonb arrays to native arrays


0.0.3
-----

* Doc fixes
* Added `sqla_ext.types` module for sharing type definitions
* Added `sqla_ext.inspect` module for extracting info from sqlalchemy entities
* Added `inspect.to_core_table` for casting multiple table-like entities to a `sqlalchemy.Table`
* Added `inspect.to_table_name` for getting a table name from a table-like entity
* Added `inspect.to_schema_name` for getting a schema name from a table-like entity


0.0.4
-----

* Added `sqla_ext.types.postgresql` module for sharing postgres type definitions
* Added `sqla_ext.types.postgresql.CITEX` for case insensitive strings


Master
------

* Nothing yet


