# SHOW NETWORK RULES

Lists all network rules defined in the system.

See also:
:   [ALTER NETWORK RULE](/sql-reference/sql/alter-network-rule) , [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule) , [DESCRIBE NETWORK RULE](/sql-reference/sql/desc-network-rule) , [DROP NETWORK RULE](/sql-reference/sql/drop-network-rule)

## Syntax

Copy code

```
SHOW NETWORK RULES [ LIKE '<pattern>' ]
                   [ IN { ACCOUNT | DATABASE [ <db_name> ] | [ SCHEMA ] [ <schema_name> ] } ]
                   [ STARTS WITH '<name_string>' ]
                   [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN ACCOUNT | [ DATABASE ] db_name | [ SCHEMA ] schema_name`
:   Optionally specifies the scope of the command, which determines whether the command lists records only for the current/specified
    database or schema, or across your entire account:

    The `DATABASE` or `SCHEMA` keyword is not required; you can set the scope by specifying only the database or schema name.
    Likewise, the database or schema name is not required if the session currently has a database in use:

    - If `DATABASE` or `SCHEMA` is specified without a name and the session does not currently have a database in use, the
      parameter has no effect on the output.
    - If `SCHEMA` is specified with a name and the session does not currently have a database in use, the schema name must
      be fully qualified with the database name (e.g. `testdb.testschema`).

    Default: Depends on whether the session currently has a database in use:

    - Database: `DATABASE` is the default (i.e. the command returns the objects you have privileges to view in the database).
    - No database: `ACCOUNT` is the default (i.e. the command returns the objects you have privileges to view in your account).

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

The command output provides network rule properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the network rule was created. |
| `name` | Name of the network rule. |
| `database_name` | Database that contains the schema in which the network rule was created. |
| `schema_name` | Schema in which the network rule was created. |
| `owner` | Role that has the OWNERSHIP privilege on the network rule. |
| `comment` | Descriptive text associated with the network rule. |
| `type` | Value of the network rule’s `TYPE` property. |
| `mode` | Value of the network rule’s `MODE` property. |
| `entries_in_valuelist` | Number of network identifiers specified in the `VALUE_LIST` property of the network rule. |
| `owner_role_type` | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Network Rule | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| USAGE | Schema |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

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

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

List all network rules:

Copy code

```
SHOW NETWORK RULES;
```

To see the current list of Snowflake-managed network rules, run the following command:

Copy code

```
SHOW NETWORK RULES IN SNOWFLAKE.NETWORK_SECURITY;
```

Note

The SHOW command doesn’t explicitly expose IP addresses, only the number of IP addresses per rule.

To see your current Snowflake-managed network rules, including IP addresses, use the [NETWORK\_RULES view](/sql-reference/account-usage/network_rules).
