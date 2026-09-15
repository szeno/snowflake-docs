# REVOKE DATABASE ROLE … FROM SHARE

Revokes a database role from a share.

Revoking a database role effectively removes privileges on objects granted to the database role from the share, disabling access to the
objects in all consumer accounts that have created a database from the share.

For more details, see [About Secure Data Sharing](/user-guide/data-sharing-intro) and [Create and configure shares](/user-guide/data-sharing-provider).

See also:
:   [GRANT DATABASE ROLE … TO SHARE](/sql-reference/sql/grant-database-role-share)

## Syntax

Copy code

```
REVOKE DATABASE ROLE <name>
  FROM SHARE <share_name>
```

## Parameters

`name`
:   Specifies the identifier (i.e. name) for the database role; must be unique in the database in which the role is created.

    The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    If the identifier is not fully qualified (in the form of `db_name.database_role_name`, the command looks for the database role
    in the current database for the session.

`share_name`
:   Specifies the identifier for the share to which the specified database role is revoked.

## Usage notes

None.

## Examples

Revoke the database role `dr1` in database `d1` from share `share1`:

> Copy code
>
> ```
> REVOKE DATABASE ROLE d1.dr1 FROM SHARE share1;
> ```
