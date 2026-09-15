# SHOW APPLICATION PACKAGES

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Lists the application packages for which you have access privileges across your entire account in the Native Apps Framework.

The output returns application package metadata and properties, ordered lexicographically by name.
This is important to note if you wish to filter the results using the provided filters.

See also:
:   [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package), [CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package), [DROP APPLICATION PACKAGE](/sql-reference/sql/drop-application-package)

## Syntax

Copy code

```
SHOW APPLICATION PACKAGES [ LIKE '<pattern>' ]
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

## Output

The command output provides application package properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the application package was created. |
| `name` | The name of the application package. |
| `is_default` | Specifies whether the application package is in the default namespace for the current user. |
| `is_current` | Specifies whether the application package is in the current session context. |
| `distribution` | The distribution type of the application package. Valid values are `INTERNAL` and `EXTERNAL`. |
| `owner` | The role that owns the application package. |
| `comment` | Text that provides information about the application package. |
| `options` | Reserved for future use. This field is always empty. |
| `retention_time` | The Time Travel retention period for the application package, in days. |
| `dropped_on` | The date and time when the application package was dropped. `NULL` if the application package has not been dropped. |
| `application_class` | Reserved for internal use. |
| `multiple_instances` | Indicates whether the provider has configured the application package to allow consumers to install multiple instances of an app. Valid values are `TRUE` and `FALSE`. |
| `type` | The type of the application package. This value is always `NATIVE`. |

Expand

Show lessSee more

## Examples

Copy code

```
SHOW APPLICATION PACKAGES;
```

```
+-------------------------------+-------------------------+------------+------------+--------------+----------------+----------+---------+----------------+------------+-------------------+-----------+
| created_on                    | name                    | is_default | is_current | distribution | owner          | comment  | options | retention_time | dropped_on | application_class | type      |
| 2023-06-02 16:28:31.371 -0700 | hello_snowflake_package | N          | N          | INTERNAL     | ACCOUNTADMIN   |          |         | 1              | NULL       | NULL              | NATIVE    |
+-------------------------------+-------------------------+------------+------------+--------------+----------------+----------+---------+----------------+------------+-------------------+-----------+
```
