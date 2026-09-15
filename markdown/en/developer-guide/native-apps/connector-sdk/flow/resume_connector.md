# Resume connector

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

Resuming the connector is available after the wizard. It can be executed after the `Finalize Configuration` additionally with `Pause Connector`.
This step allows user to manipulate the status of the connector after it is launched. The entry point for this phase is a procedure
called `PUBLIC.RESUME_CONNECTOR()`. It can be customized by replacing it in SQL or by using `ResumeConnectorHandlerBuilder`.
The reverse process of resuming the connector, allowing user to suspend it, is [Available to accounts in all regions in all cloud providers (including…](/developer-guide/native-apps/connector-sdk/flow/pause_connector#label-connectors-native-sdk-pause-connector).

Calling this procedure requires the user to have the `ADMIN` application role assigned.

The resume connector step internally consists of several phases. Some of them are fully customizable and by default,
don’t do anything. The phases are as follows:

1. Privileges validation
2. Status validation
3. State validation
4. Status update (STARTING)
5. Internal callback
6. Resuming of Task Reactor (if Task Reactor is enabled)
7. Status update (STARTED)

## Requirements

Resume connector requires at least the following sql files to be executed during native app installation:

- `core.sql`
- `configuration/app_config.sql`
- `lifecycle/resume.sql`
- Recommended: `lifecycle/pause.sql`
- Recommended: `configuration/finalize_configuration.sql`

## Privileges validation

To resume connector the `EXECUTE TASK` privilege must be granted to the application.

This validation cannot be overwritten by using `ResumeConnectorHandlerBuilder` nor by overwriting stored procedure.
However, it is possible to implement a custom handler.

## Status validation

To resume the connector the internal status of the connector needs to be `PAUSED`.

This validation cannot be overwritten by using `ResumeConnectorHandlerBuilder` nor by overwriting stored procedure.
However, it is possible to implement a custom handler.

## State validation

In case there are some additional custom validations that need to be satisfied there is a `PUBLIC.RESUME_CONNECTOR_VALIDATE()`
stored procedure, which can be customized by the user. By default, this procedure just returns `'response_code': 'OK'`.
The procedure can be customized by overwriting through the SQL or by using `ResumeConnectorHandlerBuilder` and providing a custom implementation of the
`ResumeConnectorStateValidator` interface.

## Internal callback

Internal callback is another customizable step. By default, it invokes `PUBLIC.RESUME_CONNECTOR_INTERNAL()`, which returns `'response_code': 'OK'`.
This procedure allows the user to perform any additional duties needed when resuming connector. For example resuming additional connector specific tasks.
It can be overwritten through the SQL script or by using a `ResumeConnectorHandlerBuilder` to provide custom implementation of the `ResumeConnectorCallback` interface.

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

When the procedure successfully resumes all tasks in the background and changes status tocSTARTED, then the `Connector successfully resumed.`
message will be returned directly from ResumeConnectorHandler method body. It is recommended to use the following format:

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
>   "message": "error message"
> }
> ```

Possible error codes include:

- `INVALID_CONNECTOR_STATUS` - The procedure was called on connector with state different than `[PAUSED, STARTING]`
- `CONNECTOR_STATUS_NOT_FOUND` - Connector status record does not exist in database (independent of user’s input at this stage - an internal error)
- `ROLLBACK_CODE` - An error occurred, but the changes were successfully reverted.
- `INTERNAL_ERROR` - Something went wrong internally, the message should be descriptive
- `UNKNOWN_ERROR_CODE` - An unknown error occurred and the connector is now in an unspecified state
