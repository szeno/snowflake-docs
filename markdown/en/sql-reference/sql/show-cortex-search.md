# SHOW CORTEX SEARCH SERVICES

Lists the [Cortex Search services](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) for which you have access
privileges.

## Syntax

Copy code

```
SHOW CORTEX SEARCH SERVICES
  [ LIKE PATTERN '<pattern>' ]
  [ STARTS WITH '<name_string>' ]
  [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

> `LIKE 'pattern'`
> :   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
>     wildcard characters (`%` and `_`).
>
>     For example, the following patterns return the same results:
>
>     `... LIKE '%testing%' ...`
>     `... LIKE '%TESTING%' ...`
>
>     Default: No value (no filtering is applied to the output).
>
> `STARTS WITH 'name_string'`
> :   Optionally filters the command output based on the characters that appear at the beginning of
>     the object name. The string must be enclosed in single quotes and is case sensitive.
>
>     For example, the following strings return different results:
>
>     `... STARTS WITH 'B' ...`
>     `... STARTS WITH 'b' ...`
>
>     Default: No value (no filtering is applied to the output)
>
> `LIMIT rows [ FROM 'name_string' ]`
> :   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
>     returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.
>
>     The optional `FROM 'name_string'` subclause effectively serves as a “cursor” for the results. This enables fetching the
>     specified number of rows following the first row whose object name matches the specified string:
>
>     - The string must be enclosed in single quotes and is case sensitive.
>     - The string does not have to include the full object name; partial names are supported.
>
>     Default: No value (no limit is applied to the output)
>
>     Note
>
>     For SHOW commands that support both the `FROM 'name_string'` and `STARTS WITH 'name_string'` clauses, you can combine
>     both of these clauses in the same statement. However, both conditions must be met or they cancel out each other and no results are
>     returned.
>
>     In addition, objects are returned in lexicographic order by name, so `FROM 'name_string'` only returns rows with a higher
>     lexicographic value than the rows returned by `STARTS WITH 'name_string'`.
>
>     For example:
>
>     - `... STARTS WITH 'A' LIMIT ... FROM 'B'` would return no results.
>     - `... STARTS WITH 'B' LIMIT ... FROM 'A'` would return no results.
>     - `... STARTS WITH 'A' LIMIT ... FROM 'AB'` would return results (if any rows match the input strings).

## Output

The command output provides the Cortex Search service properties and metadata in the following columns:

| Column | Data Type | Description |
| --- | --- | --- |
| `created_on` | TIMESTAMP\_LTZ | Creation time of the Cortex Search Service. |
| `name` | TEXT | Name of the service. |
| `schema_name` | TEXT | The schema in which the service resides. |
| `database_name` | TEXT | The database in which the service resides. |
| `warehouse` | TEXT | The warehouse used for service refreshes. |
| `target_lag` | TEXT | The maximum amount of time that the service’s content should lag behind updates to the base tables. |
| `comment` | TEXT | Any comments associated with the service. |
| `definition` | TEXT | SQL query used to create the service. |
| `search_column` | TEXT | Name of the search column. |
| `attribute_columns` | TEXT | Comma-separated list of attribute columns in the service. |
| `columns` | TEXT | Comma-separated list of columns in the service. |
| `primary_key_columns` | TEXT | Comma-separated list of [primary key column](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys) names defined on the service. Empty if no primary key is set. |
| `scoring_profile_count` | NUMBER | The number of [named scoring profiles](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-named-scoring-profiles) defined in the service. |

Expand

Show lessSee more

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

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

The following example lists the Cortex Search service that you have the privileges to view in the PUBLIC schema of the `mydb` database:

Copy code

```
USE DATABASE mydb;

SHOW CORTEX SEARCH SERVICES;
```
