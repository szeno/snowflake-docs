# DESCRIBE DATA MOVEMENT POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Describes the properties of a [data movement policy](/user-guide/data-movement-policies), including the creation date,
name, and the rules in the policy’s `ENFORCE_RULES` and `ALERT_RULES` lists.

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE DATA MOVEMENT POLICY](/sql-reference/sql/create-data-movement-policy) , [ALTER DATA MOVEMENT POLICY](/sql-reference/sql/alter-data-movement-policy) , [DROP DATA MOVEMENT POLICY](/sql-reference/sql/drop-data-movement-policy) , [SHOW DATA MOVEMENT POLICIES](/sql-reference/sql/show-data-movement-policies)

    [CREATE DATA MOVEMENT RULE](/sql-reference/sql/create-data-movement-rule) , [ALTER DATA MOVEMENT RULE](/sql-reference/sql/alter-data-movement-rule) , [DROP DATA MOVEMENT RULE](/sql-reference/sql/drop-data-movement-rule)

## Syntax

Copy code

```
{ DESC | DESCRIBE } DATA MOVEMENT POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the data movement policy to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Data type | Description |
| --- | --- | --- |
| `created_on` | TIMESTAMP\_LTZ | Date and time when the policy was created. |
| `name` | VARCHAR | Name of the policy. |
| `enforce_rules` | ARRAY | Rules in the `ENFORCE_RULES` list. |
| `alert_rules` | ARRAY | Rules in the `ALERT_RULES` list. |
| `comment` | VARCHAR | Comment for the policy, if any. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Data movement policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

A role with any privilege on the data movement policy can also describe it.

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

## Examples

The following example describes the data movement policy named `hr_pii_dmp`:

Copy code

```
DESCRIBE DATA MOVEMENT POLICY hr_pii_dmp;
```
