# SHOW APPLICATIONS

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Lists the Snowflake Native Apps that you have access privileges for across your entire account.

The output returns metadata and properties for the app, ordered lexicographically
by name. This is important to note if you want to filter the results using the provided filters.

See also:
:   [ALTER APPLICATION](/sql-reference/sql/alter-application),
    [CREATE APPLICATION](/sql-reference/sql/create-application),
    [DESCRIBE APPLICATION](/sql-reference/sql/desc-application),
    [DROP APPLICATION](/sql-reference/sql/drop-application)

## Syntax

Copy code

```
SHOW APPLICATIONS [ LIKE '<pattern>' ]
  [ STARTS WITH '<name_string>' ]
  [ LIMIT <rows> [ FROM '<name_string>' ] ];
```

## Parameters

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

## Output

The command output provides app properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the app was created. |
| `name` | The name of the app. |
| `is_default` | Specifies whether the app is in the default namespace for the user. |
| `is_current` | Specifies whether the app is in the current session context. |
| `source_type` | Specifies the source of the app. The following values are valid:   - APPLICATION PACKAGE - LISTING |
| `source` | The name of the application package or listing used to create the app. |
| `owner` | The role used to create the app. |
| `comment` | Text that provides information about the app. |
| `version` | The version identifier used to create the app. |
| `label` | The version label of the app. This label is visible to consumers when they install an app. |
| `patch` | The patch number used to create the app. |
| `options` | For an app, this field is always empty. |
| `retention_time` | The retention time of the app. |
| `upgrade_state` | The current state of the background installation or upgrade of the app. See [Application version upgrade states](/sql-reference/data-sharing-usage/application-state-view#label-app-state-view-application-version-upgrade-states) for more information. |
| `disablement_reasons` | The reason why the app was disabled. For more information, see [Disabled apps](/developer-guide/native-apps/release-channels-upgrade#label-native-apps-disabled-apps). |
| `last_upgraded_on` | The timestamp when the app was last upgraded. |
| `release_channel_name` | The name of the release channel used to create the app. If the app was not created from a release channel, the value of this property is `default`. |
| `type` | The type of the application. This value is always `NATIVE`. |

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

Copy code

```
SHOW APPLICATIONS;
```

```
+-------------------------------+------------------------+------------+------------+---------------------+----------------------------+---------------+---------+---------------------+-----------------+-------+---------+----------------+---------------+-----------+
| created_on                    | name                   | is_default | is_current | source_type         | source                     | owner         | comment | version             | label           | patch | options | retention_time | upgrade_state | type      |
|-------------------------------+------------------------+------------+------------+---------------------+----------------------------+---------------+---------+---------------------+-----------------+-------+---------+----------------|---------------+-----------+
| 2023-02-03 10:14:09.828 -0800 | hello_snowflake_app    | N          | Y          | APPLICATION PACKAGE | hello_snowflake_package    | PROVIDER_ROLE |         | v1                  | Version v1      |     0 |         | 1              | COMPLETE      | NATIVE    |
| 2023-03-22 16:12:40.373 -0700 | PRODUCTION_APP         | Y          | Y          | APPLICATION PACKAGE | hello_snowflake_package    | PROVIDER_ROLE |         | v2                  | Version v2      |     0 |         | 1              | COMPLETE      | NATIVE    |
+-------------------------------+------------------------+------------+------------+---------------------+----------------------------+---------------+---------+---------------------+-----------------+-------+---------+----------------+---------------+-----------+
```
