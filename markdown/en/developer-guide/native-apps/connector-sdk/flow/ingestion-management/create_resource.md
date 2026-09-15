# Create resource

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

Creating a resource is required in order to define and schedule data ingestion from a source system.
The `PUBLIC.CREATE_RESOURCE` procedure is the entry point from the UI or worksheet to create a new resource.

Calling this procedure requires the user to have the `ADMIN` application role assigned.

The resource creation process consists of several phases, several of which are customizable but include reasonable defaults.
Phases are:

1. Initial validation
2. Custom validation
3. Custom logic before a resource is created
4. Creation of resource ingestion definition and ingestion processes
5. Custom logic after a resource is created

## Initial validation

Initial validation is performed at the very beginning of the resource creation process, and checks:

- whether the given input data represents a valid resource ingestion definition object
- whether a resource with given `id` and `resourceId` does not exist

## Custom validation

Custom validation is executed after initial validation and is designed to support customized connector-specific logic.
For example, it can be used to verify that a given resource exists in a source system.

By default, it invokes `PUBLIC.CREATE_RESOURCE_VALIDATE(resource VARIANT)`,
which returns `'response_code': 'OK'`. It can be overwritten using a SQL script or by using
a `CreateResourceHandlerBuilder` to provide custom implementation of the `CreateResourceValidator` interface.

If the custom validation returns an error, the following steps will not be executed and the error response will be returned from the `CREATE_RESOURCE` procedure.

## Custom logic before a resource is created

You can implement custom logic before a resource is created and scheduled.
For example, it can be used to create a new destination table where ingestion data will be saved.

By default, it invokes `PUBLIC.PRE_CREATE_RESOURCE(resource VARIANT)`,
which returns `'response_code': 'OK'`. It can be overwritten through the SQL script or by using
a `CreateResourceHandlerBuilder` to provide custom implementation of the `PreCreateResourceCallback` interface.

If custom logic returns an error, the follow-on steps will not be executed and the provided error response will be returned from the `CREATE_RESOURCE` procedure.

## Creation of resource ingestion definition and ingestion processes

During this step a new record is added to `STATE.RESOURCE_INGESTION_DEFINITION` table.
Additionally, when a resource should be initially enabled (`enabled` parameter equals `true`),
a new ingestion process is added for each provided ingestion configuration.
Ingestion processes are created with `SCHEDULED` status which means that the ingestion will begin later.
If the `enabled` flag is set to `false`, no ingestion process is created and the `ENABLE_RESOURCE` procedure must be called to enable ingestion.

## Custom logic after a resource is created

Custom logic can be specified after a resource is created and scheduled.
For example, it can be used to create a new destination table where ingestion data will be saved.

By default, it invokes `PUBLIC.POST_CREATE_RESOURCE(id VARCHAR)`,
which returns `'response_code': 'OK'`. It can be overwritten through the SQL script or by using
a `CreateResourceHandlerBuilder` to provide custom implementation of the `PostCreateResourceCallback` interface.

If custom logic returns an error, the given error response will be returned from the `CREATE_RESOURCE` procedure but the creation of resource ingestion definition and ingestion processes will not be rolled back.

## Response

### Successful response

When successful, the procedure returns a response resembling:

> Copy code
>
> ```
> {
>   "response_code": "OK",
>   "id": "<new resource ingestion definition id>"
> }
> ```

The `id` returned in the response is an id of resource ingestion definition and can be used to enable, disable or update the resource afterwards.

### Error response

On error, the procedure returns a response resembling:

> Copy code
>
> ```
> {
>   "response_code": "<ERROR_CODE>",
>   "message": "<error message>"
> }
> ```

Possible error codes include:

- `INVALID_INPUT` - Provided procedure’s arguments are invalid and it is not possible to create a valid resource object or a resource with given id already exists.
- `CREATE_RESOURCE_ERROR` - Something unexpected happened when creating the new resource ingestion definition or when creating ingestion processes. All changes are rolled back.
