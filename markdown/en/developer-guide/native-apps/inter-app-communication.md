# Inter-app Communication

This topic describes how one Snowflake Native App can communicate with another Snowflake Native App
using inter-app communication (IAC).

## Inter-app Communication: Overview

Inter-app communication (IAC) allows a Snowflake Native App to provide additional
functionality to other Snowflake Native Apps in the same consumer account by providing access to objects
that other apps can use.

For example, a Snowflake Native App that resolves customer IDs can help other Snowflake Native Apps
enhance customer data by joining data sets from different vendors.

IAC provides the infrastructure for two or more independent apps to communicate
with each other while respecting their needs for management and security.
App developers enable IAC for their app by doing the following:

- Creating interfaces
- Using app roles to control access to the interfaces.
- Choosing synchronous or asynchronous interaction. Synchronous interaction uses
  stored procedures or functions that other apps can call directly,
  while asynchronous interaction provides access to request results that are stored in tables or views,
  which other apps can poll to check for results.

## Terminology

IAC uses the following terms:

Client
:   The app that initiates the connection request and uses the server app’s objects.

Server
:   The app that provides access to its objects using app roles.

Consumer
:   The user who installs the client and server apps.

Application configuration
:   A SQL object that the client app uses to request the name of the server app. IAC uses an application configuration of type `APPLICATION_NAME` to store the server app name.

Application specification
:   A SQL object that the client app creates to request a connection to the server app. IAC uses an application specification of type `CONNECTION`.
    For information about app specifications, see [Use app specifications to request controlled access](/developer-guide/native-apps/requesting-app-specs).

## Workflow for Inter-app communication

Establishing and using a connection involves a handshake process between the client app and the server app.

