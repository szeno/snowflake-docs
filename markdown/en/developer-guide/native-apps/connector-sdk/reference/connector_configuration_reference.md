# Connector configuration reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## Database objects and procedures

The following database objects are created through the file `configuration/connector_configuration.sql`.

### PUBLIC.CONFIGURE\_CONNECTOR (config VARIANT)

Entry point procedure available to the `ADMIN` role. This procedure invokes the Java function [ConfigureConnectorHandler.configureConnector](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connector/ConfigureConnectorHandler.html#configureConnector(com.snowflake.snowpark_java.Session,com.snowflake.snowpark_java.types.Variant)).

### PUBLIC.CONFIGURE\_CONNECTOR\_VALIDATE (config VARIANT)

Procedure used for connector specific validation of the configuration. By default, it returns `'response_code': 'OK'`.
It is invoked by the `DefaultConfigureConnectorInputValidator` function. Can be overwritten both in SQL and Java.

### PUBLIC.CONFIGURE\_CONNECTOR\_INTERNAL (config VARIANT)

Procedure used for connector specific additional configuration. By default, it returns `'response_code': 'OK'`.
It is invoked by the `InternalConfigureConnectorCallback`. Can be overwritten both in SQL and Java.

## Related tables and views

Connector configuration is related to and dependent on the objects from the following files:

- `core.sql` (See [Core SQL reference](/developer-guide/native-apps/connector-sdk/reference/core_reference))
- `configuration/app_config.sql` (See: [App config SQL reference](/developer-guide/native-apps/connector-sdk/reference/app_config_reference))

## Related Java objects

The following Java objects from the `com.snowflake.connectors.application.configuration.connector` package and some common components are tightly connected with the above procedures:

- [ConfigureConnectorHandler](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connector/ConfigureConnectorHandler.html)
- [ConfigureConnectorInputValidator](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connector/ConfigureConnectorInputValidator.html)
- [ConfigureConnectorCallback](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connector/ConfigureConnectorCallback.html)
- [ConnectorConfigurationService](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connector/ConnectorConfigurationService.html)
- [ConfigureConnectorHandlerBuilder](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connector/ConfigureConnectorHandlerBuilder.html)
- [ConnectorErrorHelper](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/common/exception/helper/ConnectorErrorHelper.html)

## Custom handler

Handler and its internals can be customized using the following two approaches.

### Procedure replacement approach

The following components can be replaced using SQL.

#### Handler

To provide whole custom implementation of the [ConfigureConnectorHandler](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connector/ConfigureConnectorHandler.html) the [PUBLIC.CONFIGURE\_CONNECTOR](#label-connectors-native-sdk-configure-connector) procedure must be replaced. For example:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.CONFIGURE_CONNECTOR(config VARIANT)
RETURNS VARIANT
LANGUAGE JAVA
RUNTIME_VERSION = '11'
PACKAGES = ('com.snowflake:snowpark:1.11.0')
IMPORTS = ('/connectors-native-sdk.jar')
HANDLER = 'com.custom.handler.CustomConfigureConnectorHandler.configureConnector';

GRANT USAGE ON PROCEDURE PUBLIC.CONFIGURE_CONNECTOR(VARIANT) TO APPLICATION ROLE ADMIN;
```

#### Internal procedures

Internal `VALIDATE` and `INTERNAL` procedures can be also customized through the SQL. They can even invoke another Java handler:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.CONFIGURE_CONNECTOR_INTERNAL(config VARIANT)
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

CREATE OR REPLACE PROCEDURE PUBLIC.CONFIGURE_CONNECTOR_VALIDATE(config VARIANT)
    RETURNS VARIANT
    LANGUAGE JAVA
    RUNTIME_VERSION = '11'
    PACKAGES = ('com.snowflake:snowpark:1.11.0')
    IMPORTS = ('/connectors-native-sdk.jar')
    HANDLER = 'com.custom.handler.CustomConfigureConnectorInternalHandler.configureConnector';
```

### Builder approach

[ConfigureConnectorHandler](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connector/ConfigureConnectorHandler.html) can be customized using [ConfigureConnectorHandlerBuilder](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connector/ConfigureConnectorHandlerBuilder.html). This builder allows user to provide custom implementations of the following interfaces:

- [ConfigureConnectorInputValidator](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connector/ConfigureConnectorInputValidator.html)
- [ConfigureConnectorCallback](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connector/ConfigureConnectorCallback.html)
- [ConnectorErrorHelper](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/common/exception/helper/ConnectorErrorHelper.html)

In case one of them is not provided the default implementation provided by the SDK will be used.

Copy code

```
class CustomConfigureConnectorInputValidator implements ConfigureConnectorInputValidator {
    @Override
    public ConnectorResponse validate(Variant config) {
        // CUSTOM LOGIC
        return ConnectorResponse.success();
    }
}

class CustomHandler {

    // Path to this method needs to be specified in the PUBLIC.CONFIGURE_CONNECTOR procedure using SQL
    public static Variant configureConnector(Session session, Variant configuration) {
            //Using builder
        var handler = ConfigureConnectorHandler.builder(session)
            .withInputValidator(new CustomConfigureConnectorInputValidator())
            .build();
        return handler.configureConnector(configuration).toVariant();
    }
}
```
