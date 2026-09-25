# Monitor Data Connectivity Proxy

DCP provides observability through SQL interfaces and a Prometheus metrics endpoint on the agent.

## Describe a DCP client

Use `DESCRIBE DATA CONNECTIVITY PROXY` to view the current state of a DCP client. The command returns one row. You need USAGE on the
object, which is the same privilege DESCRIBE requires. If the client name needs quoting, quote it in the statement:

Copy code

```
DESCRIBE DATA CONNECTIVITY PROXY my_dcp_client;

DESCRIBE DATA CONNECTIVITY PROXY "quoted_client_name";
```

`AGENT_HEALTH` is a derived summary of the reported statuses. It isn’t a stored field of its own. Values are `HEALTHY`, `DEGRADED`, or
`DOWN`:

- `DOWN`: `AGENT_STATUS` isn’t `DCP_AGENT_LIFECYCLE_CONNECTED`, including a client that has never reported a status.
- `HEALTHY`: the client is connected, bootstrap succeeded, certificate rotation isn’t failed, and the data path isn’t failed or in
  progress.
- `DEGRADED`: the client is connected, but bootstrap success isn’t confirmed, or certificate rotation or the data path isn’t healthy.

An unreported data path doesn’t count as unhealthy. A certificate rotation in progress doesn’t demote health, because traffic still uses
the current certificate. `LAST_HEARTBEAT_AT` is the last heartbeat timestamp; heartbeat is already folded into `AGENT_HEALTH`.

For current state, use DESCRIBE. Event history records when a status was entered, not what is true now.

The output includes the following columns:

| Column | Description |
| --- | --- |
| `NAME` | DCP client name |
| `ENABLED` | Whether the client is enabled |
| `EXTERNAL_ACCESS_INTEGRATIONS` | External access integrations associated with the client. Set this with `CREATE` or `ALTER DATA CONNECTIVITY PROXY`. |
| `NETWORK_POLICY` | Network policy attached to the client, if any |
| `COMMENT` | Comment on the client, if any |
| `AGENT_STATUS` | Control-plane lifecycle status (for example, `DCP_AGENT_LIFECYCLE_CONNECTED`) |
| `BOOTSTRAP_STATUS` | Latest bootstrap status (for example, `DCP_AGENT_BOOTSTRAP_SUCCEEDED`) |
| `BOOTSTRAP_FAILURE_REASON` | Reason for the latest bootstrap failure, if any |
| `LAST_BOOTSTRAP_AT` | When the latest bootstrap status was recorded |
| `CERT_ROTATION_STATUS` | Latest control-plane certificate rotation status |
| `LAST_CERT_ROTATION_AT` | When the latest certificate rotation status was recorded |
| `OPERATIONAL_CERT_EXPIRES_AT` | Expiry of the agent’s current operational certificate |
| `LAST_AUTH_FAILURE_REASON` | Reason for the latest authentication failure, if any |
| `LAST_AUTH_FAILURE_AT` | When the latest authentication failure was recorded |
| `DATA_PATH_STATUS` | Latest data-path health status |
| `AGENT_HEALTH` | Derived summary: `HEALTHY`, `DEGRADED`, or `DOWN` |
| `AGENT_VERSION` | Agent version last reported by the client |
| `LAST_HEARTBEAT_AT` | When the client last sent a heartbeat |
| `POLICY_APPLIED_EPOCH` | Policy epoch the agent last applied |
| `AUTH_TOKEN_EXPIRES_AT` | Expiry of the agent’s current authentication token |
| `POLICY_EPOCH` | Current policy epoch for the client (NULL until a policy snapshot is delivered) |
| `REACHABLE_DESTINATIONS` | Destinations the current policy allows (NULL until a policy snapshot is delivered) |

Expand

Show lessSee more

## View event history

`INFORMATION_SCHEMA.DCP_CLIENT_EVENT_HISTORY` returns one row per recorded status transition for a DCP client. `AGENT_ID` is required and
is the DCP client name (the same identifier you use in DESCRIBE). You need USAGE on that client. If you don’t have it, Snowflake treats
the object as not existing.

A row means the client entered that `STATUS` at `OCCURRED_AT`. It isn’t the current state. Use DESCRIBE for current state. Authentication
failures appear on DESCRIBE (`LAST_AUTH_FAILURE_REASON` and `LAST_AUTH_FAILURE_AT`); they aren’t a published event type.

