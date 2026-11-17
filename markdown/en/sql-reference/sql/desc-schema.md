# DESCRIBE SCHEMA

Describes the schema. For example, lists the tables and views in the schema.

DESCRIBE can be abbreviated to DESC.

See also:
:   [ALTER SCHEMA](/sql-reference/sql/alter-schema) , [CREATE SCHEMA](/sql-reference/sql/create-schema) , [DROP SCHEMA](/sql-reference/sql/drop-schema) , [SHOW SCHEMAS](/sql-reference/sql/show-schemas) , [UNDROP SCHEMA](/sql-reference/sql/undrop-schema)

    [SCHEMATA view](/sql-reference/info-schema/schemata) (Information Schema)

## Syntax

Copy code

```
DESC[RIBE] SCHEMA <schema_name>
```

## Parameters

`schema_name`
:   Specifies the [identifier](/sql-reference/identifiers) of the schema to describe.

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Output

The command output provides the `created_on`, `name`, and `kind` columns for each object in the schema. The `kind` column
identifies the object’s type and can contain any of the following values:

| Kind | Description |
| --- | --- |
| TABLE | A permanent or [transient](/user-guide/tables-temp-transient) table, including [hybrid tables](/user-guide/tables-hybrid) and [Apache Iceberg™ tables](/user-guide/tables-iceberg). Hybrid tables and Iceberg tables don’t have a distinct `kind` value. |
| TEMPORARY | A [temporary table](/user-guide/tables-temp-transient) created in the current session. |
| VIEW | A non-materialized view, including secure views. |
| TEMP VIEW | A temporary view created in the current session. |
| MATERIALIZED\_VIEW | A [materialized view](/user-guide/views-materialized). |
| DYNAMIC\_TABLE | A [dynamic table](/user-guide/dynamic-tables/overview). |
| EXTERNAL\_TABLE | An [external table](/user-guide/tables-external-intro). |
| EVENT\_TABLE | An [event table](/developer-guide/logging-tracing/event-table-setting-up). |
| ONLINE\_FEATURE\_TABLE | An [online feature table](/developer-guide/snowflake-ml/feature-store/overview) used by the Snowflake Feature Store. |
| INTERACTIVE\_TABLE | An [interactive table](/user-guide/interactive). |

Expand

Show lessSee more

[Semantic views](/user-guide/views-semantic/overview) don’t appear in `DESCRIBE SCHEMA` output. This differs from
[SHOW OBJECTS](/sql-reference/sql/show-objects#usage-notes), which lists semantic views with `kind` set to `VIEW`.

## Examples

This demonstrates the DESCRIBE SCHEMA command:

Copy code

```
CREATE SCHEMA sample_schema_2;
USE SCHEMA sample_schema_2;

CREATE TABLE sample_table_1 (i INTEGER);

CREATE VIEW sample_view_1 AS
    SELECT i FROM sample_table_1;

CREATE MATERIALIZED VIEW sample_mview_1 AS
    SELECT i FROM sample_table_1 WHERE i < 100;

DESCRIBE SCHEMA sample_schema_2;

+-------------------------------+----------------+-------------------+
| created_on                    | name           | kind              |
|-------------------------------+----------------+-------------------|
| 2022-06-23 01:00:00.000 -0700 | SAMPLE_TABLE_1 | TABLE             |
| 2022-06-23 02:00:00.000 -0700 | SAMPLE_VIEW_1  | VIEW              |
| 2022-06-23 03:00:00.000 -0700 | SAMPLE_MVIEW_1 | MATERIALIZED_VIEW |
+-------------------------------+----------------+-------------------+
```
