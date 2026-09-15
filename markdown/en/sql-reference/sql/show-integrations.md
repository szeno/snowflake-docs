# SHOW INTEGRATIONS

Lists the integrations in your account.

The output returns integration metadata and properties.

See also:
:   [CREATE INTEGRATION](/sql-reference/sql/create-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [ALTER INTEGRATION](/sql-reference/sql/alter-integration) , [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

API integrations:
:   [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration)

Catalog integrations:
:   [CREATE CATALOG INTEGRATION](/sql-reference/sql/create-catalog-integration)

External access integrations:
:   [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration)

Notification integrations:
:   [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration)

Security integrations:
:   [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration)

Storage integrations:
:   [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration)

## Syntax

Copy code

```
SHOW [ { API | CATALOG | EXTERNAL ACCESS | NOTIFICATION | SECURITY | STORAGE } ] INTEGRATIONS [ LIKE '<pattern>' ]
```

## Parameters

`{ API | CATALOG | EXTERNAL ACCESS | NOTIFICATION | SECURITY | STORAGE }`
:   Returns integrations of the specified type only.

    For more information about some of these types, see the following topics:

    - [SHOW CATALOG INTEGRATIONS](/sql-reference/sql/show-catalog-integrations)
    - [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations)

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Integration |  |
| OWNERSHIP | Integration | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Currently, only the `API | CATALOG | EXTERNAL ACCESS | NOTIFICATION | SECURITY | STORAGE` parameter is supported.

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

The command output provides integration properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | Name of the integration |
| `type` | Type of the integration |
| `category` | Category of the integration |
| `enabled` | Current status of the integration, either TRUE (enabled) or FALSE (disabled) |
| `comment` | Comment for the integration |
| `created_on` | Date and time when the integration was created |

Expand

Show lessSee more

For more information about the properties that can be specified for an integration, see the following topic for the integration by type:

- [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration)
- [CREATE CATALOG INTEGRATION](/sql-reference/sql/create-catalog-integration)
- [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration)
- [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration)
- [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration)
- [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration)

## Examples

Show all notification integrations:

> Copy code
>
> ```
> SHOW NOTIFICATION INTEGRATIONS;
> ```

Show all the integrations whose name starts with `line` that you have privileges to view:

> Copy code
>
> ```
> SHOW INTEGRATIONS LIKE 'line%';
> ```
