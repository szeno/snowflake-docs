# Access control

Snowpipe Streaming uses the default role of the user unless you specify another role. SDK users set the `role` property in the [client configuration](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-configurations). REST API users add a role scope to the JWT, as described in [Use a non-default role](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-rest-api#use-a-non-default-role). Whichever role you use must hold the privileges in the following section.

## Required access privileges

Calling the Snowpipe Streaming API requires a role with the following privileges:

| Object | Privilege |
| --- | --- |
| Table | INSERT. When schema evolution is enabled, the role also requires EVOLVE SCHEMA or OWNERSHIP. |
| Database | USAGE |
| Schema | USAGE |
| Pipe | OPERATE is required only for named (custom) pipes, not default pipes. |
| External volume | USAGE, required when ingesting into an Iceberg table that uses an external volume you manage. This isn’t required for Iceberg tables that use Snowflake storage. |

Expand

Show lessSee more
