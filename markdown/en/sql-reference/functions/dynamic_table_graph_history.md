Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# DYNAMIC\_TABLE\_GRAPH\_HISTORY

This table function returns information on all [dynamic tables](/user-guide/dynamic-tables/overview) in the current account.
This information includes the dependencies between dynamic tables and on base tables.
A common use is to identify all dynamic tables that are part of a pipeline.

In the output of this function, each row represents a dynamic table.
The VALID\_FROM and VALID\_TO columns specify the range of time over which the description of a dynamic table was valid
(i.e., accurately described the dynamic table).

Changes to a dynamic table such as altering the TARGET\_LAG result in the creation of new entries.

This table function provides only descriptions with a VALID\_TO value within 7 days of the current time.

## Syntax

Copy code

```
DYNAMIC_TABLE_GRAPH_HISTORY(
  [ AS_OF => <constant_expr> ]
  [ , HISTORY_START => <constant_expr> [ , HISTORY_END => <constant_expr> ] ]
)
```

## Arguments

All arguments are optional. If no arguments are provided, only the most recent description of existing dynamic tables are returned. Specify `constant_expr` in [TIMESTAMP\_LTZ format](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations).

`AS_OF => constant_expr`
:   Time at which to return the state of the graph. You can specify a time that corresponds to a value in
    the REFRESH\_VERSION column in the output of the [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) function.

`HISTORY_START => constant_expr` , `HISTORY_END => constant_expr`
:   Date/time range of the dynamic table refresh history.
    HISTORY\_START specifies the earliest date/time, inclusive, to return data.
    HISTORY\_END, which must be specified with HISTORY\_START, specifies the end date/time for returning data.

## Output

The function returns the following columns.

To view these columns, you must use a role with the MONITOR privilege. Otherwise, the function only returns a value for `NAME`,
`SCHEMA_NAME`, `DATABASE_NAME`, and `QUALIFIED_NAME`. For more information about dynamic table privileges, see
[Grant MONITOR to view metadata](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges-view-metadata).

| Column Name | Data Type | Description |
| --- | --- | --- |
| NAME | TEXT | Name of the dynamic table. |
| SCHEMA\_NAME | TEXT | Name of the schema that contains the dynamic table. |
| DATABASE\_NAME | TEXT | Name of the database that contains the dynamic table. |
| QUALIFIED\_NAME | TEXT | Fully qualified name of the dynamic table as it appears in the graph of dynamic tables. You can use this to join the output with the output of the [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) function. |
| INPUTS | ARRAY of OBJECTs | Each OBJECT represents a table, view, or dynamic table that serves as the input to this dynamic table, and consists of:   - `name` (TEXT): fully qualified name. - `kind` (TEXT): type of input (TABLE, VIEW, or DYNAMIC TABLE). - `insideRefreshBoundary` (BOOLEAN): only present for VIEW and DYNAMIC TABLE inputs when the value is TRUE, indicating the   input is wrapped in [DYNAMIC\_TABLE\_REFRESH\_BOUNDARY()](/user-guide/dynamic-tables/data-consistency). Inputs inside a refresh   boundary are not refreshed together with this dynamic table. |
| TARGET\_LAG\_TYPE | TEXT | One of:   - USER\_DEFINED - Determined by the TARGET\_LAG parameter specified for the dynamic table. - DOWNSTREAM - Indicates a dynamic table with a DOWNSTREAM TARGET\_LAG. Refer to [Understanding dynamic table initialization and refresh](/user-guide/dynamic-tables/refresh-modes) for more information. |
| TARGET\_LAG\_SEC | NUMBER | The target lag time in seconds of this dynamic table. This is the value that was specified in the TARGET\_LAG parameter of the dynamic table. |
| QUERY\_TEXT | TEXT | The SELECT statement for this dynamic table. |
| VALID\_FROM | TIMESTAMP\_LTZ | The description of the dynamic table is valid after this time. |
| VALID\_TO | TIMESTAMP\_LTZ | If present, the description of the dynamic table is valid up to this time. If null, the description is still accurate. |
| SCHEDULING\_STATE | OBJECT | OBJECT consisting of:   - `state` (TEXT): Scheduling state (ACTIVE or SUSPENDED). - `reason_code` (TEXT): Optional reason for the reason if the state is not ACTIVE. - `reason_message` (TEXT): Text description of the reason the dynamic table is not active.   Only applies if the state is not active. - `suspended_on` (TIMESTAMP\_LTZ): Optional timestamp when the dynamic table was suspended. - `resumed_on` (TIMESTAMP\_LTZ): Optional timestamp when it was last resumed if dynamic table is ACTIVE. |
| ALTER\_TRIGGER | ARRAY | Describes why a new entry is created in the DYNAMIC\_TABLE\_GRAPH\_HISTORY function. Can be one of the following:   - NONE (backwards-compatible) - CREATE\_DYNAMIC\_TABLE - ALTER\_TARGET\_LAG - SUSPEND - RESUME - REPLICATION\_REFRESH - ALTER\_WAREHOUSE |

Expand

Show lessSee more

## Usage notes

- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully qualified. For more information, see [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

Retrieve the graph history of each dynamic table in the account, its properties, and its dependencies on other tables and dynamic tables:

> Copy code
>
> ```
> SELECT
>   name,
>   inputs,
>   target_lag_type,
>   target_lag_sec,
>   scheduling_state,
>   alter_trigger
> FROM
>   TABLE (
>     INFORMATION_SCHEMA.DYNAMIC_TABLE_GRAPH_HISTORY ()
>   )
> ORDER BY
>   name;
> ```
>
> ```
> +--------------------+---------------------------------------------------+-----------------+----------------+---------------------------------------------+------------------+
> | NAME               |[] INPUTS                                          | TARGET_LAG_TYPE | TARGET_LAG_SEC | [] SCHEDULING_STATE                         | [] ALTER_TRIGGER |
> |--------------------+---------------------------------------------------+-----------------+----------------+---------------------------------------------|------------------+
> | MY_DYNAMIC_TABLE_1 | [                                                 | USER_DEFINED    | 300            | {                                           | [                |
> |                    |  {                                                |                 |                |   "resumed_on": "2024-03-01 10:29:02.066 Z",|   "RESUME"       |
> |                    |    "kind": "DYNAMIC_TABLE",                       |                 |                |   "state": "ACTIVE"                         | ]                |
> |                    |    "name": "MY_QUALIFIED_NAME.MY_DYNAMIC_TABLE_2" |                 |                | }                                           |                  |
> |                    |  }                                                |                 |                |                                             |                  |
> |                    | ]                                                 |                 |                |                                             |                  |
> +--------------------+---------------------------------------------------+-----------------+----------------+---------------------------------------------+------------------+
> ```
