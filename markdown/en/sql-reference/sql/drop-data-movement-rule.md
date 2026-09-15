# DROP DATA MOVEMENT RULE

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes a [data movement rule](/user-guide/data-movement-policies) from the current/specified schema.

See also:
:   [CREATE DATA MOVEMENT RULE](/sql-reference/sql/create-data-movement-rule) , [ALTER DATA MOVEMENT RULE](/sql-reference/sql/alter-data-movement-rule) , [SHOW DATA MOVEMENT RULES](/sql-reference/sql/show-data-movement-rules) , [DESCRIBE DATA MOVEMENT RULE](/sql-reference/sql/desc-data-movement-rule)

    [CREATE DATA MOVEMENT POLICY](/sql-reference/sql/create-data-movement-policy) , [ALTER DATA MOVEMENT POLICY](/sql-reference/sql/alter-data-movement-policy) , [DROP DATA MOVEMENT POLICY](/sql-reference/sql/drop-data-movement-policy)

## Syntax

Copy code

```
DROP DATA MOVEMENT RULE [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the data movement rule to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Data movement rule | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

- A data movement rule that’s currently referenced by a data movement policy can’t be dropped. Remove the rule from the
  policy’s ENFORCE\_RULES or ALERT\_RULES before you drop it.

## Examples

Drop a data movement rule:

Copy code

```
DROP DATA MOVEMENT RULE hr_pii_copy_guard;
```
