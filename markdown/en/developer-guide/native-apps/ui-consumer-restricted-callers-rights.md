# Grant restricted caller’s rights to an executable in an app

Preview Feature — Private

Support for this feature is currently not in production and is available only to selected accounts.

This topic describes how a consumer can grant caller grants to an executable
in a Snowflake Native App.

## About owner’s rights and restricted caller’s rights in an app

In the context of an app, the following
types of executables are supported:

- Stored procedures owned by the app
- Services available in apps with containers

Each of these types of executables can be configured to use either owner’s rights or restricted caller’s rights.

Owner’s rights:
:   By default, executables within an app use owner’s rights, which means that they run with the privileges granted to the owner of the executable, which is the app itself.

    > For example, owner’s rights allow an executable to access data in the provider account
    > and present that data to the consumer. However, they do not allow the consumer to access
    > the data directly.
    >
    > For example, the [CREATE PROCEDURE](/sql-reference/sql/create-procedure) command creates a
    > stored procedure that uses owner’s rights by default. Consumers can call the
    > stored procedure if they have been granted access using application roles. If the
    > app has the privileges to perform an operation, then the stored procedure can perform that
    > operation.
    >
    > For general information on owner’s rights, see
    > [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).

Restricted caller’s rights:
:   Restricted caller’s rights allow an executable to run with caller’s rights, but restrict
    which of the caller’s privileges the executable runs with. With restricted caller’s rights,
    an executable owned by an app cannot run with a specific privilege unless an administrator
    in the consumer account explicitly allows it by using the [GRANT CALLER](/sql-reference/sql/grant-caller)
    command.

    Note

    To guarantee that executables in an app are secure, Snowflake Native Apps do not support unrestricted
    caller’s rights.

    For general information on restricted caller’s rights, see
    [Restricted caller’s rights](/developer-guide/restricted-callers-rights).

### Scope of restricted caller’s rights in an app

Snowflake recommends that consumers grant caller grants at a container level and not on specific objects in their account.

Schema level:
:   Grants caller rights to the schema, but does not grant any rights to objects
    in the schema. For example, granting the CALLER USAGE caller grant on a schema only
    grants the USAGE privilege on the schema. To grant access to a specific object, for
    example a function, use GRANT INHERITED CALLER USAGE ON ALL FUNCTIONS IN SCHEMA.

Database level:
:   Granting caller grants at the database level only allows an executable to
    access the database and all schemas in the database. For example, granting the
    CALLER USAGE caller grant grants the USAGE privilege on the database. However, to
    grant access to a specific object, you must use the following command:

    Copy code

    ```
    GRANT INHERITED CALLER USAGE ON ALL FUNCTIONS IN DATABASE;
    ```

Account level:
:   Granting caller grants at the account level allows an executable to perform account-level operations.
    Granting the CALLER USAGE caller grant only allows the executable to access the account,
    it does not provide access to objects within the account.

    To allow access to specific objects, you grant access to specific types of object in the account.
    For example, granting the CREATE DATABASE caller grant allows an executable to create databases in
    the consumer account as shown in the following example:

    Copy code

    ```
    GRANT CALLER CREATE DATABASE ON ACCOUNT TO my_app;
    ```

### Account-level caller grants that can be granted to an app

Providers can configure an executable in an app to use the following account-level caller grants:

- CREATE DATABASE
- EXECUTE ALERT
- EXECUTE MANAGED TASK
- EXECUTE TASK
- READ SESSION
- VIEW LINEAGE

Note

Consumers should use caution when granting account-level caller grants to an app.

## Privileges required to grant restricted caller’s rights to an app

To grant caller grants to an app as a consumer, you must use the ACCOUNTADMIN role or use
a role that has the MANAGE CALLER GRANTS privilege. For more information, see
[GRANT CALLER](/sql-reference/sql/grant-caller).

## Grant caller grants to an executable in an app using Snowsight

Using Snowsight, you can grant caller grants to an app on objects in the consumer account.

Note

To perform other tasks, including revoking caller grants from an app, granting caller grants to a
specific table, or granting account-level caller’s rights, you must use the appropriate SQL commands.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select an app.
4. Click the **Settings** icon in the toolbar, then select the
   **Privileges** tab.

   If the app supports restricted caller’s rights, the **Restricted caller’s rights** section
   is displayed in the **Privileges** tab.

   Note

   You can only grant caller grants from Snowsight if the provider has configured the app
   to display the restricted caller’s rights UI.
5. Click **Add grants**.
6. Select an **Access scope**.

   This determines whether the caller’s rights apply to a schema, a database, or at the account level.
   You should select the option with the least amount of scope possible to avoid granting unnecessary
   rights to the app.

   Caution

   Use caution when selecting account level scope, which can grant caller’s rights to the app on all
   supported object types.
7. If you selected schema or database scope, select the schema or
   database as required.

> Note
>
> You can select multiple schemas or databases. You can also select schemas in different databases.

1. Click **Next**.
2. Select the type of objects to which caller’s rights will be granted.

   Use search to find an object type. The list of object types depends on the scope you chose above.

   When you select an object type, the object’s entry in the list expands to available privileges for
   each object type.
3. Select the privileges you want to grant.

   You can select multiple privileges for each object type. You can also select privileges for
   other object types.

   Note

   Snowflake automatically grants the USAGE privilege on any objects you select.
4. Click **Next**.
5. Select **Grant summary** to verify the scope, object types, and privileges that you select.

   Note

   Any objects of the selected type that are created in the future will be created with the same
   privileges using the scope and object types selected.
6. Select **SQL** to view the [GRANT CALLER](/sql-reference/sql/grant-caller) commands the Snowsight will run.

   Note

   If required, you can copy these commands and run them manually in a worksheet.
7. Click **Save**

> The scope, objects, and privileges you selected are displayed in the **Restricted caller’s rights section**.

To modify the privileges you selected, click **Edit** and select or deselect privileges as required.

## Grant caller grants to an executable in an app using SQL

When configuring an app that requests restricted caller’s rights, perform the
following tasks to grant caller grants to the app:

1. Check the listing of the app to verify if the provider has communicated that
   the app has RCR executables.
2. Grant the caller grants as mentioned in the listing. The following example shows how to use
   the [GRANT CALLER](/sql-reference/sql/grant-caller) command to grant the SELECT privilege on all tables
   in a specific database and schema:

   Copy code

   ```
   GRANT CALLER USAGE ON DATABASE db1
     TO APPLICATION hello_snowflake_app;
   GRANT CALLER USAGE ON SCHEMA db1.sch1
     TO APPLICATION hello_snowflake_app;
   GRANT INHERITED CALLER SELECT ON ALL TABLES IN SCHEMA db.sch1
     TO APPLICATION hello_snowflake_app;
   ```

   This command allows an executable with restricted caller’s rights to access run queries on
   all tables with the `db.sch1` database and schema. In addition to granting the SELECT privilege
   on all tables, you must also grant USAGE on the database and schema.
