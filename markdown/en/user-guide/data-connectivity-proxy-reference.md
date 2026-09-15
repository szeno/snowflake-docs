# Data Connectivity Proxy reference

This page summarizes Data Connectivity Proxy (DCP) SQL syntax, INFORMATION\_SCHEMA table functions, agent CLI flags, and limitations.
Dedicated SQL command and function reference pages will replace these summaries after syntax is finalized.

## SQL commands

### CREATE DATA CONNECTIVITY PROXY

Copy code

```
CREATE [ OR REPLACE ] DATA CONNECTIVITY PROXY [ IF NOT EXISTS ] <name>
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]
  [ NETWORK_POLICY = <policy_name> ]
  [ ENABLED = { TRUE | FALSE } ]
  [ COMMENT = '<comment>' ]
```

Associate at least one external access integration whose network rules use
`MODE = DATA_CONNECTIVITY_PROXY_EGRESS`. You can set this at create time or later with ALTER.

### ALTER DATA CONNECTIVITY PROXY

Copy code

```
ALTER DATA CONNECTIVITY PROXY <name> SET
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]
  [ NETWORK_POLICY = <policy_name> ]
  [ ENABLED = { TRUE | FALSE } ]
  [ COMMENT = '<comment>' ]

ALTER DATA CONNECTIVITY PROXY <name> UNSET
  [ EXTERNAL_ACCESS_INTEGRATIONS ]
  [ NETWORK_POLICY ]
  [ COMMENT ]

ALTER DATA CONNECTIVITY PROXY <name> RENAME TO <new_name>
```

### DESCRIBE DATA CONNECTIVITY PROXY

Returns one row with the current configuration and agent status for a DCP client. Requires USAGE on the object.

Copy code

```
DESCRIBE DATA CONNECTIVITY PROXY <name>
```

Key columns: `NAME`, `ENABLED`, `EXTERNAL_ACCESS_INTEGRATIONS`, `NETWORK_POLICY`, `COMMENT`, `AGENT_STATUS`, `BOOTSTRAP_STATUS`,
`BOOTSTRAP_FAILURE_REASON`, `LAST_BOOTSTRAP_AT`, `CERT_ROTATION_STATUS`, `LAST_CERT_ROTATION_AT`, `OPERATIONAL_CERT_EXPIRES_AT`,
`LAST_AUTH_FAILURE_REASON`, `LAST_AUTH_FAILURE_AT`, `DATA_PATH_STATUS`, `AGENT_HEALTH`, `AGENT_VERSION`, `LAST_HEARTBEAT_AT`,
`POLICY_APPLIED_EPOCH`, `AUTH_TOKEN_EXPIRES_AT`, `POLICY_EPOCH`, `REACHABLE_DESTINATIONS`.

