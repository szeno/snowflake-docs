# Disable resource reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## Database objects and procedures

The following database objects are created when the file `ingestion/resource_management.sql` is executed.

### PUBLIC.DISABLE\_RESOURCE(resource\_ingestion\_definition\_id VARCHAR)

Entry point procedure available to the `ADMIN` role. This procedure invokes the Java function `DisableResourceHandler.disableResource`.

### PUBLIC.PRE\_DISABLE\_RESOURCE(resource\_ingestion\_definition\_id VARCHAR)

Procedure used for adding connector specific logic which is invoked before a resource is disabled.
By default, it returns `'response_code': 'OK'`.
It is invoked by `DefaultPreDisableResourceCallback`. Can be overwritten both in SQL and Java.

### PUBLIC.POST\_DISABLE\_RESOURCE(resource\_ingestion\_definition\_id VARCHAR)

Procedure used for adding connector specific logic which is invoked after a resource is disabled.
By default, it returns `'response_code': 'OK'`.
It is invoked by `DefaultPostDisableResourceCallback`. Can be overwritten both in SQL and Java.

## Related Java objects

The following Java objects from the `com.snowflake.connectors.application.ingestion.disable` package and some common components are tightly connected with the above procedures:

- `DisableResourceHandler`
- `DisableResourceHandlerBuilder`
- `PreDisableResourceCallback`
- `PostDisableResourceCallback`
- `ConnectorErrorHelper`

## Custom handler

The handler and its internals can be customized using the following approaches.

### Procedure replacement approach

The following components can be replaced using SQL.

#### Handler

To provide a custom implementation of `DisableResourceHandler`, replace the `PUBLIC.DISABLE_RESOURCE` procedure.

For example:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.DISABLE_RESOURCE(resource_ingestion_definition_id VARCHAR)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/connectors-native-sdk.jar')
  HANDLER = 'com.custom.handler.CustomDisableResourceHandler.disableResource';

GRANT USAGE ON PROCEDURE PUBLIC.DISABLE_RESOURCE(VARCHAR) TO APPLICATION ROLE ADMIN;
```

#### Internal procedures

Internal procedures `PRE_DISABLE_RESOURCE` and `POST_DISABLE_RESOURCE` can be also customized through the SQL. These procedures can also invoke other Java handlers:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.PRE_DISABLE_RESOURCE(resource_ingestion_definition_id VARCHAR)
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

CREATE OR REPLACE PROCEDURE PUBLIC.PRE_DISABLE_RESOURCE(resource_ingestion_definition_id VARCHAR)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/connectors-native-sdk.jar')
  HANDLER = 'com.custom.handler.CustomHandler.disableResourceValidate';
```

### Builder approach

`DisableResourceHandler` can be customized using `DisableResourceHandlerBuilder`. This builder allows user to provide custom implementations of the following interfaces:

- `PreDisableResourceCallback`
- `PostDisableResourceCallback`
- `ConnectorErrorHelper`

When a function is not provided the default implementation provided by the SDK is used.

Copy code

```
class CustomPreDisableResourceCallback implements PreDisableResourceCallback {
  @Override
  public ConnectorResponse execute(String resourceIngestionDefinitionId) {
    // CUSTOM LOGIC
    return ConnectorResponse.success();
  }
}

class CustomHandler {

  // Path to this method needs to be specified in the PUBLIC.DISABLE_RESOURCE procedure using SQL
  public static Variant disableResource(Session session, String resourceIngestionDefinitionId) {
    //Using builder
    var handler = DisableResourceHandlerBuilder.builder(session)
      .withPreDisableResourceCallback(new CustomPreDisableResourceCallback())
      .build();
    return handler.disableResource(resourceIngestionDefinitionId).toVariant();
  }
}
```
