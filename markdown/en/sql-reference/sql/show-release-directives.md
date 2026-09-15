# SHOW RELEASE DIRECTIVES

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Lists the release directives defined for an application package.

The output returns metadata and properties for the release directives in an application package,
ordered lexicographically by name. This is important to note if you want to filter the results
using the provided filters.

See also:
:   [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package), [CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package),
    [DROP APPLICATION PACKAGE](/sql-reference/sql/drop-application-package), [SHOW APPLICATION PACKAGES](/sql-reference/sql/show-application-packages)

## Syntax

Copy code

```
SHOW RELEASE DIRECTIVES [ LIKE '<pattern>' ]
  IN APPLICATION PACKAGE <name>
  [ FOR RELEASE CHANNEL <release_channel> ]
```

## Parameters

`name`
:   Specifies the identifier of the application package.

`LIKE 'pattern'`
:   Optionally filters the command output by the version name specified in the application
    package. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%v1%' ...`
    `... LIKE '%V1%' ...`

    Default: No value (no filtering is applied to the output).

`FOR RELEASE CHANNEL release_channel`
:   Returns only the release directives defined for the specified release channels.

## Output

The command output provides release directive properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | Specifies the name of the release directive. For the default release directive, the name is `DEFAULT`. |
| `target_type` | Specifies the type of target for the directive. The following values are possible:   - DEFAULT - ACCOUNT |
| `target_name` | Specifies the name of the organization or account. The value for the default release directive is always `NULL`. |
| `created_on` | Specifies the timestamp when the release directive was created. |
| `version` | Specifies the application version literal if applicable; if not, the value is NULL. |
| `patch` | Specifies the patch number of the application version if applicable; if not, the value is NULL. |
| `modified_on` | Specifies the timestamp when the release directive was last modified or NULL if it hasn’t been modified. |
| `active_regions` | Specifies the list of Snowflake regions where the release directive is allowed to affect upgrades. This value is ignored when `RELEASE_STATUS` is `HOLDING`. |
| `pending_regions` | Specifies the list of Snowflake regions where the release directive will be applied in the future. Upgrade progress in active regions is monitored for a period before new regions are activated. |
| `release_status` | Specifies the current release status. The following values are possible:   - IN\_PROGRESS: Upgrades are proceeding in the listed `ACTIVE_REGIONS`. - HOLDING: Upgrades are temporarily suspended. - DEPLOYED: Upgrades are permitted in all regions where the app is installed. |
| `deployed_on` | Specifies the time and date the release directive was deployed. When too many target regions are identified as unhealthy during deployment, the release directive temporarily moves to `HOLDING`. |
| `release_channel` | Specifies the release channel the release directive belongs to. |
| `upgrade_in_maintenance_window` | TRUE if the upgrade is configured to respect consumer maintenance windows, otherwise FALSE. |
| `upgrade_deadline` | The deadline by which the upgrade must be completed. After this time, the system automatically upgrades the application regardless of the consumer’s maintenance policy. |

Expand

Show lessSee more

## Usage notes

- This command requires the OWNERSHIP privilege, the MANAGE
  RELEASES privilege, or the MANAGE VERSIONS privilege on the application package.
- The command returns results for release directives that match the privileges granted to the role that
  executes this command.

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
SHOW RELEASE DIRECTIVES IN APPLICATION PACKAGE hello_snowflake_package;
```

```
+---------+-------------+---------------------------------+-------------------------------+---------+-------+-------------------------------+------------------------+--------------------------+----------------+-------------------------------+
| name    | target_type | target_name                     | created_on                    | version | patch | modified_on                   | active_regions         | pending_regions          | release_status | deployed_on                   |
|---------+-------------+---------------------------------+-------------------------------+---------+-------+-------------------------------+------------------------+--------------------------+----------------+-------------------------------+
| DEFAULT | DEFAULT     | NULL                            | 2023-04-02 14:55:17.304 -0700 | V2      |     0 | 2023-04-02 15:47:08.673 -0700 | PUBLIC.AWS_AP_SOUTH_1  | PUBLIC.AWS_AP_SOUTH_1    | IN PROGRESS    |                               |
| NEW_RD  | ACCOUNT     | [PROVIDER_DEV.PROVIDER_AWS]     | 2023-04-02 16:30:44.443 -0700 | V1      |     1 | 2023-04-03 07:10:42.428 -0700 | ALL                    |                          | DEPLOYED       | 2023-04-03 07:10:42.428 -0700 |         |
+---------+-------------+---------------------------------+-------------------------------+---------+-------+-------------------------------+------------------------+--------------------------+----------------+-------------------------------+
```
