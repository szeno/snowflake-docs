# SHOW INGRESS POLICIES

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Lists [ingress policies](/user-guide/ingress-policies) that you can see, including the
creation date, database and schema names, owner, and comment.

See also:
:   [CREATE INGRESS POLICY](/sql-reference/sql/create-ingress-policy),
    [ALTER INGRESS POLICY](/sql-reference/sql/alter-ingress-policy),
    [DESCRIBE INGRESS POLICY](/sql-reference/sql/desc-ingress-policy),
    [DROP INGRESS POLICY](/sql-reference/sql/drop-ingress-policy)

## Syntax

Copy code

```
SHOW INGRESS POLICIES
  [ LIKE '<pattern>' ]
  [ IN
       {
         ACCOUNT                  |

         DATABASE                 |
         DATABASE <database_name> |

         SCHEMA                   |
         SCHEMA <schema_name>     |
       }
    |
    ON
       {
         ACCOUNT          |
         USER <user_name> |
       }
  ]
  [ STARTS WITH '<name_string>' ]
  [ LIMIT <rows> ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`[ IN ... ]`
:   Optionally specifies the scope of the command. Specify one of the following:

    `ACCOUNT`
    :   Returns records for the entire account.

    `DATABASE`, `DATABASE db_name`
    :   Returns records for the current database in use or for a specified database (`db_name`).

        If you specify `DATABASE` without `db_name` and no database is in use, the keyword has no effect on the output.

        Note

        Using SHOW commands without an `IN` clause in a database context can result in fewer than expected results.

        Objects with the same name are only displayed once if no `IN` clause is used. For example, if you have table `t1` in
        `schema1` and table `t1` in `schema2`, and they are both in scope of the database context you’ve specified (that is, the database
        you’ve selected is the parent of `schema1` and `schema2`), then SHOW TABLES only displays one of the `t1` tables.

    `SCHEMA`, `SCHEMA schema_name`
    :   Returns records for the current schema in use or a specified schema (`schema_name`).

        `SCHEMA` is optional if a database is in use or if you specify the fully qualified `schema_name` (for example, `db.schema`).

        If no database is in use, specifying `SCHEMA` has no effect on the output.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

`[ ON ... ]`
:   Lists the ingress policy that is in effect on the specified object. A user-level policy overrides
    the account-level policy, so `ON USER` returns the user-level policy when one is set, and the
    account-level policy when the user has none.

    `ACCOUNT`
    :   Returns the ingress policy set on the account.

    `USER user_name`
    :   Returns the ingress policy in effect for the specified user.

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows`
:   Optionally limits the maximum number of rows returned. The actual number of rows returned might be less than the specified limit. For
    example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Ingress policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

`SHOW INGRESS POLICIES` without `ON` returns only ingress policies that your current role can see.
A role with no privilege on a policy does not see that policy in the results.

With `ON ACCOUNT` or `ON USER`, if the policy in effect is not visible to your current role,
Snowflake returns one row with `name`, `database_name`, `schema_name`, `owner`, and `comment`
empty, `options` set to `{"unauthorized":true}`, and `set_on` set to where the policy is attached.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

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

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

## Output

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the ingress policy was created. |
| `name` | Name of the ingress policy. |
| `database_name` | Database that contains the ingress policy. |
| `schema_name` | Schema that contains the ingress policy. |
| `kind` | `INGRESS_POLICY` |
| `owner` | Role that owns the ingress policy. |
| `comment` | Comment for the ingress policy. |
| `owner_role_type` | Type of the owner role. |
| `options` | Always empty for an ingress policy, except in the `unauthorized` row described in [Access control requirements](#access-control-requirements). |
| `set_on` | Where the policy is attached: `ACCOUNT` or `USER`. Returned only for `SHOW INGRESS POLICIES ON`. For `ON USER`, this is `ACCOUNT` when the user inherits the account-level policy. |

Expand

Show lessSee more

## Examples

List ingress policies in the current schema:

Copy code

```
SHOW INGRESS POLICIES;
```

List the ingress policy in effect for a user:

Copy code

```
SHOW INGRESS POLICIES ON USER etl_runner;
```
