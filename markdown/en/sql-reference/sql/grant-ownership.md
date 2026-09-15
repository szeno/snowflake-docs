# GRANT OWNERSHIP

Transfers ownership of an object or all objects of a specified type in a schema from one role to another role. *Role* refers to either
a role or a database role.

OWNERSHIP is a special type of privilege that can only be granted from one role to another role; it cannot be revoked. For more details,
see [Overview of Access Control](/user-guide/security-access-control-overview).

This command is a variation of [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege).

See also:
:   [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege)

## Syntax

**For object types that are not an instance of a class:**

Copy code

```
GRANT OWNERSHIP
  { ON {
            <object_type> <object_name>
          | ALL <object_type_plural> IN { DATABASE <database_name> | SCHEMA <schema_name> }
       }
    | ON FUTURE <object_type_plural> IN { DATABASE <database_name> | SCHEMA <schema_name> }
  }
  TO { ROLE <role_name> | DATABASE ROLE <database_role_name> }
  [ { REVOKE | COPY } CURRENT GRANTS ]
```

**For an instance of a class:**

Copy code

```
GRANT OWNERSHIP
  ON  <class_name> <instance_name>
  TO { ROLE <role_name> | DATABASE ROLE <database_role_name> }
  [ { REVOKE | COPY } CURRENT GRANTS ]
```

## Required parameters

`object_name`
:   Specifies the identifier for the object on which you are transferring ownership.

`object_type`
:   Specifies the type of object.

    One of the following:

    - `AGENT`
    - `AGGREGATION POLICY`
    - `ALERT`
    - `AUTHENTICATION POLICY`
    - `COMPUTE POOL`
    - `CORTEX SEARCH SERVICE`
    - `DATA METRIC FUNCTION`
    - `DATABASE`
    - `DATABASE ROLE`
    - `DBT PROJECT`
    - `DYNAMIC TABLE`
    - `EVENT TABLE`
    - `EXPERIMENT`
    - `EXTERNAL TABLE`
    - `EXTERNAL VOLUME`
    - `FAILOVER GROUP`
    - `FILE FORMAT`
    - `FUNCTION`
    - `GATEWAY`
    - `GIT REPOSITORY`
    - `ICEBERG TABLE`
    - `IMAGE REPOSITORY`
    - `INTEGRATION`
    - `JOIN POLICY`
    - `MASKING POLICY`
    - `MATERIALIZED VIEW`
    - `MCP SERVER`
    - `NETWORK POLICY`
    - `NETWORK RULE`
    - `NOTEBOOK`
    - `ONLINE FEATURE TABLE`
    - `PACKAGES POLICY`
    - `PASSWORD POLICY`
    - `PIPE`
    - `PRIVACY POLICY`
    - `PROCEDURE`
    - `PROJECTION POLICY`
    - `REPLICATION GROUP`
    - `RESOURCE MONITOR`
    - `RESTRICTED SESSION SCOPE`
    - `ROLE`
    - `ROW ACCESS POLICY`
    - `SCHEMA`
    - `SEMANTIC VIEW`
    - `SESSION POLICY`
    - `SECRET`
    - `SEQUENCE`
    - `SNAPSHOT`
    - `SNAPSHOT POLICY`
    - `SNAPSHOT SET`
    - `STAGE`
    - `STORAGE LIFECYCLE POLICY`
    - `STREAM`
    - `TABLE`
    - `TAG`
    - `TASK`
    - `TYPE`
    - `USER`
    - `VIEW`
    - `WAREHOUSE`
    - `WORKSPACE`

`object_type_plural`
:   Plural form of `object_type` (e.g. `TABLES`, `VIEWS`).

    Note that bulk grants on pipes and data metric functions are not allowed.

`role_name`
:   The identifier for the role to which the object ownership is transferred.

