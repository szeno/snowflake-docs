# DROP RESTRICTED SESSION SCOPE

Removes the specified [restricted session scope](/user-guide/restricted-session-scope) from the
current/specified schema.

`RSS` is a shorthand alias for `RESTRICTED SESSION SCOPE`. You can use either form in this
statement.

See also:
:   [CREATE RESTRICTED SESSION SCOPE](/sql-reference/sql/create-restricted-session-scope) ,
    [ALTER RESTRICTED SESSION SCOPE](/sql-reference/sql/alter-restricted-session-scope) ,
    [SHOW RESTRICTED SESSION SCOPES](/sql-reference/sql/show-restricted-session-scopes) ,
    [DESCRIBE RESTRICTED SESSION SCOPE](/sql-reference/sql/desc-restricted-session-scope)

## Syntax

Copy code

```
DROP { RESTRICTED SESSION SCOPE | RSS } [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Identifier for the restricted session scope to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Restricted session scope | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- If anything still references the object by fully qualified name, Snowflake blocks the drop.
  Remove or update that reference first.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Example

Copy code

```
DROP RESTRICTED SESSION SCOPE mydb.governance.agent_scope;
```
