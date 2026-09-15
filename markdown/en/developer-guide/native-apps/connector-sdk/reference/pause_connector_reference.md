# Pause connector reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## Database objects and procedures

The following database objects are created through the file `lifecycle/pause.sql`.

### PUBLIC.PAUSE\_CONNECTOR()

Entry point procedure available to the `ADMIN` role. This procedure invokes the Java function `PauseConnectorHandler.pauseConnector`.

### PUBLIC.PAUSE\_CONNECTOR\_VALIDATE()

Procedure used for connector specific validation of pausing process. By default, it returns `'response_code': 'OK'`.
It is invoked by `DefaultPauseConnectorStateValidator`. Can be overwritten both in SQL and Java.

### PUBLIC.PAUSE\_CONNECTOR\_INTERNAL()

Procedure used for connector specific additional pausing duties. By default, it returns `'response_code': 'OK'`.
It is invoked by `InternalPauseConnectorCallback`. Can be overwritten both in SQL and Java.

## Related tables and views

The pause connector is related to and dependent on the objects from the following files:

- `core.sql` (See [Core SQL reference](/developer-guide/native-apps/connector-sdk/reference/core_reference))
- `configuration/app_config.sql` (See: [App config SQL reference](/developer-guide/native-apps/connector-sdk/reference/app_config_reference))
- `configuration/finalize_configuration.sql` (See [Finalize configuration reference](/developer-guide/native-apps/connector-sdk/reference/finalize_configuration_reference))

## Related Java objects

The following Java objects from the `com.snowflake.connectors.application.lifecycle` package and some common components are tightly connected with the above procedures:

- `PauseConnectorHandler`
- `PauseConnectorStateValidator`
- `PauseConnectorCallback`
- `ConnectorStatusService`
- `LifecycleService`
- `ConnectorErrorHelper`

## Custom handler

The handler and its internals can be customized using the following two approaches.

### Procedure replacement approach

The following components can be replaced using SQL.

#### Handler

To provide whole custom implementation of `PauseConnectorHandler`, the `PUBLIC.PAUSE_CONNECTOR` procedure must be replaced. For example:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.PAUSE_CONNECTOR()
RETURNS VARIANT
LANGUAGE JAVA
RUNTIME_VERSION = '11'
PACKAGES = ('com.snowflake:snowpark:1.11.0')
IMPORTS = ('/connectors-native-sdk.jar')
HANDLER = 'com.custom.handler.CustomPauseConnectorHandler.pauseConnector';

GRANT USAGE ON PROCEDURE PUBLIC.PAUSE_CONNECTOR() TO APPLICATION ROLE ADMIN;
```

#### Internal procedures

Internal `VALIDATE` and `INTERNAL` procedures can be also customized through the SQL. They can also invoke another Java handler:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.PAUSE_CONNECTOR_INTERNAL()
RETURNS VARIANT
LANGUAGE SQL
EXECUTE AS OWNER
AS
BEGIN
    -- SOME CUSTOM LOGIC BEGIN
    SELECT sysdate();
    -- SOME CUSTOM LOGIC END

    RETURN OBJECT_CONSTRUCT('response_code', 'OK');
END;

CREATE OR REPLACE PROCEDURE PUBLIC.PAUSE_CONNECTOR_VALIDATE()
RETURNS VARIANT
LANGUAGE JAVA
RUNTIME_VERSION = '11'
PACKAGES = ('com.snowflake:snowpark:1.11.0')
IMPORTS = ('/connectors-native-sdk.jar')
HANDLER = 'com.custom.handler.CustomPauseConnectorInternalHandler.pauseConnector';
```

### Builder approach

`PauseConnectorHandler` can be customized using `PauseConnectorHandlerBuilder`. This builder allows user to provide custom implementations of the following interfaces:

- `PauseConnectorStateValidator`
- `PauseConnectorCallback`
- `ConnectorErrorHelper`

In case a function is not provided the default implementation provided by the SDK will be used.

Copy code

```
class CustomPauseConnectorStateValidator implements PauseConnectorStateValidator {
    @Override
    public ConnectorResponse validate() {
        // CUSTOM LOGIC
        return ConnectorResponse.success();
    }
}

class CustomHandler {

    // Path to this method needs to be specified in the PUBLIC.PAUSE_CONNECTOR procedure using SQL
    public static Variant pauseConnector(Session session) {
            //Using builder
        var handler = PauseConnectorHandlerBuilder.builder(session)
            .withStateValidator(new CustomPauseConnectorStateValidator())
            .build();
        return handler.pauseConnector().toVariant();
    }
}
```
