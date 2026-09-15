# Data Manipulation Language (DML) commands

This topic provides links to all the DML commands, grouped by category.

## General DML

Commands for inserting, deleting, updating, and merging data in Snowflake tables:

- [INSERT](/sql-reference/sql/insert)
- [INSERT (multi-table)](/sql-reference/sql/insert-multi-table)
- [MERGE](/sql-reference/sql/merge)
- [UPDATE](/sql-reference/sql/update)
- [DELETE](/sql-reference/sql/delete)
- [TRUNCATE TABLE](/sql-reference/sql/truncate-table)

## Data loading / unloading DML

Commands for bulk copying data into and out of Snowflake tables:

- [COPY INTO <table>](/sql-reference/sql/copy-into-table) (loading/importing data)
- [COPY INTO <location>](/sql-reference/sql/copy-into-location) (unloading/exporting data)

See also:
:   [VALIDATE](/sql-reference/functions/validate) (table function)

## File staging commands (for data loading / unloading)

These commands do not perform any actual DML, but are used to stage and manage files stored in Snowflake locations (named internal stages, table stages,
and user stages), for the purpose of loading and unloading data:

- [PUT](/sql-reference/sql/put)
- [GET](/sql-reference/sql/get)
- [LIST](/sql-reference/sql/list) (can also be used with named external stages)
- [REMOVE](/sql-reference/sql/remove)
