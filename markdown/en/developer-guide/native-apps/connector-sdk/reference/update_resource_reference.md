# Update resource reference

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

## Database objects and procedures

The following database objects are created when the file `ingestion/resource_management.sql` is executed.

### PUBLIC.UPDATE\_RESOURCE(resource\_ingestion\_definition\_id VARCHAR, ingestion\_configurations VARIANT)

Entry point procedure available to the `ADMIN` role. This procedure invokes the Java function `UpdateResourceHandler.updateResource`.

### PUBLIC.UPDATE\_RESOURCE\_VALIDATE(resource\_ingestion\_definition\_id VARCHAR, ingestion\_configurations VARIANT)

Procedure used for connector specific validation of update process. By default, it returns `'response_code': 'OK'`.
It is invoked by `DefaultUpdateResourceValidator`. Can be overwritten both in SQL and Java.

### PUBLIC.PRE\_UPDATE\_RESOURCE(resource\_ingestion\_definition\_id VARCHAR, ingestion\_configurations VARIANT)

Procedure used for adding connector specific logic which is invoked before a resource is updated.
By default, it returns `'response_code': 'OK'`.
It is invoked by `DefaultPreUpdateResourceCallback`. Can be overwritten both in SQL and Java.

### PUBLIC.POST\_UPDATE\_RESOURCE(resource\_ingestion\_definition\_id VARCHAR, ingestion\_configurations VARIANT)

Procedure used for adding connector specific logic which is invoked after a resource is updated.
By default, it returns `'response_code': 'OK'`.
It is invoked by `DefaultPostUpdateResourceCallback`. Can be overwritten both in SQL and Java.

## Related Java objects

The following Java objects from the `com.snowflake.connectors.application.ingestion.update` package and some common components are tightly connected with the above procedures:

- `UpdateResourceHandler`
- `UpdateResourceHandlerBuilder`
- `UpdateResourceValidator`
- `PreUpdateResourceCallback`
- `PostUpdateResourceCallback`
- `ConnectorErrorHelper`

## Custom handler

The handler and its internals can be customized using the following approaches.

### Procedure replacement approach

The following components can be replaced using SQL.

#### Handler

To provide whole custom implementation of `UpdateResourceHandler`, the `PUBLIC.UPDATE_RESOURCE` procedure must be replaced. For example:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.UPDATE_RESOURCE(resource_ingestion_definition_id VARCHAR, ingestion_configurations VARIANT)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/connectors-native-sdk.jar')
  HANDLER = 'com.custom.handler.CustomUpdateResourceHandler.updateResource';

GRANT USAGE ON PROCEDURE PUBLIC.UPDATE_RESOURCE(VARCHAR, VARIANT) TO APPLICATION ROLE ADMIN;
```

#### Internal procedures

Internal procedures `UPDATE_RESOURCE_VALIDATE`, `PRE_UPDATE_RESOURCE` and `POST_UPDATE_RESOURCE` can be also customized through the SQL. These procedures can also invoke other Java handlers:

Copy code

```
CREATE OR REPLACE PROCEDURE PUBLIC.UPDATE_RESOURCE_VALIDATE(resource_ingestion_definition_id VARCHAR, ingestion_configurations VARIANT)
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

CREATE OR REPLACE PROCEDURE PUBLIC.UPDATE_RESOURCE_VALIDATE(resource_ingestion_definition_id VARCHAR, ingestion_configurations VARIANT)
  RETURNS VARIANT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:1.11.0')
  IMPORTS = ('/connectors-native-sdk.jar')
  HANDLER = 'com.custom.handler.CustomHandler.updateResourceValidate';
```

### Builder approach

`UpdateResourceHandler` can be customized using `UpdateResourceHandlerBuilder`. This builder allows user to provide custom implementations of the following interfaces:

- `UpdateResourceValidator`
- `PreUpdateResourceCallback`
- `PostUpdateResourceCallback`
- `ConnectorErrorHelper`

In case a function is not provided the default implementation provided by the SDK will be used.

Copy code

```
class CustomPreUpdateResourceCallback implements PreUpdateResourceCallback {
  @Override
  public ConnectorResponse execute(String resourceIngestionDefinitionId, Variant updatedIngestionConfigurations) {
    // CUSTOM LOGIC
    return ConnectorResponse.success();
  }
}

class CustomHandler {

  // Path to this method needs to be specified in the PUBLIC.UPDATE_RESOURCE procedure using SQL
  public static Variant updateResource(Session session, String resourceIngestionDefinitionId, Variant updatedIngestionConfigurations) {
    //Using builder
    var handler = UpdateResourceHandlerBuilder.builder(session)
      .withPreUpdateResourceCallback(new CustomPreUpdateResourceCallback())
      .build();
    return handler.updateResource(resourceIngestionDefinitionId).toVariant();
  }
}
```
