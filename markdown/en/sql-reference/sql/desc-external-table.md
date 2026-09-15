# DESCRIBE EXTERNAL TABLE

Describes the VALUE column and virtual columns in an external table.

DESCRIBE can be abbreviated to DESC.

See also:
:   [DROP EXTERNAL TABLE](/sql-reference/sql/drop-external-table) , [ALTER EXTERNAL TABLE](/sql-reference/sql/alter-external-table) , [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table) , [SHOW EXTERNAL TABLES](/sql-reference/sql/show-external-tables)

    [DESCRIBE VIEW](/sql-reference/sql/desc-view)

## Syntax

Copy code

```
DESC[RIBE] [ EXTERNAL ] TABLE <name> [ TYPE =  { COLUMNS | STAGE } ]
```

## Parameters

`name`
:   Specifies the identifier for the external table to describe. If the identifier contains spaces or special characters, the entire string
    must be enclosed in double quotes. Identifiers enclosed in double quotes are also case sensitive.

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

Create an example external table:

> Copy code
>
> ```
> CREATE EXTERNAL TABLE emp ( ... );
> ```

Describe the columns in the table:

> Copy code
>
> ```
> DESC EXTERNAL TABLE emp;
> ```
