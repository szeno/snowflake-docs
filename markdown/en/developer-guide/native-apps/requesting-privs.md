# Request global privileges from consumers

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how providers can configure a Snowflake Native App to request global
privileges from a consumer after the consumer installs the app. These privileges allow
the Snowflake Native App to perform tasks in the consumer account, for example creating a warehouse or
a database.

If an app needs to perform actions or create objects outside the context of the Snowflake Native App,
the consumer must grant the privileges to allow the application to do so.

## Workflow for requesting global privileges from the consumer

Note

Refer to [Create a user interface to request privileges and references](/developer-guide/native-apps/requesting-ui) for information on creating a user interface that
allows consumers to grant privileges using Snowsight.

To configure a Snowflake Native App to request global privileges providers use the following workflow:

1. Determine the privileges required by the app.

   For example, if an app needs to create a database in the consumer account, the provider must
   request that the consumer grant the CREATE DATABASE global privilege to the application.

   Refer to [Privileges the provider can request from the consumer](#label-native-apps-privs-supported) for details on the global privileges
   an app can request.
2. Add the required privileges to the manifest file. See
   [Add a privilege request to the manifest file](#label-native-apps-privs-manifest) for details.

After installing the Snowflake Native App, the consumer performs the following:

1. Review the global privileges required by the application. See
   [View the privileges requested by a Snowflake Native App](#label-native-apps-privs-view) for more information.
2. Grant the global privileges on the application. See [Grant privileges to an application](#label-native-apps-privs-grant-sql) for more
   information.

## Privileges the provider can request from the consumer

The Snowflake Native App Framework allows providers to request the following
[global privileges](/user-guide/security-access-control-privileges#label-global-privileges) in the consumer account:

- BIND SERVICE ENDPOINT
- CREATE COMPUTE POOL
- CREATE DATABASE
- CREATE WAREHOUSE
- EXECUTE ALERT
- EXECUTE TASK
- EXECUTE MANAGED TASK
- IMPORTED PRIVILEGES ON SNOWFLAKE DB
- MANAGE WAREHOUSES
- READ SESSION

Note

Granting IMPORTED PRIVILEGES ON SNOWFLAKE DB allows the Snowflake Native App to see information about usage and costs
associated with the consumer account. You should ensure that consumers are aware of this
when publishing your Snowflake Native App.

## Add a privilege request to the manifest file

The following example shows how to add the EXECUTE TASK privilege to the manifest file:

Copy code

```
privileges:
  - EXECUTE TASK:
    description: "Privilege to run tasks within the consumer account"
```

A provider can add any of the [supported privileges](#label-native-apps-privs-supported)
in the same manner.

## View the privileges requested by a Snowflake Native App

When a provider specifies a privilege in the manifest file, the privilege requests are
included as part of the installed Snowflake Native App. The consumer can view the privilege requests
after installing the app.

To view the global privileges required by an app, run the [SHOW PRIVILEGES](/sql-reference/sql/show-privileges)
command as shown in the following example:

Copy code

```
SHOW PRIVILEGES IN APPLICATION hello_snowflake_app;
```

## Grant privileges to an application

After determining the privileges required by a Snowflake Native App, the consumer must then grant
these privileges to the app.

To grant the global privilege request in the example above, the consumer runs the
[GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command as shown in the following example:

Copy code

```
GRANT CREATE DATABASE ON ACCOUNT TO APPLICATION hello_snowflake_app;
```

To grant the IMPORT privilege on the MYDATABASE database, run the following command:

Copy code

```
GRANT IMPORTED PRIVILEGES ON DATABASE MYDATABASE TO APPLICATION hello_snowflake_app;
```
