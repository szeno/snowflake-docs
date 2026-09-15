# Reset configuration reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

Details about objects and procedures associated with the reset configuration feature.

## Database objects and procedures

The following database objects are created using the `configuration/reset_configuration.sql`.

### PUBLIC.RESET\_CONFIGURATION()

Entry point procedure available to the `ADMIN` role. This procedure invokes the Java `ResetConfigurationHandler.resetConfiguration` handler.

### PUBLIC.RESET\_CONFIGURATION\_VALIDATE()

Used to provide additional connector specific validation. By default returns `'response_code': 'OK'`.
It is invoked by the default `ResetConfigurationValidator`. Can be overwritten both in SQL and Java.

### PUBLIC.RESET\_CONFIGURATION\_INTERNAL()

Used to provide additional connector specific logic. By default returns `'response_code': 'OK'`.
It is invoked by the default `ResetConfigurationCallback`. Can be overwritten both in SQL and Java.

## Related tables and views

Configuration reset is related to and dependent on the objects from the following files:

- `core.sql` (See [Core SQL reference](/developer-guide/native-apps/connector-sdk/reference/core_reference))
- `prerequisites.sql` (See [Prerequisites SQL Reference](/developer-guide/native-apps/connector-sdk/reference/prerequisites_reference))
- `configuration/app_config.sql` (See: [App config SQL reference](/developer-guide/native-apps/connector-sdk/reference/app_config_reference))
- `configuration/connector_configuration.sql` (See: [Connector configuration reference](/developer-guide/native-apps/connector-sdk/reference/connector_configuration_reference))

## Related Java objects

The following Java objects from the `com.snowflake.connectors.application.configuration.reset` package and some common components are tightly connected with the above procedures:

- `ResetConfigurationHandler`
- `ResetConfigurationValidator`
- `ResetConfigurationCallback`
- `ResetConfigurationSdkCallback`
- `ResetConfigurationHandlerBuilder`
- `ConnectorStatusService`
- `ConfigurationRepository`
- `PrerequisitesRepository`
- `TransactionManager`
- `ConnectorErrorHandler`

## Custom handler

Handlers can be customized by being completely replaced using SQL or by implementing Java interfaces.

### Replacing using SQL

The following components can be replaced using SQL.

#### Handler

To provide a custom implementation of `ResetConfigurationHandler` the `PUBLIC.RESET_CONFIGURATION` procedure must be replaced. For example:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.RESET_CONFIGURATION()
RETURNS VARIANT
LANGUAGE JAVA
RUNTIME_VERSION = '11'
PACKAGES = ('com.snowflake:snowpark:1.11.0')
IMPORTS = ('/connectors-native-sdk.jar')
HANDLER = 'com.snowflake.connectors.application.configuration.reset.CustomResetConfigurationHandler.resetConfiguration';

GRANT USAGE ON PROCEDURE PUBLIC.RESET_CONFIGURATION() TO APPLICATION ROLE ADMIN;
```

#### Internal procedure

The `INTERNAL` procedure can also be customized through SQL.

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.RESET_CONFIGURATION_INTERNAL()
    RETURNS VARIANT
LANGUAGE SQL
EXECUTE AS OWNER
AS
BEGIN
    -- SOME CUSTOM LOGIC

    RETURN OBJECT_CONSTRUCT('response_code', 'OK');
END;
```

It can also invoke another Java handler:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.RESET_CONFIGURATION_INTERNAL()
RETURNS VARIANT
LANGUAGE JAVA
RUNTIME_VERSION = '11'
PACKAGES = ('com.snowflake:snowpark:1.11.0')
IMPORTS = ('/connectors-native-sdk.jar')
HANDLER = 'com.snowflake.connectors.application.configuration.reset.CustomResetConfigurationCallback.resetConfiguration';
```

### Builder approach

`ResetConfigurationHandler` can be customized using `ResetConfigurationHandlerBuilder`. This builder allows the developer to provide custom implementations of the following interfaces:

- `ResetConfigurationValidator`
- `ResetConfigurationCallback`
- `ConnectorErrorHelper`

Not all interfaces need to be implemented, in which case the default implementation provided by the SDK is used.

The following example shows how `ResetConfigurationValidator` can be customized.

Copy code

```
class CustomResetConfigurationValidator implements ResetConfigurationValidator {

    @Override
    public ConnectorResponse validate() {
        // CUSTOM VALIDATION LOGIC
        return ConnectorResponse.success();
    }
}

class CustomHandler {

    // Path to this method needs to be specified in the SQL definition of the PUBLIC.RESET_CONFIGURATION procedure
    public static Variant resetConfiguration(Session session) {
        // Using the builder
        var handler = ResetConfigurationHandler.builder(session)
            .withValidator(new CustomResetConfigurationValidator())
            .build();
        return handler.resetConfiguration().toVariant();
    }
}
```
