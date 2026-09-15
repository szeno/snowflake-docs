# Enable resource

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

Enabling a resource is used to start ingesting data for a given resource.
`PUBLIC.ENABLE_RESOURCE` procedure is the entry point from the UI or worksheet to enable a resource.
It can be used after a resource was disabled or when a resource was created as disabled and now it is needed to enable it.

Calling this procedure requires the user has been assigned the `ADMIN` application role.
Phases are:

1. Initial validation
2. Custom validation
3. Custom logic before a resource is enabled
4. Marking a resource ingestion definition as enabled and creating new ingestion processes
5. Custom logic after a resource is created

## Initial validation

Initial validation is performed at the very beginning of the enable resource process, and checks:

- whether a resource with given id exists
- whether a resource with given id is already enabled

When a resource is already enabled, nothing is done and success response is returned.

## Custom validation

Custom validation is executed after initial validation, and is designed to be support customized connector-specific logic.
For example, it can be used to verify that a given resource still exists in a source system.

By default, it invokes `PUBLIC.ENABLE_RESOURCE_VALIDATE(resource_ingestion_definition_id)`,
which returns `'response_code': 'OK'`. It can be overwritten through the SQL script or by using
a `EnableResourceHandlerBuilder` to provide custom implementation of the `EnableResourceValidator` interface.

If the custom validation returns error, the next steps will not be executed and given error response will be returned from `ENABLE_RESOURCE` procedure.

## Custom logic before a resource is enabled

Custom logic can be specified and executed before a resource is enabled.

By default, it invokes `PUBLIC.PRE_ENABLE_RESOURCE(resource_ingestion_definition_id VARCHAR)`,
which returns `'response_code': 'OK'`. It can be overwritten through the SQL script or by using
a `EnableResourceHandlerBuilder` to provide custom implementation of the `PreEnableResourceCallback` interface.

If custom logic returns error, following steps will not be executed and an error response will be returned from `ENABLE_RESOURCE` procedure.

## Marking a resource ingestion definition as enabled and creating new ingestion processes

Within this step the resource ingestion definition’s `enabled` flag is changed to `true` and then
a new ingestion process is created for each ingestion configuration.
Ingestion processes are created with `SCHEDULED` status which means that the ingestion will start a while later.
When a new ingestion process is being created, the metadata column is inherited from the last finished process with given ingestion configuration id.

## Custom logic after a resource is enabled

Custom logic can be defined to be executed after a resource is enabled.

By default, it invokes `PUBLIC.POST_ENABLE_RESOURCE(resource_ingestion_definition_id VARCHAR)`,
which returns `'response_code': 'OK'`. It can be overwritten through the SQL script or by using
a `EnableResourceHandlerBuilder` to provide custom implementation of the `PostEnableResourceCallback` interface.

If custom logic returns error, given error response will be returned from `ENABLE_RESOURCE` procedure but
the process marking a resource ingestion definition as enabled and creating new ingestion processes will not be rolled back.

## Response

### Successful response

On procedure success, a response resembling the one below is returned:

> Copy code
>
> ```
> {
>   "response_code": "OK"
> }
> ```

### Error response

On procedure error, a response resembling the one below is returned:

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
- `ENABLE_RESOURCE_ERROR` - Something unexpected happened when updating the resource ingestion definition or when creating ingestion processes. All changes are rolled back.
