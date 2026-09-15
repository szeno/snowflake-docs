# Data movement

Snowflake Postgres offers two complementary ways to move data between your Postgres instance and
Snowflake. Both are built into the platform — no external CDC service, no connectors, no separate
infrastructure to run.

- **[Data mirroring](/user-guide/snowflake-postgres/postgres-data-mirroring)** for continuous,
  whole-table replication into Snowflake with schema evolution and a queryable change feed.
- **[pg\_lake](/user-guide/snowflake-postgres/postgres-pg_lake)** for selective, on-demand data
  movement between Postgres and Iceberg tables, stages, or customer-managed cloud storage.

## Compare your options

|  | Data mirroring | pg\_lake |
| --- | --- | --- |
| **What moves** | Whole tables, continuously | Specific data you select |
| **Direction** | Postgres → Snowflake (currently) | Bidirectional |
| **Latency** | ~30 seconds via $live views; configurable syncs | On-demand (you control when data moves) |
| **Use case** | Analytics replica of operational data | Selective sync, file exchange, Iceberg tables |

Expand

Show lessSee more

You can use both in the same account — they solve different problems.

## Data mirroring

Data mirroring continuously replicates tables from Snowflake Postgres into a Snowflake analytics
database. Every insert, update, delete, and schema change on the source appears on the target
automatically, without ETL pipelines, batch jobs, or third-party connectors.

Use it when you want the analytics side to look like a live, always-fresh copy of the OLTP side.

**Learn more:** [Data mirroring](/user-guide/snowflake-postgres/postgres-data-mirroring)

## pg\_lake

pg\_lake is a Postgres extension that lets you selectively move data between Postgres and
object-storage formats like Parquet and Iceberg. With pg\_lake, you can create Iceberg tables
directly in Postgres, sync individual datasets to Snowflake, or exchange files bidirectionally
through stages or customer-managed cloud storage.

Use it when you need direct control over what moves and when, or when you need file-based
exchange or bidirectional data movement.

**Learn more:** [pg\_lake](/user-guide/snowflake-postgres/postgres-pg_lake)
