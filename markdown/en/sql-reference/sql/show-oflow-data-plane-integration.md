# SHOW OPENFLOW DATA PLANE INTEGRATIONS

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

List OPENFLOW DATA PLANE INTEGRATIONS.
Shows only OPENFLOW DATA PLANE INTEGRATIONS where the user running the command
has any of USAGE, MODIFY, or OWNERSHIP against the OPENFLOW DATA PLANE INTEGRATION.

See also:
:   [ALTER OPENFLOW DATA PLANE](/sql-reference/sql/alter-oflow-data-plane), [DESCRIBE OPENFLOW DATA PLANE INTEGRATION](/sql-reference/sql/desc-oflow-data-plane-integration)

## Syntax

Copy code

```
SHOW OPENFLOW DATA PLANE INTEGRATIONS [ LIKE '<pattern>' ]
              [ STARTS WITH '<name_string>' ]
              [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Optional parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows [ FROM 'name_string' ]`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

    The optional `FROM 'name_string'` subclause effectively serves as a “cursor” for the results. This enables fetching the
    specified number of rows following the first row whose object name matches the specified string:

    - The string must be enclosed in single quotes and is case sensitive.
    - The string does not have to include the full object name; partial names are supported.

    Default: No value (no limit is applied to the output)

    Note

    For SHOW commands that support both the `FROM 'name_string'` and `STARTS WITH 'name_string'` clauses, you can combine
    both of these clauses in the same statement. However, both conditions must be met or they cancel out each other and no results are
    returned.

    In addition, objects are returned in lexicographic order by name, so `FROM 'name_string'` only returns rows with a higher
    lexicographic value than the rows returned by `STARTS WITH 'name_string'`.

    For example:

    - `... STARTS WITH 'A' LIMIT ... FROM 'B'` would return no results.
    - `... STARTS WITH 'B' LIMIT ... FROM 'A'` would return no results.
    - `... STARTS WITH 'A' LIMIT ... FROM 'AB'` would return results (if any rows match the input strings).

## Usage notes

- Openflow data plane integrations cannot be created directly, but rather are created when a deployment is created.
- To SHOW an OPENFLOW DATA PLANE INTEGRATION, you must be using a role that has USAGE, MODIFY, or OWNERSHIP privilege on the Openflow data plane integration.

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

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

## Output

The command output provides Openflow data plane integration properties and metadata in the following columns:

|  |  |
| --- | --- |
| Column | Description |
| `name` | Name of the Openflow data plane integration |
| `type` | Always `OPENFLOW_DATA_PLANE` |
| `category` | Always `OPENFLOW_DATA_PLANE` |
| `enabled` | True if enabled, otherwise false |
| `comment` | Associated comment. |
| `created_on` | Date and time the data plane integration was created |
| `data_plane_id` | Internal identifier for the data plane integration |

Expand

Show lessSee more

## Examples

Show all the data plane integrations with names that start with MYDATAPLANE:

> Copy code
>
> ```
> SHOW OPENFLOW DATA PLANE INTEGRATIONS LIKE 'MYDATAPLANE%'
> ```