1. **Obtain app role names from the server app provider**: The client app provider coordinates with the server app provider outside of Snowflake to determine which server app roles to request in the connection specification.
2. [Identify the target app](#label-native-apps-iac-identify-target-app): The client app creates a configuration definition object to request the name of the server app. The consumer detects incoming requests, and provides the server app name to the client app through the configuration object.
3. [Request and approve a connection](#label-native-apps-iac-request-and-approve-connection): The client app creates an application specification to request a connection to the server app, and the consumer approves the connection request.
4. [Communicate with the Server App](#label-native-apps-iac-communicate-with-server-app): The client app calls the server app’s procedures or functions.

### Identify the target app

Before a client app can communicate with a server app, it must first identify the exact name of the app. Because the consumer can choose a custom name for an app during installation, the client app must first identify the exact name of the server app.

The client app’s setup script creates a `CONFIGURATION DEFINITION` object to request this information.

The following example shows how the client app’s setup script creates a `CONFIGURATION DEFINITION` object to request the name of the server app:

Copy code

```
ALTER APPLICATION
  SET CONFIGURATION DEFINITION my_server_app_name_configuration
    TYPE = APPLICATION_NAME
    LABEL = 'Server App'
    DESCRIPTION = 'Request for an app that will provide access to server procedures and functions. The server app version must be greater than or equal to 3.2.'
    APPLICATION_ROLES = (my_server_app_role);
```

The following example shows how the consumer checks for incoming configuration definition requests:

Copy code

```
SHOW CONFIGURATIONS IN APPLICATION my_server_app_name;
```

This command returns results similar to the following:

```
name                             | created_on              | updated_on              | type               | ...
my_server_app_name_configuration | 2026-02-09 10:00:00.000 | 2026-02-09 10:00:00.000 | APPLICATION_NAME   | ...
```

The consumer then uses the following command to provide the server app name:

Copy code

```
ALTER APPLICATION my_client_app_name
  SET CONFIGURATION my_server_app_name_configuration
  VALUE = MY_SERVER_APP_NAME;
```

### Request and approve a connection

Once the client app has the name of the server app, it creates an `APPLICATION SPECIFICATION` to request a connection to the server app. Note that the application role names are obtained through offline communication outside of snowflake.

The following example shows how to create an `APPLICATION SPECIFICATION` for a connection to the server app named `my_server_app_name`:

Copy code

```
ALTER APPLICATION SET SPECIFICATION my_server_app_name_connection_specification
  TYPE = CONNECTION
  LABEL = 'Server App'
  DESCRIPTION = 'Request for an app that will provide access to server procedures and functions. The server app version must be greater than or equal to 3.2.'
  SERVER_APPLICATION = MY_SERVER_APP_NAME -- server name obtained from Step 1
  SERVER_APPLICATION_ROLES = (my_server_app_role);
```

By creating the application specification, the client app is requesting to be granted the server app roles specified in the app specification.

Note

The values given for `LABEL` and `DESCRIPTION` in the app specification must match the values given for `LABEL` and `DESCRIPTION` in the `CONFIGURATION DEFINITION` object created in Step 1. If the values do not match, the connection won’t display properly in Snowsight.

To create an efficient connection workflow, we recommend that the client app create the application specification in the [before\_configuration\_change](/developer-guide/native-apps/callbacks#label-native-apps-configuration-callbacks-before-configuration-change) synchronous callback. This callback is run when the `ALTER APPLICATION SET CONFIGURATION VALUE` command is run. For information about callbacks, see [Callbacks](#label-native-apps-iac-callbacks). For an example setup script that creates the application specification in the [before\_configuration\_change](/developer-guide/native-apps/callbacks#label-native-apps-configuration-callbacks-before-configuration-change) synchronous callback, see [Examples](#label-native-apps-iac-examples).

Once the client app has created the app specification, the consumer can review and approve or refuse the connection request.

#### Approving the connection request using SQL

The following example shows how the consumer approves the connection request using SQL:

Copy code

```
ALTER APPLICATION my_server_app_name
  APPROVE SPECIFICATION my_server_app_name_connection_specification
  SEQUENCE_NUMBER = 1;
```

#### Approving the connection request using Snowsight

To view and approve connection requests in Snowsight, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Select the app. A section titled **Application connections** appears under **Configurations**. Each pending connection shows the name or label for the connection, a brief description of the connection, and a **Review** button.
3. Click the **Review** button. The details of the connection request appear.
4. Select the target app from **Select from your apps**.
5. Click **Next**. The following information appears:

   - A diagram showing that the client app will connect to the server app, and what roles the apps will use.
   - The details of the connection.
   - A subset of the server permissions that will be granted to the client app. For information about security considerations for IAC, see [Security considerations](#label-native-apps-iac-security-considerations).
   - An **Approve Connection** toggle switch. The switch is set to **On**.
6. To approve the connection, leave the toggle switch set to **On**, and click **Save**. The updated connection list appears showing the status of the connection.
7. To refuse the connection, switch the toggle switch to **Off**.
8. To exit the review page without approving or refusing the connection, click the **Cancel** button.

#### Post-approval

When the consumer approves the connection request, the Snowflake Native App Framework grants the requested server app roles to the client app. The approval
also grants USAGE on the client app to the server app. This allows the server app to be aware of what client apps are connected to it.

When the consumer approves the connection request, the following callbacks are triggered in the client and server apps, respectively:

- [after\_server\_connection\_change](/developer-guide/native-apps/callbacks#label-native-apps-connection-callbacks-after-server-connection-change) is triggered in the client app
- [after\_client\_connection\_change](/developer-guide/native-apps/callbacks#label-native-apps-connection-callbacks-after-client-connection-change) is triggered in the server app

These callbacks allow the server and client apps to perform additional actions when the connection is established.

For more information about approving application specifications, see the following topics:

- [ALTER APPLICATION … { APPROVE | DECLINE} SPECIFICATION](/sql-reference/sql/alter-application-sequence-number)
- [Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec)

### Communicate with the server app

Once the connection is established and the client app is granted the requested server app roles, the client app can communicate with the server app.

Note

Before calling server app methods, the client app should retrieve the server app’s name at runtime from the approved application specification, to ensure it uses the correct name in case the server app is renamed. The following example shows how to retrieve the server app’s name at runtime:

Copy code

```
SHOW APPROVED SPECIFICATIONS ->>
  SELECT PARSE_JSON("definition"):"SERVER_APPLICATION"::STRING
  FROM $1
  WHERE "name" = 'MY_SERVER_APP_NAME_CONNECTION_SPECIFICATION';
```

The client app can communicate with the server app synchronously or asynchronously.

- Synchronous communication involves invoking the server app’s procedures or functions directly.
- Asynchronous communication involves using a queue stored in a data object, such as a table. For
  example, the server app can provide a procedure to insert records into a table as requests, which the server app then processes periodically. The client app can then use a different server-provided procedure to check the table for results.

The following example of a synchronous operation shows a client app calling a server app’s procedure using Python:

Copy code

```
session.call("server_app_name.customer_schema.get_customer_data", customer_id);
```

The following example of an asynchronous operation shows a client app calling a server app’s procedure using Python. The client app calls the server app’s procedure, which creates a request in a table, which the server app then processes. The client app can poll the table to check for updated records for results.

Copy code

```
session.call("server_app_name.customer_schema.request_customer_data_async", customer_id);
```

The client app can then poll the table to check for updated records for results:

Copy code

```
session.call("server_app_name.customer_schema.check_customer_data_requests_async", customer_id);
```

## Managing connections

To view existing connections in Snowsight, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select the app. All app connections are shown in a section titled **Configurations**. Below that section, there is a sub-section titled **Application connections**.
4. To modify a connection, click the pencil icon for the connection. You can change the following:

   - Which app is connected to the app
   - The approval status of the connection
5. To view the connected app, click the **View app** button.
6. To change security settings for the connection, click the gear icon.

## Security considerations

When approving a specification request, consumers should be aware that granting server app access to a client app can elevate the privileges the client app has. For example, if a server app has external access, the client app might gain indirect access to the Internet or other external resources through the server app. If the
server app is a client app of another server app, the client app may be able to access the resources of the other
server app through the first server app.

Consumers should inspect the capabilities and privileges of the server app before approving a connection.
Use an admin role (for example, `ACCOUNTADMIN`) to inspect the capabilities of the server.
Inspecting the server with a lower privileged role won’t reveal all of the server’s capabilities and privileges.
Consumers should note that the server app code is not visible to the consumer, and the server app permissions and capabilities can be changed after the consumer approves the connection.

Example SQL commands to inspect the capabilities and privileges of the server app include, but are not limited to the following:

- [SHOW GRANTS TO APPLICATION](/sql-reference/sql/show-grants): This command lists what grants on the client app have
  been granted to the server app.
- [SHOW PRIVILEGES IN APPLICATION](/sql-reference/sql/show-privileges): This command lists what
  potential account-level privileges could be granted to the client app.
- [SHOW REFERENCES IN APPLICATION](/sql-reference/sql/show-references): This command lists
  references that the client app could potentially use without using grants.
- [SHOW SPECIFICATIONS IN APPLICATION](/sql-reference/sql/show-specifications): This command lists the application
  specifications that the consumer has approved, including external access integrations (EAIs),
  security integrations, shares, listings, and connections.

## SQL Reference

The following SQL commands are used to manage inter-app communication.

- [ALTER APPLICATION SET SPECIFICATION](/sql-reference/sql/alter-application-set-app-spec): Creates an app specification that the server app uses to grant access to its objects to the client app.
- [ALTER APPLICATION DROP SPECIFICATION](/sql-reference/sql/alter-application-drop-app-spec): Deletes an app specification.
- [ALTER APPLICATION … { APPROVE | DECLINE} SPECIFICATION](/sql-reference/sql/alter-application-sequence-number): Approves or refuses an app specification request.
- [SHOW SPECIFICATIONS](/sql-reference/sql/show-specifications): Lists all of the application specifications in an app.
- [DESCRIBE SPECIFICATION](/sql-reference/sql/desc-specification): Describes the app specifications for an app.
- [ALTER APPLICATION SET CONFIGURATION DEFINITION](/sql-reference/sql/alter-application-set-configuration-definition): Creates or updates an application configuration (a key-value pair) that requests the name of another application from the consumer.
- [ALTER APPLICATION DROP CONFIGURATION DEFINITION](/sql-reference/sql/alter-application-drop-configuration-definition): Deletes an application configuration.
- [ALTER APPLICATION SET CONFIGURATION VALUE](/sql-reference/sql/alter-application-set-configuration-value): Sets a value in an application configuration.
- [ALTER APPLICATION UNSET CONFIGURATION](/sql-reference/sql/alter-application-unset-configuration): Unsets the value to the specified application configuration.
- [SHOW CONFIGURATIONS](/sql-reference/sql/show-configurations): Lists all of the application configurations in an app.
- [DESCRIBE CONFIGURATION](/sql-reference/sql/desc-configuration): Describes the details of an application configuration.
- [IS\_CONFIGURATION\_SET (SYS\_CONTEXT function)](/sql-reference/functions/is_configuration_set): Returns whether or not the configuration has a value set.
- [GET\_CONFIGURATION\_VALUE (SYS\_CONTEXT function)](/sql-reference/functions/get_configuration_value): Returns the current value of the configuration.
- [SHOW GRANTS TO APPLICATION](/sql-reference/sql/show-grants): Lists all the privileges and database/application roles granted to the specified app.
- [SHOW GRANTS TO APPLICATION ROLE](/sql-reference/sql/show-grants): Lists all the permissions that the application role has.
- [SHOW GRANTS OF APPLICATION ROLE](/sql-reference/sql/show-grants): Lists all the roles and applications to whom the specified application role is granted.

## Callbacks

The Snowflake Native App Framework provides lifecycle callbacks to help manage the inter-app communication
workflow. These callbacks let an app react to changes in configurations, connections,
and specifications. To use callbacks, register them in the `lifecycle_callbacks`
section of the app’s manifest file.

For general information about callbacks, see [Callbacks](/developer-guide/native-apps/callbacks).

### Configuration callbacks

These callbacks are triggered when a configuration value is set or unset. A common use
case is to use the [before\_configuration\_change](/developer-guide/native-apps/callbacks#label-native-apps-configuration-callbacks-before-configuration-change)
callback to automatically create a connection specification when the consumer provides
the server app name.

[validate\_configuration\_change](/developer-guide/native-apps/callbacks#label-native-apps-configuration-callbacks-validate-configuration-change)
:   A synchronous callback called as part of the `ALTER APPLICATION SET CONFIGURATION VALUE`
    command. Lets the app perform custom validation on the provided value. If the callback
    returns an error, the command fails and the new value is not set.

[before\_configuration\_change](/developer-guide/native-apps/callbacks#label-native-apps-configuration-callbacks-before-configuration-change)
:   A synchronous callback called as part of the `ALTER APPLICATION SET CONFIGURATION VALUE`
    and `ALTER APPLICATION UNSET CONFIGURATION` commands. Lets the app perform operations
    based on the configuration value before it is saved.

[after\_configuration\_change](/developer-guide/native-apps/callbacks#label-native-apps-configuration-callbacks-after-configuration-change)
:   An asynchronous callback called after the `ALTER APPLICATION SET CONFIGURATION VALUE`
    or `ALTER APPLICATION UNSET CONFIGURATION` commands complete. Lets the app react to
    the change, for example for notification or tracking purposes.

### Connection callbacks

These callbacks are triggered when a connection’s status changes, such as when a
connection is established, refused, dropped, or when the connected app is deleted.

[after\_server\_connection\_change](/developer-guide/native-apps/callbacks#label-native-apps-connection-callbacks-after-server-connection-change)
:   An asynchronous callback triggered in the client app by any operation that impacts
    the connection state, including approving, refusing, or dropping a specification,
    or dropping the server app.

[after\_client\_connection\_change](/developer-guide/native-apps/callbacks#label-native-apps-connection-callbacks-after-client-connection-change)
:   An asynchronous callback triggered in the server app by any operation that impacts
    the connection state, including approving, refusing, or dropping a specification,
    or dropping the client app.

[after\_server\_version\_change](/developer-guide/native-apps/callbacks#label-native-apps-connection-callbacks-after-server-version-change)
:   An asynchronous callback called in the client app after the server app’s version or
    patch number changes. Lets the client app react to an upgrade or downgrade.

## Examples

The following examples show how to configure an app to use inter-app communication.

- [Example: Setup script and manifest files](#label-native-apps-iac-examples-setup-script-and-manifest-files)
- [Example: Asynchronous communication between apps](#label-native-apps-iac-examples-asynchronous-communication-between-apps)

### Example: Setup script and manifest files

The following example shows a client app’s setup script (`setup.sql`):

Copy code

```
CREATE OR ALTER VERSIONED SCHEMA app_schema;

-- create a callback that creates the connection request before the config value of the server name is saved
CREATE OR REPLACE PROCEDURE app_schema.before_config_change_callback(config_name STRING, config_value STRING)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    spec_name VARCHAR;
    existing_target VARCHAR;
BEGIN
    IF (config_value IS NOT NULL AND config_name = 'MY_SERVER_APP_NAME_CONFIGURATION') THEN
        SHOW SPECIFICATIONS;
        SELECT PARSE_JSON("definition"):SERVER_APPLICATION::STRING
            INTO existing_target
            FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));

        IF(existing_target IS NOT NULL AND UPPER(existing_target) != UPPER(config_value)) THEN
            EXECUTE IMMEDIATE 'ALTER APPLICATION DROP SPECIFICATION CONNECTION_' || UPPER(existing_target);
        END IF;

        spec_name := 'CONNECTION_' || UPPER(config_value);
        EXECUTE IMMEDIATE
        'ALTER APPLICATION SET SPECIFICATION ' || spec_name || '
            TYPE = CONNECTION
            LABEL = ''Server App''
            DESCRIPTION = ''Request for an app that will provide access to server procedures and functions. The server app version must be greater than or equal to 3.2.''
            SERVER_APPLICATION = ' || config_value || '
            SERVER_APPLICATION_ROLES = (my_server_app_role)';
    END IF;
RETURN 'success';
END;
$$;

CREATE APPLICATION ROLE IF NOT EXISTS client_app_user;
GRANT USAGE ON SCHEMA app_schema TO APPLICATION ROLE client_app_user;
ALTER APPLICATION SET CONFIGURATION DEFINITION my_server_app_name_configuration
    TYPE = APPLICATION_NAME
    LABEL = 'Server App'
    DESCRIPTION = 'Request for an application that will provide access to server procedures and functions. The server app version must be greater than or equal to 3.2'
    APPLICATION_ROLES = (client_app_user);
```

The following example shows a client app’s manifest file (`manifest.yml`):

Copy code

```
manifest_version: 2

artifacts:
  setup_script: setup.sql

lifecycle_callbacks:
    before_configuration_change: app_schema.before_config_change_callback
```

Note the following about the preceding code example:

- In the [before\_configuration\_change](/developer-guide/native-apps/callbacks#label-native-apps-configuration-callbacks-before-configuration-change) callback, the app checks for an existing connection
  specification matching the configuration’s previous value, and drops it if it exists. The callback
  then creates a new connection specification for the newly provided server app name. Creating a new connection when the server name is set prevents duplicate connection specifications from being created.

### Example: Asynchronous communication between apps

The following example shows how to create procedures in a server app’s setup script (`setup.sql`) for asynchronous communication. The server app creates a processing queue table, and provides two procedures to client apps through an app role: `submit_request` to add a request to the queue and `fetch_response` to retrieve the result of a completed request. The server app periodically uses the `process_requests` procedure to process all pending requests.

Copy code

```
CREATE TABLE IF NOT EXISTS app_schema.processing_queue (
  request_id NUMBER AUTOINCREMENT,
  operation STRING,
  input STRING,
  status STRING DEFAULT 'PENDING',
  response STRING DEFAULT ''
);

CREATE OR REPLACE PROCEDURE app_schema.submit_request(operation STRING, input STRING)
RETURNS STRING
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
BEGIN
    INSERT INTO app_schema.processing_queue (operation, input) VALUES (:operation, :input);
    RETURN 'Request submitted successfully';
END;
$$;

CREATE OR REPLACE PROCEDURE app_schema.process_requests()
RETURNS STRING
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
DECLARE
    -- Cursor to find all PENDING requests
    c1 CURSOR FOR SELECT * FROM app_schema.processing_queue WHERE status = 'PENDING';
    result STRING;
BEGIN
    FOR request IN c1 DO

        IF (request.operation = 'OPERATION_X') THEN
            -- assuming there is a UDF func_x(input) to perform operation_x
            result := (SELECT func_x(:request.input));
        END IF;

        -- update the processing queue with the result
        LET stmt STRING :=
            'UPDATE app_schema.processing_queue SET status = 'DONE', response = ' ||
            result ||
            ' WHERE request_id = ' ||
            request.request_id;
        EXECUTE IMMEDIATE (:stmt);

    END FOR;

    RETURN 'Processed pending requests.';
END;
$$;

CREATE OR REPLACE PROCEDURE app_schema.fetch_response(operation STRING, input STRING)
RETURNS STRING
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
BEGIN
    LET res STRING := (SELECT response FROM app_schema.processing_queue WHERE operation = :operation AND input = :input);
    RETURN res;
END;
$$;

CREATE APPLICATION ROLE IF NOT EXISTS my_server_app_role;
GRANT USAGE ON SCHEMA app_schema TO APPLICATION ROLE my_server_app_role;
GRANT USAGE ON PROCEDURE app_schema.submit_request(string, string) TO APPLICATION ROLE my_server_app_role;
GRANT USAGE ON PROCEDURE app_schema.process_requests() TO APPLICATION ROLE my_server_app_role;
GRANT USAGE ON PROCEDURE app_schema.fetch_response(string, string) TO APPLICATION ROLE my_server_app_role;
```
