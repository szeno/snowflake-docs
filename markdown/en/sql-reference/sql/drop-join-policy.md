# DROP JOIN POLICY

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes a [join policy](/user-guide/join-policies) from the current/specified schema.

See also:
:   [Join policy DDL reference](/user-guide/join-policies#label-join-policy-ddl)

## Syntax

Copy code

```
DROP JOIN POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the join policy to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Join policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For more information about join policy DDL and privileges, see [Managing join policies](/user-guide/join-policies#label-join-policy-manage).

## Usage notes

- Prior to dropping the join policy, execute the following statement to determine if the policy is set on any tables or
  views.

  Copy code

  ```
  SELECT * FROM TABLE(mydb.INFORMATION_SCHEMA.POLICY_REFERENCES(POLICY_NAME=>'my_join_policy'));
  ```

  For more information, see [Getting information about tables and views attached to join policies](/user-guide/join-policies#label-join-constraint-policy-refs).
- A join policy cannot be dropped successfully if it is currently assigned to a table or view.

  Before executing a DROP statement, [detach the join policy](/user-guide/join-policies#label-join-policy-detach) from the table or view with an ALTER TABLE or ALTER VIEW statement.

## Example

Drop a join policy:

Copy code

```
DROP JOIN POLICY my_join_policy;
```
