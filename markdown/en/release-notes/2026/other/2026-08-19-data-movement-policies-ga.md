# August 19, 2026: Data movement policies (*General availability*)

With this release, data movement policies are now generally available for Enterprise Edition (or higher). Data movement policies are part of Snowflake’s data exfiltration protection controls. These SQL-style conditional policies can help you limit, alert on, or block data movement operations based on specific movement types.

Data movement policies support the following movement types:

- `COPY_INTO_EXTERNAL_STAGE`: Export or `COPY INTO` to an external stage.
- `COPY_INTO_INTERNAL_STAGE`: `COPY INTO` to a Snowflake-managed internal stage.
- `SNOWSIGHT_UI`: Data access originating from Snowsight.
- `AGENT_ACCESS`: Data access through an agent or MCP-style client.
- `UI_DOWNLOAD`: Query result downloads from the Snowsight UI. When an enforce rule threshold is met, the download button is disabled.
- `PROGRAMMATIC_FETCH`: Programmatic data access from a driver, connector, SnowSQL, Snowflake CLI, SQL API, or stored procedure.

Policies can be attached to tags at column, table, schema, or database scope, or directly to the account as a baseline policy.

For more information, see [Data movement policies](/user-guide/data-movement-policies).
