# Create resource reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## Database objects and procedures

The following database objects are created when the file `ingestion/resource_management.sql` is executed.

### PUBLIC.CREATE\_RESOURCE(name VARCHAR,resource\_id VARIANT,ingestion\_configurations VARIANT,id VARCHAR,enabled BOOLEAN,resource\_metadata VARIANT)

Entry point procedure available to the `ADMIN` role. This procedure invokes the Java function `CreateResourceHandler.createResource`.

### PUBLIC.CREATE\_RESOURCE\_VALIDATE(resource VARIANT)

Procedure used for connector specific validation of create process. By default, it returns `'response_code': 'OK'`.
It is invoked by `DefaultCreateResourceValidator`. Can be overwritten both in SQL and Java.

### PUBLIC.PRE\_CREATE\_RESOURCE(resource VARIANT)

Procedure used for adding connector specific logic which is invoked before a resource is created.
By default, it returns `'response_code': 'OK'`.
It is invoked by `DefaultPreCreateResourceCallback`. Can be overwritten both in SQL and Java.

### PUBLIC.POST\_CREATE\_RESOURCE(resource\_ingestion\_definition\_id VARCHAR)

Procedure used for adding connector specific logic which is invoked after a resource is created and scheduled.
By default, it returns `'response_code': 'OK'`.
It is invoked by `DefaultPostCreateResourceCallback`. Can be overwritten both in SQL and Java.

## Related Java objects

The following Java objects from the `com.snowflake.connectors.application.ingestion.create` package and some common components are tightly connected with the above procedures:

- `CreateResourceHandler`
- `CreateResourceHandlerBuilder`
- `CreateResourceValidator`
- `PreCreateResourceCallback`
- `PostCreateResourceCallback`
- `ConnectorErrorHelper`

## Custom handler

The handler and its internals can be customized using the following approaches.

### Procedure replacement approach

The following components can be replaced using SQL.

#### Handler

To provide whole custom implementation of `CreateResourceHandler`, the `PUBLIC.CREATE_RESOURCE` procedure must be replaced. For example:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.CREATE_RESOURCE(name VARCHAR,resource_id VARIANT,ingestion_configurations VARIANT,id VARCHAR,enabled BOOLEAN,resource_metadata VARIANT)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/connectors-native-sdk.jar')
  HANDLER = 'com.custom.handler.CustomCreateResourceHandler.createResource';

  GRANT USAGE ON PROCEDURE PUBLIC.CREATE_RESOURCE(VARCHAR, VARIANT, VARIANT, VARCHAR, BOOLEAN, VARIANT) TO APPLICATION ROLE ADMIN;
```

#### Internal procedures

Internal procedures `CREATE_RESOURCE_VALIDATE`, `PRE_CREATE_RESOURCE` and `POST_CREATE_RESOURCE` can be also customized through the SQL. They can also invoke another Java handler:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.CREATE_RESOURCE_VALIDATE(resource VARIANT)
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

  CREATE OR REPLACE PROCEDURE PUBLIC.CREATE_RESOURCE_VALIDATE(resource VARIANT)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/connectors-native-sdk.jar')
  HANDLER = 'com.custom.handler.CustomHandler.createResourceValidate';
```

### Builder approach

`CreateResourceHandler` can be customized using `CreateResourceHandlerBuilder`. This builder allows user to provide custom implementations of the following interfaces:

- `CreateResourceValidator`
- `PreCreateResourceCallback`
- `PostCreateResourceCallback`
- `ConnectorErrorHelper`

In case a function is not provided the default implementation provided by the SDK will be used.

Copy code

```
class CustomPreCreateResourceCallback implements PreCreateResourceCallback {
  @Override
  public ConnectorResponse execute(String resourceIngestionDefinitionId) {
    // CUSTOM LOGIC
    return ConnectorResponse.success();
  }
}

class CustomHandler {

  // Path to this method needs to be specified in the PUBLIC.CREATE_RESOURCE procedure using SQL
  public static Variant createResource(
      Session session,
      String name,
      Variant resourceId,
      Variant ingestionConfigurations,
      String id,
      boolean enabled,
      Variant resourceMetadata) {
    //Using builder
    var handler = CreateResourceHandlerBuilder.builder(session)
      .withPreCreateResourceCallback(new CustomPreCreateResourceCallback())
      .build();
    return handler.createResource(resourceIngestionDefinitionId).toVariant();
  }
}
```
