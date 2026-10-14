# MySQL

## Overview

Horizon Catalog ingests MySQL metadata via a direct database connection using a dedicated
read-only service account. Query logs (used for lineage and popularity) are optional and, for
instances on Amazon RDS, come from Amazon CloudWatch via a cross-account IAM role that
Horizon Catalog assumes.

| Log source | What it is | AWS work required |
| --- | --- | --- |
| `none` | Metadata only; lineage and popularity disabled. | None. |
| `cloudwatch` | The MySQL general query log exported to CloudWatch Logs on AWS RDS. | Enable the general log and a cross-account IAM role. See [Query Logs](/user-guide/snowflake-horizon/connectors/mysql/query-log). |

Expand

Show lessSee more

## Prerequisites

- Administrative access to the MySQL instance so you can `CREATE USER` and `GRANT`.
- Only if you’ll use the `cloudwatch` log source: an AWS user with permission to modify RDS
  parameter groups, the RDS instance, and IAM.
- Open the Horizon Catalog connector in another browser tab. To reach it, sign in to Snowflake,
  open **Catalog > Connections**, then pick **MySQL** from the list.

## 1. Create a MySQL user for Horizon Catalog

Connect as an administrative user and create a dedicated service account. Replace `<username>`
and `<password>` with real values.

Copy code

```
CREATE USER '<username>' IDENTIFIED BY '<password>';
GRANT SELECT ON *.* TO '<username>';
GRANT SHOW VIEW ON *.* TO '<username>';
FLUSH PRIVILEGES;
```

`SELECT` lets Horizon Catalog run `DESCRIBE`, `SHOW CREATE TABLE`, and `INFORMATION_SCHEMA`
queries to read table structure; `SHOW VIEW` is required to read view definitions.

## 2. Ensure network connectivity

Horizon Catalog connects to your MySQL instance over the public internet. The instance must be
publicly reachable — either set **Publicly accessible = Yes** on the RDS instance, or place it
behind an internet-facing load balancer or proxy you control. Allow inbound TCP on the MySQL
port (default 3306).

About egress IPs

Horizon Catalog doesn’t guarantee stable egress IPs. The egress IPs it connects from can change
at any time without notice. If you’d rather allowlist specific CIDRs instead of allowing
`0.0.0.0/0`, contact Snowflake support for the egress IPs currently in use, and expect to update
that allowlist when they change. For details, see
[Horizon Catalog egress](/user-guide/snowflake-horizon/connectors/security#horizon-catalog-egress).

## 3. Choose a query-log source

- **none**: Metadata only. Lineage and popularity are disabled; metadata sync still works.
- **cloudwatch**: The general query log exported to CloudWatch Logs. Follow
  [Query Logs](/user-guide/snowflake-horizon/connectors/mysql/query-log) before you finish
  in the UI.

## 4. Finish in the Horizon Catalog UI

Back in the connector wizard, fill in the **Add data source** step:

| Field | Value |
| --- | --- |
| **Display Name** | A name for this data source |
| **Hostname** | The MySQL instance hostname |
| **Port** | `3306` unless overridden |
| **Username** | The `<username>` from Step 1 |
| **Password** | The `<password>` from Step 1 |
| **Source Database** | Optional. Scopes crawling to a single database; leave blank to crawl all |
| **Snowflake Database** | The Snowflake database where the connector stores its metadata |
| **Snowflake Schema** | The Snowflake schema where the connector stores its metadata |

Expand

Show lessSee more

In the **Connect query log** step, pick **None** or **CloudWatch Logs**. For CloudWatch, paste
the AWS Region, Role ARN, and Log Group Name Prefix from
[Query Logs](/user-guide/snowflake-horizon/connectors/mysql/query-log).

In the **Select databases** step, choose the databases you want Horizon Catalog to crawl.

Initial metadata typically appears within a few minutes; for the `cloudwatch` source, lineage and
popularity fill in as query log history accumulates.

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

Horizon Catalog uses a TLS-capable MySQL client. If your instance is configured to accept TLS
connections, the connection is encrypted automatically. However, if TLS isn’t available on the
server, the connection proceeds unencrypted.

You are responsible for enabling TLS on your database instance

Snowflake strongly recommends enforcing TLS 1.2 or higher on your MySQL instance. For RDS MySQL,
set the following parameter in the DB parameter group:

| Parameter | Recommended value | Effect |
| --- | --- | --- |
| `require_secure_transport` | `ON` | Reject any connection that doesn’t use TLS. |

Expand

Show lessSee more

After applying this setting, Horizon Catalog connects over TLS without any changes on the connector
side.

For more details on the shared-responsibility model for Horizon Catalog connectors, see
[Security and data protection](/user-guide/snowflake-horizon/connectors/security).

## Troubleshooting

| Symptom | Most likely cause | Where to look |
| --- | --- | --- |
| Access denied for user | Wrong password, or the service account is missing `SELECT` / `SHOW VIEW` | Step 1 |
| Connection timeout | Instance not publicly reachable, or IP allowlist out of date | Step 2 |
| UI rejects Role ARN | Role name doesn’t match `SnowflakeHorizon-*` or `/SnowflakeHorizon/` | [Query Logs](/user-guide/snowflake-horizon/connectors/mysql/query-log) |
| UI says “no query log found” | General log not enabled or not exported to CloudWatch | [Query Logs](/user-guide/snowflake-horizon/connectors/mysql/query-log) |

Expand

Show lessSee more
