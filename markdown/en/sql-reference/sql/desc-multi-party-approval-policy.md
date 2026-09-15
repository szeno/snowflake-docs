# DESCRIBE MULTI PARTY APPROVAL POLICY

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the definition of a Multi-party Approval policy.

DESCRIBE can be abbreviated to DESC.

## Syntax

Copy code

```
{ DESCRIBE | DESC } MULTI PARTY APPROVAL POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the Multi-party Approval policy to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY MULTI PARTY APPROVAL POLICY | Account |  |
| OWNERSHIP | Multi-party Approval policy |  |

Expand

Show lessSee more

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

The command returns the properties of a Multi-party Approval policy as rows with the
following columns:

| Column | Description |
| --- | --- |
| `property` | The name of the property. |
| `value` | The value assigned to the property. |

Expand

Show lessSee more

The `property` column includes the following rows:

| Property | Description |
| --- | --- |
| `NAME` | Identifier for the policy. |
| `OWNER` | Role that owns the policy. |
| `POLICY_DEFINITION` | The full YAML policy definition, as specified in the `AS $$ ... $$` body. The returned definition may be normalized by Snowflake and look different from the original statement. |
| `CREATED_ON` | The timestamp when the policy was created. |

Expand

Show lessSee more

## Example

Copy code

```
DESC MULTI PARTY APPROVAL POLICY security_db.policies.mpa_policy;
```
