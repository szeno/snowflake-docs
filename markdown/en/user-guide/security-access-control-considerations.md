# Access control best practices

This topic describes best practices and important considerations for managing secure access to your Snowflake account and data stored within
the account. Primarily, it provides general guidance for configuring role-based access control (RBAC), which limits access to objects based
on a user’s role. For specific considerations about user-based access control (UBAC), see [Comparing and contrasting RBAC with UBAC](#label-security-ubac-considerations).

## Using the ACCOUNTADMIN Role

The account administrator (users with the ACCOUNTADMIN system role) role is the most powerful role in the system. This role alone is
responsible for configuring parameters at the account level. Users with the ACCOUNTADMIN role can view and manage Snowflake billing
and credit data, and can stop any running SQL statements.

Note that ACCOUNTADMIN is not a superuser role. This role only allows viewing and managing objects in the account if this role, or a
role lower in a [role hierarchy](/user-guide/security-access-control-overview#label-role-hierarchy-and-privilege-inheritance), has sufficient privileges on the objects.

In the system role hierarchy, the other administrator roles are children of this role:

- The user administrator (USERADMIN) role includes the privileges to create and manage users and roles (assuming ownership of those roles or
  users has not been transferred to another role).
- The security administrator (SECURITYADMIN system-defined) role includes the global MANAGE GRANTS privilege to grant or revoke privileges
  on objects in the account. The USERADMIN role is a child of this role in the default access control hierarchy. For more information about
  the children system-defined roles, see [System-defined roles](/user-guide/security-access-control-overview#label-access-control-overview-roles-system).
- The system administrator (SYSADMIN) role includes the privileges to create warehouses, databases, and all database objects (schemas,tables,
  and so on).

Attention

By default, when your account is provisioned, the first user is assigned the ACCOUNTADMIN role. This user should then create one or more
additional users who are assigned the USERADMIN role. All remaining users should be created by the user(s) with the USERADMIN role or
another role that is granted the global CREATE USER privilege.

### Control the assignment of the ACCOUNTADMIN role to users

Snowflake strongly recommends the following precautions when assigning the ACCOUNTADMIN role to users:

- Assign this role only to a select/limited number of people in your organization.
- All users assigned the ACCOUNTADMIN role should also be required to use multi-factor authentication (MFA) for login (for details, see
  [Configuring access control](/user-guide/security-access-control-configure)).
- Assign this role to at least two users. We follow strict security procedures for resetting a forgotten or lost password for users with the
  ACCOUNTADMIN role. These procedures can take up to two business days. Assigning the ACCOUNTADMIN role to more than one user avoids having
  to go through these procedures because the users can reset each other’s passwords.

Tip

Assigning email addresses for current employees to ACCOUNTADMIN users helps Snowflake Support know who to contact in an urgent situation.

### Avoid using the ACCOUNTADMIN role to create objects

The ACCOUNTADMIN role is intended for performing initial setup tasks in the system and managing account-level objects and tasks on a
day-to-day basis. As such, it should not be used to create objects in your account, unless you absolutely need these objects to have the
highest level of secure access. If you create objects with the ACCOUNTADMIN role and you want users to have access to these objects, you
must explicitly grant privileges on the objects to the roles for these users.

Instead, Snowflake recommends creating a hierarchy of roles aligned with business functions in your organization and ultimately assigning
these roles to the SYSADMIN role. For more information, see [Aligning Object Access with Business Functions](#aligning-object-access-with-business-functions) in this topic.

Tip

To help prevent account administrators from inadvertently using the ACCOUNTADMIN role to create objects, assign these users additional
roles and designate one of these roles as their default (do not make ACCOUNTADMIN the default role for any users in the system).

This doesn’t prevent users from using the ACCOUNTADMIN role to create objects, but it forces them to explicitly change their role to
ACCOUNTADMIN each time they log in. This can help raise awareness of the purpose/function of roles in the system and encourage users to
change to the appropriate role for performing a given task, particularly account administrator tasks.

### Avoid using the ACCOUNTADMIN Role for automated scripts

Snowflake recommends using a role other than ACCOUNTADMIN for automated scripts. If, as recommended, you create a role hierarchy under the
SYSADMIN role, all warehouse and database object operations can be performed using the SYSADMIN role or lower roles in the hierarchy. The
only limitations you would encounter is creating or modifying users or roles. These operations must be performed by a user with the
SECURITYADMIN role or another role with sufficient object privileges.

## Accessing database objects

All securable database objects (such as TABLE, FUNCTION, FILE FORMAT, STAGE, SEQUENCE, etc.) are contained within a SCHEMA object within a
DATABASE. As a result, to access database objects, in addition to the privileges on the specific database objects, users must be granted
USAGE or any other privilege on the container database and schema.

For example, suppose `mytable` is created in `mydb.myschema`. In order to query `mytable`, a user must have the following
privileges at a minimum:

Database:
:   USAGE on `mydb`

Schema:
:   USAGE on `myschema`

Table:
:   SELECT on `mytable`

## Managing custom roles

When a custom role is first created, it exists in isolation. The role must be assigned to any users who will use the object privileges
associated with the role. The custom role must also be granted to any roles that will manage the objects created by the custom role.

Important

By default, not even the ACCOUNTADMIN role can modify or drop objects created by a custom role. The custom role must be granted to the
ACCOUNTADMIN role directly or, preferably, to another role in a hierarchy with the SYSADMIN role as the parent. The SYSADMIN role is
managed by the ACCOUNTADMIN role.

For instructions to create a role hierarchy, see [Creating a role hierarchy](/user-guide/security-access-control-configure#label-security-role-hierarchy).

## Aligning object access with business functions

Consider taking advantage of role hierarchies to align access to database objects with business functions in your organization. In a role
hierarchy, roles are granted to other roles to form an inheritance relationship. Permissions granted to roles at a lower level are inherited
by roles at a higher level.

For optimal flexibility in controlling access to database objects, create a combination of object *access roles* with different permissions
on objects and assign them as appropriate to *functional roles*:

- Grant permissions on database objects or account objects (such as warehouses) to access roles.
- Grant access roles to functional roles to create a role hierarchy. These roles correspond to the business functions of your organization
  and serve as a catch-all for any access roles required for these functions.

  When appropriate, grant lower-level functional roles to higher-level functional roles in a parent-child relationship where the parent
  roles map to business functions that should subsume the permissions of the child roles.

  Following best practices for role hierarchies, grant the highest-level functional roles in a role hierarchy to the system administrator
  (SYSADMIN) role. System administrators can then grant privileges on database objects to any roles in this hierarchy:

Note

There is no technical difference between an object access role and a functional role in Snowflake. The difference is in how they are used
logically to assemble and assign sets of permissions to groups of users.

### Example

As a simple example, suppose two databases in an account, `fin` and `hr`, contain payroll and employee data, respectively. Accountants
and analysts in your organization require different permissions on the objects in these databases to perform their business functions.
Accountants should have read-write access to `fin` but might only require read-only access to `hr` because human resources personnel
maintain the data in this database. Analysts could require read-only access to both databases.

Permissions on existing database objects are granted via the following hierarchy of access roles and functional roles:

Note

When new objects are added in each database, consider automatically granting privileges on the objects to roles based on object type
(for example schemas, tables, or views). For information, see [Simplifying Grant Management Using Future Grants](#simplifying-grant-management-using-future-grants) (in this topic).

| Custom Role | Description | Privileges |
| --- | --- | --- |
| `db_hr_r` | Access role that permits read-only access to tables in the `hr` database. | USAGE on database `hr`.  USAGE on all schemas in database `hr`.  SELECT on all tables in database `hr`. |
| `db_fin_r` | Access role that permits read-only access to tables in the `fin` database. | USAGE on database `fin`.  USAGE on all schemas in database `fin`.  SELECT on all tables in database `fin`. |
| `db_fin_rw` | Access role that permits read-write access to tables in the `fin` database. | USAGE on database `fin`.  USAGE on all schemas in database `fin`.  SELECT, INSERT, UPDATE, DELETE on all tables in database `fin`. |
| `accountant` | Functional role for accountants in your organization. | N/A |
| `analyst` | Functional role for analysts in your organization. | N/A |

Expand

Show lessSee more

The following diagram shows the role hierarchy for this example:

![Example: Hierarchy of access and functional roles](/static/images/role-hierarchy-practical.png)

To configure access control for this example:

1. As a user administrator (user with the USERADMIN role) or another role with the CREATE ROLE privilege on the account, create the access
   roles and functional roles in this example:

   Copy code

   ```
   CREATE ROLE db_hr_r;
   CREATE ROLE db_fin_r;
   CREATE ROLE db_fin_rw;
   CREATE ROLE accountant;
   CREATE ROLE analyst;
   ```
2. As a security administrator (user with the SECURITYADMIN role) or another role with the MANAGE GRANTS privilege on the account, grant the
   required minimum permissions to each of the access roles:

   Copy code

   ```
   -- Grant read-only permissions on database HR to db_hr_r role.
   GRANT USAGE ON DATABASE hr TO ROLE db_hr_r;
   GRANT USAGE ON ALL SCHEMAS IN DATABASE hr TO ROLE db_hr_r;
   GRANT SELECT ON ALL TABLES IN DATABASE hr TO ROLE db_hr_r;

   -- Grant read-only permissions on database FIN to db_fin_r role.
   GRANT USAGE ON DATABASE fin TO ROLE db_fin_r;
   GRANT USAGE ON ALL SCHEMAS IN DATABASE fin TO ROLE db_fin_r;
   GRANT SELECT ON ALL TABLES IN DATABASE fin TO ROLE db_fin_r;

   -- Grant read-write permissions on database FIN to db_fin_rw role.
   GRANT USAGE ON DATABASE fin TO ROLE db_fin_rw;
   GRANT USAGE ON ALL SCHEMAS IN DATABASE fin TO ROLE db_fin_rw;
   GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN DATABASE fin TO ROLE db_fin_rw;
   ```
3. As a security administrator (user with the SECURITYADMIN role) or another role with the MANAGE GRANTS privilege on the account, grant the
   `db_fin_rw` access role to the `accountant` functional role, and grant the `db_hr_r` `db_fin_r` access roles to the `analyst`
   functional role:

   Copy code

   ```
   GRANT ROLE db_fin_rw TO ROLE accountant;
   GRANT ROLE db_hr_r TO ROLE analyst;
   GRANT ROLE db_fin_r TO ROLE analyst;
   ```
4. As a security administrator (user with the SECURITYADMIN role) or another role with the MANAGE GRANTS privilege on the account, grant
   both the `analyst` and `accountant` roles to the system administrator (SYSADMIN) role:

   Copy code

   ```
   GRANT ROLE accountant,analyst TO ROLE sysadmin;
   ```
5. As a security administrator (user with the SECURITYADMIN role) or another role with the MANAGE GRANTS privilege on the account, grant the
   business functional roles to the users who perform those business functions in your organization. In this example, the `analyst`
   functional role is granted to user `user1`, and the `accountant` functional role is granted to user `user2`.

   Copy code

   ```
   GRANT ROLE accountant TO USER user1;
   GRANT ROLE analyst TO USER user2;
   ```

## Managing database object access using database roles

Database roles are essentially the same as traditional [roles](/user-guide/security-access-control-overview#label-access-control-overview-role-types) created at the account
level (custom *account roles*) except for their scope: To permit SQL actions on objects within a database, privileges can be granted
to a database role in the same database.

Database roles are intended to satisfy the following use cases:

Ease of management:
:   Database owners can independently manage access to securable objects within their own databases. Database owners can perform the
    following actions:

    - Create and manage database roles.
    - Grant privileges to database roles.

      Privileges on objects granted to the database roles must be scoped to objects contained in the database where the role exists.
      Privileges on objects in one database (such as tables or views) cannot be granted to database roles in another database.

      Any privilege, including OWNERSHIP, can be granted to database roles on objects in a database. Note that only an account role
      can hold the OWNERSHIP privilege on the database itself.
    - Create or extend [role hierarchies](/user-guide/security-access-control-overview#label-role-hierarchy-and-privilege-inheritance). Grant database roles to other database
      roles within the same database, and then grant the highest-level database roles in a database to account roles. For more information,
      see [Role hierarchy and privilege inheritance](/user-guide/security-access-control-overview#label-role-hierarchy-and-privilege-inheritance).

      Note that granting a database role to an account role implicitly grants the USAGE privilege on the database that contains the database
      role to that account role. Granting the USAGE privilege on the database explicitly is not required.

Data Sharing:
:   Data providers in Snowflake’s [Secure Data Sharing](/user-guide/data-sharing-intro) can segment the securable objects in a share
    by creating multiple database roles in a database to share and granting privileges on a subset of the objects in the database to each
    database role. After creating a database from a share that includes database roles, data consumers grant each shared database role to
    one or more account-level roles in their own account.

    Without database roles, account administrators in data consumer accounts grant a single privilege, IMPORTED PRIVILEGES, to roles to
    allow their users to access all databases and database objects (tables, secure views, etc.) in a share. There is no option to
    allow different groups of users in a data consumer account to access a subset of the shared objects. This all or nothing approach
    requires data providers to create multiple shares to grant access to different objects in the same databases.

Note that database roles cannot be [activated](/user-guide/security-access-control-overview#label-access-control-overview-active-roles) directly in a session. Grant database
roles to account roles, which can be activated in a session.

## Centralizing grant management using managed access schemas

With regular (non-managed) schemas in a database, object owners (roles with the OWNERSHIP privilege on one or more objects) can grant access
on those objects to other roles, with the option to further grant those roles the ability to manage object grants.

To further lock down object security, consider using managed access schemas. In a managed access schema, object owners lose the ability to
make grant decisions. Only the schema owner (the role with the OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege
can grant privileges on objects in the schema, including [future grants](/user-guide/security-access-control-configure#label-granting-future-privs-on-schema-objects), centralizing
privilege management.

Note that a role that holds the global MANAGE GRANTS privilege can grant additional privileges to the current (grantor) role.

For more information on managed access schemas, see [Creating managed access schemas](/user-guide/security-access-control-configure#label-managed-access-schemas).

## Simplifying grant management using future grants

Future grants allow defining an initial set of privileges on objects of a certain type (for example tables or views) in a specified schema.
As new objects are created, the defined privileges are automatically granted to a role, simplifying grant management.

Consider the following scenario, in which a particular role is granted the SELECT privilege on all new tables created in schema. At a later
date, the decision is made to revoke the privilege from this role and instead grant it to a different role. Using the ON FUTURE keywords
for new tables and the ALL keyword for existing tables, few SQL statements are required to grant and revoke privileges on new and existing
tables. For example:

Copy code

```
-- Grant the SELECT privilege on all new (future) tables in a schema to role R1
GRANT SELECT ON FUTURE TABLES IN SCHEMA s1 TO ROLE r1;

-- / Create tables in the schema /

-- Grant the SELECT privilege on all new tables in a schema to role R2
GRANT SELECT ON FUTURE TABLES IN SCHEMA s1 TO ROLE r2;

-- Grant the SELECT privilege on all existing tables in a schema to role R2
GRANT SELECT ON ALL TABLES IN SCHEMA s1 TO ROLE r2;

-- Revoke the SELECT privilege on all new tables in a schema (future grant) from role R1
REVOKE SELECT ON FUTURE TABLES IN SCHEMA s1 FROM ROLE r1;

-- Revoke the SELECT privilege on all existing tables in a schema from role R1
REVOKE SELECT ON ALL TABLES IN SCHEMA s1 FROM ROLE r1;
```

For more information on future grants, see [Assigning future grants on objects](/user-guide/security-access-control-configure#label-granting-future-privs-on-schema-objects).

## Viewing query results

A user cannot view the result set from a query that another user executed. This behavior is intentional. For security reasons, only the user
who executed a query can access the query results.

Note

This behavior is not connected to the Snowflake access control model for objects. Even a user with the ACCOUNTADMIN role cannot
view the results for a query run by another user.

## Understanding cloned objects and granted privileges

Cloning a database, schema or table creates a copy of the source object. The cloned object includes a snapshot of data present in the source
object when the clone was created.

A cloned object is considered a new object in Snowflake. Any privileges granted on the source object do not transfer to the cloned object.
However, a cloned container object (a database or schema) retains any privileges granted on the objects contained in the source object. For
example, a cloned schema retains any privileges granted on the tables, views, UDFs, and other objects in the source
schema.

For more details about cloning, see [Cloning considerations](/user-guide/object-clone) and [CREATE <object> … CLONE](/sql-reference/sql/create-clone).

## Comparing and contrasting RBAC with UBAC

Role-based access control (RBAC) is your foundation for access control in Snowflake. RBAC provides, by design, scalability and
centralized control. Using RBAC, you grant privileges to roles, and then assign users to those roles, simplifying administration, ensuring
consistency, and making audit access easier. RBAC is generally recommended for production environments and enterprise-level governance.
User-based access control (UBAC) is intended for use cases such as private development and collaboration.

You should consider using UBAC for collaborative scenarios, such as building Streamlit applications. During a collaborative development process, an asset owner may want to control access to the asset before sharing it with a wider audience. UBAC complements RBAC by providing flexibility to grant privileges directly to individual users. UBAC is particularly useful in scenarios that benefit from a more granular access control model.

UBAC does not provide object owners with new levels of privilege. If you currently trust object owners to manage access to their objects
using roles in RBAC, then using UBAC does not fundamentally change that level of trust. Object owners already possess the ability to grant
access to any role, including broadly accessible roles such as PUBLIC. UBAC allows object owners to grant access directly to specific
users. UBAC does not impact query performance.

## Avoiding grant proliferation when using UBAC

To prevent object owners from indiscriminately granting access to objects, use [managed access schemas](/user-guide/security-access-control-configure#label-managed-access-schemas).
Managed access schemas remove the ability for object owners to grant access to other roles or users. Only schema owners or a role with
the MANAGE GRANTS privilege can grant privileges on objects in a managed access schema. Grant proliferation can occur while using either UBAC or RBAC.
Outside managed access schemas, object owners can grant access to any role in an account when using RBAC, just as they can grant privileges
to any user when using UBAC.

## Monitoring access control privileges in your account

You can monitor privileges granted to roles, users, and applications using the GRANTS\_TO\_ROLES view in ACCOUNT\_USAGE. For more information,
see [GRANTS\_TO\_ROLES view](/sql-reference/account-usage/grants_to_roles).

You can also monitor access control privileges in your account in the following ways:

- Viewing direct grants to all users
- Showing direct grants to specific users
- Viewing the current set of privileges granted on an object
- Viewing the current permissions on a schema
- Viewing the privileges on a database schema
- Viewing the current set of privileges granted to a role or a user

For example, to view direct grants to all users, run the following query:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_ROLES
  WHERE granted_to = 'USER';
```

For example, to show direct grants to specific users, use the [pipe operator](/sql-reference/operators-flow)
(`->>`) to filter the result of a SHOW GRANTS TO USER command to show only the privileges granted directly to the user,
not through roles:

Copy code

```
SHOW GRANTS TO USER <user_name>
  ->> SELECT * FROM $1 WHERE "role" IS NULL;
```

For example, to view the current set of privileges granted on an object, you can run the [SHOW GRANTS](/sql-reference/sql/show-grants) command.

Note

Executing the SHOW GRANTS command on a specific object requires the same object privileges as running the SHOW command for that object
type.

For example, running the SHOW GRANTS command on a table requires the following privileges on the table and its database and schema:

Database:
:   USAGE

Schema:
:   USAGE

Table:
:   *any privilege*

For example, to view the current permissions on a schema, execute the following command:

Copy code

```
SHOW GRANTS ON SCHEMA <database_name>.<schema_name>;
```

For example, to view the privileges on `database_a.schema_1` that were granted in
[Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role), execute the following command:

Copy code

```
SHOW GRANTS ON SCHEMA database_a.schema_1;
```

Snowflake returns the following results:

```
+-------------------------------+-----------------------+------------+----------------------+------------+--------------------------+--------------+---------------+
| created_on                    | privilege             | granted_on | name                 | granted_to | grantee_name             | grant_option | granted_by    |
|-------------------------------+-----------------------+------------+----------------------+------------+--------------------------+--------------+---------------|
| 2022-03-07 09:04:23.635 -0800 | USAGE                 | SCHEMA     | database_a.schema_1  | ROLE       | R1                       | false        | SECURITYADMIN |
+-------------------------------+-----------------------+------------+----------------------+------------+--------------------------+--------------+---------------+
```

You can also run the SHOW GRANTS command to view the current set of privileges granted to:

- A role:

  Copy code

  ```
  SHOW GRANTS TO ROLE <role_name>;
  ```

  For example, execute the following command to view the privileges granted on role `r1`, created as a custom role:

  Copy code

  ```
  SHOW GRANTS TO ROLE r1;
  ```

  Snowflake returns the following results:

  ```
  +-------------------------------+-----------+------------+----------------------+------------+--------------+--------------+---------------+
  | created_on                    | privilege | granted_on | name                 | granted_to | grantee_name | grant_option | granted_by    |
  |-------------------------------+-----------+------------+----------------------+------------+--------------+--------------+---------------|
  | 2022-03-07 09:08:43.773 -0800 | USAGE     | DATABASE   | D1                   | ROLE       | R1           | false        | SECURITYADMIN |
  | 2022-03-07 09:08:55.253 -0800 | USAGE     | SCHEMA     | D1.S1                | ROLE       | R1           | false        | SECURITYADMIN |
  | 2022-03-07 09:09:07.206 -0800 | SELECT    | TABLE      | D1.S1.T1             | ROLE       | R1           | false        | SECURITYADMIN |
  | 2022-03-07 09:08:34.838 -0800 | USAGE     | WAREHOUSE  | W1                   | ROLE       | R1           | false        | SECURITYADMIN |
  +-------------------------------+-----------+------------+----------------------+------------+--------------+--------------+---------------+
  ```
- A user:

  Copy code

  ```
  SHOW GRANTS TO USER <user_name>;
  ```

  For example, execute the following command to view the privileges granted to user `user1`:

  Copy code

  ```
  SHOW GRANTS TO USER user1;
  ```

  Snowflake returns the following results:

  ```
  +-------------------------------+-----------+------------+---------------------------+-----------+------------+--------------+--------------+---------------+
  | created_on                    | privilege | granted_on | name                      |  role     | granted_to | grantee_name | grant_option | granted_by    |
  |-------------------------------+-----------+------------+---------------------------+-----------+------------+--------------+------------------------------|
  | 2025-05-07 09:08:43.773 -0800 | USAGE     | DATABASE   | test_db                   | null      | USER       | user1        | false        | SECURITYADMIN |
  | 2025-05-07 09:08:55.253 -0800 | USAGE     | SCHEMA     | test_db.test_sch          | null      | USER       | user1        | false        | SECURITYADMIN |
  | 2025-05-07 09:08:55.253 -0800 | SELECT    | TABLE      | test_db.test_sch.test_tbl | null      | USER       | user1        | false        | SECURITYADMIN |
  | 2025-05-07 09:08:34.838 -0800 | USAGE     | WAREHOUSE  | test_wh                   | null      | USER       | user1        | false        | SECURITYADMIN |
  +-------------------------------+-----------+------------+---------------------------+-----------+------------+--------------+--------------+---------------+
  ```
