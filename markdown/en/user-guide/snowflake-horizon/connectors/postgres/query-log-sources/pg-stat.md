# Query statistics (pg\_stat\_statements)

Horizon Catalog can read query statistics from the PostgreSQL `pg_stat_statements` extension
over the same database connection it uses for metadata. No AWS credentials, CloudWatch log
export, or IAM role is required.

Use this log type for Snowflake Postgres and for any other PostgreSQL instance that has
`pg_stat_statements` installed. Select **Query statistics (pg\_stat\_statements)** as the log
type in the Horizon Catalog PostgreSQL connector wizard.

This log type is optional. Select **None** if you don’t want Horizon Catalog to read query
statistics. Metadata still syncs; lineage and popularity stay empty except for lineage that
comes from view definitions.

## Before you start

To use query statistics as the log source, you need the following:

- A PostgreSQL user dedicated to Horizon Catalog, with `CONNECT` on each database and
  `USAGE` on each schema you want crawled.
- Membership in the built-in `pg_read_all_stats` role for that user, so Horizon Catalog can
  read statements run by other users.
- The `pg_stat_statements` extension created in the database you enter in the connector
  wizard.

Complete the following steps:

1. [Enable pg\_stat\_statements](#1-enable-pg_stat_statements).
2. [Grant access to query statistics](#2-grant-access-to-query-statistics).
3. [Finish in the Horizon Catalog UI](#3-finish-in-the-horizon-catalog-ui).

## 1. Enable pg\_stat\_statements

### Snowflake Postgres

Note

The `pg_stat_statements` extension is available on Snowflake Postgres. You don’t need to
change `shared_preload_libraries` or restart the instance. However, the extension must be
created separately in each database where you want to use it.

Copy code

```
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

Run this command as `snowflake_admin` in the database you enter in the Horizon Catalog
connector wizard. To verify that the extension exists in that database, run:

Copy code

```
SELECT * FROM pg_extension WHERE extname = 'pg_stat_statements';
```

For details, see [Snowflake Postgres Extensions](/user-guide/snowflake-postgres/postgres-extensions).

### Self-managed PostgreSQL, Amazon RDS, and Aurora

PostgreSQL records statement statistics only when both of the following are true:

1. `pg_stat_statements` is in the `shared_preload_libraries` server setting, and the server
   has been restarted after that change. On Amazon RDS and Aurora, that setting is in the
   instance or cluster parameter group.
2. The extension is created in the database Horizon Catalog connects to:

   Copy code

   ```
   CREATE EXTENSION pg_stat_statements;
   ```

To verify, connect with the Horizon Catalog user and run:

Copy code

```
SELECT * FROM pg_stat_statements LIMIT 1;
```

For details, see [pg\_stat\_statements](https://www.postgresql.org/docs/current/pgstatstatements.html)
in the PostgreSQL documentation.

## 2. Grant access to query statistics

Without this grant, PostgreSQL replaces other users’ statement text with
`<insufficient privilege>`, and Horizon Catalog can’t ingest those queries.

Copy code

```
GRANT pg_read_all_stats TO snowflake_horizon;
```

Replace `snowflake_horizon` with the user you created for the connector.

On Snowflake Postgres, `snowflake_admin` is already a member of `pg_read_all_stats`. Grant
the role to the dedicated Horizon Catalog user instead of connecting as `snowflake_admin`.

To verify, connect as the Horizon Catalog user and run:

Copy code

```
SELECT query FROM pg_stat_statements LIMIT 10;
```

If the rows show `<insufficient privilege>`, the grant is missing.

## 3. Finish in the Horizon Catalog UI

1. In Snowflake, open **Catalog > Connections** and select **PostgreSQL**.
2. Enter the connection details for your instance.
3. For **Log type**, select **Query statistics (pg\_stat\_statements)**. You don’t need a
   role ARN, AWS Region, or instance identifier for this log type.
4. Select **Test connection**, then **Save**, then select the databases and schemas you want
   crawled.

A successful test confirms that Horizon Catalog could log in as the PostgreSQL user, that
`pg_stat_statements` is installed in the database you specified, and that the user can read
statements run by other users.

Metadata typically appears within a few minutes. The first query-statistics sync creates a
baseline and emits one record for each readable statement so that initial lineage isn’t empty.
Later syncs collect executions that occur after that baseline. Allow 24-48 hours for lineage
and popularity to accumulate.

## What this log type captures

`pg_stat_statements` is a statistics view, not a full query log. That has the following
effects on lineage and popularity in Horizon Catalog:

- Query text is normalized. Literal values are replaced by placeholders such as `$1`, and
  the text is truncated at the server’s `track_activity_query_size`. Table and column
  lineage still work; literal values are not stored.
- There is no historical backfill. The first sync emits one record for each readable
  statement, but doesn’t reconstruct its historical execution count.
- Statistics live in memory. Restarting the instance resets the counters. Statements can
  also drop out of the view when it exceeds `pg_stat_statements.max`. Some executions may
  not appear in lineage.

If you need a durable, per-execution query log on Amazon RDS or Aurora, use the CloudWatch
log type on those deployment pages instead.

## Troubleshooting

Use the following table to troubleshoot query-statistics setup:

| Symptom | Most likely cause | Where to look |
| --- | --- | --- |
| Query statistics are not available in PostgreSQL | `pg_stat_statements` isn’t in `shared_preload_libraries`, or `CREATE EXTENSION` wasn’t run | [Step 1](#1-enable-pg_stat_statements) |
| Unable to read PostgreSQL query statistics of other users | The connector user isn’t a member of `pg_read_all_stats` | [Step 2](#2-grant-access-to-query-statistics) |
| Lineage and popularity stay empty after a successful test | **Log type** is **None**, or no statements have been recorded since the first sync | Recheck the log type; run workload against the database, then wait for a sync |
| Authentication failed for the PostgreSQL user | Wrong password, or the user lacks `CONNECT` on the database | Deployment setup guide, create-user step |
| Connection timeout | Instance isn’t reachable from Horizon Catalog | Amazon RDS: [Ensure network connectivity](/user-guide/snowflake-horizon/connectors/postgres/aws-rds#2-ensure-network-connectivity). Aurora: [Ensure network connectivity](/user-guide/snowflake-horizon/connectors/postgres/aws-aurora#2-ensure-network-connectivity). Snowflake Postgres: [Snowflake Postgres networking](/user-guide/snowflake-postgres/postgres-network). Self-hosted: confirm the instance is reachable from Horizon Catalog on the PostgreSQL port. |

Expand

Show lessSee more

## Connection security

Horizon Catalog uses a TLS-capable PostgreSQL client. If the instance accepts TLS
connections, the connection is encrypted automatically. If TLS isn’t available on the
server, the connection proceeds unencrypted.

Snowflake Postgres requires SSL. For other deployments, enable TLS 1.2 or higher on the
instance. For more details, see
[Security and data protection](/user-guide/snowflake-horizon/connectors/security).
