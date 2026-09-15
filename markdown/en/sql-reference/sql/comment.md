# COMMENT

Adds a comment or overwrites an existing comment for an existing object.

Comments can be added to all objects (users, roles, warehouses, databases, tables, and so on). You can also use
this command to add comments to individual table columns, but not to constraints on columns.

## Syntax

Copy code

```
COMMENT [ IF EXISTS ] ON <object_type> <object_name> IS '<string_literal>';

COMMENT [ IF EXISTS ] ON COLUMN <table_name>.<column_name> IS '<string_literal>';
```

## Parameters

`ON object_type object_name`
:   Adds a comment to the object of the specified type (for example, `TABLE`, `SCHEMA`, `VIEW`, and so on)
    with the specified identifier.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ON COLUMN table_name.column_name`
:   Adds a comment to the specified table column.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`IS string_literal`
:   Specifies the comment to add.

    Default: `NULL`

## Usage notes

- You can also add or modify comments when you are creating or altering objects:

  - To add a comment, specify the `COMMENT` parameter in the [CREATE <object>](/sql-reference/sql/create) or [ALTER <object>](/sql-reference/sql/alter) command.
  - To modify an existing comment, specify the `COMMENT` parameter in the [ALTER <object>](/sql-reference/sql/alter) command.
- A slightly different syntax is used for adding or modifying comments on table columns:

  - To add a comment at creation, follow the column declaration with the `COMMENT` keyword (not property).
  - To modify a comment, use this command.
- To add a comment to a constraint, use the [CREATE TABLE](/sql-reference/sql/create-table) or [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint) commands.
- The DESCRIBE TABLE output doesn’t show comments for table constraints, such as multi-column primary keys. To see these comments,
  query the [TABLE\_CONSTRAINTS view](/sql-reference/info-schema/table_constraints).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Create a schema with a comment, then overwrite the comment:

Copy code

```
CREATE SCHEMA my_schema COMMENT='this is comment1';

SHOW SCHEMAS LIKE 'my_schema';
```

```
+-------------------------------+-----------+------------+------------+---------------+---------+------------------+---------+----------------+------+
| created_on                    | name      | is_default | is_current | database_name | owner   | comment          | options | retention_time | ...  |
|-------------------------------+-----------+------------+------------+---------------+---------+------------------+---------+----------------+------|
| 2025-02-26 12:08:52.363 -0800 | MY_SCHEMA | N          | Y          | MY_DB         | MY_ROLE | this is comment1 |         | 1              |  ... |
+-------------------------------+-----------+------------+------------+---------------+---------+------------------+---------+----------------+------+
```

Copy code

```
COMMENT ON SCHEMA my_schema IS 'now comment2';

SHOW SCHEMAS LIKE 'my_schema';
```

```
+-------------------------------+-----------+------------+------------+---------------+---------+--------------+---------+----------------+-----+
| created_on                    | name      | is_default | is_current | database_name | owner   | comment      | options | retention_time | ... |
|-------------------------------+-----------+------------+------------+---------------+---------+--------------+---------+----------------+-----+
| 2025-02-26 12:08:52.363 -0800 | MY_SCHEMA | N          | Y          | MY_DB         | MY_ROLE | now comment2 |         | 1              | ... |
+-------------------------------+-----------+------------+------------+---------------+---------+--------------+---------+----------------+-----+
```

Create a table with a comment on a table column, then overwrite the comment:

Copy code

```
CREATE OR REPLACE TABLE test_comment_table_column(my_column STRING COMMENT 'this is comment3');

DESC TABLE test_comment_table_column;
```

```
+-----------+-------------------+--------+-------+---------+-------------+------------+-------+------------+------------------+-------------+----------------+
| name      | type              | kind   | null? | default | primary key | unique key | check | expression | comment          | policy name | privacy domain |
|-----------+-------------------+--------+-------+---------+-------------+------------+-------+------------+------------------+-------------+----------------|
| MY_COLUMN | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | this is comment3 | NULL        | NULL           |
+-----------+-------------------+--------+-------+---------+-------------+------------+-------+------------+------------------+-------------+----------------+
```

Copy code

```
COMMENT ON COLUMN test_comment_table_column.my_column IS 'now comment4';

DESC TABLE test_comment_table_column;
```

```
+-----------+-------------------+--------+-------+---------+-------------+------------+-------+------------+--------------+-------------+----------------+
| name      | type              | kind   | null? | default | primary key | unique key | check | expression | comment      | policy name | privacy domain |
|-----------+-------------------+--------+-------+---------+-------------+------------+-------+------------+--------------+-------------+----------------|
| MY_COLUMN | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | now comment4 | NULL        | NULL           |
+-----------+-------------------+--------+-------+---------+-------------+------------+-------+------------+--------------+-------------+----------------+
```

Create a view with a comment, then overwrite the comment:

Copy code

```
CREATE OR REPLACE VIEW test_comment_view COMMENT='this is comment5' AS (SELECT * FROM test_comment_table_column);

SHOW VIEWS LIKE 'test_comment_view';
```

```
+-------------------------------+-------------------+----------+---------------+-------------+---------+------------------+-----+
| created_on                    | name              | reserved | database_name | schema_name | owner   | comment          | ... |
|-------------------------------+-------------------+----------+---------------+-------------+---------+------------------+-----+
| 2025-02-26 12:38:35.440 -0800 | TEST_COMMENT_VIEW |          | MY_DB         | MY_SCHEMA   | MY_ROLE | this is comment5 | ... |
+-------------------------------+-------------------+----------+---------------+-------------+---------+------------------+-----+
```

Copy code

```
COMMENT ON VIEW test_comment_view IS 'now comment6';

SHOW VIEWS LIKE 'test_comment_view';
```

```
+-------------------------------+-------------------+----------+---------------+-------------+---------+--------------+-----+
| created_on                    | name              | reserved | database_name | schema_name | owner   | comment      | ... |
|-------------------------------+-------------------+----------+---------------+-------------+---------+--------------+-----+
| 2025-02-26 12:38:35.440 -0800 | TEST_COMMENT_VIEW |          | MY_DB         | MY_SCHEMA   | MY_ROLE | now comment6 | ... |
+-------------------------------+-------------------+----------+---------------+-------------+---------+--------------+-----+
```
