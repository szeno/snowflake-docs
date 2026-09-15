# Snowflake Postgres Roles

Postgres has its own role-based authentication for managing connections to databases and using
databases on a Postgres server. These roles are separate from Snowflake roles. Postgres
roles are used for accessing and managing databases, tables, and other objects within
Snowflake Postgres instances.

When you create an instance, Snowflake automatically creates two special managed roles for you
to use, which are described below.

For more information about managing Postgres roles, see the [Postgres documentation](https://www.postgresql.org/docs/current/user-manag.html).

Note

Here and in many other places you will see the terms “role” and “user” used interchangeably in the context of Postgres user
management. This is because a Postgres user is simply a role that has the Postgres role LOGIN attribute.

## Snowflake Postgres managed roles

Snowflake Postgres automatically creates two managed roles at the same time that it creates your instance.

### The `snowflake_admin` role

The `snowflake_admin` role is a high-privilege Postgres role used to administer your Snowflake Postgres instance. It is **not**
a full Postgres superuser; some operations remain restricted and are managed by Snowflake. However, it has elevated privileges
that include:

- Creating and managing Postgres roles.
- Creating and managing databases.
- Managing replication for your Snowflake Postgres instance.
- Bypassing row-level security (RLS) policies where applicable.

In addition, `snowflake_admin` is a member of several Postgres built-in roles that grant monitoring and operational capabilities,
including:

- `pg_signal_backend`
- `pg_use_reserved_connections`
- `pg_create_subscription`
- `pg_read_all_settings`
- `pg_read_all_stats`
- `pg_stat_scan_tables`
- `pg_monitor`
- `snowflake_admin_group`

### The `application` role

The `application` role is a non-superuser role that by default has permissions to create objects in the `postgres` database. New permissions
or ownership for this role should be granted by the `snowflake_admin` role.

## Postgres password security

### Regenerating credentials for Snowflake Postgres managed roles

Credentials for the `snowflake_admin` and `application` roles are generated when you create the instance and are displayed only once.
You can regenerate these credentials at any time, invalidating the existing credentials.

SnowsightSQL

From the dashboard you can regenerate the credentials for your instance’s `snowflake_admin` role.

1. In the navigation menu, select **Postgres**.
2. Select your instance.
3. In the **Manage** menu at the top right select **Regenerate credentials**.
4. Click the **Acknowledge & continue** button to confirm the action.

> To regenerate credentials for the `snowflake_admin` or `application` role, you can use an ALTER POSTGRES INSTANCE command with the
> RESET ACCESS FOR parameter. The value that you specify is a quoted string, either `'snowflake_admin'` or `'application'`.
> For example:
>
> Copy code
>
> ```
> ALTER POSTGRES INSTANCE my_instance_1 RESET ACCESS FOR 'snowflake_admin';
> ALTER POSTGRES INSTANCE my_instance_2 RESET ACCESS FOR 'application';
> ```
>
> - Requires **OWNERSHIP** privilege
>
> That command returns one row with the following column:
>
> > - `password`

**Rotate Credentials Example**

> > Reset the access for the `snowflake_admin` role for a Snowflake Postgres instance named `my_instance`:
>
> Copy code
>
> ```
> ALTER POSTGRES INSTANCE my_instance RESET ACCESS FOR 'snowflake_admin';
> ```

### Setting passwords for other Postgres roles

Snowflake Postgres instances are configured for scram-sha-256 password authentication. When new
passwords are set, the server generates and stores a scram-sha-256 hash, but when the Postgres
[log\_statement](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-STATEMENT) parameter
is set to any value other than `none`, then CREATE ROLE and ALTER ROLE DDL commands are fully
logged to the Postgres server log. Therefore, you should make sure that clear-text passwords are not
logged as part of those statements.

#### Disabling statement logging for CREATE ROLE and ALTER ROLE Postgres DDL commands

The simplest way to prevent clear-text passwords used in CREATE ROLE and ALTER ROLE DDL statements from appearing in the Postgres server
log is to disable the `log_statement` parameter for the transaction that you run them in. Do so by using SET LOCAL:

Copy code

```
BEGIN;
SET LOCAL log_statement = 'none';
CREATE USER mynewrole PASSWORD 'mynewpassword';
COMMIT;
```

#### Using the `psql` Postgres client’s `\password` command

The Postgres [psql](https://www.postgresql.org/docs/current/app-psql.html) client program has a
[\password](https://www.postgresql.org/docs/current/app-psql.html) meta-command that can be used
to change the password for existing users. The `\password` meta-command precomputes the entered
password’s scram-sha-256 hash and uses that in the ALTER ROLE command that is sent to the server. To
use this method, first create new users without a password, and then set each user’s password with
the psql `\password` meta-command.

Copy code

```
postgres=# CREATE ROLE mynewrole LOGIN;
CREATE ROLE

postgres=# \password mynewrole
Enter new password for user "mynewrole":
Enter it again:
```

If `log_statement` is set to a value other than `'none'`, then the log entry for ALTER ROLE
command sent by `psql` for the above `\password` command has the calculated scram-sha-256
hash instead of the actual clear-text password. You can combine this method with disabling
`log_statement` completely, as described above, to prevent even that hash from appearing in the
Postgres log:

Copy code

```
postgres=# CREATE ROLE mynewrole LOGIN;
CREATE ROLE

postgres=# BEGIN;
BEGIN

postgres=# SET LOCAL log_statement = 'none';
SET

postgres=# \password mynewrole
Enter new password for user "mynewrole":
Enter it again:

postgres=# COMMIT;
COMMIT
```

### Leaked Password Protection

Leaked password protection is provided for roles on Snowflake Postgres instances. Discovery and notification work as described in our
main [Leaked password protection](/user-guide/leaked-password-protection). When Snowflake discovers a leaked password for one of your Snowflake Postgres roles:

- The role is added to the special `snowflake_nologin` Postgres group role to prevent future logins with it.
- All existing connections for the role are terminated.
- The email notification you receive will have “Urgent - Snowflake Postgres Role(s) Password Reset to Prevent Unauthorized Access” for
  its Subject.

Should you receive this email, you should immediately securely update the role’s password as described above. When regenerating credentials
for managed roles they are automatically removed from the `snowflake_nologin` Postgres role group. For non-managed roles, after updating
the role’s password they can be removed from the `snowflake_nologin` group role by running this Postgres SQL with the `snowflake_admin` role:

Copy code

```
REVOKE snowflake_nologin FROM {rolename};
```

## Role limitations

In Snowflake Postgres, certain operations are reserved for the service itself and can’t be
performed by any customer-managed role, including `snowflake_admin`.

Examples of operations that are restricted include:

- Logging in with superuser roles such as `postgres` or `snowflake_superuser`, or assuming such roles by
  using SET ROLE.
- Creating other superusers.
- Executing the ALTER SYSTEM command.
- Changing protected server-level configuration parameters that are managed by Snowflake.
- Modifying or disabling core Snowflake-managed components or extensions.
- Accessing or altering Snowflake-managed system databases or schemas used by the service.
- Accessing or altering the Snowflake Postgres instance filesystem.
- Directly modifying system catalog tables.
- Creating more than 64 roles in the instance.
- Creating more than 32 databases in the instance.
- Accessing the Postgres [generic file access functions](https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-ADMIN-GENFILE)
  that permit filesystem access.

The Snowflake Postgres extension may introduce further restrictions on what both `snowflake_admin`
and `application` can do within an instance. These extension-specific limitations may evolve over
time and will be documented with the corresponding extension behavior. If an operation is blocked,
you receive an error indicating that it isn’t permitted in Snowflake Postgres.
