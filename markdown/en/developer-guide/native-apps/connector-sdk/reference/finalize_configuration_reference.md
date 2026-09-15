# Finalize configuration reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## Database objects and procedures

The following database objects are created through the file `configuration/finalize_configuration.sql`.

### PUBLIC.FINALIZE\_CONNECTOR\_CONFIGURATION (CUSTOM\_CONFIGURATION VARIANT)

Entry point procedure available to the `ADMIN` role. This procedure invokes the Java function `FinalizeConnectorHandler.finalizeConnectorConfiguration`.

### PUBLIC.FINALIZE\_CONNECTOR\_CONFIGURATION\_VALIDATE (CUSTOM\_CONFIGURATION VARIANT)

Procedure used for connector specific validation of the custom configuration. By default, it returns `'response_code': 'OK'`.
It is invoked by `DefaultFinalizeConnectorValidator`. Can be overwritten both in SQL and Java.

### PUBLIC.VALIDATE\_SOURCE (CUSTOM\_CONFIGURATION VARIANT)

Procedure checking the connection to the source system with additional configuration specific to the connector. In some cases
it might be the same as the `TEST_CONNECTION` procedure, but sometimes it will be performing checks in a more detailed way.
By default, it returns `'response_code': 'OK'`. It is invoked by `InternalSourceValidator`.

### PUBLIC.FINALIZE\_CONNECTOR\_CONFIGURATION\_INTERNAL (CUSTOM\_CONFIGURATION VARIANT)

Procedure used to perform any additional custom configurations. By default, it returns `'response_code': 'OK'`.
It is invoked by `InternalFinalizeConnectorCallback`. Can be overwritten both in SQL and Java.

## Related tables and views

Connector configuration is related to and dependent on the objects from the following files:

- `core.sql` (See [Core SQL reference](/developer-guide/native-apps/connector-sdk/reference/core_reference))
- `configuration/app_config.sql` (See: [App config SQL reference](/developer-guide/native-apps/connector-sdk/reference/app_config_reference))

## Related Java objects

The following Java objects are from the `com.snowflake.connectors.application.configuration.finalization` package and some common components are tightly connected with the above procedures:

- `FinalizeConnectorHandler`
- `FinalizeConnectorValidator`
- `SourceValidator`
- `FinalizeConnectorCallback`
- `ConnectorStatusService`
- `ConnectorErrorHandler`

## Custom handler

The handler and its internals can be customized using the following two approaches.

### Procedure replacement approach

The following components can be replaced using SQL.

#### Handler

To provide whole custom implementation of `FinalizeConnectorHandler` the `PUBLIC.FINALIZE_CONNECTOR_CONFIGURATION` procedure must be replaced. For example:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.FINALIZE_CONNECTOR_CONFIGURATION(CUSTOM_CONFIGURATION VARIANT)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/connectors-native-sdk.jar')
  HANDLER = 'com.custom.handler.CustomFinalizeConnectorHandler.finalizeConnectorConfiguration';

GRANT USAGE ON PROCEDURE PUBLIC.CONFIGURE_CONNECTOR(VARIANT) TO APPLICATION ROLE ADMIN;
```

#### Internal procedures

Internal `VALIDATE`, `INTERNAL` and `VALIDATE_SOURCE` procedures can be also customized through the SQL. They can even invoke another Java handler:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.FINALIZE_CONNECTOR_CONFIGURATION_INTERNAL(config VARIANT)
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

CREATE OR REPLACE PROCEDURE PUBLIC.FINALIZE_CONNECTOR_CONFIGURATION_VALIDATE (config VARIANT)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/connectors-native-sdk.jar')
  HANDLER = 'com.custom.handler.CustomFinalizeConnectorConfigurationValidateHandler.validate';
```

### Builder approach

`FinalizeConnectorHandler` can be customized using `FinalizeConnectorHandlerBuilder`. This builder allows the user to provide custom implementations of the following interfaces:

- `FinalizeConnectorValidator`
- `SourceValidator`
- `FinalizeConnectorCallback`
- `ConnectorErrorHelper`

In case one of them is not provided the default implementation provided by the SDK will be used.

Copy code

```
class CustomFinalizeConnectorValidator implements FinalizeConnectorValidator {
  @Override
  public ConnectorResponse validate(Variant config) {
    // CUSTOM LOGIC
    return ConnectorResponse.success();
  }
}

class CustomHandler {

  // Path to this method needs to be specified in the PUBLIC.FINALIZE_CONNECTOR_CONFIGURATION procedure using SQL
  public static Variant finalizeConnector(Session session, Variant configuration) {
    //Using builder
    var handler = FinalizeConnectorHandler.builder(session)
      .withValidator(new CustomFinalizeConnectorValidator())
      .build();
    return handler.finalizeConnector(configuration).toVariant();
  }
}
```
