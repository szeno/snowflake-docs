# Request references and object-level privileges from consumers

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how providers can configure a Snowflake Native App to request access to objects in
the consumer account that exist outside the app.

## About references

In some contexts an installed Snowflake Native App needs to access existing objects in
the consumer account that exist outside the app. For example, an app
might need to access existing tables in a consumer database.

In this context, it’s not sufficient for the consumer to grant access on an object to
the app because the app cannot determine the name of the schema and object in
the consumer account.

To allow the app to access existing objects outside the app, the Snowflake Native App Framework
uses references that enable the customer to specify the name and schema for an object
and enable access to the object.

### Workflow for defining references in the consumer account

To request a reference and object-level privilege, the provider performs the following when
developing and publishing a Snowflake Native App:

1. [Determine which objects require references and their corresponding privileges](#label-native-apps-supported-privs-references).
2. [Define the references in the manifest file](/developer-guide/native-apps/requesting-privs#label-native-apps-privs-manifest).
3. Add a stored procedure in the setup script to handle the callback for each reference
   defined in the manifest file.

After installing the Snowflake Native App, the consumer performs the following:

1. View the references required by the Snowflake Native App.
2. Create the reference by calling the SYSTEM$REFERENCE system function.
3. Run the callback stored procedure passing the id of the reference.

After the consumer runs the callback stored procedure, the Snowflake Native App can access the
requested object.

This workflow outlines the process where the consumer creates the reference
manually. Refer to [Create a user interface to request privileges and references](/developer-guide/native-apps/requesting-ui) for information on creating
a user interface to allow consumers to create references and grant privileges using Snowsight.

### Object types and privileges that a reference can contain

The following table lists the object types that a reference can include and the privileges
allowed for each object:

| Object Type | Privileges Allowed |
| --- | --- |
| TABLE | SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES |
| VIEW | SELECT, REFERENCES |
| EXTERNAL TABLE | SELECT, REFERENCES |
| FUNCTION | USAGE |
| PROCEDURE | USAGE |
| WAREHOUSE | MODIFY, MONITOR, USAGE, OPERATE |
| API INTEGRATION | USAGE |
| EXTERNAL ACCESS INTEGRATION | USAGE |
| SECRET | USAGE, READ |

Expand

Show lessSee more

## Define a reference in the manifest file

The following example shows how to define a reference in the manifest file for a table in the consumer account that exists outside the
APPLICATION object:

Copy code

```
references:
  - consumer_table:
      label: "Consumer table"
      description: "A table in the consumer account that exists outside the APPLICATION object."
      privileges:
        - INSERT
        - SELECT
      object_type: TABLE
      multi_valued: false
      register_callback: config.register_single_reference
```

This example defines an reference named `consumer_table` that requires the INSERT and SELECT
privileges on a table in the consumer account. The `register_callback` property specifies a stored
procedure used to bind a consumer table to this reference definition.

Use `multi_valued` to bind multiple consumer objects to the same reference. When this property is specified,
the same operations are performed on objects with a single value reference. The property can also be used with
objects with multi-valued references. See [Supported reference functions](#label-native-apps-reference-supported-functions) to learn more about Snowflake Native App Framework reference operations.

### Remove a reference definition

Note

Snowflake recommends against removing a reference definition from the manifest file in a new version of an app. If you need to
remove a defined reference, update any code that uses the removed reference in the same version release and notify the consumer
in the README file.

If an app defines a reference then later deletes the reference definition from a subsequent version of the app, calling any function or
procedure that still uses the deleted reference results in an error for consumers. For example, the manifest file for version V1 of app
`my_app` includes a reference definition for REF\_TO\_TABLE and a stored procedure CREATE\_VIEW\_FROM\_TABLE that uses the table reference
REF\_TO\_TABLE to create a view VIEW\_SELECT\_FROM\_DEFINED\_REF.

In version V2 of `my_app`, the reference definition for REF\_TO\_TABLE is removed from the manifest file. When a consumer upgrades
their installed app `my_app` to version V2, calling the CREATE\_VIEW\_FROM\_TABLE procedure results in the following error:

```
Reference definition '<REF_DEF_NAME>' cannot be found in the current version of the application '<APP_NAME>'
```

## Create a callback stored procedure for a reference

After defining a reference in the manifest file, a provider must add a
stored procedure to the setup script to register the callback for the
reference.

The following example shows a stored procedure used to handle a callback for the reference
shown in [Define a reference in the manifest file](#label-native-apps-reference-manifest-def):

Copy code

```
CREATE APPLICATION ROLE app_admin;

CREATE OR ALTER VERSIONED SCHEMA config;
GRANT USAGE ON SCHEMA config TO APPLICATION ROLE app_admin;

CREATE PROCEDURE CONFIG.REGISTER_SINGLE_REFERENCE(ref_name STRING, operation STRING, ref_or_alias STRING)
  RETURNS STRING
  LANGUAGE SQL
  AS $$
    BEGIN
      CASE (operation)
        WHEN 'ADD' THEN
          SELECT SYSTEM$SET_REFERENCE(:ref_name, :ref_or_alias);
        WHEN 'REMOVE' THEN
          SELECT SYSTEM$REMOVE_REFERENCE(:ref_name, :ref_or_alias);
        WHEN 'CLEAR' THEN
          SELECT SYSTEM$REMOVE_ALL_REFERENCES(:ref_name);
      ELSE
        RETURN 'unknown operation: ' || operation;
      END CASE;
      RETURN NULL;
    END;
  $$;

GRANT USAGE ON PROCEDURE CONFIG.REGISTER_SINGLE_REFERENCE(STRING, STRING, STRING)
  TO APPLICATION ROLE app_admin;
```

This example creates a stored procedure named `REGISTER_SINGLE_REFERENCE` that calls
a system function to perform a specific operation on a reference that is passed as an
argument to the stored procedure.

Note

Because the stored procedure uses the SYSTEM$SET\_REFERENCE system function, the stored procedure
only works for a reference with a single value in the description. To associate a reference with
multiple values, use the SYSTEM$ADD\_REFERENCE system function.

## Create a callback stored procedure for requesting object configuration

For some object types, a provider must add a stored procedure to the setup script to provide additional
configuration. This callback is used when consumers allow references using Snowsight.

The following example shows how to define a configuration callback stored procedure for the reference
shown in [Define a reference in the manifest file](#label-native-apps-reference-manifest-def):

Copy code

```
CREATE OR REPLACE CONFIG.GET_CONFIGURATION_FOR_REFERENCE(ref_name STRING)
  RETURNS STRING
  LANGUAGE SQL
  AS
  $$
  BEGIN
    CASE (ref_name)
      WHEN 'CONSUMER_EXTERNAL_ACCESS' THEN
        RETURN '{
          "type": "CONFIGURATION",
          "payload":{
            "host_ports":["google.com"],
            "allowed_secrets" : "LIST",
            "secret_references":["CONSUMER_SECRET"]}}';
      WHEN 'CONSUMER_SECRET' THEN
        RETURN '{
          "type": "CONFIGURATION",
          "payload":{
            "type" : "OAUTH2",
            "security_integration": {
              "oauth_scopes": ["https://www.googleapis.com/auth/analytics.readonly"],
              "oauth_token_endpoint": "https://oauth2.googleapis.com/token",
              "oauth_authorization_endpoint":
                "https://accounts.google.com/o/oauth2/auth"}}}';
     END CASE;
     RETURN '';
   END;
   $$;

GRANT USAGE ON PROCEDURE CONFIG.GET_CONFIGURATION_FOR_REFERENCE(STRING)
  TO APPLICATION ROLE app_admin;
```

This example creates a stored procedure named `GET_CONFIGURATION_FOR_REFERENCE` that returns
a JSON-formatted configuration that is used to build a reference of type EXTERNAL ACCESS INTEGRATION or
SECRET reference. The entries in the CASE statement should map to the reference names in the manifest file.

Note

This callback function is required by references of type EXTERNAL ACCESS INTEGRATION and SECRET.
It is only applicable to these types of references.

## View the references defined in an application

When a provider defines references in the manifest file, the references are included as part of the installed Snowflake Native App.

To view the references defined for a Snowflake Native App, run the [SHOW REFERENCES](/sql-reference/sql/show-references)
command as shown in the following example:

Copy code

```
SHOW REFERENCES IN APPLICATION hello_snowflake_app;
```

## Bind an object to the application

After viewing the reference definition for a Snowflake Native App, the consumer creates a reference by running
the SYSTEM$REFERENCE system function as shown in the following example:

Copy code

```
SELECT SYSTEM$REFERENCE('table', 'db1.schema1.table1', 'persistent', 'select', 'insert');
```

This command returns an identifier for the reference. The consumer can pass the identifier to the
callback stored procedure for the reference as shown in the following example:

Copy code

```
CALL app.config.register_single_reference(
  'consumer_table' , 'ADD', SYSTEM$REFERENCE('TABLE', 'db1.schema1.table1', 'PERSISTENT', 'SELECT', 'INSERT'));
```

In this example, `consumer_table` is the name of the reference defined in the manifest file.
After the consumer runs the stored procedure that associates the reference, the Snowflake Native App can access the
table in the consumer account.

The callback stored procedure in the [previous section](#label-native-apps-reference-create-callback)
calls the SYSTEM$SET\_REFERENCE system function as shown in the following example:

Copy code

```
SELECT SYSTEM$SET_REFERENCE(:ref_name, :ref_or_alias);
```

Refer to [Supported reference functions](#label-native-apps-reference-supported-functions) for other system functions related
to references.

## Considerations when using references

Snowflake recommends that you do not modify reference definitions across versions.
To update a reference definition in a new version, for example, to change the privileges
to SELECT, INSERT from SELECT, you must define a new reference definition with a different name
The updated Snowflake Native App can use this new reference in the new version of the app.

To embed a reference within another object, for example to assign a reference to a variable,
the reference must already be bound to an object in the consumer account. For example, you
cannot create a task unless you first bind the reference to the consumer warehouse.

## Examples of using references in a Snowflake Native App

The following sections provide examples of using references in different contexts.

Note

The `reference()` functions in the following examples can only be called in a stored procedure
in the APPLICATION object.

### Run queries using a reference

The following examples show how to run queries using references:

Copy code

```
SELECT * FROM reference('consumer_table');
```

Copy code

```
SELECT reference('encrypt_func')(t.c1) FROM consumer_table t;
```

### Call a stored procedure using a reference

The following example shows how to call a stored procedure using a reference:

Copy code

```
CALL reference('consumer_proc')(11, 'hello world');
```

### Run DML commands using a reference

The following examples show how to modify data in a table using references:

Copy code

```
INSERT INTO reference('data_export')(C1, C2)
  SELECT T.C1, T.C2 FROM reference('other_table')
```

Copy code

```
COPY INTO reference('the_table') ...
```

### Run the DESCRIBE command using a reference

The following example shows how to run the DESCRIBE operation using a reference:

Copy code

```
DESCRIBE TABLE reference('the_table')
```

### Use references in a task

Copy code

```
CREATE TASK app_task
  WAREHOUSE = reference('consumer_warehouse')
  ...;

ALTER TASK app_task SET WAREHOUSE = reference('consumer_warehouse');
```

### Use references in a view definition

Copy code

```
CREATE VIEW app_view
  AS SELECT reference('function')(T.C1) FROM reference('table') AS T;
```

### Use references in a function body

Copy code

```
CREATE FUNCTION app.func(x INT)
  RETURNS STRING
  AS $$ select reference('consumer_func')(x) $$;
```

### Use references in an external function

Copy code

```
CREATE EXTERNAL FUNCTION app.func(x INT)
  RETURNS STRING
  ...
  API_INTEGRATION = reference('app_integration');
```

### Use references in a function or procedure

Copy code

```
CREATE FUNCTION app.func(x INT)
  RETURNS STRING
  ...
  EXTERNAL_ACCESS_INTEGRATIONS = (reference('consumer_external_access_integration'), ...);
  SECRETS = ('cred1' = reference('consumer_secret'), ...);
```

Note

Consumers cannot directly call functions or stored procedures that use references
to external access integrations or secrets.

However, other components of the app, including Streamlit apps, tasks, and other functions and stored procedures, can use these references.

To allow consumers to call a function or stored procedure that uses references to external
access integrations or secrets, providers can do the following:

1. In the setup script, create a function or stored procedure that uses a reference, for
   example: `function_with_eai_secret_reference` as shown in the following example:

   Copy code

   ```
   CREATE FUNCTION app_schema.function_with_eai_secret_reference(arg1 STRING)
     RETURNS string
     LANGUAGE python
     RUNTIME_VERSION = 3.11
     HANDLER = 'my_handler'
     EXTERNAL_ACCESS_INTEGRATIONS = (reference('eai_ref'))
     PACKAGES = ('snowflake-snowpark-python','requests')
     SECRETS = ('cred' = reference('secret_ref') )
     ...
   AS
   $$
   ```
2. In the setup script, create a wrapper stored procedure named `my_wrapper_procedure`.

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE app_schema.my_wrapper_procedure(arg1 STRING)
     RETURNS STRING
     LANGUAGE SQL
     AS
     $$
    BEGIN
        ...
    END;
     $$;
   ```

> Note
>
> The wrapper must be a stored procedure, not a function.

1. Within `my_wrapper_procedure`, add a call to
   `function_with_eai_secret_reference` as shown in the following example:

   Copy code

   ```
   BEGIN
     RETURN app_schema.function_with_eai_secret_reference(arg1);
   END;
   ```
2. Grant `my_wrapper_procedure` to an application role to allow consumers to call the
   procedure as shown in the following example:

   Copy code

   ```
   GRANT USAGE ON PROCEDURE app_schema.my_wrapper_procedure(STRING)
     TO APPLICATION ROLE app_role;
   ```

After the app is installed, consumers can call `my_wrapper_procedure` which then calls
`function_with_eai_secret_reference`.

### Use references in a policy

Copy code

```
CREATE ROW ACCESS POLICY app_policy
  AS (sales_region varchar) RETURNS BOOLEAN ->
  'sales_executive_role' = reference('get_sales_team')
    or exists (
      select 1 from reference('sales_table')
        where sales_manager = reference('get_sales_team')()
        and region = sales_region
      );
```

## JSON format for the configuration callback response

The configuration callback function returns a response in JSON format. The JSON
format returned is different for external access integration and secret references.

### JSON format for external access integration

For EXTERNAL ACCESS INTEGRATION references, the expected structure of the JSON response is:

Copy code

```
{
  "type": "CONFIGURATION",
  "payload": {
    "host_ports": ["host_port_1", ...],
    "allowed_secrets": "NONE%ALL%LIST",
    "secret_references": ["ref_name_1", ...]
  }
}
```

- `host_ports`
  An array of strings. Each value must be a valid domain.

  Optionally, it can also include a port. The valid port range is 1 to 65535, inclusive.
  If you do not specify a port, it defaults to 443. If an external network location supports
  dynamic ports, you need to specify all possible ports.

  - To allow access to all ports, specify the port as 0; for example, `example.com:0`.

  These values are used to create an egress network rule for the external access integration.
  See [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule) for more information.
- `allowed_secrets`
  Specifies the secrets allowed by the EXTERNAL ACCESS INTEGRATION reference. Valid values are:

  - `NONE`: Secrets are not allowed.
  - `ALL`: Allows any existing secret.
  - `LIST`: Allows a specific set of secrets as specified in the `secret_references`
    property.

  The values of the `allowed_secrets` are used to create the external access integration.
  See [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration) for more information.
- `secret_references`:
  Specifies a list of secret references that are allowed by the external access integration.

  The values specified here must be the same as the secret references defined in the manifest.

  This property is only applicable if the `allowed_secrets` is set to `LIST`. In this
  context, `secret_references` is required.

### JSON format for secret references

For secret references, the expected structure of the JSON response is:

Copy code

```
{
  "type": "CONFIGURATION",
    "payload": {
            "type": "<payload_type>",
            "security_integration": {
                    "oauth_scopes": ["scope_1", "scope_2"],
                    "oauth_token_endpoint" : "token_endpoint",
                    "oauth_authorization_endpoint" : "auth_endpoint"
            }
    }
}
```

- `payload.type`
  :   The type of secret. Valid values are:

      - `OAUTH2`: Specifies the secret to use with the OAuth2 grant flow.
      - `GENERIC_STRING`: Specifies a generic string secret.
      - `PASSWORD`: Specifies a password secret.

      See [CREATE SECRET](/sql-reference/sql/create-secret) for more information.
- `payload.security_integration`
  :   Specifies the values required to configure the
      [API Authentication](/sql-reference/sql/create-security-integration-api-auth) for an OAuth secret.

### JSON format error responses

In case of errors or if the reference is not yet ready for configuration, the expected structure of
the error response is:

Copy code

```
{
  "type": "ERROR",
  "payload":{
    "message": "The reference is not available for configuration ..."
 }
}
```

- `message`:
  The error message from the application that is displayed in Snowsight.

## Supported reference functions

The Snowflake Native App Framework supports the following functions to perform different operations related to references:

- [SYSTEM$ADD\_REFERENCE](/sql-reference/functions/system_add_reference)
- [SYSTEM$GET\_ALL\_REFERENCES](/sql-reference/functions/system_get_all_references)
- [SYSTEM$GET\_REFERENCED\_OBJECT\_ID\_HASH](/sql-reference/functions/system_get_referenced_object_id_hash)
- [SYSTEM$REMOVE\_ALL\_REFERENCES](/sql-reference/functions/system_remove_all_references)
- [SYSTEM$REMOVE\_REFERENCE](/sql-reference/functions/system_remove_reference)
- [SYSTEM$SET\_REFERENCE](/sql-reference/functions/system_set_reference)
