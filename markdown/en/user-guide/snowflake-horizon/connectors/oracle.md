# Oracle

## Overview

Horizon Catalog ingests Oracle metadata via a direct database connection using a dedicated
service account with metadata-read privileges. For query logs (used for lineage and popularity)
you pick one of three sources:

| Log source | What it is | AWS work required |
| --- | --- | --- |
| `system` | Horizon Catalog reads Oracle’s data dictionary and system views on each crawl. | None. Works for any hosting variant. |
| `s3` (Database Activity Streams) | AWS RDS for Oracle emits a Database Activity Stream to Kinesis; a customer-owned Firehose + Lambda pipeline lands records in S3; Horizon Catalog reads S3 via a cross-account role. | Substantial: see [Query Logs](/user-guide/snowflake-horizon/connectors/oracle/query-log). |
| `none` | Metadata only; lineage and popularity disabled. | None. |

Expand

Show lessSee more

Tip

Start with `system`. It requires no AWS resources and is what most customers use. The DAS path
exists for customers who need complete, durable query history beyond what the system views
retain.

## Prerequisites

- Administrative access to the Oracle instance so you can `CREATE USER`, `CREATE ROLE`, and `GRANT`.
- Open the Horizon Catalog connector in another browser tab. To reach it, sign in to Snowflake,
  open **Catalog > Connections**, then pick **Oracle** from the list. For the `s3` log source
  you’ll need two values from the wizard:
  - **IAM Principal**: The ARN of the Horizon Catalog service role that will assume your role. Copy it verbatim.
  - **External ID**: A per-connector secret starting with `sf_horizon_`. Don’t regenerate or rewrite it.
- Only if you’ll use the DAS (`s3`) log source: an AWS user with permission to create IAM
  roles/policies, S3 buckets, Kinesis Data Firehose delivery streams, and Lambda functions in the
  AWS account that hosts the RDS for Oracle instance, plus the ability to enable Database Activity
  Streams on that instance.

## 1. Create an Oracle user for Horizon Catalog

Connect as an administrative user and create a dedicated service account with metadata-read
privileges. Replace `<username>`, `<password>`, and `<role>` with real values.

Copy code

```
CREATE USER <username> IDENTIFIED BY <password>;
CREATE ROLE <role>;
GRANT <role> TO <username>;
GRANT CREATE SESSION TO <role>;
GRANT SELECT_CATALOG_ROLE TO <role>;
```

`SELECT_CATALOG_ROLE` grants read access to the data dictionary and system views that Horizon
Catalog uses to read metadata and (for the `system` log source) query history.

Optional: table preview

If you want Horizon Catalog to preview table contents, also grant read access to the tables:

Copy code

```
GRANT SELECT ANY TABLE TO <role>;
```

## 2. Ensure network connectivity

Horizon Catalog connects to your Oracle instance over the public internet. The instance must be
publicly reachable — either set **Publicly accessible = Yes** on the RDS instance, or place it
behind an internet-facing load balancer or proxy you control. Allow inbound TCP on the Oracle
port (default 1521).

About egress IPs

Horizon Catalog doesn’t guarantee stable egress IPs. The egress IPs it connects from can change
at any time without notice. If you’d rather allowlist specific CIDRs instead of allowing
`0.0.0.0/0`, contact Snowflake support for the egress IPs currently in use, and expect to update
that allowlist when they change. For details, see
[Horizon Catalog egress](/user-guide/snowflake-horizon/connectors/security#horizon-catalog-egress).

## 3. Choose a query-log source

- **system** (default, no AWS work): Horizon Catalog reads Oracle’s system views on each crawl.
- **s3 via Database Activity Streams**: Full DAS pipeline. See
  [Query Logs](/user-guide/snowflake-horizon/connectors/oracle/query-log).
- **none**: Metadata only. Lineage and popularity are disabled; metadata sync still works.

## 4. Finish in the Horizon Catalog UI

Back in the connector wizard, fill in the **Add data source** step:

| Field | Value |
| --- | --- |
| **Display Name** | A name for this data source |
| **Hostname** | The Oracle instance hostname |
| **Port** | `1521` unless overridden |
| **Username** | The `<username>` from Step 1 |
| **Password** | The `<password>` from Step 1 |
| **SID** | The Oracle system identifier |
| **Snowflake Database** | The Snowflake database where the connector stores its metadata |
| **Snowflake Schema** | The Snowflake schema where the connector stores its metadata |

Expand

Show lessSee more

In the **Connect query log** step, pick **System Table/View**, **RDS Database Activity Stream**,
or **None**. For the DAS option, paste the S3 Bucket, S3 Object Prefix (`processed/`), AWS
Region, and Role ARN from [Query Logs](/user-guide/snowflake-horizon/connectors/oracle/query-log).

In the **Select databases** step, choose the databases you want Horizon Catalog to crawl.

Initial metadata typically appears within a few minutes; for the `s3` source, lineage and
popularity fill in as Firehose flushes batches into the bucket (up to 15 minutes per batch by
default).

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

Horizon Catalog uses a TLS-capable Oracle client. If your instance is configured to accept TLS
connections, the connection is encrypted automatically. However, if TLS isn’t available on the
server, the connection proceeds unencrypted.

You are responsible for enabling TLS on your database instance

Snowflake strongly recommends encrypting the connection with TLS 1.2 or higher. For RDS for Oracle,
add the **SSL** option to the instance’s option group, set the option’s `SQLNET.SSL_VERSION` value
to `1.2`, then connect Horizon Catalog on the instance’s SSL/TLS port. See the AWS documentation on
[Oracle SSL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.Oracle.Options.SSL.html)
for the exact steps.

For more details on the shared-responsibility model for Horizon Catalog connectors, see
[Security and data protection](/user-guide/snowflake-horizon/connectors/security).

## Troubleshooting

| Symptom | Most likely cause | Where to look |
| --- | --- | --- |
| Login failed / insufficient privileges | Wrong password, or the role is missing `CREATE SESSION` / `SELECT_CATALOG_ROLE` | Step 1 |
| Connection timeout | Instance not publicly reachable, or IP allowlist out of date | Step 2 |
| `s3` test fails: AccessDenied on bucket | Cross-account role policy scope or name wrong | [Query Logs](/user-guide/snowflake-horizon/connectors/oracle/query-log) |
| `s3` test passes but no data | Firehose buffer is up to 15 min; run a query and wait | [Query Logs](/user-guide/snowflake-horizon/connectors/oracle/query-log) |

Expand

Show lessSee more
