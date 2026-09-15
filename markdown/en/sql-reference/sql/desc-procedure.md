# DESCRIBE PROCEDURE

Describes the specified stored procedure, including the stored procedure’s signature (i.e. arguments), return value, language, and
body (i.e. definition).

See also:
:   [DROP PROCEDURE](/sql-reference/sql/drop-procedure) , [ALTER PROCEDURE](/sql-reference/sql/alter-procedure) , [CREATE PROCEDURE](/sql-reference/sql/create-procedure) , [SHOW PROCEDURES](/sql-reference/sql/show-procedures), [SHOW USER PROCEDURES](/sql-reference/sql/show-user-procedures)

## Syntax

Copy code

```
DESC[RIBE] PROCEDURE <procedure_name> ( [ <arg_data_type> [ , <arg_data_type_2> ... ] ] )
```

## Usage notes

- To describe a stored procedure, you must specify the name and the argument data type(s), if any, for the stored procedure. The
  arguments are required because stored procedures support name overloading (i.e. two stored procedures in the same schema can have
  the same name as long as their argument data types are different).
- The `body` property in the output displays the code for the stored procedure.

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

This example shows how to describe a stored procedure that has no parameters:

> Copy code
>
> ```
> DESC PROCEDURE my_pi();
> +---------------+----------------------+
> | property      | value                |
> |---------------+----------------------|
> | signature     | ()                   |
> | returns       | FLOAT                |
> | language      | JAVASCRIPT           |
> | null handling | CALLED ON NULL INPUT |
> | volatility    | VOLATILE             |
> | execute as    | CALLER               |
> | body          |                      |
> |               |   return 3.1415926;  |
> |               |                      |
> +---------------+----------------------+
> ```

This example shows how to describe a stored procedure that has a parameter:

> Copy code
>
> ```
> DESC PROCEDURE area_of_circle(FLOAT);
> +---------------+------------------------------------------------------------------+
> | property      | value                                                            |
> |---------------+------------------------------------------------------------------|
> | signature     | (RADIUS FLOAT)                                                   |
> | returns       | FLOAT                                                            |
> | language      | JAVASCRIPT                                                       |
> | null handling | CALLED ON NULL INPUT                                             |
> | volatility    | VOLATILE                                                         |
> | execute as    | OWNER                                                            |
> | body          |                                                                  |
> |               |   var stmt = snowflake.createStatement(                          |
> |               |       {sqlText: "SELECT pi() * POW($RADIUS, 2)", binds:[RADIUS]} |
> |               |       );                                                         |
> |               |   var rs = stmt.execute();                                       |
> |               |   rs.next()                                                      |
> |               |   var output = rs.getColumnValue(1);                             |
> |               |   return output;                                                 |
> |               |                                                                  |
> +---------------+------------------------------------------------------------------+
> ```
