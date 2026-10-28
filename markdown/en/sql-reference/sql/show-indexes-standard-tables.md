# SHOW INDEXES (STANDARD TABLE)

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Lists [secondary indexes](/user-guide/search-optimization/secondary-indexes) on a standard table.

See also:
:   [Secondary indexes](/user-guide/search-optimization/secondary-indexes) , [SEARCH\_OPTIMIZATION\_HISTORY view](/sql-reference/account-usage/search_optimization_history)

## Syntax

Copy code

```
SHOW INDEXES IN TABLE <table_name>
```

## Parameters

`IN TABLE table_name`
:   Specifies the standard table whose secondary indexes are listed. Views, materialized views, and Iceberg tables aren’t supported.

## Output

Key expressions and included expressions are ordered lists, shown in square brackets.

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the index was created. |
| `name` | Name of the index. The name is unique for the base table. |
| `is_unique` | Whether the index is unique. A secondary index on a standard table isn’t a unique index. |
| `table` | Name of the base table. |
| `key_expressions` | Ordered list of key expressions, shown in square brackets. |
| `included_expressions` | Ordered list of INCLUDE expressions, shown in square brackets. |
| `database_name` | Database that contains the index. |
| `schema_name` | Schema that contains the index. |
| `owner` | Role that owns the index. |
| `status` | Status of the index:   - `ACTIVE`: The index can be used to retrieve data. - `INVALID`: The index can’t be used to retrieve data. |
| `status_info` | Additional detail about the index status. |
| `owner_role_type` | Role type of the owner. |
| `kind` | Type of index. The value is `ANALYTICAL TABLE INDEX`. |
| `progress_percentage` | Build progress for the index. The value is an integer from 0 through 100. |
| `storage_bytes` | Storage used by the index, in bytes. |

Expand

Show lessSee more

## Usage notes

- Lists indexes for one table. This command doesn’t list secondary indexes at the schema, database, or account level.
- `kind` is `ANALYTICAL TABLE INDEX`.

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

List the secondary indexes on `table_a`:

Copy code

```
SHOW INDEXES IN TABLE table_a;
```
