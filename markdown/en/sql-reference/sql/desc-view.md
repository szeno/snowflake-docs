# DESCRIBE VIEW

Describes the columns in a view (or table).

DESCRIBE can be abbreviated to DESC.

See also:
:   [DROP VIEW](/sql-reference/sql/drop-view) , [ALTER VIEW](/sql-reference/sql/alter-view) , [CREATE VIEW](/sql-reference/sql/create-view) , [SHOW VIEWS](/sql-reference/sql/show-views)

    [DESCRIBE TABLE](/sql-reference/sql/desc-table)

## Syntax

Copy code

```
DESC[RIBE] VIEW <name>
```

## Parameters

`name`
:   Specifies the identifier for the view to describe. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- The command output does not include the view definition. Instead, use [SHOW VIEWS](/sql-reference/sql/show-views).
- DESC VIEW and [DESCRIBE TABLE](/sql-reference/sql/desc-table) are interchangeable. Either command retrieves the details for the table or view that matches the criteria
  in the statement.
- The output returns a `POLICY NAME` column to indicate the [masking policy](/user-guide/security-column-intro) set on the column.

  If a masking policy is not set on the column or if the Snowflake account is not Enterprise Edition or higher, Snowflake returns
  `NULL`.

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

Example setup:

> Copy code
>
> ```
> CREATE VIEW emp_view AS SELECT id "Employee Number", lname "Last Name", location "Home Base" FROM emp;
> ```

Describe the view:

> Copy code
>
> ```
> DESC VIEW emp_view;
>
> +-----------------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+-----------------+
> | name            | type         | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |  privacy domain |
> |-----------------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+-----------------+
> | Employee Number | NUMBER(38,0) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL            |
> | Last Name       | VARCHAR(50)  | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL            |
> | Home Base       | VARCHAR(100) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL            |
> +-----------------+--------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+-----------------+
> ```
