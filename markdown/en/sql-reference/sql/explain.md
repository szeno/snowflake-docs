# EXPLAIN

Returns the logical execution plan for the specified SQL statement.

An explain plan shows the operations (for example, table scans and joins) that Snowflake would perform to execute the
query.

See also:
:   [SYSTEM$EXPLAIN\_PLAN\_JSON](/sql-reference/functions/system_explain_plan_json) ,
    [SYSTEM$EXPLAIN\_JSON\_TO\_TEXT](/sql-reference/functions/system_explain_json_to_text) ,
    [EXPLAIN\_JSON](/sql-reference/functions/explain_json)

## Syntax

Copy code

```
EXPLAIN [ USING { TABULAR | JSON | TEXT } ] <statement>
```

## Parameters

`statement`
:   This is the SQL statement for which you want the explain plan.

`USING output_format`
:   This optional clause specifies the output format. The possible output formats are:

    - JSON: JSON output is easier to store in a table and query.
    - TABULAR: tabular output is generally more human-readable than JSON output.
    - TEXT: formatted text output is generally more human-readable than JSON output.

    The default is TABULAR.

## Output

The output contains the following information:

| Column | Description |
| --- | --- |
| `step` | Most queries contain a single step, but some are executed as multiple distinct steps. This column denotes to which step the operation belongs. |
| `id` | Unique identifier assigned to each operation in the query plan. |
| `parentOperators` | Array of identifiers for the operation’s parent nodes. In the query profile, a parent is shown above its child with a link connecting the two. |
| `operation` | Name of the operation, for example, Result, Filter, TableScan, Join, or CreateTableFromArchiveData. |
| `objects` | Name of the object referenced by a table scan operation, for example, table, materialized view, secure view, or ARCHIVE OF <table>. |
| `alias` | Alias of a referenced object, if the object has been given an alias in the query. |
| `expressions` | List of expressions relevant to the current operation such as filters, join predicates, projections, aggregations, etc. |
| `partitionsTotal` | The total number of micro-partitions in the referenced database object. |
| `partitionsAssigned` | The number of partitions from the referenced object that are left after compile-time pruning, i.e. the number of partitions that might be scanned by the query. |
| `bytesAssigned` | The number of bytes contained in the partitionsAssigned. |

Expand

Show lessSee more

## Usage notes

- EXPLAIN compiles the SQL statement, but does not execute it, so EXPLAIN does not require a running warehouse.
- The EXPLAIN plan might differ depending on the size of the current warehouse. If you run EXPLAIN outside of a
  current warehouse, Snowflake constructs the EXPLAIN plan based on the capacity of an XSMALL warehouse.
- Although EXPLAIN does not consume any compute credits, the compilation of the query does consume Cloud Service
  credits, just as other metadata operations do.
- To post-process the output of this command, you can:

  - Use the [RESULT\_SCAN](/sql-reference/functions/result_scan) function, which treats the output as a table that can be
    queried.
  - Generate the output in JSON format and insert the JSON-formatted output into a table for analysis later.
    If you store the output in JSON format, you can use the function [SYSTEM$EXPLAIN\_JSON\_TO\_TEXT](/sql-reference/functions/system_explain_json_to_text) or
    [EXPLAIN\_JSON](/sql-reference/functions/explain_json) to convert the JSON to a more human readable format (either tabular or formatted text).
- The assignedPartitions and assignedBytes values are upper bound estimates for query execution. Runtime optimizations
  such as join pruning can reduce the number of partitions and bytes scanned during query execution.
- The EXPLAIN plan is the “logical” explain plan. It shows the operations that will be performed, and their
  logical relationship to each other. The actual execution order of the operations in the plan does not necessarily
  match the logical order shown by the plan.
- If any of the database objects in the EXPLAIN statement are INFORMATION\_SCHEMA objects, the statement fails with error
  `EXPLAIN command has insufficient privilege on object <objName>`.

## Examples

This example shows the EXPLAIN output for a simple query against two small tables.

