# Use owner’s rights and restricted caller’s rights in an app

This topic describes how to configure an app to use owner’s rights and
restricted caller’s rights.

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

### High-level caller privileges in an app

For more information about high-level caller privileges, see:

- [High-level caller privileges](/developer-guide/restricted-callers-rights/high-level-caller-privileges) — overview of the
  available high-level caller privileges and what each one authorizes.
- [Operations and the required high-level caller privilege](/developer-guide/restricted-callers-rights/high-level-caller-privileges#operations-and-the-required-high-level-caller-privilege)
  — operations that require a specific high-level caller privilege.

## Determine the access requirements of an app

Snowflake Native Apps give providers flexibility in how they configure access to the data and executables
managed by the app. The following table provides guidelines for which mechanism to use depending on
the access requirements of the app:

| Access required | How to get access |
| --- | --- |
| Data or functions owned by the app | Use owner’s rights by default. Providers do not need to request access from the consumer to create or access objects owned by the app. |
| Specific tables, views, or functions in the consumer account | Request references from the consumer |
| Tables, views, functions, and row policies owned by another user or role. | Use restricted caller’s rights, which allow the consumer to enable access to these objects. |
| Broad access to consumer-owned databases | Use database role grants |
| Queries that access a combination of consumer and provider data | Use references and owner’s rights together |
| Account-level objects | Provide custom scripts that contain GRANT commands to grant privileges on specific objects. |
| Perform account-level operations such as creating databases or executing tasks. | Use restricted caller’s rights, which allow the consumer to enable access to perform these actions. |

Expand

Show lessSee more

## Add the `restricted_callers_rights` property to the manifest

As a provider, if you configure an executable in an app to use restricted caller’s rights,
Snowflake recommends that you add the `restricted_callers_rights` to the manifest
file as shown in the following example:

Copy code

```
restricted_callers_rights:
  enabled: true
  description: This app includes stored procedure that uses restricted caller's rights.
```

Although `restricted_callers_rights` is not required, if it is present and `enabled`
is set to `true`, Snowsight includes a section named **Restricted caller’s rights**
in the app’s listing.

## Configure a procedure or service to use restricted caller’s rights

To create a stored procedure that uses restricted caller’s rights, use the
EXECUTE AS RESTRICTED CALLER clause when the app creates an executable as shown
in the following example:

Copy code

```
CREATE OR REPLACE PROCEDURE CORE.HELLO()
RETURNS STRING
LANGUAGE SQL
EXECUTE AS RESTRICTED CALLER
AS
BEGIN
  RETURN 'Hello Snowflake!';
END;
```

For more information, see [CREATE PROCEDURE](/sql-reference/sql/create-procedure).

## Using a restricted caller’s rights service in an app with containers

For more information on configuring a service to use restricted caller’s rights, see
[About using Snowflake-provided caller credentials (caller’s rights)](/developer-guide/snowpark-container-services/spcs-execute-sql#label-spcs-additional-considerations-configuring-callers-rights).

In an app with containers, a Snowpark Container Services service can run with privileges of the app (owner’s rights)
or with the privileges of the caller of the service (restricted caller’s rights). However,
the service *owner* role, instead of the service *user* role, is the app. When granting caller
grants, a consumer specifies the app by using the TO APPLICATION clause as shown in the
following example:

Copy code

```
GRANT CALLER USAGE ON DATABASE consumer_db TO APPLICATION hello_snowflake_app;
```

This example allows the service to run with restricted caller’s rights to
use the caller’s role to access the `consumer_db` database.

## Limitations on restricted caller’s rights in an app

The following limitations apply when using restricted caller’s rights within an app:

- *Unrestricted* caller’s rights are not supported for executables in an app.
- Persistent [reference functions](/developer-guide/native-apps/requesting-refs#supported-reference-functions) are not supported.
- Relative paths to objects on a stage are not supported.
- Restricted caller’s rights executables cannot access the app’s internal objects.
- Executables with owner’s rights cannot call other executables that use unrestricted
  caller’s rights.

  Although executables with owner’s rights owned by the application can invoke executables
  with restricted caller’s rights, these executables must also be owned by the app. For example,
  an app’s stored procedure with owner’s rights cannot call a consumer’s stored procedure with
  restricted caller’s rights.

## Calling billing functions from a restricted caller’s rights procedure in an app

Billing functions such as [SYSTEM$CREATE\_BILLING\_EVENT](/sql-reference/functions/system_create_billing_event)
or [SYSTEM$CREATE\_BILLING\_EVENTS](/sql-reference/functions/system_create_billing_events) cannot be called from an
RCR executable. To call these functions from an
RCR executable in an app, include these functions in an owner’s rights procedure
and call the procedure from the restricted caller’s rights procedure.

## Intellectual property protection and restricted caller’s rights

Apps that include owner’s rights stored procedures redact information about the internal
implementation of the app. For more information, see
[Protect provider intellectual property](/developer-guide/native-apps/redacted-content).

Stored procedures with restricted caller’s rights also redact internal information about the app.
In particular, this applies to the following commands, views, and functions where much of the information
is redacted:

- The [DESCRIBE PROCEDURE](/sql-reference/sql/desc-procedure) command
- The [PROCEDURES view](/sql-reference/info-schema/procedures) of the Information Schema
- The [PROCEDURES view](/sql-reference/account-usage/procedures) of the Account Information Schema
- The [GET\_DDL](/sql-reference/functions/get_ddl) function

However, unlike stored procedures with owner’s rights, procedures using restricted caller’s rights
do not redact information from the query history and query profiles.

## Developing apps that use restricted caller’s rights

In general, only roles that have been granted the MANAGE CALLER GRANTS privilege can
grant caller grants to an executable. However, during the development lifecycle of a
Snowflake Native App, providers may need to create and drop the app frequently. Snowflake Native Apps
provide a mechanism for creating caller grants for an
[app in development mode](/developer-guide/native-apps/installing-testing-application#label-native-apps-dev-mode).

Providers can use a role without the MANAGE CALLER GRANTS to grant caller grants to an app.
However, this requires all of the following:

- The app must be created in [development mode](/developer-guide/native-apps/installing-testing-application#label-native-apps-dev-mode).
- The current role has the app owner role in the role hierarchy.
- The app owner role has a superset of the caller grants that are being granted.

  Note

  The ALL CALLER PRIVILEGES privilege is a superset of any set of caller privileges.

The superset requirement cannot be met through INHERITED CALLER grants, which normally
cover all current and future objects of a particular type under a specific container.
For more information, see [GRANT CALLER](/sql-reference/sql/grant-caller).

To meet this requirement, the caller grants being granted must be explicitly covered by the
caller grants that are granted to the app owner role.

### Enable app developers to grant caller rights to an app in dev mode

To allow an app owner role to grant a certain set of caller grants to an app in development
mode, a user with the ACCOUNTADMIN role or a role that has been granted the MANAGE CALLER GRANTS
privilege must first grant caller grants that cover the set of grants to the app owner role.

The following example shows how to grant the required caller privileges on the databases in an
account:

Copy code

```
GRANT ALL INHERITED CALLER PRIVILEGES
  ON ALL DATABASES IN ACCOUNT
  TO ROLE app_dev_role;
```

This command grants all caller grants on all databases to the `app_dev_role` role.

Note

This command only grants caller grants. It does not allow the app developer to access
an object that they are not already allowed to access.

### Additional security measures for apps in development mode

Allowing app developers owner roles without the MANAGE CALLER GRANTS privilege streamlines
the app development process, but it also introduces potential security risks. To minimize
these risks, Snowflake verifies that the app owner continues to have required caller grants
for the app. If the app owner loses the required caller grants, the app loses them also.
