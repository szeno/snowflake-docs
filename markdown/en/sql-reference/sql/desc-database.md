# DESCRIBE DATABASE

Describes the database. For example, shows the schemas in the database.

DESCRIBE can be abbreviated to DESC.

See also:
:   [ALTER DATABASE](/sql-reference/sql/alter-database) , [CREATE DATABASE](/sql-reference/sql/create-database) , [DROP DATABASE](/sql-reference/sql/drop-database) , [SHOW DATABASES](/sql-reference/sql/show-databases) , [UNDROP DATABASE](/sql-reference/sql/undrop-database)

    [DATABASES view](/sql-reference/info-schema/databases) (Information Schema)

## Syntax

Copy code

```
DESC[RIBE] DATABASE <database_name>
```

## Parameters

`database_name`
:   Specifies the [identifier](/sql-reference/identifiers) of the database to describe.

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

## Examples

This demonstrates the DESCRIBE DATABASE command:

Copy code

```
CREATE DATABASE desc_demo;

CREATE SCHEMA sample_schema_1;

CREATE SCHEMA sample_schema_2;

DESCRIBE DATABASE desc_demo;
```

```
+-------------------------------+--------------------+--------+
| created_on                    | name               | kind   |
|-------------------------------+--------------------+--------|
| 2022-06-23 00:00:00.000 -0700 | INFORMATION_SCHEMA | SCHEMA |
| 2022-06-23 00:00:00.000 -0700 | PUBLIC             | SCHEMA |
| 2022-06-23 01:00:00.000 -0700 | SAMPLE_SCHEMA_1    | SCHEMA |
| 2022-06-23 02:00:00.000 -0700 | SAMPLE_SCHEMA_2    | SCHEMA |
+-------------------------------+--------------------+--------+
```
