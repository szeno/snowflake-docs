# Using Cortex Code CLI with Snowflake Postgres

The Cortex Code CLI Postgres skill lets you ask natural-language questions about a Postgres database and have
Cortex Code generate and run SQL for you. It is designed for debugging, schema exploration, and lightweight
analytics without needing to hand-write every query.

For installation, connection setup, and general Cortex Code CLI usage, see
[CoCo CLI](/user-guide/cortex-code/cortex-code-cli).

This Postgres-specific skill:

- Helps create and manage Snowflake Postgres instances.
- Translates natural-language questions into Postgres SQL.
- Executes the generated SQL against a configured Postgres instance.
- Returns a short, readable summary plus optional raw results.
- Can set up `pg_lake` for object storage and data movement between Postgres and Snowflake via Snowflake stages or S3 buckets.

## Managing connections

The skill stores connections using PostgreSQL’s native `~/.pg_service.conf` and `~/.pgpass` files,
making them compatible with all standard PostgreSQL clients (`psql`, pgAdmin, DBeaver, etc.).
When you ask Cortex Code to create an instance or reset credentials, the connection is saved automatically
via `pg_connect.py`.

Warning

Never display `.pgpass` contents in chat or logs. Use `pg_connect.py` for all credential operations.

## Running queries

Once a connection is saved, Cortex Code can run `psql` commands against your instances directly from chat.
Passwords are resolved automatically from `~/.pgpass`. You can use natural-language prompts:

- *“Show me all tables on my\_instance”*
- *“Run a SELECT on the orders table to get the last 10 rows”*
- *“What indexes exist on the users table?”*

Cortex Code translates these into `psql` commands, checks that the instance is ready (auto-resuming
if suspended), executes the query, and presents the results.

```
You:          How many orders were placed this month?
Cortex Code:  Running: psql "service=my_instance" -c \
         "SELECT count(*) FROM orders
          WHERE created >= date_trunc('month', current_date);"

         count
        -------
           142
```

Cortex Code does not execute write operations (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `TRUNCATE`)
unless you explicitly ask. Write operations require confirmation before proceeding.

## Postgres health checks

`pg_doctor` is a read-only diagnostic tool that runs health checks against a Postgres
instance with a 30-second statement timeout.

| Check | Description | Thresholds |
| --- | --- | --- |
| `cache_hit` | Index and table cache hit rate | Pass: >= 99% / Warn: 95-99% / Fail: < 95% |
| `bloat` | Table and index bloat estimation | Pass: < 30% / Warn: 30-50% / Fail: > 50% |
| `vacuum_stats` | Dead rows and autovacuum status | Warn if tables need vacuum |
| `connections` | Connection counts per role | Informational |
| `locks` | Exclusive locks held | Warn if locks present |
| `blocking` | Blocked queries | Fail if queries are blocked |
| `long_running` | Queries running longer than 5 minutes | Warn if found |
| `outliers` | Top slow queries (requires `pg_stat_statements`) | Informational |
| `unused_indexes` | Indexes never scanned | Warn if any found |
| `table_sizes` | Table size breakdown (total, index, toast) | Informational |

Expand

Show lessSee more

After presenting results, Cortex Code explains flagged checks and offers to investigate further.
Any remediation actions (`VACUUM`, `REINDEX`, etc.) require explicit confirmation before execution.

## Setting up pg\_lake

`pg_lake` is a PostgreSQL extension that enables object storage and S3 data movement on Snowflake
Postgres instances. For details on the extension itself, see [pg\_lake](/user-guide/snowflake-postgres/postgres-pg_lake).

The Cortex Code skill assists the multi-system setup (Snowflake SQL, AWS IAM, Postgres SQL) for both
Snowflake stages and S3 buckets managed outside Snowflake. You can ask Cortex Code to walk you through
the setup interactively:

- *“Set up pg\_lake on my\_instance with s3://my-bucket/data/”*
- *“Configure pg\_lake with a Snowflake managed stage on my\_instance”*

## Approval gates

Cortex Code requires confirmation before executing operations that are billable, destructive, or
security-sensitive.

| Operation | Reason |
| --- | --- |
| Create / suspend instance | Billable resource or drops active connections |
| Network policy changes | Modifies access control |
| Create / modify storage integration | Cloud resources, requires `ACCOUNTADMIN` |
| Update AWS trust policy | Modifies IAM permissions |
| Drop / destructive operations | Permanent data loss |
| Write operations from diagnostics | `VACUUM`, `REINDEX`, `pg_terminate_backend`, etc. |

Expand

Show lessSee more

Read-only operations (`SHOW`, `DESCRIBE`, health checks, `SELECT` queries) do not require approval.