`AGENT_HEALTH` is derived (`HEALTHY`, `DEGRADED`, or `DOWN`). See [Describe a DCP client](/user-guide/data-connectivity-proxy-monitor#label-dcp-describe).

### DROP DATA CONNECTIVITY PROXY

Copy code

```
DROP DATA CONNECTIVITY PROXY [ IF EXISTS ] <name>
```

### SHOW DATA CONNECTIVITY PROXIES

Copy code

```
SHOW DATA CONNECTIVITY PROXIES [ LIKE '<pattern>' ]
```

## SQL functions

Setup also requires [SYSTEM$ISSUE\_PER\_ACCOUNT\_CERTIFICATES](/sql-reference/functions/system_issue_per_account_certificates). See the
[note in the setup topic](/user-guide/data-connectivity-proxy-setup#label-dcp-setup-issue-certificates).

### SYSTEM$GENERATE\_DATA\_CONNECTIVITY\_PROXY\_BOOTSTRAP\_TOKEN

Generates a bootstrap JWT for an agent to authenticate with the DCP control plane.

Copy code

```
SYSTEM$GENERATE_DATA_CONNECTIVITY_PROXY_BOOTSTRAP_TOKEN(
  '<dcp_client_name>',
  <validity_days>
)
```

Arguments:

| Argument | Type | Description |
| --- | --- | --- |
| `dcp_client_name` | VARCHAR | Name of the DCP object to generate a token for |
| `validity_days` | INTEGER | Token validity in days (maximum: 90) |

Expand

Show lessSee more

Returns a VARCHAR containing the bootstrap JWT. Write this value to the credentials file on the agent host.

**Required privilege:** ACCOUNTADMIN, or OWNERSHIP on the DCP object.

## INFORMATION\_SCHEMA table functions

These functions take `AGENT_ID` as the DCP client name. You need USAGE on that client (the same privilege DESCRIBE requires). If you don’t
have it, Snowflake treats the object as not existing.

### DCP\_CLIENT\_EVENT\_HISTORY

Returns one row per recorded status transition for a DCP client. A row is the status entered at `OCCURRED_AT`, not the current state.

Copy code

```
TABLE(INFORMATION_SCHEMA.DCP_CLIENT_EVENT_HISTORY(
  AGENT_ID => '<dcp_client_name>'
))
```

**Output columns:** `AGENT_ID`, `OCCURRED_AT`, `EVENT_TYPE`, `STATUS`, `REASON`, `RECORDED_AT`

**EVENT\_TYPE:** `BOOTSTRAP`, `CONTROL_PLANE`, `CERT_ROTATION`, `DATAPLANE_CERT_ROTATION`, `DATA_PATH`

**STATUS:** `SUCCESS`, `FAILURE`, `PENDING`, `IN_PROGRESS`

### DCP\_CLIENT\_CONNECTION\_HISTORY

Returns one row per closed connection from agent telemetry. `TIME_RANGE_HOURS` is optional (default 24, minimum 1, maximum 2160). The
window is on recorded time.

Copy code

```
TABLE(INFORMATION_SCHEMA.DCP_CLIENT_CONNECTION_HISTORY(
  AGENT_ID => '<dcp_client_name>'
  [ , TIME_RANGE_HOURS => <hours> ]
))
```

**Output columns:** `AGENT_ID`, `CONNECTION_ID`, `WORKLOAD_ID`, `DESTINATION_HOST`, `DESTINATION_PORT`, `STATUS`, `REASON`, `STARTED_AT`,
`ENDED_AT`, `RECORDED_AT`, `SETUP_DURATION_MS`, `BYTES_TO_DESTINATION`, `BYTES_FROM_DESTINATION`

**STATUS:** `SUCCESS`, `FAILURE`, `UNKNOWN`

### DCP\_CLIENT\_ROUTE\_CHECK

Evaluates the live route from Snowflake through a DCP client to a destination. `DESTINATION` is `host:port`. Returns one row per stage.

Copy code

```
TABLE(INFORMATION_SCHEMA.DCP_CLIENT_ROUTE_CHECK(
  AGENT_ID => '<dcp_client_name>',
  DESTINATION => '<host>:<port>'
))
```

**Output columns:** `AGENT_ID`, `STAGE_ORDER`, `STAGE`, `STATUS`, `DETAIL`, `REASON`, `CHECKED_AT`

**STAGE:** `EGRESS_CONFIG`, `POLICY`, `BOOTSTRAP`, `CONTROL_PLANE`, `CERTIFICATES`, `DATA_PATH`, `SNOWFLAKE_INTERNAL`, `DESTINATION`

**STATUS:** `SUCCESS`, `FAILURE`, `IN_PROGRESS`, `SKIPPED`, `UNKNOWN`

## Agent CLI reference

| Flag | Default | Description |
| --- | --- | --- |
| `--sf-bootstrap-credentials` | `/etc/dcp-agent/secrets/dcp-bootstrap-token` | Path to the bootstrap JWT. Re-read on certificate rotation. Omit this flag if you mount the token at the default path. |
| `--metrics-addr` | `127.0.0.1:9092` | Address for the Prometheus metrics endpoint and the `/ready` health probe |
| `--drain-timeout-secs` | `300` | Seconds to wait for active tunnels to finish on `SIGTERM` |
| `--health-check` | None | Run bootstrap validation and exit without starting workers |
| `--log-level` | `info` | Log verbosity: `error`, `warn`, `info`, `debug`, `trace` |

Expand

Show lessSee more

## Agent environment variables

Each variable below is an alternative to the equivalent flag. Where both are supplied, the flag wins.

| Variable | Flag equivalent | Description |
| --- | --- | --- |
| `DCP_BOOTSTRAP_TOKEN` | `--sf-bootstrap-credentials` | The bootstrap JWT itself, or a path to a file containing it. Prefer mounting the token as a file: a value supplied inline isn’t re-read on certificate rotation and is visible in the container environment. |
| `DCP_METRICS_ADDRESS` | `--metrics-addr` | Full `host:port` for the metrics and `/ready` endpoints. Default `127.0.0.1:9092`. An empty value disables both endpoints. |
| `DCP_METRICS_PORT` | None | Bare port that binds `0.0.0.0:<port>` — the usual way to expose metrics from a container. Ignored when `DCP_METRICS_ADDRESS` or `--metrics-addr` is set. |
| `DCP_LOG_LEVEL` | `--log-level` | Log verbosity: `error`, `warn`, `info`, `debug`, `trace`. Default `info`. |

Expand

Show lessSee more

## Limitations

- DCP is available for use with Snowflake Openflow. Support for additional services is planned.
- A single DCP object corresponds to one network scope. For data sources in isolated networks, deploy a separate agent and DCP object per
  network.
- Corporate HTTP proxy support (routing the agent’s outbound traffic through an enterprise-managed forward proxy) isn’t supported.
- Active-active load-balancing across agent instances for the same destination isn’t supported.
- Hitless agent-process upgrade (live TCP session handoff on agent restart) isn’t supported.
- Agent telemetry shipping to a Snowflake event table is available on AWS. Azure support follows in a subsequent release.
