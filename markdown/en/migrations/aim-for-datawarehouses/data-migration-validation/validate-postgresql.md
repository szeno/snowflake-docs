# Validating Data from PostgreSQL

This page covers PostgreSQL-specific setup for [Data validation](./data-validation). For workflow field definitions, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

## Prerequisites

- **Npgsql driver** on Workers (no ODBC install). Same `ssl_mode` guidance as [Migrating Data from PostgreSQL](./migrate-postgresql).

## Connectivity

Reuse `[connections.source.postgresql]` Worker TOML from data migration:

Copy code

```
[connections.source.postgresql]
auth_method = "standard"
username = "scai"
password = "your_password"
database = "analytics"
host = "db.example.com"
port = "5432"
ssl_mode = "Require"
use_copy = true
```

Set `source_platform: postgresql` in the validation workflow YAML. Set **`ssl_mode`** in Worker TOML to match your PostgreSQL host’s TLS requirement (`Disable`, `Allow`, `Prefer`, `Require`, or `VerifyFull`).

**Example workflow excerpt:**

Copy code

```
source_platform: postgresql
target_database: TARGET_DB
schema_mappings:
  public: PUBLIC
validation_configuration:
  schema_validation: true
  metrics_validation: true
  row_validation: false
tables:
  - fully_qualified_name: public.customers
    column_names_to_partition_by:
      - customer_id
  - fully_qualified_name: public.orders
    column_names_to_partition_by:
      - order_id
    indexColumnList:
      - order_id
    validation_configuration:
      row_validation: true
```

## Data type mappings

| PostgreSQL type | Snowflake target type | Supported for validation | Notes |
| --- | --- | --- | --- |
| integer, bigint, numeric, decimal | NUMBER | Yes |  |
| real, double precision | FLOAT | Yes |  |
| boolean | BOOLEAN | Yes | Native `BOOLEAN` values are supported in L3 row validation. |
| date | DATE | Yes |  |
| time, timestamp types | TIME / TIMESTAMP | Yes |  |
| character varying, text | VARCHAR | Yes |  |
| bytea | BINARY | Yes |  |
| uuid | VARCHAR(36) | Yes | Native `UUID` values are supported in L3 row validation. |
| json, jsonb | VARIANT | Yes | Native `JSON` and `JSONB` values are supported in L3 row validation. |
| integer[], text[] | ARRAY | Yes | Native `INTEGER[]` and `TEXT[]` values are supported in L3 row validation. |
| xml |  | No |  |
| money |  | No |  |
| bit, bit varying |  | No |  |
| point |  | No |  |
| oid |  | No |  |
| interval | INTERVAL or VARCHAR | Yes | Depends on `intervalHandling`. Match the setting used for migration. See [INTERVAL columns and intervalHandling](#interval-columns-and-intervalhandling). |
| range types | VARCHAR | Yes | Compared as VARCHAR text |
| pgvector vector | VECTOR(*element\_type*, *n*) | Yes | Row-level validation compares element by element |
| PostGIS geometry/geography |  | No |  |

Expand

Show lessSee more

Important

[L3 row validation](./data-validation#row-validation-l3) supports the PostgreSQL native types in the preceding table. [L1 schema validation](./data-validation#schema-validation-l1) can report a `FAILURE` for native PostgreSQL types because of a known catalog metadata comparison limitation.

## INTERVAL columns and intervalHandling

PostgreSQL’s `interval` type can store year-month and day-time fields in the same value. Snowflake has no single interval qualifier that spans both families.

Validation uses the same `intervalHandling` choice as migration. Neither setting is universally better: choose (and keep consistent) based on how the table was migrated and what you need on Snowflake.

| `intervalHandling` | Comparison behavior | Implications |
| --- | --- | --- |
| `"interval"` (default) | Compares as Snowflake `INTERVAL DAY TO SECOND` | Matches tables migrated with `intervalHandling: "interval"`. Mixed year-month and day-time values were folded into day-time during migration (via total seconds), so calendar-accurate year-month precision is already lost on the target. Validation normalizes both sides the same way. |
| `"varchar"` | Compares as text | Matches tables migrated with `intervalHandling: "varchar"`. Preserves mixed-family interval text, but you don’t compare against a native `INTERVAL` column. |

Expand

Show lessSee more

Set `intervalHandling` at the workflow root or per table, and keep it aligned with the migration workflow for the same objects. A mismatch between migration and validation produces false `MISMATCH` results. For the property reference, see [INTERVAL data type handling](../manual-migration/data-validation-configuration-reference#interval-data-type-handling). For the migration-side choice, see [Migrating Data from PostgreSQL](./migrate-postgresql#interval-columns-and-intervalhandling).

**Prompt:**

Copy code

```
The EVENTS table was migrated with intervalHandling set to varchar. Use the same setting for validation.
```

## Platform-specific considerations

- **Starting validation**: Ask the agent to generate a validation workflow with the depth you need (schema validation, metrics validation, and row-level validation, per table).

  **Prompt:**

  Copy code

  ```
  Run cloud data validation for my PostgreSQL tables, with schema and metrics validation on all tables and row-level validation on orders
  ```
- Confirm the Worker’s **`ssl_mode`** matches your PostgreSQL host before running validation workflows; a mismatch fails connectivity, not just validation.
- **`use_copy = true`** speeds up source reads on large tables; confirm your role and network allow the PostgreSQL `COPY` path.
- **Anti-locking**: No automatic hint is added on PostgreSQL. Set `queryModifiers` only when you need custom source SQL hints. See [Anti-locking and query modifiers](../manual-migration/data-validation-configuration-reference#anti-locking-and-query-modifiers).

## Related content

- [Data validation](./data-validation)
- [Migrating Data from PostgreSQL](./migrate-postgresql)
- [Manual Migration: Data validation](../manual-migration/data-validation)
