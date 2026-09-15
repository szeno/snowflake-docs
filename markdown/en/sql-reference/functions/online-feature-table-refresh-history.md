Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# ONLINE\_FEATURE\_TABLE\_REFRESH\_HISTORY

This table function returns information about each refresh (completed and running) of [online feature tables](/sql-reference/sql/create-online-feature-table).

This table function returns all refreshes that are in progress as well as all refreshes that have a REFRESH\_START\_TIME within 7 days of the current time.

See also:
:   [CREATE ONLINE FEATURE TABLE](/sql-reference/sql/create-online-feature-table) , [ALTER ONLINE FEATURE TABLE](/sql-reference/sql/alter-online-feature-table), [DESCRIBE ONLINE FEATURE TABLE](/sql-reference/sql/desc-online-feature-table) , [DROP ONLINE FEATURE TABLE](/sql-reference/sql/drop-online-feature-table) , [SHOW ONLINE FEATURE TABLES](/sql-reference/sql/show-online-feature-tables)

## Syntax

Copy code

```
ONLINE_FEATURE_TABLE_REFRESH_HISTORY(
  [ REFRESH_START_TIMESTAMP => <constant_expr> ]
  [ , REFRESH_END_TIMESTAMP => <constant_expr> ]
  [ , RESULT_LIMIT => <integer> ]
  [ , NAME => '<string>' ]
  [ , NAME_PREFIX => '<string>' ]
  [ , ERROR_ONLY => { TRUE | FALSE } ]
)
```

## Arguments

All the arguments are optional. If no arguments are provided, 100 refreshes from all online feature tables in the account will be returned.

`REFRESH_START_TIMESTAMP => constant_expr` , `REFRESH_END_TIMESTAMP => constant_expr`
:   Time range (in TIMESTAMP\_LTZ format) during which the refreshes started. If an end version is not specified, CURRENT\_TIMESTAMP is used as the end of the range.

`RESULT_LIMIT => integer`
:   A number specifying the maximum number of rows returned by the function. If the number of matching rows is greater than this limit, the refreshes that finished most recently (and those that are still running) are returned, up to the specified limit.

    Range: 1 to 10000

    Default: 100.

`NAME => 'string'`
:   The name of an online feature table.

    You can specify the unqualified name (`online_feature_table_name`), the partially qualified name (`schema_name.online_feature_table_name`), or the fully qualified name (`database_name.schema_name.online_feature_table_name`).

    > For more information on object name resolution, see [Object name resolution](/sql-reference/name-resolution).

    The function returns the refreshes for this table.

`NAME_PREFIX => 'string'`
:   A prefix for online feature tables.

    The function returns refreshes for tables with names that start with this prefix.

    You can use this argument to return the refreshes for online feature tables in a specific database or schema.

`ERROR_ONLY => { TRUE | FALSE }`
:   When set to TRUE, this function returns only refreshes that failed or were cancelled.

    Default: FALSE

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Data type | Description |
| --- | --- | --- |
| `NAME` | TEXT | Name of the online feature table. |
| `SCHEMA_NAME` | TEXT | Name of the schema that contains the online feature table. |
| `DATABASE_NAME` | TEXT | Name of the database that contains the online feature table. |
| `QUALIFIED_NAME` | TEXT | Fully qualified name of the online feature table. |
| `STATE` | TEXT | Status of the refresh for the online feature table. The status can be one of the following:   - `EXECUTING`: refresh in progress. - `SUCCEEDED`: refresh completed successfully. - `FAILED`: refresh failed during execution. - `CANCELLED`: refresh was canceled before completion. |
| `REFRESH_START_TIME` | TIMESTAMP\_LTZ | Time when the refresh job started. |
| `REFRESH_END_TIME` | TIMESTAMP\_LTZ | Time when the refresh completed. |
| `REFRESH_TRIGGER` | TEXT | One of:   - `SCHEDULED`: normal background refresh to meet target lag. - `MANUAL`: user/task ran `ALTER ONLINE FEATURE TABLE <name> REFRESH` command. - `CREATION`: refresh performed during the creation DDL statement, triggered by the creation of the online feature table. |
| `REFRESH_ACTION` | TEXT | One of:   - `NO_DATA`: no new data in base tables. Doesn’t apply to the initial refresh of newly created online feature tables regardless of whether or not the base tables have data. - `REINITIALIZE`: base table changed. - `FULL`: Full refresh, because refresh mode of the online feature table is set to FULL. - `INCREMENTAL`: normal incremental refresh. |
| `QUERY_ID` | TEXT | ID of the SQL statement that produced the results for the online feature table. |
| `STATE_CODE` | TEXT | Code representing the current state of the refresh. |
| `STATE_MESSAGE` | TEXT | Description of the current state of the refresh. |

Expand

Show lessSee more

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| MONITOR | Online feature table | Role that has the MONITOR privilege on the online feature table. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- This function is available in the INFORMATION\_SCHEMA.
- The information returned by this function is up to date. Online Feature Table refresh history in the ACCOUNT\_USAGE.ONLINE\_FEATURE\_TABLE\_REFRESH\_HISTORY view may lag by up to 3 hours.

## Examples

The following example returns the refresh history for all online feature tables in the account:

Copy code

```
SELECT *
FROM TABLE(INFORMATION_SCHEMA.ONLINE_FEATURE_TABLE_REFRESH_HISTORY());
```

The following example returns the refresh history for a specific online feature table named `my_feature_table`:

Copy code

```
SELECT *
FROM TABLE(INFORMATION_SCHEMA.ONLINE_FEATURE_TABLE_REFRESH_HISTORY(
  NAME => 'my_feature_table'
));
```

The following example returns only failed refreshes from the last 24 hours:

Copy code

```
SELECT *
FROM TABLE(INFORMATION_SCHEMA.ONLINE_FEATURE_TABLE_REFRESH_HISTORY(
  REFRESH_START_TIMESTAMP => CURRENT_TIMESTAMP - INTERVAL '1 DAY',
  ERROR_ONLY => TRUE
));
```

The following example returns refreshes for online feature tables with names starting with `feature_` and limits the results to 50 rows:

Copy code

```
SELECT *
FROM TABLE(INFORMATION_SCHEMA.ONLINE_FEATURE_TABLE_REFRESH_HISTORY(
  NAME_PREFIX => 'feature_',
  RESULT_LIMIT => 50
));
```
