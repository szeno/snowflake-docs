# Connection configuration reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## Database objects and procedures

The following database objects are created through the file `configuration/connection_configuration.sql`.

### PUBLIC.SET\_CONNECTION\_CONFIGURATION (connection\_configuration VARIANT)

Entry point procedure available to `ADMIN` role. This procedure invokes the Java function [ConnectionConfigurationHandler.setConnectionConfiguration()](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connection/ConnectionConfigurationHandler.html#setConnectionConfiguration(com.snowflake.snowpark_java.Session,com.snowflake.snowpark_java.types.Variant)).

### PUBLIC.SET\_CONNECTION\_CONFIGURATION\_VALIDATE (connection\_configuration VARIANT)

Procedure used for Connector specific validation of the configuration. It can also be used to transform some parts of the configuration.
Transformed configuration needs to be returned as additional `"config"` property. By default, it returns `'response_code': 'OK'`.
It is invoked by the `DefaultConnectionConfigurationInputValidator`. Can be overwritten both in SQL and Java.

### PUBLIC.SET\_CONNECTION\_CONFIGURATION\_INTERNAL (connection\_configuration VARIANT)

Procedure used for Connector specific additional connection configuration, for example adding external access integration to other procedures.
By default, it returns `'response_code': 'OK'`. It is invoked by the `InternalConnectionConfigurationCallback`. Can be overwritten both in SQL and Java.

### PUBLIC.GET\_CONNECTION\_CONFIGURATION()

A procedure to retrieve current connection configuration from the internal table. It is available to `ADMIN` and `VIEWER` users.

## Related tables and views

Connector configuration is related to and dependent on the objects from the following files:

- `core.sql` (See [Core SQL reference](/developer-guide/native-apps/connector-sdk/reference/core_reference))
- `configuration/app_config.sql` (See: [App config SQL reference](/developer-guide/native-apps/connector-sdk/reference/app_config_reference))

### PUBLIC.TEST\_CONNECTION()

This procedure is not provided by default in any file, but is necessary for the `Connection Configuration` feature.
This procedure will be used as a light weight way to check access to the external source system.

## Related Java objects

The following Java objects from the [com.snowflake.connectors.application.configuration.connector](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/package-summary.html) package and some common components are tightly connected with the above procedures:

- [ConnectionConfigurationHandler](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connection/ConnectionConfigurationHandler.html)
- [ConnectionConfigurationInputValidator](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connection/ConnectionConfigurationInputValidator.html)
- [ConnectionValidator](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connection/ConnectionValidator.html)
- [ConnectorConfigurationService](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connector/ConnectorConfigurationService.html)
- [ConnectionConfigurationHandlerBuilder](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connection/ConnectionConfigurationHandlerBuilder.html)
- [ConnectorErrorHelper](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/common/exception/helper/ConnectorErrorHelper.html)

## Custom handler

Handler and its internals can be customized using the following two approaches.

### Procedure replacement approach

The following components can be replaced using SQL.

#### Handler

To provide whole custom implementation of the [ConnectionConfigurationHandler](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connection/ConnectionConfigurationHandler.html) the [PUBLIC.SET\_CONNECTION\_CONFIGURATION](#label-connectors-native-sdk-set-connection-configuration) procedure must be replaced. For example:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.SET_CONNECTION_CONFIGURATION(config VARIANT)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/connectors-native-sdk.jar')
  HANDLER = 'com.custom.handler.CustomConnectionConfigurationHandler.setConnectionConfiguration';

GRANT USAGE ON PROCEDURE PUBLIC.CONFIGURE_CONNECTOR(VARIANT) TO APPLICATION ROLE ADMIN;
```

#### Internal procedures

Internal `VALIDATE` and `INTERNAL` procedures can be also customized through the SQL. They can even invoke another Java handler:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.SET_CONNECTION_CONFIGURATION_INTERNAL(config VARIANT)
  RETURNS VARIANT
  LANGUAGE SQL
  EXECUTE AS OWNER
  AS
  BEGIN
    -- SOME CUSTOM LOGIC BEGIN
    SELECT sysdate();
    -- SOME CUSTOM LOGIC END

    RETURN OBJECT_CONSTRUCT('response_code', 'OK', '"config"', '"transformed config variant"');
  END;

CREATE OR REPLACE PROCEDURE PUBLIC.SET_CONNECTION_CONFIGURATION_VALIDATE(config VARIANT)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/connectors-native-sdk.jar')
  HANDLER = 'com.custom.handler.CustomConnectionConfigurationValidateHandler.setConnectionConfiguration';
```

### Builder approach

[ConnectionConfigurationHandler](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connection/ConnectionConfigurationHandler.html) can be customized using [ConnectionConfigurationHandlerBuilder](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connection/ConnectionConfigurationHandlerBuilder.html). This builder allows user to provide custom implementations of the following interfaces:

- [ConnectionConfigurationInputValidator](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connection/ConnectionConfigurationInputValidator.html)
- [ConnectionConfigurationCallback](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connection/ConnectionConfigurationCallback.html)
- [ConnectionValidator](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/configuration/connection/ConnectionValidator.html)
- [ConnectorErrorHelper](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/common/exception/helper/ConnectorErrorHelper.html)

In case one of them is not provided the default implementation provided by the SDK will be used.

Copy code

```
class CustomConnectionConfigurationInputValidator implements ConnectionConfigurationInputValidator {
  @Override
  public ConnectorResponse validate(Variant config) {
    // CUSTOM LOGIC
    return ConnectorResponse.success();
  }
}

class CustomHandler {

  // Path to this method needs to be specified in the PUBLIC.SET_CONNECTION_CONFIGURATION procedure using SQL
  public static Variant configureConnection(Session session, Variant configuration) {
    //Using builder
    var handler = ConnectionConfigurationHandler.builder(session)
      .withInputValidator(new CustomConnectionConfigurationInputValidator())
      .build();
    return handler.connectionConfiguration(configuration).toVariant();
  }
}
```
