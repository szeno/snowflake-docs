# DESCRIBE TASK

Shows information about a task.

DESCRIBE can be abbreviated to DESC.

See also:
:   [DROP TASK](/sql-reference/sql/drop-task) , [ALTER TASK](/sql-reference/sql/alter-task) , [CREATE TASK](/sql-reference/sql/create-task) , [SHOW TASKS](/sql-reference/sql/show-tasks)

## Syntax

Copy code

```
DESC[RIBE] TASK <name>
```

## Parameters

`name`
:   Specifies the identifier for the task to describe. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Output

The command provides the same output as [SHOW\_TASKS](/sql-reference/sql/show-tasks#label-show-tasks-output).

## Usage notes

- Only returns rows for a task owner—that is, the role with the OWNERSHIP privilege on a task—or a role with either the MONITOR
  or OPERATE privilege on a task.

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

Create an example task:

> Copy code
>
> ```
> CREATE TASK mytask ( ... );
> ```

Show information about the task:

> Copy code
>
> ```
> DESC TASK mytask;
> ```

For output examples, see [SHOW\_TASKS](/sql-reference/sql/show-tasks#label-show-tasks-output).
