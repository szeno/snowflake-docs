# Enable resource reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## Database objects and procedures

The following database objects are created when the file `ingestion/resource_management.sql` is executed.

### PUBLIC.ENABLE\_RESOURCE(resource\_ingestion\_definition\_id VARCHAR)

Entry point procedure available to the `ADMIN` role. This procedure invokes the Java function `EnableResourceHandler.enableResource`.

### PUBLIC.ENABLE\_RESOURCE\_VALIDATE(resource\_ingestion\_definition\_id VARCHAR)

Procedure used for connector specific validation of enable process. By default, it returns `'response_code': 'OK'`.
It is invoked by `DefaultEnableResourceValidator`. Can be overwritten both in SQL and Java.

### PUBLIC.PRE\_ENABLE\_RESOURCE(resource\_ingestion\_definition\_id VARCHAR)

Procedure used for adding connector specific logic which is invoked before a resource is enabled.
By default, it returns `'response_code': 'OK'`.
It is invoked by `DefaultPreEnableResourceCallback`. Can be overwritten both in SQL and Java.

### PUBLIC.POST\_ENABLE\_RESOURCE(resource\_ingestion\_definition\_id VARCHAR)

Procedure used for adding connector specific logic which is invoked after a resource is enabled.
By default, it returns `'response_code': 'OK'`.
It is invoked by `DefaultPostEnableResourceCallback`. Can be overwritten both in SQL and Java.

## Related Java objects

The following Java objects from the `com.snowflake.connectors.application.ingestion.enable` package and some common components are tightly connected with the above procedures:

- `EnableResourceHandler`
- `EnableResourceHandlerBuilder`
- `EnableResourceValidator`
- `PreEnableResourceCallback`
- `PostEnableResourceCallback`
- `ConnectorErrorHelper`

## Custom handler

The handler and its internals can be customized using the following approaches.

### Procedure replacement approach

The following components can be replaced using SQL.

#### Handler

To provide whole custom implementation of `EnableResourceHandler`, the `PUBLIC.ENABLE_RESOURCE` procedure must be replaced. For example:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.ENABLE_RESOURCE(resource_ingestion_definition_id VARCHAR)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/connectors-native-sdk.jar')
  HANDLER = 'com.custom.handler.CustomEnableResourceHandler.enableResource';

  GRANT USAGE ON PROCEDURE PUBLIC.ENABLE_RESOURCE(VARCHAR) TO APPLICATION ROLE ADMIN;
```

#### Internal procedures

Internal procedures `ENABLE_RESOURCE_VALIDATE`, `PRE_ENABLE_RESOURCE` and `POST_ENABLE_RESOURCE` can be also customized through the SQL. These procedures can also invoke other Java handlers:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.ENABLE_RESOURCE_VALIDATE(resource_ingestion_definition_id VARCHAR)
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

CREATE OR REPLACE PROCEDURE PUBLIC.ENABLE_RESOURCE_VALIDATE(resource_ingestion_definition_id VARCHAR)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/connectors-native-sdk.jar')
  HANDLER = 'com.custom.handler.CustomHandler.enableResourceValidate';
```

### Builder approach

`EnableResourceHandler` can be customized using `EnableResourceHandlerBuilder`. This builder allows user to provide custom implementations of the following interfaces:

- `EnableResourceValidator`
- `PreEnableResourceCallback`
- `PostEnableResourceCallback`
- `ConnectorErrorHelper`

In case a function is not provided the default implementation provided by the SDK will be used.

Copy code

```
class CustomPreEnableResourceCallback implements PreEnableResourceCallback {
  @Override
  public ConnectorResponse execute(String resourceIngestionDefinitionId) {
    // CUSTOM LOGIC
    return ConnectorResponse.success();
  }
}

class CustomHandler {

  // Path to this method needs to be specified in the PUBLIC.ENABLE_RESOURCE procedure using SQL
  public static Variant enableResource(Session session, String resourceIngestionDefinitionId) {
    //Using builder
    var handler = EnableResourceHandlerBuilder.builder(session)
      .withPreEnableResourceCallback(new CustomPreEnableResourceCallback())
      .build();
    return handler.enableResource(resourceIngestionDefinitionId).toVariant();
  }
}
```