> Create the tables:
>
> > Copy code
> >
> > ```
> > CREATE TABLE Z1 (ID INTEGER);
> > CREATE TABLE Z2 (ID INTEGER);
> > CREATE TABLE Z3 (ID INTEGER);
> > ```
>
> Generate the EXPLAIN plan in tabular format for the query:
>
> > Copy code
> >
> > ```
> > EXPLAIN USING TABULAR SELECT Z1.ID, Z2.ID
> >     FROM Z1, Z2
> >     WHERE Z2.ID = Z1.ID;
> > +------+------+-----------------+-------------+------------------------------+-------+--------------------------+-----------------+--------------------+---------------+
> > | step | id   | parentOperators | operation   | objects                      | alias | expressions              | partitionsTotal | partitionsAssigned | bytesAssigned |
> > |------+------+-----------------+-------------+------------------------------+-------+--------------------------+-----------------+--------------------+---------------|
> > | NULL | NULL |            NULL | GlobalStats | NULL                         | NULL  | NULL                     |               2 |                  2 |          1024 |
> > |    1 |    0 |            NULL | Result      | NULL                         | NULL  | Z1.ID, Z2.ID             |            NULL |               NULL |          NULL |
> > |    1 |    1 |             [0] | InnerJoin   | NULL                         | NULL  | joinKey: (Z2.ID = Z1.ID) |            NULL |               NULL |          NULL |
> > |    1 |    2 |             [1] | TableScan   | TESTDB.TEMPORARY_DOC_TEST.Z2 | NULL  | ID                       |               1 |                  1 |           512 |
> > |    1 |    3 |             [1] | JoinFilter  | NULL                         | NULL  | joinKey: (Z2.ID = Z1.ID) |            NULL |               NULL |          NULL |
> > |    1 |    4 |             [3] | TableScan   | TESTDB.TEMPORARY_DOC_TEST.Z1 | NULL  | ID                       |               1 |                  1 |           512 |
> > +------+------+-----------------+-------------+------------------------------+-------+--------------------------+-----------------+--------------------+---------------+
> > ```
>
> Generate the EXPLAIN plan for the query as formatted text:
>
> > Copy code
> >
> > ```
> > EXPLAIN USING TEXT SELECT Z1.ID, Z2.ID
> >     FROM Z1, Z2
> >     WHERE Z2.ID = Z1.ID;
> > +------------------------------------------------------------------------------------------------------------------------------------+
> > | content                                                                                                                            |
> > |------------------------------------------------------------------------------------------------------------------------------------|
> > | GlobalStats:                                                                                                                       |
> > |     partitionsTotal=2                                                                                                              |
> > |     partitionsAssigned=2                                                                                                           |
> > |     bytesAssigned=1024                                                                                                             |
> > | Operations:                                                                                                                        |
> > | 1:0     ->Result  Z1.ID, Z2.ID                                                                                                     |
> > | 1:1          ->InnerJoin  joinKey: (Z2.ID = Z1.ID)                                                                                 |
> > | 1:2               ->TableScan  TESTDB.TEMPORARY_DOC_TEST.Z2  ID  {partitionsTotal=1, partitionsAssigned=1, bytesAssigned=512}      |
> > | 1:3               ->JoinFilter  joinKey: (Z2.ID = Z1.ID)                                                                           |
> > | 1:4                    ->TableScan  TESTDB.TEMPORARY_DOC_TEST.Z1  ID  {partitionsTotal=1, partitionsAssigned=1, bytesAssigned=512} |
> > |                                                                                                                                    |
> > +------------------------------------------------------------------------------------------------------------------------------------+
> > ```
>
> Generate the EXPLAIN plan for the query as JSON:
>
> > Copy code
> >
> > ```
> > EXPLAIN USING JSON SELECT Z1.ID, Z2.ID
> >     FROM Z1, Z2
> >     WHERE Z2.ID = Z1.ID;
> > +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> > | content                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
> > |---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
> > | {"GlobalStats":{"partitionsTotal":2,"partitionsAssigned":2,"bytesAssigned":1024},"Operations":[[{"id":0,"operation":"Result","expressions":["Z1.ID","Z2.ID"]},{"id":1,"parentOperators":[0],"operation":"InnerJoin","expressions":["joinKey: (Z2.ID = Z1.ID)"]},{"id":2,"parentOperators":[1],"operation":"TableScan","objects":["TESTDB.TEMPORARY_DOC_TEST.Z2"],"expressions":["ID"],"partitionsAssigned":1,"partitionsTotal":1,"bytesAssigned":512},{"id":3,"parentOperators":[1],"operation":"JoinFilter","expressions":["joinKey: (Z2.ID = Z1.ID)"]},{"id":4,"parentOperators":[3],"operation":"TableScan","objects":["TESTDB.TEMPORARY_DOC_TEST.Z1"],"expressions":["ID"],"partitionsAssigned":1,"partitionsTotal":1,"bytesAssigned":512}]]} |
> > +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> > ```
