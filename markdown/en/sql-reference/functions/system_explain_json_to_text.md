Categories:
:   [System functions](/sql-reference/functions-system)

# SYSTEM$EXPLAIN\_JSON\_TO\_TEXT

This function converts EXPLAIN output from JSON to formatted text.

See also:
:   [SYSTEM$EXPLAIN\_PLAN\_JSON](/sql-reference/functions/system_explain_plan_json) , [EXPLAIN\_JSON](/sql-reference/functions/explain_json)

## Syntax

Copy code

```
SYSTEM$EXPLAIN_JSON_TO_TEXT( <explain_output_in_json_format> )
```

## Arguments

`explain_output_in_json_format`
:   A string, or an expression that evaluates to a string, containing EXPLAIN output as a JSON-compatible string.
    If the input is a string, the string should be enclosed in single quotes `'`.

## Returns

The function returns a VARCHAR containing the EXPLAIN output as text that has been formatted to be relatively easy for
humans to read.

## Usage notes

- This function converts EXPLAIN information from JSON to formatted text.
  Often, the JSON value is produced directly or indirectly from the [SYSTEM$EXPLAIN\_PLAN\_JSON](/sql-reference/functions/system_explain_plan_json) function.
  For example, the output from SYSTEM$EXPLAIN\_PLAN\_JSON could be stored in a table, then displayed later using this
  SYSTEM$EXPLAIN\_JSON\_TO\_TEXT function.
- If a string literal is passed as input, the delimiter around the string can be either a single quote `'` or a
  double dollar sign `$$`. If the string literal contains single quotes (and does not contain double dollar
  signs), then delimiting the string with double dollar signs avoids the need to escape the embedded single quote
  characters inside the string.

## Examples

The example(s) below use these tables:

> Copy code
>
> ```
> CREATE TABLE Z1 (ID INTEGER);
> CREATE TABLE Z2 (ID INTEGER);
> CREATE TABLE Z3 (ID INTEGER);
> ```

If you want to store the EXPLAIN output in JSON format, but display it as formatted text, you can call
`SYSTEM$EXPLAIN_JSON_TO_TEXT()` as shown below:

> First, get EXPLAIN output in JSON format and store it in a table:
>
> > Copy code
> >
> > ```
> > SET QUERY_10 = 'SELECT Z1.ID, Z2.ID FROM Z1, Z2 WHERE Z2.ID = Z1.ID';
> > CREATE TABLE json_explain_output_for_analysis (
> >     ID INTEGER,
> >     query VARCHAR,
> >     explain_plan VARCHAR
> >     );
> > INSERT INTO json_explain_output_for_analysis (ID, query, explain_plan) 
> >     SELECT 
> >         1,
> >         $QUERY_10 AS query,
> >         SYSTEM$EXPLAIN_PLAN_JSON($QUERY_10) AS explain_plan;
> > ```
>
> The JSON looks like the output shown below:
>
> > Copy code
> >
> > ```
> > SELECT query, explain_plan FROM json_explain_output_for_analysis;
> > +-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> > | QUERY                                               | EXPLAIN_PLAN                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
> > |-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
> > | SELECT Z1.ID, Z2.ID FROM Z1, Z2 WHERE Z2.ID = Z1.ID | {"GlobalStats":{"partitionsTotal":2,"partitionsAssigned":2,"bytesAssigned":1024},"Operations":[[{"id":0,"operation":"Result","expressions":["Z1.ID","Z2.ID"]},{"id":1,"parentOperators":[0],"operation":"InnerJoin","expressions":["joinKey: (Z2.ID = Z1.ID)"]},{"id":2,"parentOperators":[1],"operation":"TableScan","objects":["TESTDB.TEMPORARY_DOC_TEST.Z2"],"expressions":["ID"],"partitionsAssigned":1,"partitionsTotal":1,"bytesAssigned":512},{"id":3,"parentOperators":[1],"operation":"JoinFilter","expressions":["joinKey: (Z2.ID = Z1.ID)"]},{"id":4,"parentOperators":[3],"operation":"TableScan","objects":["TESTDB.TEMPORARY_DOC_TEST.Z1"],"expressions":["ID"],"partitionsAssigned":1,"partitionsTotal":1,"bytesAssigned":512}]]} |
> > +-----------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> > ```
>
> After you have stored the JSON in a table, you can pass the JSON to the SYSTEM$EXPLAIN\_JSON\_TO\_TEXT function to
> convert it to a more human-readable text format by calling SYSTEM$EXPLAIN\_JSON\_TO\_TEXT:
>
> > Copy code
> >
> > ```
> > SELECT SYSTEM$EXPLAIN_JSON_TO_TEXT(explain_plan) 
> >     FROM json_explain_output_for_analysis
> >     WHERE json_explain_output_for_analysis.ID = 1;
> > +------------------------------------------------------------------------------------------------------------------------------------+
> > | SYSTEM$EXPLAIN_JSON_TO_TEXT(EXPLAIN_PLAN)                                                                                          |
> > |------------------------------------------------------------------------------------------------------------------------------------|
> > | GlobalStats:                                                                                                                       |
> > | 	bytesAssigned=1024                                                                                                                                                                                                                                                                         |
> > | 	partitionsAssigned=2                                                                                                                                                                                                                                                                         |
> > | 	partitionsTotal=2                                                                                                                                                                                                                                                                         |
> > | Operations:                                                                                                                        |
> > | 1:0     ->Result  Z1.ID, Z2.ID                                                                                                     |
> > | 1:1          ->InnerJoin  joinKey: (Z2.ID = Z1.ID)                                                                                 |
> > | 1:2               ->TableScan  TESTDB.TEMPORARY_DOC_TEST.Z2  ID  {partitionsTotal=1, partitionsAssigned=1, bytesAssigned=512}      |
> > | 1:3               ->JoinFilter  joinKey: (Z2.ID = Z1.ID)                                                                           |
> > | 1:4                    ->TableScan  TESTDB.TEMPORARY_DOC_TEST.Z1  ID  {partitionsTotal=1, partitionsAssigned=1, bytesAssigned=512} |
> > |                                                                                                                                    |
> > +------------------------------------------------------------------------------------------------------------------------------------+
> > ```
