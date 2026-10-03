# REVOKE ROLE

Removes a role from another role or a user.

See also:
:   [GRANT ROLE](/sql-reference/sql/grant-role)

## Syntax

Copy code

```
REVOKE [ GRANT OPTION FOR ]
  ROLE <name>
  FROM ROLE <parent_role_name>
  [ RESTRICT | CASCADE ]

REVOKE ROLE <name> FROM USER <user_name>
```

## Parameters

`name`
:   Specifies the identifier for the role to revoke. If the identifier contains spaces or special characters, the entire string must
    be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`ROLE parent_role_name`
:   Revokes the role from the specified role.

`USER user_name`
:   Revokes the role from the specified user.

## Optional parameters

`GRANT OPTION FOR`
:   If specified, removes the ability for the recipient role to grant the role to another role. The role
    grant itself remains, so the recipient role still inherits the granted role’s privileges.

    Default: No value, which revokes the role grant.

`RESTRICT | CASCADE`
:   Determines whether the revoke operation succeeds when the role has been re-granted to another role.
    These clauses apply to `REVOKE ROLE ... FROM ROLE`.

    - `RESTRICT`: If the role being revoked has been re-granted to another role, the REVOKE command fails.
    - `CASCADE`: If the role being revoked has been re-granted, the REVOKE command recursively revokes
      these dependent grants. `GRANT OPTION FOR ... CASCADE` revokes the dependent grants and leaves the
      role grant in place without the grant option. `CASCADE` without `GRANT OPTION FOR` revokes the role
      grant and the dependent grants.

    Default: `RESTRICT`

## Examples

Copy code

```
REVOKE ROLE analyst FROM ROLE SYSADMIN;
```

Copy code

```
REVOKE ROLE analyst FROM USER user1;
```

Remove only the grant option from the `data_steward` role. `data_steward` keeps the `analyst` role:

Copy code

```
REVOKE GRANT OPTION FOR ROLE analyst FROM ROLE data_steward;
```

Revoke the `analyst` role from `data_steward`, including grants of `analyst` that `data_steward` made:

Copy code

```
REVOKE ROLE analyst FROM ROLE data_steward CASCADE;
```
