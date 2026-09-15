# Dec 03, 2025: Access history improvements

[Access history](/user-guide/access-history) lets you monitor the SQL statements executed in Snowflake. It keeps track of the
following types of statements:

- Data Manipulation Language (DML) statements. For example, statements used to insert data into a table.
- Data Query Language (DQL) statements. For example, statements that use a SELECT statement to project data.
- Data Definition Language (DDL) statements. For example, statements that create or alter a Snowflake object.

Snowflake is expanding which SQL statements are included in the access history. Recent improvements include the following:

- Added support for the following objects: listing, role, share, and session.
- Added DQL command support for externally managed Apache Iceberg™ tables.
- Enhanced support for database DDL commands, including the ALTER DATABASE command and commands related to database replication.
- Enhanced DDL support for tables, including variations of ALTER TABLE and variations of ALTER TABLE…MODIFY COLUMN.
- Enhanced support for [file staging commands](/sql-reference/commands-file) like GET and PUT.

For a complete list of objects and commands that appear in your access history, see [Supported Objects](/user-guide/access-history#label-access-history-supported-objects).
