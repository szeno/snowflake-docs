# Update the warehouse

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

Warehouse update is a step which can be called directly after the [Pause connector](/developer-guide/native-apps/connector-sdk/flow/pause_connector) step. This step allows the user
to update the warehouse, set up during `Connector Configuration`, which is used for running SDK-controlled tasks.
When overwriting with custom logic, this procedure needs to be replaced, to specify a custom Java handler.

Calling this procedure requires the user to have the `ADMIN` application role assigned.

Warehouse update step internally consists of several phases. Some of them are fully customizable and by default,
don’t do anything. The phases are as follows:

1. Status validation
2. Input validation
3. Internal callback
4. SDK callback
5. Configuration update

## Requirements

Warehouse configuration requires at least the following sql files to be executed during native app installation:

- `core.sql`
- `configuration/app_config.sql`
- `configuration/connector_configuration.sql`
- `configuration/update_warehouse.sql`

## Status validation

To perform the warehouse update the internal status of the connector needs to be `PAUSED`.

This validation cannot be overwritten neither using the `UpdateWarehouseHandlerBuilder`, nor by overwriting the stored procedure.
However, it is possible to implement a custom handler, which will not have this kind of validation.

## Input validation

Input needs to be a `String` containing the new warehouse. This provided warehouse is then validated using an implementation of `UpdateWarehouseInputValidator`.
By default the following validations are performed, each throwing an exception if the required criteria are not met:

1. Validating if the provided warehouse is a valid Snowflake Identifier.
2. Validating if the new warehouse is different than the already configured one.
3. Validating if the application instance can access the new warehouse (by using the `SHOW WAREHOUSES` query).

This input validation step can only be customized by using the `UpdateWarehouseHandlerBuilder` and building a new, custom handler instance.

## Internal callback

Internal callback is also a customizable step.
By default it invokes the `PUBLIC.UPDATE_WAREHOUSE_INTERNAL` procedure, whose default implementation returns `'response_code': 'OK'`.
This step can be used to provide custom logic for the warehouse update process, e.g. altering the tasks created by the application developer.
The callback can be overwritten through the sql script or by using the `UpdateWarehouseHandlerBuilder` to provide a custom implementation of the `UpdateWarehouseCallback` interface.

## SDK callback

SDK callback is similar to the internal callback phase. Its purpose is to update the SDK-controlled components, e.g. tasks created by the Task Reactor.

This validation cannot be overwritten by using the `UpdateWarehouseHandlerBuilder`, nor by overwriting the stored procedure.
It is possible to implement a custom handler, which will not have this kind of validation, however it is highly discouraged.

## Configuration update

Once the validations and callbacks have passed successfully, the new warehouse will be saved to the internal `APP_CONFIG` table.
Service responsible for this will save the provided warehouse under the `connector_configuration` key, replacing the previously configured value.

## Viewing the configuration

There is a `PUBLIC.CONNECTOR_CONFIGURATION` view available to the `ADMIN` and `VIEWER` application roles, which
returns current configuration from the internal `APP_CONFIG` table.

## Response

### Successful response

If the procedure finishes successfully it returns a response with the `OK` response code:

Copy code

```
{
  "response_code": "OK"
}
```

### Error response

In case of an error the response has the following format:

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
- `PROCEDURE_NOT_FOUND` - Procedure which was called does not exist
- `UNKNOWN_SQL_ERROR` - This error occurs when something unexpected happen when calling internal procedures
- `INVALID_RESPONSE` - This error occurs when response received from internal procedure does not contain `response_code` or an error response does not contain `message`, but contains `response_code`
- `UNKNOWN_ERROR` - It means that something unexpected went wrong (message of thrown exception is forwarded)
- `EMPTY_IDENTIFIER` - Provided identifier is a NULL value or an empty String
- `INVALID_IDENTIFIER` - Provided warehouse identifier is not valid
- `WAREHOUSE_ALREADY_USED` - Provided warehouse is already used by the application
- `INACCESSIBLE_WAREHOUSE` - Provided warehouse cannot be used access by the application instance
- Custom error codes received from `UPDATE_WAREHOUSE_INTERNAL` procedure - defined by the connector developer
