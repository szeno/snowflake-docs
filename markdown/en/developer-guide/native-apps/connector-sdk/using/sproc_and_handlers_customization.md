# Stored procedures and handlers customization

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

The Snowflake Native SDK for Connectors provides the general structure of the connector,
however, it allows for some customizations, depending on the source system and the actual needs of the developer.
For that reason, some features have empty basic implementations and it is possible to overwrite them with custom logic.
Furthermore, the components can be enabled and disabled according to specific needs, more on this in the choosing components section.

## Stored procedures

Stored procedures provided by the SDK can be split into two categories:

1. High-level entry points to the logic implemented in Java
2. Internal procedures with smaller scope

Because they have different responsibilities, the customization process is also different.

### High level procedures customization

High level procedures are used only as an entry point to the actual logic implemented in Java.
So to change the underlying logic a path to the new handler needs to be specified when recreating the stored procedure.
This procedure needs to be added as custom code in the `setup.sql` script.
This requires the new Java implementation to be provided, it can be done from scratch or using the provided in the SDK `builders`,
which are described below:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.CONFIGURE_CONNECTOR(input VARIANT)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/jar_with_custom_code.jar')
  HANDLER = 'com.custom.handler.CustomHandler.configure';
```

### Smaller scope procedures customization

Some of the procedures provided by the Snowflake Native SDK for Connectors have so little logic that they can be easily written using only SQL.
For those procedures it is possible to replace the default implementations using SQL only. For example some procedures with `_VALIDATE` or `_INTERNAL` suffixes can be reimplemented this way.
All those procedures can be also customized using Java only approach through `Builders`. This approach is explained below.
There is also a possibility to replace a procedure that was using only plain SQL to use handler instead. In this case it will be
the same as for the high level stored procedures above.

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.CONFIGURE_CONNECTOR_INTERNAL(config VARIANT)
  RETURNS VARIANT
  LANGUAGE SQL
  EXECUTE AS OWNER
  AS
  BEGIN
    -- input some custom logic here
    RETURN OBJECT_CONSTRUCT('response_code', 'OK');
  END;
```

## Handlers

The Snowflake Native SDK for Connectors defines default handlers for the stored procedures. They can be used as they are, customized or completely replaced.
For the latter case, the whole custom implementation does not need to follow standards defined by
the SDK and the custom implementation needs to be specified in SQL as it was mentioned above for customizing high level procedures.

However, if you wish to follow the flow of the connector defined by the SDK there is a way to customize only some parts of the flow.
Each existing handler is using multiple underlying objects, in the most cases those are:
`validator`, `callback` or `helper` classes. Each of them satisfies some interface and it’s
possible to replace default implementations with the custom implementations of the interface.

### Builders

To retain the SDK-defined flow in the connector during customization helper objects called `builders` are provided.
Each `handler` class has its own `builder` bundled. Those allow the user to provide a custom implementation of the underlying Java objects.
This way the developer does not need to touch the connector internal flow and can focus on customizing just the needed parts.
There is a small catch when using `builders`, this approach also requires the developer to
specify the new entry point method that will be referenced in the stored procedure.

For example, a `handler` using a customized `validator` using the `builder` looks like this:

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

Then the entry point method in SQL needs to be specified like this:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.SET_CONNECTION_CONFIGURATION(input VARIANT)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/jar_with_custom_code.jar')
  HANDLER = 'com.custom.handler.CustomHandler.configureConnection';
```
