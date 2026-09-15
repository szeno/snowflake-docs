# DROP AUTHENTICATION POLICY

Removes an [authentication policy](/user-guide/authentication-policies) from the system.

See also:
:   [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy), [ALTER AUTHENTICATION POLICY](/sql-reference/sql/alter-authentication-policy), [DESCRIBE AUTHENTICATION POLICY](/sql-reference/sql/desc-authentication-policy), [SHOW AUTHENTICATION POLICIES](/sql-reference/sql/show-authentication-policies)

## Syntax

Copy code

```
DROP AUTHENTICATION POLICY [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the authentication policy to drop. If the identifier contains spaces or special characters, you must enclose
    the string in double quotation marks. Identifiers enclosed in double quotation marks are case-sensitive. The identifier must meet the
    [identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Authentication policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You cannot recover dropped authentication policies. You must recreate them.
- You cannot drop an authentication policy if it is set on an account or user.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Drop an authentication policy named `my_auth_policy`:

Copy code

```
DROP AUTHENTICATION POLICY my_auth_policy;
```