`database_role_name`
:   The identifier for the database role to which the object ownership is transferred. If the identifier is not fully qualified (in the
    form of `db_name.database_role_name`, the command looks for the database role in the current database for the session.

    Ownership is limited to objects in the database that contains the database role.

## Optional parameters

`[ REVOKE | COPY ] CURRENT GRANTS`
:   Specifies whether to remove or transfer all existing outbound privileges on the object when ownership is transferred to a new role:

    Note

    *Outbound* privileges refer to any privileges granted on the individual object whose ownership is changing.

    When transferring ownership of a role, current grants refers to any roles that were granted to the current role (to create a role
    hierarchy). If ownership of a role is transferred with the current grants copied, then
    the output of the SHOW GRANTS command shows the new owner as the grantor of any child roles to the current role.

    `REVOKE`
    :   Enforces RESTRICT semantics, which require removing all outbound privileges on an object before transferring ownership to a new role.
        This is intended to protect the new owning role from unknowingly inheriting the object with privileges already granted on it.

        After transferring ownership, the privileges for the object must be explicitly re-granted on the role.

        Note that the REVOKE keyword does not work when granting ownership of future objects of a specified type in a database or schema to
        a role (using GRANT OWNERSHIP ON FUTURE `<object_type>`).

    `COPY`
    :   Transfers ownership of an object along with a copy of any existing outbound privileges on the object. After the transfer, the new
        owner is identified in the system as the grantor of the copied outbound privileges (that is, in the [SHOW GRANTS](/sql-reference/sql/show-grants) output for the
        object, the new owner is listed in the GRANTED\_BY column for all privileges). As a result, any privileges that were subsequently
        re-granted before the change in ownership are no longer dependent on the original grantor role.

        Revoking a privilege using [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege) with the `CASCADE` option does not recursively revoke these formerly
        dependent grants. The grants must be explicitly revoked.

        The `COPY` parameter requires at least one of the following:

        - An active role has the MANAGE GRANTS privilege on the account.
        - An active role is the new owner (or a higher) role. The system role PUBLIC is naturally captured by this requirement because PUBLIC is
          granted to every role.

        The active role considers both primary and secondary roles. For more information, see [Active roles](/user-guide/security-access-control-overview#label-access-control-overview-active-roles).

    Default: None. Neither operation is performed on any existing outbound privileges.

    > Note
    >
    > A GRANT OWNERSHIP statement fails if existing outbound privileges on the object are neither revoked nor copied.

## Usage notes

- You cannot transfer the OWNERSHIP privilege for the following objects:

  - `APPLICATION ROLE`
  - `CONNECTION`

    Only the ACCOUNTADMIN role can have the OWNERSHIP privilege on a connection object.
  - Instances of a [class](/sql-reference/snowflake-db-classes).
  - Machine learning objects (that is, models, model versions, and model monitors).
  - `SERVICE`
  - `SHARE`
- The GRANT OWNERSHIP statement is blocked if outbound (that is, dependent) privileges exist on the object. The object owner (or a higher role)
  can explicitly copy all current privileges to the new owning role (using the `COPY CURRENT GRANTS` option) or revoke all outbound
  privileges on the object before transferring ownership (using the `REVOKE CURRENT GRANTS` option).

  For role objects, if you do not specify these clauses, the GRANT OWNERSHIP statement is not blocked when transferring a role to a new
  owner role. The new owner role is updated. However, a `SHOW GRANTS OF ROLE transferred_role` command shows two rows for the
  transferred role being granted to the same user:

  - In the `granted_by` column, the value in one row is for the grant by the original owner role.
  - In the `granted_by` column, the value in the other row is for the grant by the new owner role.

  Snowflake prevents the GRANT OWNERSHIP … REVOKE CURRENT GRANTS command on a shared database. For details, see the [Shared database](#shared-database)
  example in this topic.
- The transfer of ownership only affects existing objects at the time the command is issued. Any objects created after the command is
  issued are owned by the role in use when the object is created.
- Transferring ownership of objects of the following types is blocked unless additional conditions are met:

  Pipes:
  :   The pipe must be paused.

  Tasks:
  :   You must suspend the scheduled task. Snowflake suspends all tasks in the container automatically if all tasks in a specified database or schema are transferred to another role. Tasks transferred to the same role using the `COPY CURRENT GRANTS` option are also suspended automatically. For more information, see [Task security](/user-guide/tasks-intro#label-task-security-reqs).
- When future grants on the same object type are defined at both the database and
  schema level, the schema-level grants take precedence over the database-level grants, and
  the database-level grants are ignored.
- To grant ownership on a materialized view, use `GRANT OWNERSHIP ON VIEW`. There is no separate
  `GRANT OWNERSHIP ON MATERIALIZED VIEW` statement.
- To grant ownership on a hybrid table, use `GRANT OWNERSHIP ON TABLE`. There is no separate
  `GRANT OWNERSHIP ON HYBRID TABLE` statement.
- You cannot transfer the OWNERSHIP privilege on a share, nor can you transfer the OWNERSHIP privilege on a connection. Only the ACCOUNTADMIN role can own the connection.
- For granting the OWNERSHIP privilege on dynamic tables, ensure the receiving role has the USAGE privilege on the database and schema
  that contains the dynamic table, and on the warehouse used to refresh the table. Otherwise, subsequent scheduled refreshes fail.
- For granting the OWNERSHIP privilege on future dynamic tables:

  - If the dynamic table is set to initialize on creation (that is, `INITIALIZE = ON_CREATE`), ensure the new role has
    [sufficient privileges](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges) on referenced objects. Otherwise, the initial refresh fails and results in
    an error stating that the object cannot be found.
  - If the dynamic table is set to initialize on schedule (that is, `INITIALIZE = ON_SCHEDULE`), ensure the new role has
    [sufficient privileges](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges) on referenced objects. Otherwise, the subsequent scheduled refreshes fail.
- When you transfer ownership of an Apache Iceberg™ table to a different role,
  Snowflake doesn’t transfer the OWNERSHIP privilege on the external volume
  (and catalog integration if the table is externally managed) associated with the table.

  To give the target role full control over the table and its related objects,
  you must grant the OWNERSHIP privilege on the external volume and catalog integration to the role.
- After the ownership of a notebook is transferred to a new role, the original owner role loses all access to the notebook.
- **Database roles:**

  Ownership can only be transferred on objects in the same database as the database role.
- Transferring ownership on an external table or its parent database blocks automatic refreshes of the table metadata
  by setting the `AUTO_REFRESH` property to `FALSE`. To reset the property after you transfer ownership,
  use the [ALTER EXTERNAL TABLE](/sql-reference/sql/alter-external-table) command.

## Examples

### Roles

Revoke all outbound privileges on the `mydb` database, currently owned by the `manager` role, before transferring ownership
to the `analyst` role:

> Copy code
>
> ```
> REVOKE ALL PRIVILEGES ON DATABASE mydb FROM ROLE manager;
>
> GRANT OWNERSHIP ON DATABASE mydb TO ROLE analyst;
>
> GRANT ALL PRIVILEGES ON DATABASE mydb TO ROLE analyst;
> ```
>
> Note that this example illustrates the default (and recommended) multi-step process for transferring ownership.

In a single step, revoke all privileges on the existing tables in the `mydb.public` schema and transfer ownership of the tables
(along with a copy of their current privileges) to the `analyst` role:

> Copy code
>
> ```
> GRANT OWNERSHIP ON ALL TABLES IN SCHEMA mydb.public TO ROLE analyst COPY CURRENT GRANTS;
> ```

Grant ownership on the `mydb.public.mytable` table to the `analyst` role along with a copy of all current outbound privileges
on the table:

> Copy code
>
> ```
> GRANT OWNERSHIP ON TABLE mydb.public.mytable TO ROLE analyst COPY CURRENT GRANTS;
> ```

Grant ownership on a notebook called `mynotebook` from the `data_science` role to the `finance` role:

> Copy code
>
> ```
> USE ROLE data_science;
> GRANT OWNERSHIP ON NOTEBOOK db_one.schema_one.mynotebook TO ROLE finance;
> ```

### Database roles

In a single step, revoke all privileges on the existing tables in the `mydb.public` schema and transfer ownership of the tables
(along with a copy of their current privileges) to the `mydb.dr1` database role:

> Copy code
>
> ```
> GRANT OWNERSHIP ON ALL TABLES IN SCHEMA mydb.public
>   TO DATABASE ROLE mydb.dr1
>   COPY CURRENT GRANTS;
> ```

Grant ownership on the `mydb.public.mytable` table to the `mydb.dr1` database role along with a copy of all current outbound
privileges on the table:

> Copy code
>
> ```
> GRANT OWNERSHIP ON TABLE mydb.public.mytable
>   TO ROLE mydb.dr1
>   COPY CURRENT GRANTS;
> ```

### Shared database

To transfer the OWNERSHIP privilege on a shared database, use these commands:

> Copy code
>
> ```
> REVOKE USAGE ON DATABASE mydb FROM SHARE myshare;
> GRANT OWNERSHIP ON DATABASE mydb TO ROLE r2;
> GRANT USAGE ON DATABASE mydb TO ROLE r2;
> ```

If necessary, re-grant the database to the share using a [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share) command.
