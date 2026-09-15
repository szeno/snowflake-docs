# Update the connection configuration

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

Updating the connection configuration is a step that can be called directly after [pausing the connector](/developer-guide/native-apps/connector-sdk/flow/pause_connector). This step allows the user
to update properties required to establish a connection with the source system to start ingesting data into Snowflake.
When overwriting with custom logic, this procedure needs to be replaced, to specify a custom Java handler.

Calling this procedure requires the user to have the `ADMIN` application role assigned.

The connection configuration step internally consists of several phases. Some of them are fully customizable and by default,
don’t do anything. The phases are as follows:

1. Status validation
2. Input validation
3. Draft callback
4. Draft connection validation
5. Configuration update
6. Internal callback
7. Connection validation
8. Status update

## Requirements

Connection configuration requires at least the following sql files to be executed during Native App installation:

- `core.sql`
- `configuration/app_config.sql`
- `configuration/connection_configuration.sql`
- `configuration/update_connection_configuration.sql`

In case of this feature there is additional requirement dependent on the SDK user:

- Custom implementation of `PUBLIC.TEST_DRAFT_CONNECTION()` and `PUBLIC.TEST_CONNECTION()` procedures

## Status validation

To perform connection configuration update the internal status of the connector needs to be `PAUSED`.

This validation cannot be overwritten by using `UpdateConnectionConfigurationHandlerBuilder` nor by overwriting stored procedure.
However, it is possible to implement a custom handler, which will not have this kind of validation.

## Input validation

Input needs to be a `variant` containing a map of properties, however this is not enough sometimes. For that reason the SDK provides
an internal stored procedure called: `PUBLIC.UPDATE_CONNECTION_CONFIG_VALIDATE(config VARIANT)`. By default,
this procedure just returns `'response_code': 'OK'`, but when overwriting it can update the provided config during validation.
This feature enables custom logic like for example trimming the input, conversion to upper/lower case etc.
To return config transformed in any way the response needs to contain additional `"config"` property in the response `Variant`,
this property should contain the updated config as `Variant`.
The procedure can be customized by overwriting through the SQL or by using `UpdateConnectionConfigurationHandlerBuilder` and providing custom implementation of the
`ConnectionConfigurationInputValidator` interface.

The valid response from the custom implementation with transformation looks like this:

Copy code

```
{
    "response_code" : "OK",
    "config": {
        "key1": "value1",
        "key2": "value2"
    }
}
```

## Configuration update

Once the validations are passed successfully, configuration will be saved to the internal `APP_CONFIG` table.
Service responsible for this will save the provided `Variant` under the `connection_configuration` key.
This configuration has to be successfully validated by internal draft callback and draft connection validation to be updated,
the set of provided properties is completely up to the user.

## Internal draft callback

Internal callback is another customizable step. By default, it invokes `PUBLIC.DRAFT_CONNECTION_CONFIGURATION_INTERNAL(connection_configuration VARIANT)`,
which returns `'response_code': 'OK'`. For example it can be used to alter other procedures by granting them external access integration.
It can be overwritten through the sql script or by using a `ConnectionConfigurationHandlerBuilder` to provide custom implementation of the `ConnectionConfigurationCallback` interface.

## Draft connection validation

This step will trigger a `PUBLIC.TEST_DRAFT_CONNECTION(connection_configuration VARIANT)` procedure. This procedure tries to query the source system
for the data using data from input parameter as connection configuration. This procedure is not implemented by default and needs to be provided by the
SDK user. Additionally, a `ConnectionValidator` interface implementation can be provided to the `UpdateConnectionConfigurationHandlerBuilder` to
customize this phase. In this case, there is no need to implement stored procedure. The recommendation is to perform just a minimal connectivity check
in this procedure to ensure that external access capabilities of Snowflake were configured correctly and the Connector has all required privileges to use them.

## Internal callback

Internal callback is another customizable step. By default, it invokes `PUBLIC.SET_CONNECTION_CONFIGURATION_INTERNAL(connection_configuration VARIANT)`,
which returns `'response_code': 'OK'`. For example it can be used to alter other procedures by granting them external access integration.
It can be overwritten through the sql script or by using a `ConnectionConfigurationHandlerBuilder` to provide custom implementation of the `ConnectionConfigurationCallback` interface.

## Connection validation

This step will trigger a `PUBLIC.TEST_CONNECTION` procedure. This procedure has twinning action to the `PUBLIC.TEST_DRAFT_CONNECTION(connection_configuration VARIANT)`
but has no input parameter and should be used for testing the official connection using a configuration saved in the database.

## Viewing the configuration

There is a `PUBLIC.GET_CONNECTION_CONFIGURATION()` procedure available to the `ADMIN` and `VIEWER` users that
returns a current connection configuration from the internal table.

## Response

### Successful response

If the procedure finishes successfully it returns a response from `TEST_CONNECTION` procedure. We recommend using the following format:

Copy code

```
{
  "response_code": "OK"
}
```

### Error response

In case of an error the response follows the below format:

Copy code

```
{
  "response_code": "<ERROR_CODE>",
  "message": "<error message>"
}
```

Possible error codes include:

- `INVALID_CONNECTOR_STATUS` - Invalid connector status. Expected status: `[PAUSED]`
- `INTERNAL_ERROR` - Something went wrong internally, the message should be descriptive
- `PROCEDURE_NOT_FOUND` - Procedure which was called does not exist. In this case it’s about `TEST_CONNECTION` and `TEST_DRAFT_CONNECTION` procedure mostly
- `UNKNOWN_SQL_ERROR` - This error occurs when something unexpected happen when calling internal procedures
- `INVALID_RESPONSE` - This error occurs when response received from internal procedure does not contain `response_code` or an error response does not contain `message`, but contains `response_code`
- `UNKNOWN_ERROR` - It means that something unexpected went wrong - message of thrown exception is forwarded
- Custom error codes received from `TEST_DRAFT_CONNECTION()` procedure - defined by connector developer
- Custom error codes received from `DRAFT_CONNECTION_CONFIGURATION_INTERNAL()` procedure - defined by connector developer
- Custom error codes received from `TEST_CONNECTION()` procedure - defined by connector developer
- Custom error codes received from `SET_CONNECTION_CONFIGURATION_INTERNAL()` procedure - defined by connector developer