Copy code

```
SELECT *
FROM TABLE(INFORMATION_SCHEMA.DCP_CLIENT_EVENT_HISTORY(
  AGENT_ID => 'my_dcp_client'
))
ORDER BY occurred_at DESC;
```

Columns: `AGENT_ID`, `OCCURRED_AT`, `EVENT_TYPE`, `STATUS`, `REASON`, `RECORDED_AT`.

`EVENT_TYPE` values:

| Event type | Description |
| --- | --- |
| `BOOTSTRAP` | Agent registration and bootstrap |
| `CONTROL_PLANE` | Control-connection lifecycle |
| `CERT_ROTATION` | Control-plane credential renewal. Snowflake records a rotation row only when a rotation occurred. |
| `DATAPLANE_CERT_ROTATION` | Data-tunnel credential renewal |
| `DATA_PATH` | Data-path health |

Expand

Show lessSee more

`STATUS` values: `SUCCESS`, `FAILURE`, `PENDING`, `IN_PROGRESS`. `PENDING` and `IN_PROGRESS` mean the operation hadn’t finished when the
row was recorded. A later row carries the outcome.

`REASON` is a DCP error code on failure (for example, `DCP_BOOTSTRAP_TOKEN_INVALID` or `DCP_BOOTSTRAP_NETWORK_POLICY_BLOCKED`), or NULL.

## Check route reachability

`INFORMATION_SCHEMA.DCP_CLIENT_ROUTE_CHECK` is a live diagnostic. It returns one row per stage of the route from Snowflake through the
named DCP client to a destination. Both arguments are required constants. `AGENT_ID` is the DCP client name. `DESTINATION` is
`host:port`. You need USAGE on the client.

Copy code

```
SELECT *
FROM TABLE(INFORMATION_SCHEMA.DCP_CLIENT_ROUTE_CHECK(
  AGENT_ID => 'my_dcp_client',
  DESTINATION => 'my-private-db.internal:5432'
))
ORDER BY stage_order;
```

Columns: `AGENT_ID`, `STAGE_ORDER`, `STAGE`, `STATUS`, `DETAIL`, `REASON`, `CHECKED_AT`.

Stages, in order: `EGRESS_CONFIG`, `POLICY`, `BOOTSTRAP`, `CONTROL_PLANE`, `CERTIFICATES`, `DATA_PATH`, `SNOWFLAKE_INTERNAL`,
`DESTINATION`.

`STATUS` values: `SUCCESS`, `FAILURE`, `IN_PROGRESS`, `SKIPPED`, `UNKNOWN`.

- `SKIPPED`: an earlier stage didn’t resolve, so this stage wasn’t attempted. `DETAIL` names the gate to fix first.
- `IN_PROGRESS`: a caller action can still produce an answer. `DETAIL` names that action.
- `UNKNOWN`: nothing you change produces an answer for this stage.

Some stages use client telemetry. Those rows are empty or `UNKNOWN` until telemetry is reachable for the account.

Use this when a connector can’t reach a private source.

## View connection history

`INFORMATION_SCHEMA.DCP_CLIENT_CONNECTION_HISTORY` returns one row per closed connection for a DCP client. Rows come from agent telemetry
spans (`dcp.connection`) in the account event table. You need USAGE on the client. `AGENT_ID` is required (the DCP client name).
`TIME_RANGE_HOURS` is optional: default 24, minimum 1, maximum 2160 (90 days). The window is on recorded time, not start time, so
`STARTED_AT` can fall before the window.

Copy code

```
SELECT *
FROM TABLE(INFORMATION_SCHEMA.DCP_CLIENT_CONNECTION_HISTORY(
  AGENT_ID => 'my_dcp_client',
  TIME_RANGE_HOURS => 24
))
ORDER BY recorded_at DESC;
```

Columns: `AGENT_ID`, `CONNECTION_ID`, `WORKLOAD_ID`, `DESTINATION_HOST`, `DESTINATION_PORT`, `STATUS`, `REASON`, `STARTED_AT`, `ENDED_AT`,
`RECORDED_AT`, `SETUP_DURATION_MS`, `BYTES_TO_DESTINATION`, `BYTES_FROM_DESTINATION`.

