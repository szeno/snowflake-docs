Categories:
:   [System functions](/sql-reference/functions-system)

# SYSTEM$EXPLAIN\_PLAN\_JSON

Given the text of a SQL statement, this function generates the EXPLAIN plan in JSON.

See also:
:   [SYSTEM$EXPLAIN\_JSON\_TO\_TEXT](/sql-reference/functions/system_explain_json_to_text) , [EXPLAIN\_JSON](/sql-reference/functions/explain_json)

## Syntax

Copy code

```
SYSTEM$EXPLAIN_PLAN_JSON( { <sql_statement_expression> | <sql_query_id_expression> } )
```

## Arguments

`sql_statement_expression`
:   A string, or an expression that evaluates to a string, containing the SQL statement for which you want the EXPLAIN
    plan.
    If a literal string is used, it should be surrounded by single quote characters `'`.

`sql_query_id_expression`
:   A string, or an expression that evaluates to a string, containing the query ID for which you want the EXPLAIN plan.
    If a literal string is used, it should be surrounded by single quote characters `'`.

    Snowflake retains historical data for query IDs executed within the previous 14 days. If you specify the query ID
    for a query executed more than 14 days in the past, an error is returned. For more information, see
    [Monitor query activity with Query History](/user-guide/ui-snowsight-activity).

## Returns

The function returns a VARCHAR containing the EXPLAIN output in JSON-compatible format.

## Usage notes

- If a string literal is passed as input, the delimiter around the string can be either a single quote `'` or a
  double dollar sign `$$`. If the string literal contains single quotes (and does not contain double dollar
  signs), then delimiting the string with double dollar signs avoids the need to escape the embedded single quote
  characters inside the string.
- SQL statements that would fail if they were run standalone can’t be used as arguments to this function.
  For example, if a CREATE TABLE statement is specified, it can’t be run again (the table name already exists).
  The system function fails with an error when it attempts to recompile the statement.
- To post-process the output of this command, you can:
  - Use the [RESULT\_SCAN](/sql-reference/functions/result_scan) function, which treats the output as a table that can be
    queried.
  - Insert the JSON-formatted output into a table for analysis later.
    If you store the output in JSON format, you can use the function
    [SYSTEM$EXPLAIN\_JSON\_TO\_TEXT](/sql-reference/functions/system_explain_json_to_text) or
    [EXPLAIN\_JSON](/sql-reference/functions/explain_json) to convert the JSON to a more human readable format (either tabular
    or formatted text).

## Examples

These examples use the tables shown below:

Copy code

```
CREATE TABLE Z1 (ID INTEGER);
CREATE TABLE Z2 (ID INTEGER);
CREATE TABLE Z3 (ID INTEGER);
```

This example uses a literal string that contains an SQL statement as the input argument:

Copy code

```
SELECT SYSTEM$EXPLAIN_PLAN_JSON(
  'SELECT Z1.ID, Z2.ID FROM Z1, Z2 WHERE Z2.ID = Z1.ID'
  ) AS explain_plan;
```

```
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| EXPLAIN_PLAN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| {"GlobalStats":{"partitionsTotal":2,"partitionsAssigned":2,"bytesAssigned":1024},"Operations":[[{"id":0,"operation":"Result","expressions":["Z1.ID","Z2.ID"]},{"id":1,"parentOperators":[0],"operation":"InnerJoin","expressions":["joinKey: (Z2.ID = Z1.ID)"]},{"id":2,"parentOperators":[1],"operation":"TableScan","objects":["TESTDB.TEMPORARY_DOC_TEST.Z2"],"expressions":["ID"],"partitionsAssigned":1,"partitionsTotal":1,"bytesAssigned":512},{"id":3,"parentOperators":[1],"operation":"JoinFilter","expressions":["joinKey: (Z2.ID = Z1.ID)"]},{"id":4,"parentOperators":[3],"operation":"TableScan","objects":["TESTDB.TEMPORARY_DOC_TEST.Z1"],"expressions":["ID"],"partitionsAssigned":1,"partitionsTotal":1,"bytesAssigned":512}]]} |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

Use `$$` to delimit queries that contain single quotes:

Copy code

```
SELECT SYSTEM$EXPLAIN_PLAN_JSON(
    $$ SELECT symptom, IFNULL(diagnosis, '(not yet diagnosed)') FROM medical $$
    );
```

The code below shows how to look at the EXPLAIN plan for a query that you already executed.

Run the query:

Copy code

```
SELECT Z1.ID, Z2.ID FROM Z1, Z2 WHERE Z2.ID = Z1.ID;
```

Run EXPLAIN on the query, calling `LAST_QUERY_ID()` to look up the query ID:

Copy code

```
SELECT SYSTEM$EXPLAIN_PLAN_JSON(LAST_QUERY_ID()) AS explain_plan;
```
