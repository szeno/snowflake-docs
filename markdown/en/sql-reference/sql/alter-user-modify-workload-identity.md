# ALTER USER … MODIFY WORKLOAD IDENTITY

Changes the name of a [workload identity](/user-guide/workload-identity-federation) or a property of the workload identity.

See also:
:   [ALTER USER … ADD WORKLOAD IDENTITY](/sql-reference/sql/alter-user-add-workload-identity) ,
    [ALTER USER … REMOVE WORKLOAD IDENTITY](/sql-reference/sql/alter-user-remove-workload-identity) ,
    [SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS](/sql-reference/sql/show-user-workload-identity-authentication-methods)

## Syntax

Copy code

```
ALTER USER [ IF EXISTS ] [ <username> ] MODIFY WORKLOAD IDENTITY <workload_identity_name>
  RENAME TO <new_workload_identity_name>

ALTER USER [ IF EXISTS ] [ <username> ] MODIFY WORKLOAD IDENTITY <workload_identity_name> SET
  [ DISABLED = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]

ALTER USER [ IF EXISTS ] [ <username> ] MODIFY WORKLOAD IDENTITY <workload_identity_name> UNSET
  [ DISABLED ]
  [ COMMENT ]
```

## Parameters

`username`
:   The name of the user that the workload identity is associated with.

    If you omit `username`, the command modifies a workload identity for the user who is currently logged in (the active user of this session).

`MODIFY WORKLOAD IDENTITY workload_identity_name`
:   Modifies the named workload identity.

    The name `DEFAULT` is reserved for the workload identity assigned with the `WORKLOAD_IDENTITY` user property. You can’t modify that workload identity with this command. Use [ALTER USER](/sql-reference/sql/alter-user) to set or unset the property.

`RENAME TO new_workload_identity_name`
:   Specifies a new name for the workload identity. The new name must be unique for the user. You can’t rename a workload identity to `DEFAULT`.

`SET ...`
:   Specifies one or more properties to set for the workload identity (separated by blank spaces, commas, or new lines):

    `DISABLED = { TRUE | FALSE }`
    :   Disables or enables the workload identity. A disabled workload identity can’t be used to authenticate, but its metadata is retained. You can enable it again by setting `DISABLED` to `FALSE`.

    `COMMENT = '<string_literal>'`
    :   Specifies a comment for the workload identity.

    You can’t use `SET` to change `TYPE`, `ARN`, `ISSUER`, `SUBJECT`, or `OIDC_AUDIENCE_LIST`. Those properties are fixed when the workload identity is created. To change them, remove the workload identity and add a new one.

`UNSET ...`
:   Unsets one or more properties for the workload identity, which resets the properties to their defaults:

    - `DISABLED`
    - `COMMENT`

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | User | Required to modify a workload identity. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can’t modify a workload identity for a user in a read-only secondary account. Make the change in the primary account.
- Renaming a workload identity doesn’t change the provider settings, and sessions that authenticated with that workload identity stay open.
- Disabling a workload identity blocks new authentication attempts that use it. To remove it and close sessions that authenticated with it, use [ALTER USER … REMOVE WORKLOAD IDENTITY](/sql-reference/sql/alter-user-remove-workload-identity).

## Examples

Rename a workload identity associated with the user `example_service_user`:

Copy code

```
ALTER USER IF EXISTS example_service_user MODIFY WORKLOAD IDENTITY aws_prod
  RENAME TO aws_prod_renamed;
```

Disable a workload identity so that it can no longer be used for authentication:

Copy code

```
ALTER USER IF EXISTS example_service_user MODIFY WORKLOAD IDENTITY aws_prod
  SET DISABLED = TRUE;
```

Change the comment associated with a workload identity:

Copy code

```
ALTER USER IF EXISTS example_service_user MODIFY WORKLOAD IDENTITY aws_prod
  SET COMMENT = 'production AWS role';
```
