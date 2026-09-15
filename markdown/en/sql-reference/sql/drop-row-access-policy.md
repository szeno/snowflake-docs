# DROP ROW ACCESS POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes a row access policy from the system.

See also:
:   [Row access policy DDL](/user-guide/security-row-intro#label-security-row-ddl)

## Syntax

Copy code

```
DROP ROW ACCESS POLICY [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Identifier for the row access policy; must be unique for your account.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Schema or  Row access policy | The schema that contains the row access policy.  OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on masking policy DDL and privileges, see [Manage row access policies](/user-guide/security-row-intro#label-security-row-mgmt-approach).

## Usage notes

- Prior to dropping a row access policy, execute the following statement to determine if the row access policy is applied to any tables or
  views. For more information, see [POLICY\_REFERENCES](/sql-reference/functions/policy_references).

  Copy code

  ```
  SELECT * from table(information_schema.policy_references(policy_name=>'<string>'));
  ```
- A row access policy cannot be dropped successfully if it is currently attached to a resource. Before executing a DROP statement, detach
  the row access policy from the table or view with an ALTER TABLE or ALTER VIEW statement as shown in
  [ALTER TABLE](/sql-reference/sql/alter-table) or [ALTER VIEW](/sql-reference/sql/alter-view).
- Snowflake does not support `UNDROP` with row access policy objects. Using `UNDROP` triggers an error message. For more information
  on this error message, see [Troubleshoot row access policies](/user-guide/security-row-intro#label-security-row-troubleshooting).
- If a table column has a row access policy attached to it, the column cannot be dropped from the table.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

- You can drop a row access policy that’s in use by a table inside a [backup](/user-guide/backups). In that case, you
  can’t immediately use the table after you restore it from the backup. To use the restored table, run an
  ALTER TABLE … DROP ALL ROW ACCESS POLICIES command after restoring it.

## Example

The following example drops a row access policy from a table.

> Copy code
>
> ```
> DROP ROW ACCESS POLICY rap_table_employee_info;
> ```
