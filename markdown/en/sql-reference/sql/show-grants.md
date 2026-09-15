# SHOW GRANTS

Lists all access control privileges that have been explicitly granted to roles, users, and shares.

For more information about privileges and roles, refer to [Overview of Access Control](/user-guide/security-access-control-overview).

For more information about shares, refer to [About Secure Data Sharing](/user-guide/data-sharing-intro).

Note

SHOW GRANTS is a special variation that uses different syntax from all the other [SHOW <objects>](/sql-reference/sql/show) commands.

## Syntax

Copy code

```
SHOW GRANTS [ LIMIT <rows> ]

SHOW GRANTS ON ACCOUNT [ LIMIT <rows> ]

SHOW GRANTS ON <object_type> <object_name> [ LIMIT <rows> ]

SHOW GRANTS TO {
  APPLICATION <app_name>
  | APPLICATION ROLE [ <app_name>. ]<app_role_name>
  | SERVICE ROLE <service_name>!<service_role_name>
  | <class_name> ROLE <instance_name>!<instance_role_name>
  | ROLE <role_name>
  | SHARE <share_name> [ IN APPLICATION PACKAGE <app_package_name> ]
  | USER <user_name>
} [ LIMIT <rows> ]

SHOW GRANTS OF {
  APPLICATION ROLE <app_role_name>
  | SERVICE ROLE <service_name>!<service_role_name>
  | ROLE <role_name>
} [ LIMIT <rows> ]

SHOW GRANTS OF SHARE <share_name> [ LIMIT <rows> ]

SHOW FUTURE GRANTS IN SCHEMA { <schema_name> } [ LIMIT <rows> ]

SHOW FUTURE GRANTS IN DATABASE { <database_name> } [ LIMIT <rows> ]

SHOW FUTURE GRANTS TO ROLE <role_name> [ LIMIT <rows> ]

SHOW FUTURE GRANTS TO DATABASE ROLE <database_role_name>
```

## Variants

`SHOW GRANTS`
:   Syntactically equivalent to `SHOW GRANTS TO USER current_user`. Lists all the roles granted to the current user.

`LIMIT rows`
:   Optionally limits the maximum number of rows returned. The actual number of rows returned might be less than the specified limit. For
    example, the number of existing objects is less than the specified limit.

    Default: No value (no limit is applied to the output).

`SHOW GRANTS ON ...`
:   `ACCOUNT`
    :   Lists all the account-level (i.e. global) privileges that have been granted to roles.

    `object_type object_name`
    :   Lists all privileges that have been granted on the object.

        For database roles, you can use the fully qualified name, `database_name.database_role_name`, or the relative name,
        `database_role_name`. If you use the relative name for the database role, Snowflake uses the database in session to resolve the
        relative name of the database role.

