# Access control

## Required access privileges

Calling the Snowpipe Streaming API requires a role with the following privileges:

| Object | Privilege |
| --- | --- |
| Table | INSERT. When schema evolution is enabled, the role also requires EVOLVE SCHEMA or OWNERSHIP. |
| Database | USAGE |
| Schema | USAGE |
| Pipe | OPERATE is required only for named (custom) pipes, not default pipes. |

Expand

Show lessSee more
