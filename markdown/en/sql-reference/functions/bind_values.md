Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# BIND\_VALUES

This INFORMATION\_SCHEMA table function returns information about the values of
[bind variables](/sql-reference/bind-variables) used in queries.

## Syntax

Copy code

```
BIND_VALUES( <query_id> )
```

## Arguments

`query_id`
:   The string identifier of a query that includes one or more bind variables.

    Snowflake query IDs are unique strings that resemble `01b71944-0001-b181-0000-0129032279f6`.

    If NULL, an empty table is returned.

## Usage notes

- Returns bind variable values for queries that are run by the current user. Also returns bind variable values for queries
  that are run by any user when the role that is currently active in a user’s session, or a higher role in a hierarchy,
  has the MONITOR or OPERATE privilege on the user-managed warehouses where the queries were run. For more information,
  see [Virtual warehouse privileges](/user-guide/security-access-control-privileges#label-warehouse-privileges).
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the
  function name must be fully qualified. For more information, see [Snowflake Information Schema](/sql-reference/info-schema).
- This function can return all queries run in the past seven days.
- This function might not return the bind values or might return an error for the following scenarios:
  - The [ALLOW\_BIND\_VALUES\_ACCESS](/sql-reference/parameters#label-allow-bind-values-access) account-level parameter is set to `FALSE`.
  - The bind variables have large values that exceed Snowflake storage thresholds.
  - The queries have a large number of bind variables that exceed Snowflake storage thresholds.
  - The bind variables contain sensitive data. The extraction and processing are done on a best-effort basis, and
    whether data is considered sensitive depends on the context.
  - The function call specifies a query that includes [array binds](/sql-reference/bind-variables#label-bind-variables-array-binds).
  - The function call specifies a query that doesn’t exist.
  - The function call specifies a query that has expired and is no longer in the query history.

## Output

The BIND\_VALUES table function produces one row for each bind variable that is used in the specified query. Each row contains the
following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| QUERY\_ID | VARCHAR | The ID of the query. |
| POSITION | NUMBER | For positional bind variables, the position of the bind variable. The field is NULL for named bind variables. |
| NAME | VARCHAR | For named bind variables, the name of the bind variable. The field is NULL for positional bind variables. |
| TYPE | VARCHAR | The Snowflake data type of the bind variable. |
| VALUE | VARCHAR | The value of the bind variable. Bind values that contain more than 100,000 characters are truncated. |

Expand

Show lessSee more

## Examples

See [Retrieve bind variable values](/sql-reference/bind-variables#label-bind-variables-retrieving-values).
