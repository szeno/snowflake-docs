# DESCRIBE INGRESS POLICY

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Describes the properties of an [ingress policy](/user-guide/ingress-policies).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE INGRESS POLICY](/sql-reference/sql/create-ingress-policy),
    [ALTER INGRESS POLICY](/sql-reference/sql/alter-ingress-policy),
    [DROP INGRESS POLICY](/sql-reference/sql/drop-ingress-policy),
    [SHOW INGRESS POLICIES](/sql-reference/sql/show-ingress-policies)

## Syntax

Copy code

```
DESC[RIBE] INGRESS POLICY <name>
```

## Parameters

`name`
:   Identifier for the ingress policy to describe. If the identifier contains spaces or special
    characters, enclose the entire string in double quotes. Identifiers enclosed in double quotes are
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Ingress policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

A role with no privilege on the policy cannot describe it. Snowflake reports that the policy
does not exist.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

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

The command returns one row for each property:

| Property | Description |
| --- | --- |
| `CREATED_ON` | Date and time when the ingress policy was created. |
| `NAME` | Name of the ingress policy. |
| `OWNER` | Role that owns the ingress policy. |
| `OWNER_ROLE_TYPE` | Type of the owner role. |
| `COMMENT` | Comment for the ingress policy. |
| `POLICY_DEFINITION` | YAML body of the ingress policy. |

Expand

Show lessSee more

## Examples

Describe an ingress policy:

Copy code

```
DESC INGRESS POLICY security_db.policies.corp_only;
```

```
+-------------------+------------------------------------------------+
| property          | value                                          |
|-------------------+------------------------------------------------|
| CREATED_ON        | 2026-10-12 09:00:00.000 -0700                  |
| NAME              | CORP_ONLY                                      |
| OWNER             | SECURITYADMIN                                  |
| OWNER_ROLE_TYPE   | ROLE                                           |
| COMMENT           | Allow requests from the corporate network      |
| POLICY_DEFINITION | conditions: ...                                |
+-------------------+------------------------------------------------+
```
