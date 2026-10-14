# Microsoft SQL Server

## Overview

Horizon Catalog ingests SQL Server metadata via a direct database connection using a
dedicated service account with metadata-read privileges. For query logs (used for lineage and
popularity) you pick one of three sources, each with a different AWS footprint:

| Log source | What it is | AWS work required |
| --- | --- | --- |
| `system` | Horizon Catalog reads the SQL Server DMVs / system views on each crawl. | None. Works for on-prem SQL Server, Azure SQL, AWS RDS, Cloud SQL for SQL Server, and more. |
| `s3` (Database Activity Streams) | AWS RDS for SQL Server emits a Database Activity Stream to Kinesis; a customer-owned Firehose + Lambda pipeline decrypts, transforms, and lands records in S3; Horizon Catalog reads the S3 bucket via a cross-account IAM role. | Substantial: see [Query Logs](/user-guide/snowflake-horizon/connectors/sqlserver/query-log). |
| `none` | Metadata only; lineage and popularity disabled. | None. |

Expand

Show lessSee more

Tip

Start with `system`. It works for every hosting variant of SQL Server, requires no AWS resources, and
is what most customers use. The DAS path exists for customers who need complete, durable query
history beyond what SQL Server’s system views retain. If you don’t already use the DAS flow, you
almost certainly don’t need it.

By the time you finish this guide you’ll have:

1. A metadata-read SQL Server user dedicated to Horizon Catalog.
2. Network connectivity between your SQL Server instance and the Horizon Catalog service.
3. A working query-log source: `system` (default), `s3`, or `none`.
4. An active connector in the Horizon Catalog UI that uses all of the above.

## Prerequisites

- Administrative access to the SQL Server instance so you can `CREATE LOGIN`, `CREATE USER`, and `GRANT` permissions.
- Open Horizon Catalog connector in another browser tab. To reach it, sign in
  to Snowflake, open **Catalog > Connections**, pick **SQL Server** from the list.
  There are two values you’ll need to paste into any IAM role you create for the `s3` log source:
  - **IAM Principal**: The ARN of the Horizon Catalog service role that will assume your role. Copy it verbatim.
  - **External ID**: A per-connector secret starting with `sf_horizon_` (for example, `sf_horizon_Abc123…`). Horizon Catalog rejects External IDs that don’t match this prefix. Don’t regenerate or rewrite it.
- Only if you’ll use the DAS (`s3`) log source: an AWS user with permission to
  create IAM roles/policies, S3 buckets, Kinesis Data Firehose delivery streams, and
  Lambda functions in the same AWS account that hosts the RDS for SQL Server
  instance; plus ability to modify that RDS instance to enable Database Activity Streams.

## 1. Create a SQL Server user for Horizon Catalog

Connect to the instance as an administrative user and create a login + user with metadata-read
privileges. Replace `<username>` and `<password>` with real values.

Copy code

```
CREATE LOGIN <username> WITH PASSWORD = '<password>';
CREATE USER <username> FOR LOGIN <username>;
GRANT VIEW DEFINITION TO <username>;
```

Then grant `VIEW SERVER STATE`. The exact syntax depends on the hosting variant:

### Self-hosted or AWS RDS for SQL Server

Copy code

```
USE master;
GRANT VIEW SERVER STATE TO <username>;
```

### Azure SQL Database

Copy code

```
GRANT VIEW DATABASE PERFORMANCE STATE TO <username>;
```

### Google Cloud SQL for SQL Server

Log in as the `sqlserver` user:

Copy code

```
GRANT VIEW SERVER STATE TO <username> AS CustomerDbRootRole;
```

## 2. Ensure network connectivity

Horizon Catalog connects to your SQL Server instance over the public internet only. The instance must be
publicly reachable — either set **Publicly accessible = Yes** on the RDS instance, or place it
behind an internet-facing load balancer or proxy that you control and that forwards to the SQL Server port
(default 1433).

Horizon Catalog doesn’t guarantee stable egress IP addresses. The egress IPs it connects from
can change at any time without notice. The simplest security-group rule is to allow inbound TCP
on the SQL Server port from `0.0.0.0/0` and rely on SQL Server authentication (Step 1) plus TLS
to protect the instance.

Note

