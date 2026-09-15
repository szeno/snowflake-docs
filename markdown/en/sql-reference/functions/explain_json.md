Categories:
:   [System functions](/sql-reference/functions-system)

# EXPLAIN\_JSON

This function converts an EXPLAIN plan from JSON to a table. The output is the same as the output of the command `EXPLAIN USING TABULAR <statement>`.

See also:
:   [SYSTEM$EXPLAIN\_PLAN\_JSON](/sql-reference/functions/system_explain_plan_json) , [SYSTEM$EXPLAIN\_JSON\_TO\_TEXT](/sql-reference/functions/system_explain_json_to_text)

## Syntax

Copy code

```
EXPLAIN_JSON( <explain_output_in_json_format> )
```

## Arguments

`explain_output_in_json_format`
:   A string, or an expression that evaluates to a string, containing EXPLAIN output as a JSON-compatible string.
    Typically, this input is the output of the function SYSTEM$EXPLAIN\_PLAN\_JSON.
    If a literal string is used, it should be surrounded by single quote characters `'`.

## Returns

The function returns a table containing the EXPLAIN output as an ordered set of rows.

The output of this function is equivalent to the output of `EXPLAIN USING TABULAR <sql_statement>`.

## Usage notes

- The input must be a constant expression. You cannot call this function on a column, for example.
- If a string literal is passed as input, the delimiter around the string can be either a single quote `'` or a
  double dollar sign `$$`. If the string literal contains single quotes (and does not contain double dollar
  signs), then delimiting the string with double dollar signs avoids the need to escape the embedded single quote
  characters inside the string.
- The output table can be processed using the [RESULT\_SCAN](/sql-reference/functions/result_scan) function.
- This function converts EXPLAIN information from JSON to tabular format.
  Often, the JSON value is produced directly or indirectly from the [SYSTEM$EXPLAIN\_PLAN\_JSON](/sql-reference/functions/system_explain_plan_json) function.
  For example, the output from SYSTEM$EXPLAIN\_PLAN\_JSON could be stored in a table, then displayed later using this
  EXPLAIN\_JSON function.
- Because the output is tabular, this function is classified as a [table function](/sql-reference/functions-table).

## Examples

The following example shows how to use this function:

> Copy code
>
> ```
> SELECT * FROM TABLE(
>     EXPLAIN_JSON(
>         SYSTEM$EXPLAIN_PLAN_JSON(
>            'SELECT Z1.ID, Z2.ID FROM Z1, Z2 WHERE Z2.ID = Z1.ID')
>         )
>     );
> +------+------+-----------------+-------------+------------------------------+-------+--------------------------+-----------------+--------------------+---------------+
> | step | id   | parentOperators | operation   | objects                      | alias | expressions              | partitionsTotal | partitionsAssigned | bytesAssigned |
> |------+------+-----------------+-------------+------------------------------+-------+--------------------------+-----------------+--------------------+---------------|
> | NULL | NULL |          NULL | GlobalStats | NULL                         | NULL  | NULL                     |               2 |                  2 |          1024 |
> |    1 |    0 |            NULL | Result      | NULL                         | NULL  | Z1.ID, Z2.ID             |            NULL |               NULL |          NULL |
> |    1 |    1 |             [0] | InnerJoin   | NULL                         | NULL  | joinKey: (Z2.ID = Z1.ID) |            NULL |               NULL |          NULL |
> |    1 |    2 |             [1] | TableScan   | TESTDB.TEMPORARY_DOC_TEST.Z2 | NULL  | ID                       |               1 |                  1 |           512 |
> |    1 |    3 |             [1] | JoinFilter  | NULL                         | NULL  | joinKey: (Z2.ID = Z1.ID) |            NULL |               NULL |          NULL |
> |    1 |    4 |             [3] | TableScan   | TESTDB.TEMPORARY_DOC_TEST.Z1 | NULL  | ID                       |               1 |                  1 |           512 |
> +------+------+-----------------+-------------+------------------------------+-------+--------------------------+-----------------+--------------------+---------------+
> ```
