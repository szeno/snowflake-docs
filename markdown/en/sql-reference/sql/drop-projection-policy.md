# DROP PROJECTION POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes a [projection policy](/user-guide/projection-policies) from the current/specified schema.

See also:
:   [Projection policy DDL reference](/user-guide/projection-policies#label-projection-policy-ddl)

## Syntax

Copy code

```
DROP PROJECTION POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the projection policy to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Projection policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on projection policy DDL and privileges, see [Privileges and commands](/user-guide/projection-policies#label-projection-policy-manage).

## Usage notes

- Prior to dropping the projection policy, execute the following statement to determine if the projection policy is set on any columns.

  Copy code

  ```
  SELECT * from table(mydb.information_schema.policy_references(policy_name=>'do_not_project'));
  ```

  For more information, see [Identify projection policy references](/user-guide/projection-policies#label-projection-constraint-policy-refs).
- A projection policy cannot be dropped successfully if it is currently assigned to a column.

  Before executing a DROP statement, UNSET the projection policy from the column with an [ALTER TABLE … ALTER COLUMN](/sql-reference/sql/alter-table-column) or an
  [ALTER VIEW](/sql-reference/sql/alter-view) statement.

## Example

Drop the projection policy:

Copy code

```
DROP PROJECTION POLICY do_not_project;
```
