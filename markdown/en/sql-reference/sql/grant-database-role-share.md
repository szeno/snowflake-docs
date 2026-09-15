# GRANT DATABASE ROLE … TO SHARE

Grants a database role to a share. Granting a database role effectively adds privileges on a single database to the share, which can then
be shared with one or more consumer accounts.

After consumers create a database from the share, they can grant the shared database roles to roles in their account to allow users with
those roles to access database objects in the share.

For more details, see [About Secure Data Sharing](/user-guide/data-sharing-intro) and [Create and configure shares](/user-guide/data-sharing-provider).

See also:
:   [REVOKE DATABASE ROLE … FROM SHARE](/sql-reference/sql/revoke-database-role-share)

## Syntax

Copy code

```
GRANT DATABASE ROLE <name>
  TO SHARE <share_name>
```

## Parameters

`name`
:   Specifies the identifier (i.e. name) for the database role; must be unique in the database in which the role is created.

    The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    If the identifier is not fully qualified (in the form of `db_name.database_role_name`, the command looks for the database role
    in the current database for the session.

`share_name`
:   Specifies the identifier for the share from which the specified database role is granted.

## Usage notes

- Granting a database role to a share fails if any DDL or other restricted privilege was granted to the database role. A database role can
  only grant permissions for read-only activity on a database and its objects.
- A shared database role does not support future grants. Snowflake returns the following error message depending on the action that you
  take:

  - Grant future privileges on an object to a database role and grant the database role to the share:

    Copy code

    ```
    GRANT SELECT ON FUTURE TABLES IN SCHEMA sh TO DATABASE ROLE dbr1;
    GRANT DATABASE ROLE dbr1 TO SHARE myshare;
    ```

    ```
    Cannot share a database role with future grants to it.
    ```
  - Grant the database role to a share and grant future privileges on an object to the database role:

    Copy code

    ```
    GRANT DATABASE ROLE dbr1 TO SHARE myshare;
    GRANT SELECT ON FUTURE TABLES IN SCHEMA sh TO DATABASE ROLE dbr1;
    ```

    ```
    Cannot grant future grants to a database role that is granted to a share.
    ```

  Use the following commands to identify whether you have future grants associated with a database role to avoid these error messages:

  Copy code

  ```
  SHOW FUTURE GRANTS IN DATABASE parent_db;
  SHOW FUTURE GRANTS IN shared_schema;
  ```

## Examples

Grant the database role `dr1` in database `d1` to share `share1`:

> Copy code
>
> ```
> GRANT DATABASE ROLE d1.dr1 TO SHARE share1;
> ```
