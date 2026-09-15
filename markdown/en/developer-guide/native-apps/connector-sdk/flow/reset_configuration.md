# Reset configuration

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

Resetting the configuration is possible only in the wizard phase, and it can be done by calling the `PUBLIC.RESET_CONFIGURATION()` procedure.
This procedure resets all prerequisites as not completed, deletes previously saved configuration, and sets the connector status to `INSTALLED`.
It can be used if there is a need to reconfigure the connector (that is, go through the [Prerequisites](/developer-guide/native-apps/connector-sdk/flow/prerequisites), [Connection configuration](/developer-guide/native-apps/connector-sdk/flow/connection_configuration), or [Connector configuration](/developer-guide/native-apps/connector-sdk/flow/connector_configuration) step again).
Connectors can only be reconfigured if you have not completed [Finalize configuration](/developer-guide/native-apps/connector-sdk/flow/finalize_configuration) step.
Connector reconfiguration can be customized using SQL or `ResetConfigurationHandlerBuilder`.

Only users assigned the `ADMIN` application role can call the `PUBLIC.RESET_CONFIGURATION()` procedure.

Resetting configuration consists of the following configurable phases, which by default have no effect:

1. Status validation
2. State validation
3. Internal callback
4. SDK callback
5. Status update

## Requirements

Configuration reset requires executing the following SQL files during native app installation:

- `core.sql`
- `configuration/app_config.sql`
- `configuration/prerequisites.sql`
- `configuration/connector_configuration.sql`
- `configuration/connection_configuration.sql`
- `configuration/reset_configuration.sql`

## Status validation

To reset the configuration, the connector needs to be in the `CONFIGURING` status. The configuration status needs to be equal to one of the following:
`INSTALLED`, `PREREQUISITES_DONE`, `CONFIGURED`, or `CONNECTED`. For the complete diagram of status transitions, see [Connector flow](/developer-guide/native-apps/connector-sdk/flow/overview).

Validation cannot be overwritten using `ResetConfigurationHandlerBuilder` or overwriting stored procedure.
However, it is possible to implement a custom handler, which will not have this kind of validation.

## State validation

The state validation phase is customizable and, by default, executes the `PUBLIC.RESET_CONFIGURATION_VALIDATE()` procedure, which returns `'response_code': 'OK'`.
This procedure can be customized by replacing the procedure using SQL or by implementing the `ResetConfigurationValidator` interface.

## Internal callback

The internal callback phase is customizable and, by default, executes the `PUBLIC.RESET_CONFIGURATION_INTERNAL()` procedure, which returns `'response_code': 'OK'`.
This procedure supports executing custom logic required when resetting the configuration. For example, deleting custom configuration.
This procedure can be customized by replacing the procedure using SQL or by implementing the `ResetConfigurationCallback` interface.

## SDK callback

SDK callback is used to update the SDK-controlled components.
This step consists of the following processes, which are executed as a single transaction:

1. Set all prerequisites as not completed
2. Delete connector configuration
3. Delete connections configuration

### Set all prerequisites as not completed

During this step the `IS_COMPLETED` column is set to false for all records in the internal `PREREQUISITES` table.

### Delete connector configuration

During this step, `connector_configuration` is deleted from the internal `APP_CONFIG` table.

### Delete connector configuration

During this step, `connection_configuration` is deleted from the internal `APP_CONFIG` table.

The SDK callback cannot be overwritten using the `ResetConfigurationHandlerBuilder` or overwriting the stored procedure.
It is possible to implement a custom handler, which will not have this callback.

Note

The `PUBLIC.CONNECTOR_CONFIGURATION` view returns the current configuration from the internal `APP_CONFIG` table.
The `PUBLIC.PREREQUISITES` view returns prerequisites from the internal `PREREQUISITES` table. Both views are available to the `ADMIN` and `VIEWER` application roles.

## Status update

When complete, this step sets the internal status of the connector to:

Copy code

```
{
    "status": "CONFIGURING",
    "configurationStatus": "INSTALLED"
}
```

## Response

### Successful response

If the procedure completes successfully it returns an `OK` response code as shown below:

Copy code

```
{
  "response_code": "OK"
}
```

### Error response

On error, the following response is returned:

Copy code

```
{
  "response_code": "<ERROR_CODE>",
  "message": "<error message>"
}
```

Possible error codes include:

- `INVALID_CONNECTOR_STATUS` - Invalid connector status. Expected status: `[CONFIGURING]`.
- `INVALID_CONNECTOR_CONFIGURATION_STATUS` - Invalid connector status. Expected statuses: `[INSTALLED, PREREQUISITES_DONE, CONFIGURED, CONNECTED]`.
- `INTERNAL_ERROR` - Something went wrong internally, the message should be descriptive.
- `PROCEDURE_NOT_FOUND` - The procedure that was called does not exist.
- `UNKNOWN_SQL_ERROR` - This error occurs when something unexpected happen when calling internal procedures.
- `INVALID_RESPONSE` - This error occurs when response received from internal procedure does not contain `response_code` or an error response does not contain `message`, but contains `response_code`.
- `UNKNOWN_ERROR` - It means that something unexpected went wrong (message of thrown exception is forwarded).
- Custom error codes received from `RESET_CONFIGURATION_INTERNAL` and `RESET_CONFIGURATION_VALIDATE` procedures - defined by the connector developer.
