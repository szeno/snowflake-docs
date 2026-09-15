# DROP MASKING POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes a masking policy from the system.

See also:
:   [Masking policy DDL](/user-guide/security-column-intro#label-security-column-intro-ddl)

## Syntax

Copy code

```
DROP MASKING POLICY <name>
```

## Parameters

`name`
:   Identifier for the masking policy; must be unique for your account.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Masking policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on masking policy DDL and privileges, see [Managing Column-level Security](/user-guide/security-column-intro#label-security-column-manage).

## Usage notes

- Prior to dropping a masking policy, execute the following statement to determine if any masking policies are applied to columns. For
  more information, see [POLICY\_REFERENCES](/sql-reference/functions/policy_references).

  Copy code

  ```
  SELECT * from table(information_schema.policy_references(policy_name=>'<string>'));
  ```
- A masking policy cannot be dropped successfully if it is currently assigned to a column or a tag.

  Before executing a DROP statement, UNSET the masking policy from the column with an [ALTER TABLE … ALTER COLUMN](/sql-reference/sql/alter-table-column) or [ALTER VIEW](/sql-reference/sql/alter-view)
  statement, and, if necessary, unset the masking policy from the tag using an [ALTER TAG](/sql-reference/sql/alter-tag) statement.
- You can drop a masking policy that’s in use by a table inside a [backup](/user-guide/backups).

## Example

Copy code

```
DROP MASKING POLICY ssn_mask;
```
