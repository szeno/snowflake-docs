# Disable resource

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

Disabling a resource is used to stop ingesting data for a given resource.
`PUBLIC.DISABLE_RESOURCE` procedure is the entry point from the UI or worksheet to disable a resource.

Calling this procedure requires the user to have the been assigned the `ADMIN` application role.

The disable resource process consists of several phases. Several of which are customizable but include reasonable defaults.
Phases are:

1. Initial validation
2. Custom logic before a resource is disabled
3. Finishing active ingestion processes and marking resource ingestion definition as disabled
4. Custom logic after a resource is created

## Initial validation

Initial validation is performed at the very beginning of the disable resource process, and checks:

- whether a resource with given id exists
- whether a resource with given id is already disabled

When a resource was previously disabled, nothing is done and success response is returned.

## Custom logic before a resource is disabled

This step can be used to implement custom logic before a resource is disabled.

By default, it invokes `PUBLIC.PRE_DISABLE_RESOURCE(resource_ingestion_definition_id VARCHAR)`,
which returns `'response_code': 'OK'`. It can be overwritten through the SQL script or by using
a `DisableResourceHandlerBuilder` to provide custom implementation of the `PreDisableResourceCallback` interface.

If custom logic returns error, the next steps will not be executed and given error response will be returned from `DISABLE_RESOURCE` procedure.

## Finishing active ingestion processes and marking resource ingestion definition as disabled

Within this step all ingestion processes with state `SCHEDULED` or `IN_PROGRESS` are completed so and the next iteration of ingestion will not be executed for a given resource.
Then the resource ingestion definition’s `enabled` flag is changed to `false`.

Note

The implementation of disable resource process does not stop currently executing ingestion. It only prevents executing
next iteration of ingestion. If stopping an ongoing ingestion is required, you must implement [Custom logic after a resource is disabled](#custom-logic-after-a-resource-is-disabled).

## Custom logic after a resource is disabled

It can be used to implement custom logic after a resource is disabled. For example, it can be used to stop ongoing ingestion for a given resource.

By default, it invokes `PUBLIC.POST_DISABLE_RESOURCE(resource_ingestion_definition_id VARCHAR)`,
which returns `'response_code': 'OK'`. It can be overwritten through the SQL script or by using
a `DisableResourceHandlerBuilder` to provide custom implementation of the `PostDisableResourceCallback` interface.

If custom logic returns an error, the following steps will not be executed and the given error response will be returned from `DISABLE_RESOURCE` procedure.

## Response

### Successful response

On procedure success, a response resembling below is returned:

> Copy code
>
> ```
> {
>   "response_code": "OK"
> }
> ```

### Error response

On procedure error, a response resembling below is returned:

> Copy code
>
> ```
> {
>   "response_code": "<ERROR_CODE>",
>   "message": "<error message>"
> }
> ```

Possible error codes include:

- `INVALID_INPUT` - Resource with given resource ingestion definition id does not exist.
- `DISABLE_RESOURCE_ERROR` - Something unexpected happened when updating the resource ingestion definition or when finishing ingestion processes. All changes are rolled back.
