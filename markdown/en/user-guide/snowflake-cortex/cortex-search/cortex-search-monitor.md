# Monitor Cortex Search requests

Cortex Search logs detailed information about search requests for monitoring and debugging purposes.
With request logging enabled, you can review query patterns, response times, and request details
for a Cortex Search Service.

## Information collected in request logs

Cortex Search request logs include the following information:

- Operation type (for example, QUERY)
- Full request body, including query text and parameters
- Response status code
- Response time in milliseconds
- Database, schema, and service name
- User, role, and session information

## Enable request logging

To collect request logs for a Cortex Search Service, enable the `REQUEST_LOGGING` property on
the service.

You can enable request logging when you create a service:

Copy code

```
CREATE CORTEX SEARCH SERVICE my_search_service
  ON text_col
  ATTRIBUTES category
  WAREHOUSE = my_wh
  TARGET_LAG = '1 hour'
  REQUEST_LOGGING = TRUE
AS (SELECT * FROM my_table);
```

You can also enable request logging on an existing service:

Copy code

```
ALTER CORTEX SEARCH SERVICE my_search_service SET REQUEST_LOGGING = TRUE;
```

To disable request logging:

Copy code

```
ALTER CORTEX SEARCH SERVICE my_search_service SET REQUEST_LOGGING = FALSE;
```

## Operational considerations

### Volume of log data

Each logged Cortex Search request produces one event row in
`SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS`. How much data you accumulate depends on your request
rate and how long logging stays enabled. Set retention and storage to match the log volume you
expect to keep.

### Cost considerations

Data stored in `SNOWFLAKE.LOCAL` tables incurs Snowflake [storage charges](/user-guide/cost-understanding-data-storage).
Querying request logs with SQL uses warehouse resources like any other query.

### Query latency

Enabling request logging does not affect the latency of Cortex Search query requests.

## Access Cortex Search request logs

The request logs for a Cortex Search Service are stored in the event table
`SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS`. For what the table stores, permissions, and the recommended query path, see [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events). You can access logs using a table function or by querying the event table directly.

### Using GET\_AI\_OBSERVABILITY\_EVENTS

Users with the `MONITOR` privilege on a Cortex Search Service can view
request logs for that service using [GET\_AI\_OBSERVABILITY\_EVENTS](/sql-reference/functions/get_ai_observability_events-snowflake-local).
Pass `CORTEX SEARCH SERVICE` as the fourth argument (`agent_type`).

1. **Grant MONITOR privilege**: Grant the MONITOR privilege on the Cortex Search Service
   to the role that will use the function:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   GRANT MONITOR ON CORTEX SEARCH SERVICE <service_name> TO ROLE <role_name>;
   ```
2. **Query observability events**: Call `snowflake.local.get_ai_observability_events`
   using the role with the MONITOR privilege:

   Copy code

   ```
   USE ROLE <role_name>;
   SELECT * FROM TABLE(snowflake.local.get_ai_observability_events(
     '<database_name>',
     '<schema_name>',
     '<service_name>',
     'CORTEX SEARCH SERVICE'
   ));
   ```

### Querying the event table as ACCOUNTADMIN

Users with the ACCOUNTADMIN role can query the event table directly:

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT * FROM snowflake.local.ai_observability_events
WHERE observed_timestamp > TIMESTAMPADD(minute, -10, CURRENT_TIMESTAMP())
  AND record['name'] = 'CORTEX_SEARCH_REQUEST';
```

Note

Users with the ACCOUNTADMIN role can query the `snowflake.local.ai_observability_events` table
and access the request events for all Cortex Search Services in the account.

## Access control and permissions

To view Cortex Search request logs, users must have one of the following:

- OWNERSHIP or MONITOR privilege on the Cortex Search Service
- The ACCOUNTADMIN role (for direct event table access)

The following example uses the ACCOUNTADMIN role to create a new role `search_monitoring_role`
with the required permissions to view Cortex Search request logs:

Copy code

```
USE ROLE ACCOUNTADMIN;
CREATE ROLE search_monitoring_role;
GRANT MONITOR ON CORTEX SEARCH SERVICE my_search_service TO ROLE search_monitoring_role;
GRANT ROLE search_monitoring_role TO USER some_user;
```

## Output schema

The `snowflake.local.get_ai_observability_events` function returns
a table with the following columns:

**Columns**

| Column name | Data type | Description |
| --- | --- | --- |
| TIMESTAMP | TIMESTAMP\_NTZ(9) | Time of the event |
| START\_TIMESTAMP | TIMESTAMP\_NTZ(9) | Start time of the event (may be NULL) |
| TRACE | OBJECT | Trace information for the event (may be NULL) |
| RESOURCE\_ATTRIBUTES | OBJECT | Contains session, user, and role information including session ID, user ID, user name, role ID, and role name |
| RECORD\_TYPE | STRING | Type of record, typically ‘EVENT’ for Cortex Search requests |
| RECORD | OBJECT | Contains the event name, typically ‘CORTEX\_SEARCH\_REQUEST’ |
| RECORD\_ATTRIBUTES | OBJECT | Contains detailed observability metadata including database, schema, service, user, role, and session information |
| VALUE | VARIANT | Contains the actual request details including operation type, request body, response status code, and response time |

Expand

Show lessSee more

The VALUE column contains the following key fields:

- `snow.ai.observability.operation_type`: The type of operation, such as ‘QUERY’
- `snow.ai.observability.request_body`: The full request including query text and parameters
- `snow.ai.observability.response_status_code`: HTTP status code of the response
- `snow.ai.observability.response_time_ms`: Response time in milliseconds
- `snow.ai.observability.database.name`: Database containing the Cortex Search Service
- `snow.ai.observability.schema.name`: Schema containing the Cortex Search Service
- `snow.ai.observability.object.name`: Name of the Cortex Search Service

The following is an example of data found in the VALUE column:

Copy code

```
{
  "snow.ai.observability.operation_type": "QUERY",
  "snow.ai.observability.request_body": {
    "experimental": null,
    "limit": 10,
    "multi_index_query": null,
    "query": "hello"
  },
  "snow.ai.observability.response_status_code": 200,
  "snow.ai.observability.response_time_ms": 391
}
```

## Example

Query the request logs for the last 24 hours, using a role with `MONITOR` privilege on the service.

Copy code

```
SELECT
  timestamp,
  record_attributes['ai.observability.record_id']::STRING AS query_id,
  value['snow.ai.observability.request_body']['query']::STRING AS query_text,
  value['snow.ai.observability.request_body']['limit']::INT AS "limit",
  value['snow.ai.observability.response_status_code']::INT AS status_code,
  value['snow.ai.observability.response_time_ms']::INT AS response_time_ms,
  record_attributes['snow.ai.observability.database.name']::STRING AS database_name,
  record_attributes['snow.ai.observability.schema.name']::STRING AS schema_name,
  record_attributes['snow.ai.observability.object.name']::STRING AS service_name,
  record_attributes['snow.ai.observability.user.name']::STRING AS user_name,
  record_attributes['snow.ai.observability.role.name']::STRING AS role_name,
  record_attributes['snow.ai.observability.session.id']::STRING AS session_id
FROM TABLE(snowflake.local.get_ai_observability_events(
  '<database_name>',
  '<schema_name>',
  '<service_name>',
  'CORTEX SEARCH SERVICE'
))
WHERE timestamp > TIMESTAMPADD(hour, -24, CURRENT_TIMESTAMP())
ORDER BY timestamp DESC;
```
