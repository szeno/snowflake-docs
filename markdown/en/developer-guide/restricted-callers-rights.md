# Restricted caller’s rights

An executable such as a stored procedure, Snowpark Container Services service, or Streamlit in Snowflake app can run with privileges from the owner of
the executable (owner’s rights) or from the caller of the executable (caller’s rights). If an executable runs with caller’s
rights, the executable can perform an action only if the caller has privileges to perform that action outside the context of the executable.

Restricted caller’s rights allows an executable to run with caller’s rights, but restricts which of the caller’s privileges the executable
runs with. With restricted caller’s rights, an executable cannot run with a specific privilege unless an administrator expressly allows it.

![Owner's rights, caller's rights, and restricted caller's rights](/static/images/security-rcr.png)

## About caller grants

Administrators use *caller grants* to define which of the caller’s privileges an executable can run with. For example, if
a caller has SELECT and INSERT privileges on a table, but there isn’t a caller grant that allows the executable to run with the INSERT
privilege, then the executable with restricted caller’s rights cannot run with the INSERT privilege when acting upon the table.

A caller grant doesn’t give any privileges but rather restricts which of the caller’s existing privileges are used when they run
the executable. For example, if a caller runs a stored procedure to select from a table, the caller must already have the SELECT
privilege on the table and the caller grant must allow the stored procedure to run with the SELECT privilege.

Caller grants are granted by the administrator to the role that owns an executable. The caller grants are granted on objects
such as tables and warehouses that the executable accesses. When the executable attempts to access the objects, the caller grants associated
with the owner of the executable are used to determine which of the caller’s privileges can be used for the operation.

Some operations require a [high-level caller privilege](/developer-guide/restricted-callers-rights/high-level-caller-privileges)
in addition to the corresponding fine-grained caller grants. For details, see
[Operations and the required high-level caller privilege](/developer-guide/restricted-callers-rights/high-level-caller-privileges#operations-and-the-required-high-level-caller-privilege).

## Executables that run with restricted caller’s rights

The user who creates an executable defines whether the executable runs with owner’s rights, caller’s rights, or restricted caller’s rights.
If they choose restricted caller’s rights, every privilege required by the executable must be specified in one or more caller grants that
are granted to the owner of the executable.

For a stored procedure, the `EXECUTE AS` parameter defines whether the procedure runs with owner’s rights, caller’s rights, or
restricted caller’s rights. The following is an example of defining the procedure to run with restricted caller’s rights:

Copy code

```
CREATE OR REPLACE PROCEDURE sp_pi()
  RETURNS FLOAT NOT NULL
  LANGUAGE JAVASCRIPT
  EXECUTE AS RESTRICTED CALLER
  AS
  $$
  RETURN 3.1415926;
  $$
  ;
```

For a Streamlit in Snowflake app using a container runtime, restricted caller’s rights are configured through code.
For more information, see [Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights).

## Grant caller grants

Caller grants are granted on objects such as tables and databases that an executable accesses. The caller grants are granted
to the role or database role that owns the executable.

The GRANT statement that an administrator uses to grant a caller grant has different
variations, depending on how you want to grant caller grants. The variations are as follows:

- GRANT CALLER — Grant caller grants on a specific object. Each caller grant created by the statement allows the executable to
  run with a specified privilege.
- GRANT ALL CALLER PRIVILEGES — Grant caller grants on a specific object. The caller grants created by the statement allow the
  executable to run with all of the caller’s privileges.
- GRANT INHERITED CALLER — Grant caller grants on all current and future objects of the same type when they share a common schema, database,
  or account. Each caller grant created by the statement allows the executable to run with a specified privilege.
- GRANT ALL INHERITED CALLER PRIVILEGES — Grant caller grants on all current and future objects of the same type when they share a common
  schema, database, or account. The caller grants created by the statement allow the executable to run with all of the caller’s privileges.

A single GRANT statement can result in multiple caller grants being granted to the executable owner. For example, GRANT CALLER INSERT,
SELECT … results in two caller grants, one for the INSERT privilege and another for the SELECT privilege. Similarly, a GRANT ALL INHERITED
CALLER PRIVILEGES statement results in a caller grant for every privilege that can be granted on the specified object type.

Note

Use caution when granting caller grants to the PUBLIC role, as these caller grants become available to all roles in the account.

For the complete syntax, including parameters, for granting a caller grant, see [GRANT CALLER](/sql-reference/sql/grant-caller).

### Examples

The following are examples of how an administrator can use caller grants to control which of the caller’s privileges an executable can run with.

Executables owned by `owner_role` that access a `v1` view can run with the SELECT privilege on the view:

> Copy code
>
> ```
> GRANT CALLER SELECT ON VIEW v1 TO owner_role;
> ```

Executables owned by `owner_role` that access any table in the `db.sch` schema can run with the caller’s SELECT and INSERT privileges.

> Copy code
>
> ```
> GRANT INHERITED CALLER SELECT, INSERT ON ALL TABLES IN SCHEMA db.sch TO ROLE owner_role;
> ```

Executables owned by `owner_role` that access schemas in the current account can run with all of the caller’s privileges on the schemas.

> Copy code
>
> ```
> GRANT ALL INHERITED CALLER PRIVILEGES ON ALL SCHEMAS IN ACCOUNT TO ROLE owner_role;
> ```

Executables owned by the `db.r` database role that access the `db.sch1.t1` table can run with the SELECT privilege on the table.

> Copy code
>
> ```
> GRANT CALLER SELECT ON TABLE db.sch1.t1 TO DATABASE ROLE db.r;
> ```

Executables owned by `owner_role` that access the `my_db` database can run with all of the caller’s privileges on the database.

> Copy code
>
> ```
> GRANT ALL CALLER PRIVILEGES ON DATABASE my_db TO ROLE owner_role;
> ```

## Revoke a caller grant

Administrators use a REVOKE statement to revoke privileges that were previously granted to an executable owner through a caller grant. This
statement has different variations, depending on how you want to revoke caller grants.

- REVOKE CALLER — Revoke specific privileges on a specific object.
- REVOKE ALL CALLER PRIVILEGES — Revoke all privileges on a specific object. The executable will not be
  able to run with any privileges from the caller when it tries to access the object.
- REVOKE INHERITED CALLER — Revoke caller grants on all current and future objects of the same type when they share a common schema, database,
  or account. Only privileges in a specified list are revoked.
- REVOKE ALL INHERITED CALLER PRIVILEGES — Revoke caller grants on all current and future objects of the same type when they share a common
  schema, database, or account. All privileges are revoked; the executable will not be able to run with any privileges from the caller.

Executing a REVOKE INHERITED CALLER or REVOKE ALL INHERITED CALLER PRIVILEGES command does not revoke a caller grant
that was granted on a specific object within the account, database, or schema using a GRANT CALLER statement. For example, if you granted a
caller grant on table `my_db.sch1.t1` directly, executing `REVOKE INHERITED CALLER SELECT ON ALL TABLES IN DATABASE my_db ...` does not
revoke the caller grant on `t1`.

For the complete syntax, including parameters, of revoking a caller grant, see [REVOKE CALLER](/sql-reference/sql/revoke-caller).

### Examples

Executables owned by `owner_role` can no longer run with the caller’s privileges when they access views in the current account.

> Copy code
>
> ```
> REVOKE ALL INHERITED CALLER PRIVILEGES ON ALL VIEWS IN ACCOUNT FROM ROLE owner_role;
> ```

Executables owned by `owner_role` can no longer run with the USAGE privilege when they access the `db.sch1` schema.

> Copy code
>
> ```
> REVOKE CALLER USAGE ON SCHEMA db.sch1 FROM ROLE owner_role;
> ```

## List caller grants

Users can use the [SHOW CALLER GRANTS](/sql-reference/sql/show-caller-grants) command to list caller grants. You can use this command to list all caller grants that have been granted to a specific owner (SHOW CALLER GRANTS TO …) or to list all caller grants on a specific object (SHOW CALLER GRANTS ON …).

If you execute a SHOW CALLER GRANTS ON … command for a specific object, each row could indicate any of the following:

- A caller grant was granted directly on the object.

  For example, the output of `SHOW CALLER GRANTS ON TABLE db.sch.t1` contains a row if the administrator executed `GRANT CALLER SELECT ON TABLE db.sch.t1`.
- The object inherited a caller grant.

  For example, the output of `SHOW CALLER GRANTS ON TABLE db1.sch.t1` contains a row if the administrator executed `GRANT INHERITED CALLER SELECT ON ALL TABLES IN SCHEMA db1.sch`.
- The object was specified with an IN clause so other objects that it contains inherited caller grants.

  For example, the output of `SHOW CALLER GRANTS ON ACCOUNT` contains a row if the administrator executed `GRANT INHERITED CALLER SELECT ON ALL TABLES IN ACCOUNT`.
- The object is an ancestor of an object with an inherited caller grant as well as the descendant of the object that was specified with an IN clause that resulted in the inheritance.

  For example, `SHOW CALLER GRANTS ON SCHEMA my_db.sch1` contains a row if the administrator executed `GRANT INHERITED CALLER SELECT ON ALL TABLES IN DATABASE my_db`.

### Conditional output

The output of the SHOW CALLER GRANTS command varies depending on the privileges of the executing role. When a user executes SHOW CALLER
GRANTS, the results only contain objects on which they have at least one privilege; they cannot discover the existence of an object unless
they can access it, even if there is a caller grant on it.

For example, suppose there is a caller grant on databases `DB1` and `DB2`. Now suppose role `R2` has the USAGE privilege on
`DB1`, but no privileges on `DB2`. When `R2` executes SHOW CALLER GRANTS, the output shows that there is a caller grant on `DB1`,
but does not list `DB2`. If `R2` had privileges on both databases, then the output would show that the caller grant is on both
databases.

### Examples

List caller grants that have been granted on the table `t1`.

> Copy code
>
> ```
> SHOW CALLER GRANTS ON TABLE t1;
> ```

List all of the caller grants that have been granted for the current account. This includes grants directly on the account
(GRANT CALLER … ON ACCOUNT) and grants to all objects in an account (GRANT INHERITED CALLER … IN ACCOUNT).

> Copy code
>
> ```
> SHOW CALLER GRANTS ON ACCOUNT;
> ```

List all of the caller grants that have been granted to the database role `db.owner_role`.

> Copy code
>
> ```
> SHOW CALLER GRANTS TO DATABASE ROLE db.owner_role;
> ```