`STATUS` values: `SUCCESS`, `FAILURE`, `UNKNOWN`. `UNKNOWN` covers a missing reason and a draining agent (`shutting_down`): neither
settled the connection.

`WORKLOAD_ID`, destination host and port, and `SETUP_DURATION_MS` can be NULL when the connection was rejected before those values exist.
Byte counts are always present (0 if the tunnel never carried traffic). `REASON` is NULL on a clean close.

## Prometheus metrics (agent-side)

The agent exposes a Prometheus metrics endpoint at `127.0.0.1:9092` by default. Scrape this endpoint with any Prometheus-compatible
monitoring stack, such as Prometheus, Datadog, or Grafana Agent. The same address serves the `/ready` health probe.

A container-hosted agent using the default bind isn’t reachable from outside the container. Set `DCP_METRICS_PORT` to bind all
interfaces and publish the port:

Copy code

```
docker run -d \
  --name dcp-agent \
  -e DCP_METRICS_PORT=9092 \
  -p 9092:9092 \
  ... snowflakedb/dcp-client:latest
```

Key metrics:

| Metric | Type | Description |
| --- | --- | --- |
| `agent_connections_active` | Gauge | Currently active connections |
| `agent_connections_total` | Counter | Handled connections by `status`, with `reason` naming the cause (e.g. `verification_failed`, `internal_error`) |
| `agent_destination_connect_seconds` | Histogram | TCP connect duration to the destination |
| `agent_handshake_duration_seconds` | Histogram | Full tunnel establishment duration, from connect request to connect response |
| `agent_destination_errors_total` | Counter | Failed TCP connections to the destination, by `error_type` |
| `dcp_agent_bootstrap_jwt_expires_at_seconds` | Gauge | Expiry of the bootstrap JWT as a Unix timestamp (0 when the claim is missing or unparseable) |
| `agent_cert_rotation_total` | Counter | Agent identity rotations triggered by the control plane |

Expand

Show lessSee more

Note

Set a threshold alert on `dcp_agent_bootstrap_jwt_expires_at_seconds` to fire at least 24 hours before expiry, so you have time to rotate
the token before the agent loses the ability to renew its certificates.

### Relay path selection

The agent connects to the relay over one of the relay hostnames listed in
[Outbound ports](/user-guide/data-connectivity-proxy-setup#label-dcp-outbound-ports), choosing automatically based on what your network
allows. `agent_proxy_dial_path_used_total` counts the sessions established over each, labelled `path="direct"` or `path="fallback"`.

Both are fully supported production paths. `path="fallback"` is a normal steady state, not a misconfiguration — many deployments
run entirely over it. Don’t alert on the path label. If you are investigating a throughput or latency problem, see
[Scaling for throughput](/user-guide/data-connectivity-proxy-setup#label-dcp-scaling) first; the relay path is not the usual cause.

### Change the metrics endpoint address

To listen on a different address or port, set a full `host:port` with the `--metrics-addr` flag or the `DCP_METRICS_ADDRESS`
environment variable:

Copy code

```
docker run ... snowflakedb/dcp-client:latest \
  ... \
  --metrics-addr 0.0.0.0:9100
```

`DCP_METRICS_PORT` is a shortcut for the common container case: it takes a bare port and binds `0.0.0.0:<port>`.
`--metrics-addr` and `DCP_METRICS_ADDRESS` take precedence over it. Setting `DCP_METRICS_ADDRESS` to an empty value disables
the metrics and `/ready` endpoints altogether.

## Health check

Run the agent health check to validate connectivity without starting the data-plane workers:

Copy code

```
docker run --rm \
  -v /etc/dcp-agent/secrets:/etc/dcp-agent/secrets:ro \
  snowflakedb/dcp-client:latest \
  --health-check \
  --sf-bootstrap-credentials /etc/dcp-agent/secrets/dcp-bootstrap-token
```

The health check runs the full bootstrap sequence (verifying that the control plane is reachable, the token is valid, the portal is
reachable, and the proxy is reachable) and prints a structured pass/fail result for each step.

A local `/ready` HTTP endpoint is also available on the agent at `127.0.0.1:9092/ready` for container orchestration health probes.
