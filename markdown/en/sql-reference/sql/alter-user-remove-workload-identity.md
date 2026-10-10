# ALTER USER … REMOVE WORKLOAD IDENTITY

Removes a named [workload identity](/user-guide/workload-identity-federation) from a user.

See also:
:   [ALTER USER … ADD WORKLOAD IDENTITY](/sql-reference/sql/alter-user-add-workload-identity) ,
    [ALTER USER … MODIFY WORKLOAD IDENTITY](/sql-reference/sql/alter-user-modify-workload-identity) ,
    [SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS](/sql-reference/sql/show-user-workload-identity-authentication-methods)

## Syntax

Copy code

```
ALTER USER [ IF EXISTS ] [ <username> ] REMOVE WORKLOAD IDENTITY <workload_identity_name>
```

## Parameters

`username`
:   The name of the user that the workload identity is associated with.

    If you omit this parameter, the command removes the workload identity for the user who is currently logged in (the active user in the current session).

`REMOVE WORKLOAD IDENTITY workload_identity_name`
:   Removes the named workload identity.

    The name `DEFAULT` is reserved for the workload identity assigned with the `WORKLOAD_IDENTITY` user property. You can’t remove that workload identity with this command. Use [ALTER USER … UNSET WORKLOAD\_IDENTITY](/sql-reference/sql/alter-user) instead.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | User | Required to remove a workload identity. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can’t use a removed workload identity for authentication.
- You can’t recover a removed workload identity. To reinstate the same provider settings, run [ALTER USER … ADD WORKLOAD IDENTITY](/sql-reference/sql/alter-user-add-workload-identity) again.
- The removed workload identity’s name becomes available immediately and can be reused in a subsequent ALTER USER … ADD WORKLOAD IDENTITY.
- Removing a workload identity closes sessions that authenticated with that workload identity. Sessions that authenticated with a different workload identity for the same user stay open.
- If you only want to temporarily block a workload identity from being used for authentication, use [ALTER USER … MODIFY WORKLOAD IDENTITY … SET DISABLED = TRUE](/sql-reference/sql/alter-user-modify-workload-identity) instead.
- You can’t remove a workload identity for a user in a read-only secondary account. Make the change in the primary account.

## Examples

Remove a workload identity named `aws_prod` from the user `example_service_user`:

Copy code

```
ALTER USER IF EXISTS example_service_user REMOVE WORKLOAD IDENTITY aws_prod;
```
