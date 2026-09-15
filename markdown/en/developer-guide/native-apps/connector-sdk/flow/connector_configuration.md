# Connector configuration

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

Connector configuration is the first required step of the wizard phase. It ensures that the connector
has the configuration of the objects common between all connector types, regardless of the actual
source system and domain. The procedure called `PUBLIC.CONFIGURE_CONNECTOR(config VARIANT)`
is the entry point from the UI or worksheet to do so. When overwriting with custom logic, keep in mind that,
this procedure needs to be replaced, because it points to the `ConfigureConnectorHandler.configureConnector` static method in Java as a handler.

Calling this procedure requires the user to have the `ADMIN` application role assigned.

The connector configuration step internally consists of several phases. Some of them are fully customizable and by default,
don’t do anything. The phases are as follows:

1. Status validation
2. Fields validation
3. Input validation
4. Configuration update
5. Internal callback
6. Status update

## Requirements

The connector configuration requires at least the following SQL files to be executed during native app installation:

- `core.sql`
- `configuration/app_config.sql`
- `configuration/connector_configuration.sql`

### Status validation

To perform the connector configuration, the internal status of the connector needs to be `CONFIGURING`.
This validation cannot be overwritten by using `ConfigureConnectorHandlerBuilder` nor by overwriting a stored procedure. However,
it is possible to implement a custom handler, which will not have this kind of validation.

### Fields validation

The connector configuration needs to contain a set of specific fields. All of them are optional, but any other field causes an exception to be thrown.
The allowed keys are:

- `warehouse`
- `operational_warehouse`
- `cortex_warehouse`
- `destination_database`
- `destination_schema`
- `global_schedule`
- `data_owner_role`
- `cortex_user_role`
- `agent_username`
- `agent_role`

#### Warehouse

Warehouse is used by the Connector to run the scheduler, execute tasks and run queries.

#### Operational\_warehouse

Occasionally, the connector has a need to use a separate warehouse for performing ingestion work.
A separate warehouse will allow the connector to split the ingestion operations from the main warehouse,
which is used for internal connector operations.

#### Cortex\_warehouse

Occasionally, the connector has a need to use the Cortex AI. That use may require a separate warehouse
to split the operations from the main warehouse, which is used for internal connector operations.

#### Destination\_database

The destination database is used to store the data ingested by the connector. This database should be outside
of the connector. It can be an existing database, however the connector needs to have write privileges on it.
It can be also a newly created database, however, this won’t happen automatically and has to be implemented as a part of the
internal callback during connector configuration or configuration finalization.

#### Destination\_schema

The destination schema will be the schema used in the destination\_database above.

#### Global\_schedule

This property defines the running schedule for the scheduler task. Currently, the scheduler will only process resources with their own `scheduleType=GLOBAL`.
The value for this property should be similar to the one below:

Copy code

```
"global_schedule": {
    "scheduleType": "CRON",
    "scheduleDefinition": "*/10 * * * *"
}
```

#### Data\_owner\_role

Role that can be used to give ownership of the sync database for retaining the data upon connector un-installation.

#### Cortex\_user\_role

Role that can access the Cortex features available in the connector.

#### Agent\_username

Username used by the push based connector’s agent when connecting with Snowflake.

#### Agent\_role

Role used by the push based connector’s agent when connecting with Snowflake.

## Input validation

Input needs to be a valid `Variant`, In addition, the SDK provides
an internal stored procedure called: `PUBLIC.CONFIGURE_CONNECTOR_VALIDATE(config VARIANT)`. By default,
this procedure just returns `'response_code': 'OK'`, however it can be changed by overwriting this stored procedure.
Alternatively it can be customized using `ConfigureConnectorHandlerBuilder` and providing a custom implementation of the
`ConfigureConnectorValidator` interface.

## Configuration update

Once the validations are passed successfully configuration is saved to the internal `APP_CONFIG` table.
The service responsible for this saves the provided `Variant` under the `connector_configuration` key.

## Internal callback

Internal callback is another customizable step. By default, it invokes `PUBLIC.CONFIGURE_CONNECTOR_INTERNAL(config VARIANT)`,
which returns `'response_code': 'OK'`. It can be overwritten through the SQL script or by using
a `ConfigureConnectorHandlerBuilder` to provide custom implementation of the `ConfigureConnectorCallback` interface.

## Status update

When all the above phases are completed successfully the internal status of the Connector will be updated to:

Copy code

```
{
    "status": "CONFIGURING",
    "configurationStatus": "CONFIGURED"
}
```

For a diagram of state transitions, see [Connector flow](/developer-guide/native-apps/connector-sdk/flow/overview).

### Response

#### Successful response

If the procedure finishes successfully it will return a response in the following format:

> Copy code
>
> ```
> {
>   "response_code": "OK",
> }
> ```

#### Error response

In case of an error the response will follow the below format:

> Copy code
>
> ```
> {
>   "response_code": "<ERROR_CODE>",
>   "message": "<error message>"
> }
> ```

Possible error codes include:

- `INVALID_CONNECTOR_STATUS` - The procedure was called on already configured connector
- `CONNECTOR_CONFIGURATION_PARSING_ERROR` - Given configuration is not a valid JSON
- `CONNECTOR_STATUS_NOT_FOUND` - Connector status record does not exist in database
- `CONNECTOR_STATUS_PARSING_ERROR` - Value stored in table `APP_STATE` under `connector_status` key has incorrect format and cannot be parsed by the application
