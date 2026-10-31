# Capture Horizon Iceberg REST Catalog events in the event table

Snowflake can capture the HTTP requests that external query engines (such as Spark, Trino, DuckDB, or PyIceberg) make against the Horizon Iceberg REST Catalog (IRC) APIs and route them to the [event table](/developer-guide/logging-tracing/event-table-columns) configured for your account. Each IRC request produces a record you can query alongside your other Snowflake telemetry, so you can monitor IRC traffic and troubleshoot integrations with external engines.

These records are separate from [access history](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon-access-history). Access history records successful IRC operations. Event table records include the HTTP status code, so you can also find failed requests.

For more information about the Horizon IRC APIs, see [Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).

## Enable telemetry for Horizon IRC events

To route Horizon IRC events to an event table, set the account’s log level to at least `INFO` and set the account event table.

If your account already has an event table configured, you only need to raise `LOG_LEVEL`.

Copy code

```
USE ROLE ACCOUNTADMIN;

ALTER ACCOUNT SET LOG_LEVEL = 'INFO';

CREATE SCHEMA IF NOT EXISTS my_database.my_schema;

CREATE EVENT TABLE IF NOT EXISTS my_database.my_schema.horizon_irc_events;

-- Substitute the fully qualified name of an event table that already exists
-- in your account, or use the event table created above.
ALTER ACCOUNT SET EVENT_TABLE = 'MY_DATABASE.MY_SCHEMA.HORIZON_IRC_EVENTS';
```

For general information about configuring an event table, see [Logging, tracing, and metrics](/developer-guide/logging-tracing/logging-tracing-overview).

## Query Horizon IRC events

Every record that Snowflake writes for a Horizon IRC request sets the [SCOPE](/developer-guide/logging-tracing/event-table-columns#label-event-table-scope-column) column to `snow.managed_polaris`. Filter on that scope to return only IRC events.

Copy code

```
SELECT *
FROM my_database.my_schema.horizon_irc_events
WHERE scope:"name"::string = 'snow.managed_polaris'
ORDER BY observed_timestamp ASC;
```

## Event table columns for Horizon IRC events

The following [event table columns](/developer-guide/logging-tracing/event-table-columns) carry information about each captured IRC request.

- **TRACE:** Correlates the record with the tracing context for the IRC request.

  Copy code

  ```
  {
    "span_id": "38f4357beef90bb9",
    "trace_id": "01c561b32d2010f68d94f3b052645fc8"
  }
  ```
- **RESOURCE\_ATTRIBUTES:** Identifies the Snowflake account that served the IRC request.

  Copy code

  ```
  {
    "service.name": "managed_polaris",
    "snow.account.locator": "ab12345",
    "snow.account.name": "MY_ACCOUNT"
  }
  ```
- **SCOPE:** Identifies the record as a Horizon IRC event. Filter on this value to isolate IRC records.

  Copy code

  ```
  {
    "name": "snow.managed_polaris"
  }
  ```
- **RECORD:** Provides the severity of the event.

  Copy code

  ```
  {
    "severity_number": 9,
    "severity_text": "INFO"
  }
  ```
- **RECORD\_ATTRIBUTES:** Describes the IRC request itself, including the HTTP method and route, the IRC operation, the Snowflake principal that authenticated the client, the roles activated for the request, and the IRC request ID.

  Copy code

  ```
  {
    "http.request.method": "POST",
    "http.route": "/polaris/api/catalog/v1/MY_DATABASE/namespaces/PUBLIC/tables/TABLE_FROM_EXT_ENGINE/metrics",
    "snow.polaris.activated_roles": [
      "ACCOUNTADMIN"
    ],
    "snow.polaris.operation_id": "reportMetrics",
    "snow.polaris.principal_name": "MY_USER",
    "snow.polaris.request_id": "e74b5066-7fc4-460f-8efa-3896e3dfd8e5"
  }
  ```

  A `GET /polaris/api/catalog/v1/.../tables/<name>` request looks like this:

  Copy code

  ```
  {
    "http.request.method": "GET",
    "http.route": "/polaris/api/catalog/v1/MY_DATABASE/namespaces/PUBLIC/tables/TABLE_FROM_EXT_ENGINE",
    "snow.polaris.activated_roles": [
      "ACCOUNTADMIN"
    ],
    "snow.polaris.operation_id": "loadTable",
    "snow.polaris.principal_name": "MY_USER",
    "snow.polaris.request_id": "2ce7fd4a-3e9a-4815-a2ea-2ec3899af3ce"
  }
  ```

  Where:

  - `http.request.method` and `http.route`: The HTTP method and route of the IRC request.
  - `snow.polaris.operation_id`: The IRC operation the request performed (for example, `loadTable`, `updateTable`, `createTable`, `dropTable`, `reportMetrics`).
  - `snow.polaris.principal_name`: The Snowflake user that authenticated the IRC client.
  - `snow.polaris.activated_roles`: The roles that were active for the request.
  - `snow.polaris.request_id`: A unique identifier for the IRC request.
- **VALUE:** Contains the HTTP response status code Snowflake returned for the request. Use this to distinguish successful requests from failures.

  Copy code

  ```
  {
    "http.response.status_code": 200
  }
  ```

  Other typical values include `204` (no content, for example after a successful metrics report) and `400` (bad request).

### Example: return failed IRC requests in the last day

Copy code

```
SELECT observed_timestamp,
       record_attributes:"http.request.method"::string  AS method,
       record_attributes:"http.route"::string           AS route,
       record_attributes:"snow.polaris.operation_id"::string  AS operation,
       record_attributes:"snow.polaris.principal_name"::string AS principal,
       value:"http.response.status_code"::number        AS status_code
FROM my_database.my_schema.horizon_irc_events
WHERE scope:"name"::string = 'snow.managed_polaris'
  AND value:"http.response.status_code"::number >= 400
  AND observed_timestamp >= DATEADD('day', -1, CURRENT_TIMESTAMP())
ORDER BY observed_timestamp DESC;
```