`SHOW GRANTS TO ...`
:   `APPLICATION app_name`
    :   Lists all the privileges and roles granted to the application.

    `APPLICATION ROLE [ app_name. ]app_role_name`
    :   Lists all the privileges and roles granted to the application role.

        The name of the application, `app_name`, is optional. If not specified, Snowflake uses the current application. If the
        application is not a database, this command does not return results.

    `SERVICE ROLE service_name!service_role_name`
    :   Lists the service endpoints for which the service role is granted the USAGE privilege.

    `class_name ROLE instance_name!instance_role_name`
    :   Lists all the privileges and roles granted to the [instance role](/sql-reference/snowflake-db-classes#label-instance-roles).

        If the database and schema that contains the `class_name` is not [in use](/sql-reference/sql/use) or is not specified in
        your [search path](/sql-reference/snowflake-db-classes#label-update-search-path), specify the fully-qualified name of the class. For example,
        `SNOWFLAKE.CORE.BUDGET`.

        For details, see the [instance role example](#show-grants-instance-role).

    `ROLE role_name`
    :   Lists all privileges and roles granted to the role. If the role has a grant on a temporary object, then the grant only exists in the
        session that the temporary object was created.

        SHOW GRANTS TO ROLE PUBLIC exposes the following *irrevocable* database roles granted to the public role:

        - ALERT\_VIEWER
        - CLASSIFICATION\_VIEWER
        - CORE\_VIEWER
        - DATA\_PRIVACY\_VIEWER
        - ML\_USER
        - MONITORING\_VIEWER
        - NOTIFICATION\_VIEWER
        - SNOWFLAKE\_TEMPLATE\_SNOWGIT\_VIEWER
        - SPCS\_REGISTRY\_VIEWER

    `SHARE share_name`
    :   Lists all the privileges granted to the share.

    `SHARE share_name IN APPLICATION PACKAGE app_package_name`
    :   Lists all of the privileges and roles granted to a share in the application package.

    `USER user_name`
    :   Lists all the roles granted to the user. Note that the PUBLIC role, which is automatically available to every user, is not listed.

`SHOW GRANTS OF...`
:   `APPLICATION ROLE [ app_name. ]app_role`
    :   Lists all the users and roles to which the application role has been granted.

        The name of the application, `app_name`, is optional. If not specified, Snowflake uses the current application. If the
        application is not a database, this command does not return results.

    `SERVICE ROLE service_name!service_role_name`
    :   Lists all the users and roles to which the service role has been granted.

    `ROLE role_name`
    :   Lists all users and roles to which the role has been granted.

    `SHARE share_name`
    :   Lists all the accounts that are consuming the share. Accounts that have not yet consumed the share are excluded.
        To see all accounts that have been added to a share, query the SNOWFLAKE.ACCOUNT\_USAGE.SHARES view.

`SHOW FUTURE GRANTS IN ...`
:   `SCHEMA database_name.schema_name`
    :   Lists all privileges on new (i.e. future) objects of a specified type in the schema granted to a role. `database_name.` specifies the database in which the schema resides and is optional when querying a schema in the current database.

    `DATABASE database_name`
    :   Lists all privileges on new (i.e. future) objects of a specified type in the database granted to a role.

`SHOW FUTURE GRANTS TO ROLE role_name`
:   Lists all privileges on new (i.e. future) objects of a specified type in a database or schema granted to the role.

`SHOW FUTURE GRANTS TO DATABASE ROLE database_role_name`
:   Lists all privileges on new (i.e. future) objects of a specified type in a database or schema granted to the database role.

    A shared database role does not support future grants. For details, see the usage notes in the [GRANT DATABASE ROLE … TO SHARE](/sql-reference/sql/grant-database-role-share) command.

## Usage notes

- The `granted_by` column indicates the role that authorized a privilege grant to the grantee. The authorization role is known as the
  *grantor*.

  When you grant privileges on an object to a role using [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege), the following authorization rules
  determine which role is listed as the grantor of the privilege:

  1. If an [active role](/user-guide/security-access-control-overview#label-access-control-overview-active-roles) is the object owner (i.e. has the OWNERSHIP privilege on the
     object), that role is the grantor.
  2. If an active role holds the specified permission with the grant option authorized (i.e., the privilege was granted to the active role
     with the GRANT *<privileges>* … TO ROLE *<role\_name>* WITH GRANT OPTION, where *<role\_name>* is one of the active roles). If so, the
     role that holds the privilege with the grant option authorized is the grantor role. Note that if multiple active roles meet this
     criterion, it is non-deterministic which of the roles becomes the grantor role.
  3. If an active role holds the global MANAGE GRANTS privilege, the grantor role is the object owner, not the role that held the
     MANAGE GRANTS privilege. That is, the MANAGE GRANTS privilege allows a role to impersonate the object owner for the purposes of
     granting privileges on that object.

  If the `granted_by` column is empty, the privilege was granted by the Snowflake SYSTEM role. Certain internal operations are
  performed with this role. Grants of privileges authorized by the SYSTEM role cannot be modified by customers.
- When using the SHOW GRANTS … TO SHARE IN APPLICATION PACKAGE syntax:

  - The `grantee_name` column specifies the name of the application package.
  - The `granted_to` column specifies `APPLICATION PACKAGE SHARE`.
- The `granted_by_role_type` column specifies the type of grantor role that performed the grant: `ROLE`, `DATABASE_ROLE`, or
  `APPLICATION_ROLE`. This column only appears in the output when using the SHOW GRANTS ON syntax.
- A data sharing consumer can only view the privileges on objects that are [granted to the share](/sql-reference/sql/grant-privilege-share), such as
  SELECT on a table. Depending on how the grants are set up, the output of a SHOW GRANTS command that is run by the consumer might show
  empty values for shared objects in the following columns: `granted_to`, `grantee_name`, `granted_by_role_type`, and
  `granted_by`. For example:

  - If an account role owns the shared object, the consumer cannot view the OWNERSHIP privilege on shared objects because the consumer
    cannot access (resolve) the role that owns the object (account roles are not shared).
  - If a database role owns the shared object and the provider shares the database role, the consumer can view the OWNERSHIP privilege on
    the shared object because they can resolve the shared database role.
- The `grant_options` column returns `FALSE` when you run a SHOW GRANTS ON <object\_type> <object\_name> command for an object in the
  managed access schema.
- The `privilege` column includes the OWNERSHIP and MANAGE GRANTS privileges for the role that owns the managed access schema when
  you run a SHOW GRANTS ON SCHEMA <managed\_access\_schema> command.
- With database roles and the SHOW FUTURE GRANTS TO DATABASE ROLE syntax, the command returns results for database roles that are not
  granted to a share.

  In the data sharing consumer account, this command does not return any rows when a shared database role is granted future
  privileges. However, depending on your account and the timing of support for future privileges to database roles in this command, you
  might see this error message:

  ```
  Invalid state of the shared database role. Please revoke the future grants to the shared database role.
  ```

  As the consumer, ask the provider to revoke the future grants from the shared database role.

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

List all privileges that have been granted on the `sales` database:

Copy code

```
SHOW GRANTS ON DATABASE sales;
```

```
+---------------------------------+-----------+------------+------------+------------+--------------+--------------+----------------------+--------------+
| created_on                      | privilege | granted_on | name       | granted_to | grantee_name | grant_option | granted_by_role_type | granted_by   |
+---------------------------------+-----------+------------+------------+------------+--------------+--------------+----------------------+--------------+
| Thu, 07 Jul 2016 05:22:29 -0700 | OWNERSHIP | DATABASE   | REALESTATE | ROLE       | ACCOUNTADMIN | true         | ROLE                 | ACCOUNTADMIN |
| Thu, 07 Jul 2016 12:14:12 -0700 | USAGE     | DATABASE   | REALESTATE | ROLE       | PUBLIC       | false        | ROLE                 | ACCOUNTADMIN |
+---------------------------------+-----------+------------+------------+------------+--------------+--------------+----------------------+--------------+
```

List all privileges granted to the `analyst` role:

Copy code

```
SHOW GRANTS TO ROLE analyst;
```

```
+---------------------------------+------------------+------------+------------+------------+--------------+--------------+------------+
| created_on                      | privilege        | granted_on | name       | granted_to | grantee_name | grant_option | granted_by |
|---------------------------------+------------------+------------+------------+------------+--------------+--------------+------------+
| Wed, 17 Dec 2014 18:19:37 -0800 | CREATE WAREHOUSE | ACCOUNT    | DEMOENV    | ROLE       |  ANALYST     | false        | SYSADMIN   |
+---------------------------------+------------------+------------+------------+------------+--------------+--------------+------------+
```

List all privileges granted to the `public` role:

Copy code

```
SHOW GRANTS TO ROLE public;
```

(example trimmed to show only the irrevocable database roles granted to the public role)

```
+---------------------------------+-----------+---------------+-----------------------------------+------------+--------------+--------------+------------+
| created_on                      | privilege | granted_on    | name                              | granted_to | grantee_name | grant_option | granted_by |
|---------------------------------+-----------+---------------+-----------------------------------+------------+--------------+--------------+------------|
| ...                             |           |               |                                   |            |              |              |            |
|---------------------------------+-----------+---------------+-----------------------------------+------------+--------------+--------------+------------+
| 2023-08-18 13:33:01.156 -0700   | USAGE     | DATABASE_ROLE | ALERT_VIEWER                      | ROLE       | PUBLIC       | false        |            |
+---------------------------------+-----------+---------------+-----------------------------------+------------+--------------+--------------+------------+
| 2023-08-18 13:33:01.156 -0700   | USAGE     | DATABASE_ROLE | CLASSIFICATION_VIEWER             | ROLE       | PUBLIC       | false        |            |
+---------------------------------+-----------+---------------+-----------------------------------+------------+--------------+--------------+------------+
| 2023-08-18 13:33:01.156 -0700   | USAGE     | DATABASE_ROLE | CORE_VIEWER                       | ROLE       | PUBLIC       | false        |            |
+---------------------------------+-----------+---------------+-----------------------------------+------------+--------------+--------------+------------+
| 2023-08-18 13:33:01.156 -0700   | USAGE     | DATABASE_ROLE | DATA_PRIVACY_VIEWER               | ROLE       | PUBLIC       | false        |            |
+---------------------------------+-----------+---------------+-----------------------------------+------------+--------------+-------- -----+------------+
| 2023-08-18 13:33:01.156 -0700   | USAGE     | DATABASE_ROLE | ML_USER                           | ROLE       | PUBLIC       | false        |            |
+---------------------------------+-----------+---------------+-----------------------------------+------------+--------------+--------------+------------+
| 2023-08-18 13:33:01.156 -0700   | USAGE     | DATABASE_ROLE | MONITORING_VIEWER                 | ROLE       | PUBLIC       | false        |            |
+---------------------------------+-----------+---------------+-----------------------------------+------------+--------------+--------------+------------+
| 2023-08-18 13:33:01.156 -0700   | USAGE     | DATABASE_ROLE | NOTIFICATION_VIEWER               | ROLE       | PUBLIC       | false        |            |
+---------------------------------+-----------+---------------+-----------------------------------+------------+--------------+--------------+------------+
| 2023-08-18 13:33:01.156 -0700   | USAGE     | DATABASE_ROLE | SNOWFLAKE_TEMPLATE_SNOWGIT_VIEWER | ROLE       | PUBLIC       | false        |            |
+---------------------------------+-----------+---------------+-----------------------------------+------------+--------------+--------------+------------+
| 2023-08-18 13:33:01.156 -0700   | USAGE     | DATABASE_ROLE | SPCS_REGISTRY_VIEWER              | ROLE       | PUBLIC       | false        |            |
+---------------------------------+-----------+---------------+-----------------------------------+------------+--------------+--------------+------------+
| ...                             |           |               |                                   |            |              |              |            |
+---------------------------------+-----------+---------------+-----------------------------------+------------+--------------+--------------+------------+
```

List all the roles granted to the `user1` user:

Copy code

```
SHOW GRANTS TO USER user1;
```

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

Show all privileges granted on an interactive table:

Copy code

```
SHOW GRANTS ON TABLE my_interactive_tbl;
```

```
+-------------------------------+------------+-------------------+----------------------------------+------------+--------------+--------------+--------------+----------------------+
| created_on                    | privilege  | granted_on        | name                             | granted_to | grantee_name | grant_option | granted_by   | granted_by_role_type |
|-------------------------------+------------+-------------------+----------------------------------+------------+--------------+--------------+--------------+----------------------|
| 2025-11-06 22:41:29.679 +0000 | OWNERSHIP  | INTERACTIVE_TABLE | MYDB.MYSCHEMA.MY_INTERACTIVE_TBL | ROLE       | ACCOUNTADMIN | true         | ACCOUNTADMIN | ROLE                 |
| 2025-11-06 22:41:30.794 +0000 | REFERENCES | INTERACTIVE_TABLE | MYDB.MYSCHEMA.MY_INTERACTIVE_TBL | ROLE       | ANALYST      | false        | ACCOUNTADMIN | ROLE                 |
| 2025-11-06 22:41:30.564 +0000 | SELECT     | INTERACTIVE_TABLE | MYDB.MYSCHEMA.MY_INTERACTIVE_TBL | USER       | USER1        | false        | ACCOUNTADMIN | ROLE                 |
+-------------------------------+------------+-------------------+----------------------------------+------------+--------------+--------------+--------------+----------------------+
```

List all roles and users who have been granted the `analyst` role:

Copy code

```
SHOW GRANTS OF ROLE analyst;
```

```
+---------------------------------+---------+------------+--------------+---------------+
| created_on                      | role    | granted_to | grantee_name | granted_by    |
|---------------------------------+---------+------------+--------------+---------------|
| Tue, 05 Jul 2016 16:16:34 -0700 | ANALYST | ROLE       | ANALYST_US   | SECURITYADMIN |
| Tue, 05 Jul 2016 16:16:34 -0700 | ANALYST | ROLE       | DBA          | SECURITYADMIN |
| Fri, 08 Jul 2016 10:21:30 -0700 | ANALYST | USER       | JOESM        | SECURITYADMIN |
+---------------------------------+---------+------------+--------------+---------------+
```

List all privileges granted on future objects in the `sales.public` schema:

Copy code

```
SHOW FUTURE GRANTS IN SCHEMA sales.public;
```

```
+-------------------------------+-----------+----------+---------------------------+----------+-----------------------+--------------+
| created_on                    | privilege | grant_on | name                      | grant_to | grantee_name          | grant_option |
|-------------------------------+-----------+----------+---------------------------+----------+-----------------------+--------------|
| 2018-12-21 09:22:26.946 -0800 | INSERT    | TABLE    | SALES.PUBLIC.<TABLE>      | ROLE     | ROLE1                 | false        |
| 2018-12-21 09:22:26.946 -0800 | SELECT    | TABLE    | SALES.PUBLIC.<TABLE>      | ROLE     | ROLE1                 | false        |
+-------------------------------+-----------+----------+---------------------------+----------+-----------------------+--------------+
```

List all roles privileges granted to the instance role named `cost.budgets.my_budget!ADMIN`:

Copy code

```
SHOW GRANTS TO SNOWFLAKE.CORE.BUDGET ROLE cost.budgets.my_budget!ADMIN;
```

```
+-------------------------------+-----------+------------+----------------------------------------------------------------------------------------------------------------------------------------+
| created_on                    | privilege | granted_on | name                                                                                                                                   |
+-------------------------------+-----------+------------+----------------------------------------------------------------------------------------------------------------------------------------+
| 2023-10-31 15:57:41.489 +0000 | USAGE     | ROLE       | SNOWFLAKE.CORE.BUDGET!ADMIN                                                                                                            |
| 2023-09-25 22:56:12.798 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!ACTIVATE():VARCHAR(16777216)                                                                                     |
| 2023-09-25 22:56:13.304 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!ADD_RESOURCE(TARGET_REF VARCHAR):VARCHAR(16777216)                                                               |
| 2023-09-25 22:56:12.863 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!GET_ACTIVATION_DATE():DATE                                                                                       |
| 2023-09-25 22:56:12.412 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!GET_BUDGET_NAME():VARCHAR(16777216)                                                                              |
| 2023-09-25 22:56:11.510 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!GET_CONFIG():TABLE: ()                                                                                           |
| 2023-09-25 22:56:13.432 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!GET_LINKED_RESOURCES():TABLE: ()                                                                                 |
| 2023-09-25 22:56:11.582 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!GET_MEASUREMENT_TABLE():TABLE: ()                                                                                |
| 2023-09-25 22:56:12.153 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!GET_NOTIFICATION_EMAIL():VARCHAR(16777216)                                                                       |
| 2023-09-25 22:56:12.016 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!GET_NOTIFICATION_INTEGRATION_NAME():VARCHAR(16777216)                                                            |
| 2023-09-25 22:56:12.286 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!GET_NOTIFICATION_MUTE_FLAG():VARCHAR(16777216)                                                                   |
| 2023-09-25 22:56:13.068 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!GET_SERVICE_TYPE_USAGE(SERVICE_TYPE VARCHAR):TABLE: ()                                                           |
| 2023-09-25 22:56:13.245 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!GET_SERVICE_TYPE_USAGE(SERVICE_TYPE VARCHAR, TIME_DEPART VARCHAR, USER_TIMEZONE VARCHAR, TIME_LOWER_BOUND VARCHA |
| 2023-09-25 22:56:12.595 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!GET_SPENDING_HISTORY():TABLE: ()                                                                                 |
| 2023-09-25 22:56:12.732 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!GET_SPENDING_HISTORY(TIME_LOWER_BOUND VARCHAR, TIME_UPPER_BOUND VARCHAR):TABLE: ()                               |
| 2023-09-25 22:56:11.716 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!GET_SPENDING_LIMIT():NUMBER(38,0)                                                                                |
| 2023-09-25 22:56:13.367 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!REMOVE_RESOURCE(TARGET_REF VARCHAR):VARCHAR(16777216)                                                            |
| 2023-09-25 22:56:11.856 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!SET_EMAIL_NOTIFICATIONS(NOTIFICATION_CHANNEL_NAME VARCHAR, EMAIL VARCHAR):VARCHAR(16777216)                      |
| 2023-09-25 22:56:12.349 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!SET_NOTIFICATION_MUTE_FLAG(USER_MUTE_FLAG BOOLEAN):VARCHAR(16777216)                                             |
| 2023-09-25 22:56:11.780 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!SET_SPENDING_LIMIT(SPENDING_LIMIT FLOAT):VARCHAR(16777216)                                                       |
| 2023-09-25 22:56:12.475 +0000 | USAGE     | PROCEDURE  | SNOWFLAKE.CORE.BUDGET!SET_TASK_SCHEDULE(NEW_SCHEDULE VARCHAR):VARCHAR(16777216)                                                        |
+-------------------------------+-----------+------------+----------------------------------------------------------------------------------------------------------------------------------------+
```
