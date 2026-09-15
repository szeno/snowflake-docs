# DESCRIBE SEQUENCE

Describes a sequence, including the sequence’s interval.

DESCRIBE can be abbreviated to DESC.

See also:
:   [ALTER SEQUENCE](/sql-reference/sql/alter-sequence) , [CREATE SEQUENCE](/sql-reference/sql/create-sequence) , [DROP SEQUENCE](/sql-reference/sql/drop-sequence) , [SHOW SEQUENCES](/sql-reference/sql/show-sequences)

## Syntax

Copy code

```
DESC[RIBE] SEQUENCE <name>
```

## Parameters

`name`
:   Specifies the identifier for the sequence to describe.

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

Copy code

```
DESC SEQUENCE my_sequence;
```
