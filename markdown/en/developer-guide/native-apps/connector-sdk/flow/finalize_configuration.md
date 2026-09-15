# Finalize configuration

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

Finalize configuration is the last step of the Wizard, it comes directly after `connection configuration`.
This step allows the user to provide any custom configuration that was not included during the previous steps of the configuration.
Furthermore, it can be used to do some final touches when it comes to configuration, like creating the sink database, starting task reactor etc.
The entry point for this phase is a procedure called `PUBLIC.FINALIZE_CONNECTOR_CONFIGURATION(CUSTOM_CONFIGURATION VARIANT)`.
It can be customized by replacing it in SQL or by using `FinalizeConnectorHandlerBuilder`.
By default, the provided `custom_configuration` is NOT persisted in the database,
so if it’s required by the design, the configuration must be saved in one of the extension methods
(most likely in the `FINALIZE_CONNECTOR_CONFIGURATION_INTERNAL`).

Calling this procedure requires the user to have the `ADMIN` application role assigned.

The finalize configuration step internally consists of several phases. Some of them are fully customizable and by default,
don’t do anything. The phases are as follows:

1. Status validation
2. Input validation
3. Source validation
4. Internal callback
5. Status update

## Requirements

Finalize configuration requires at least the following sql files to be executed during native app installation:

- `core.sql`
- `configuration/finalize_configuration.sql`
- Recommended: `configuration/app_config.sql`

## Status validation

To perform connector finalization the internal status of the connector needs to be `CONFIGURING`, with configuration status `CONNECTED`.

This validation cannot be overwritten by using `FinalizeConnectorHandlerBuilder` nor by overwriting stored procedures.
However, it is possible to implement a custom handler, which will not have this kind of validation.

## Input validation

Input needs to be a valid `Variant`. IN addition, there are custom validations that need to be satisfied. One stored procedure,
`PUBLIC.FINALIZE_CONNECTOR_CONFIGURATION_VALIDATE(CUSTOM_CONFIGURATION VARIANT)` stored can be customized by the user.
By default, this procedure just returns `'response_code': 'OK'`.
Customize it by overwriting the SQL or by using `FinalizeConnectorHandlerBuilder` and providing a custom implementation of the
`FinalizeConnectorValidator` interface.

## Source validation

Once the validations are passed, the procedure `PUBLIC.VALIDATE_SOURCE(CUSTOM_CONFIGURATION VARIANT)` connects to an external source.
In some cases this procedure can be the same as the `TEST_CONNECTION` procedure that was executed during connection configuration.
However, `TEST_CONNECTION` is designed to just check some basic connectivity, while `VALIDATE_SOURCE` is a procedure
that can require some additional configuration. For example, checking permissions to a specific resource in the source system.
The default implementation of `VALIDATE_SOURCE` returns `'response_code': 'OK'`. This default implementation can be overwritten with
SQL or by implementing the `SourceValidator` interface using `FinalizeConnectorHandlerBuilder`.

## Internal callback

Internal callback is a customizable step that invokes `PUBLIC.FINALIZE_CONNECTOR_CONFIGURATION_INTERNAL(CUSTOM_CONFIGURATION VARIANT)`,
which returns `'response_code': 'OK'` by default. This procedure allows the user to perform any additional configurations needed by the connector.
For example, saving the provided `custom_configuration` in the `STATE.CONNECTOR_CONFIGURATION` table.
It can be overwritten through the SQL script or by using a `FinalizeConnectorHandlerBuilder` to provide custom implementation of the `FinalizeConnectorCallback` interface.

## Status update

When all the above phases are completed successfully the internal status of the Connector will be updated to:

Copy code

```
{
    "status": "STARTED",
    "configurationStatus": "FINALIZED"
}
```

For the whole diagram of state transitions, see [Connector flow](/developer-guide/native-apps/connector-sdk/flow/overview).

### Response

#### Successful response

If the procedure finishes successfully it will return a response from `FINALIZE_CONNECTOR_CONFIGURATION_INTERNAL` procedure. We recommend using the following format:

> Copy code
>
> ```
> {
>   "response_code": "OK"
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

Possible error codes:

- `INVALID_CONNECTOR_STATUS` - The procedure was called on already configured connector
- `INVALID_CONNECTOR_CONFIGURATION_STATUS` - The procedure was called when the `CONFIGURATION_STATUS` was different from `CONNECTED`
- `CONNECTOR_STATUS_NOT_FOUND` - Connector status record does not exist in database (independent of user’s input at this stage - an internal error)
- `INTERNAL_ERROR` - Something went wrong internally, the message should be descriptive