If your policy requires an IP allowlist instead, contact Snowflake support for the egress IPs
currently in use, and expect to update that allowlist when they change. For details, see
[Horizon Catalog egress](/user-guide/snowflake-horizon/connectors/security#horizon-catalog-egress).

## 3. Pick a query-log source

Choose one of the following:

- **system** (default, no AWS work): Horizon Catalog uses the service account from Step 1 to
  query SQL Server DMVs and system views (for example, `sys.dm_exec_query_stats`,
  `sys.dm_exec_sql_text`) on each crawl. `VIEW SERVER STATE` granted in Step 1 is what
  unlocks those views. When you reach Step 4, pick **Log source type: system**.
- **s3 via Database Activity Streams**: Full DAS pipeline. See
  [Query Logs](/user-guide/snowflake-horizon/connectors/sqlserver/query-log) for detailed
  instructions on setting up the Kinesis, Lambda, Firehose, and S3 infrastructure.
- **none**: Metadata only. Set **Log source type: none** in Step 4. Lineage and popularity are disabled;
  metadata sync still works.

Known limits of the system source

- Query history is bounded by what SQL Server keeps in the `sys.dm_exec_*` ring
  buffers, which is typically hours to days, not weeks.
- Statement text is often truncated or absent for prepared/cached statements.

If you need complete query history, use the `s3` (DAS) source instead.

## 4. Finish in the Horizon Catalog UI

Back in the Horizon Catalog connector wizard, fill in the connection details:

| Field | Value |
| --- | --- |
| **Source type** | Microsoft SQL Server |
| **Hostname** | The SQL Server instance hostname |
| **Port** | `1433` unless overridden |
| **Database name** | The database to connect to |
| **Encryption** | Encryption setting (see [Connection security](#connection-security) below) |
| **Username** | The `<username>` from Step 1 |
| **Password** | The `<password>` from Step 1 |
| **Log source type** | `system`, `s3`, or `none` per your Step 3 choice |

Expand

Show lessSee more

For `s3`, also paste the **Authorization** fields: Role ARN, AWS Region, S3 bucket name, and S3
object prefix `processed/`.

Select **Test connection**, then **Save**, then select the databases and schemas you want
crawled.

For the `s3` path the test confirms Horizon Catalog could (a) log in to SQL Server as the service
user, (b) assume the IAM role, and (c) list and read the bucket. For `system`, the test only
exercises (a).

Initial metadata typically appears within a few minutes; for the `s3` path, lineage and popularity fill
in as Firehose flushes batches into the bucket (up to 15 minutes per batch by default).

## 5. Set up metadata access

Other roles can’t see the metadata and lineage that this connector collects until you grant them
access. Grant `USAGE` on the connector, and on the database and schema that contain it, to each role
that needs to view the connector’s metadata and lineage:

Copy code

```
GRANT USAGE ON DATABASE CONNECTORS TO ROLE <role_name>;
GRANT USAGE ON SCHEMA CONNECTORS.METADATA TO ROLE <role_name>;
GRANT USAGE ON METADATA CONNECTOR CONNECTORS.METADATA.<connector_name> TO ROLE <role_name>;
```

If you stored the connector in a different database or schema, replace `CONNECTORS` and `METADATA`
with the actual database and schema names.

For more information about metadata access, see
[Metadata access control](/user-guide/snowflake-horizon/connectors/access-control).

## Connection security

Horizon Catalog connects to SQL Server with encryption enabled by default (`Encrypt=yes`).
If your SQL Server instance uses a self-signed TLS certificate, the connection still succeeds
because server certificate validation is not enforced by default.

Recommended: use a CA-signed TLS certificate

For the strongest security posture, configure your SQL Server instance with a CA-signed TLS
certificate. This protects against man-in-the-middle attacks on the connection between Horizon
Catalog and your instance.

If your instance already uses a CA-signed certificate and you want Horizon Catalog to verify
it, contact Snowflake support to enable full certificate validation for the connector.

Warning

Do not disable encryption on the connector. If `Encrypt` is set to `no`, the connection
between Horizon Catalog and your SQL Server instance is unencrypted.

For more details on the shared-responsibility model for Horizon Catalog connectors,
see [Security and data protection](/user-guide/snowflake-horizon/connectors/security).

## Troubleshooting

| Symptom | Most likely cause | Where to look |
| --- | --- | --- |
| Login failed for user | Wrong password, or `VIEW SERVER STATE` / `VIEW DEFINITION` missing | Step 1 |
| Connection timeout | Instance not publicly reachable, or IP allowlist out of date | Step 2: confirm current egress IPs with Snowflake support |
| `system` log source returns empty history | SQL Server ring buffers recycled; this is expected. Use `s3` for durable history | Step 3 |
| `s3` test fails: AccessDenied on bucket | Cross-account role policy scope or name wrong | Check that role name matches `SnowflakeHorizon-*` or `/SnowflakeHorizon/` |
| `s3` test passes but no data | Firehose buffer is 15 min; run a query and wait; check `errors/` prefix and Firehose CloudWatch logs | [Query Logs](/user-guide/snowflake-horizon/connectors/sqlserver/query-log) |

Expand

Show lessSee more
