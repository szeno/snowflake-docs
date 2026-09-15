# Update connection configuration reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## Database objects and procedures

The following database objects are created through the `configuration/update_connection_configuration.sql`

### PUBLIC.UPDATE\_CONNECTION\_CONFIGURATION( connection\_configuration VARIANT)

Entry point procedure available to the `ADMIN` role. This procedure invokes the Java `UpdateConnectionConfigurationHandler.updateConnectionConfiguration` handler.

### PUBLIC.UPDATE\_CONNECTION\_CONFIGURATION\_VALIDATE( connection\_configuration VARIANT)

Procedure used for providing additional connector specific validation logic. By default, it returns `'response_code': 'OK'`.
It is invoked by the default `ConnectionConfigurationInputValidator`. Can be overwritten both in SQL and Java.

### PUBLIC.DRAFT\_CONNECTION\_CONFIGURATION\_INTERNAL( connection\_configuration VARIANT)

Procedure used for providing additional connector specific logic. By default, it returns `'response_code': 'OK'`.
It is invoked by the default `ConnectionConfigurationCallback`. Can be overwritten both in SQL and Java.

## Related tables and views

Connection configuration update is related to and dependent on the objects from the following files:

- `core.sql` (See [Core SQL reference](/developer-guide/native-apps/connector-sdk/reference/core_reference))
- `configuration/app_config.sql` (See: [App config SQL reference](/developer-guide/native-apps/connector-sdk/reference/app_config_reference))
- `configuration/connection_configuration.sql` (See: [Connection configuration reference](/developer-guide/native-apps/connector-sdk/reference/connection_configuration_reference))

## Related Java objects

The following Java objects from the `com.snowflake.connectors.application.configuration.connection` package and some common components are tightly connected with the above procedures:

- `UpdateConnectionConfigurationHandler`
- `ConnectionConfigurationInputValidator`
- `ConnectionConfigurationCallback`
- `DraftConnectionValidator`
- `ConnectionValidator`
- `UpdateConnectionConfigurationHandlerBuilder`
- `ConnectorStatusService`
- `ConnectorConfigurationService`
- `ConnectorErrorHandler`

## Custom handler

Handler and its internals can be customized using the following two approaches.

### Procedure replacement approach

The following components can be replaced using SQL.

#### Handler

To provide a custom implementation of `UpdateConnectionConfigurationHandler` the `PUBLIC.UPDATE_CONNECTION_CONFIGURATION` procedure must be replaced. For example:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.UPDATE_CONNECTION_CONFIGURATION(connection_configuration VARIANT)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/connectors-native-sdk.jar')
  HANDLER = 'com.custom.handler.CustomUpdateConnectionConfigurationHandler.updateConnectionConfiguration';

GRANT USAGE ON PROCEDURE PUBLIC.UPDATE_CONNECTION_CONFIGURATION(VARIANT) TO APPLICATION ROLE ADMIN;
```

#### Internal procedures

The `VALIDATE` and `INTERNAL` procedures can also be customized through SQL. It can even invoke another Java handler:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.DRAFT_CONNECTION_CONFIGURATION_INTERNAL(connection_configuration VARIANT)
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

  CREATE OR REPLACE PROCEDURE PUBLIC.UPDATE_CONNECTION_CONFIGURATION_VALIDATE(connection_configuration VARIANT)
    RETURNS VARIANT
    LANGUAGE JAVA
    RUNTIME_VERSION = '11'
    PACKAGES = ('com.snowflake:snowpark:1.11.0')
    IMPORTS = ('/connectors-native-sdk.jar')
    HANDLER = 'com.custom.handler.CustomConnectionConfigurationInputValidator.validate';
```

### Builder approach

`UpdateConnectionConfigurationHandler` can be customized using `UpdateConnectionConfigurationHandlerBuilder`. This builder allows the developer to provide custom implementations of the following interfaces:

- `ConnectionConfigurationInputValidator`
- `ConnectionConfigurationCallback`
- `DraftConnectionValidator`
- `ConnectionConfigurationCallback`
- `ConnectionValidator`
- `ConnectorErrorHelper`

In case one of them is not provided - the default implementation provided by the SDK will be used.

Copy code

```
class CustomConnectionConfigurationInputValidator implements ConnectionConfigurationInputValidator {

  @Override
  public ConnectorResponse validate(Variant configuration) {
    // CUSTOM VALIDATION LOGIC
    return ConnectorResponse.success();
  }
}

class CustomHandler {

  // Path to this method needs to be specified in the PUBLIC.UPDATE_CONNECTION_CONFIGURATION procedure using SQL
  public static Variant updateConnectionConfiguration(Session session, Variant configuration) {
    // Using the builder
    var handler = UpdateConnectionConfigurationHandler.builder(session)
      .withInputValidator(new CustomConnectionConfigurationInputValidator())
      .build();
    return handler.updateConnectionConfiguration(configuration).toVariant();
  }
}
```
