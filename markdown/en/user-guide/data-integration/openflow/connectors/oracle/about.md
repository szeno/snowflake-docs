# About Openflow Connector for Oracle

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Note

The Openflow Connector for Oracle is also subject to additional terms of service beyond the standard
connector terms of service. For more information, see the
[Openflow Connector for Oracle Addendum](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-oracle-terms/).

This topic describes the basic concepts of Openflow Connector for Oracle, its workflow, and limitations.

## About the Openflow Connector for Oracle

The Openflow Connector for Oracle connects an Oracle database instance to Snowflake and replicates
data from selected tables in near real-time or on a specified schedule.
The connector also creates a log of all data changes, which is available along
with the current state of the replicated tables.

## Use cases

The connector supports the following use case:

- Replicate Oracle database tables into Snowflake for comprehensive, centralized reporting.

## Licensing models and critical constraints

The Openflow Connector for Oracle supports three distinct licensing models. You must select the correct
model before installation. Failure to select the correct model might result in deployment
failure or unintended financial commitments.

For detailed licensing terms, comparison, and configuration instructions, see
[Oracle XStream licensing](#label-oracle-xstream-licensing).

Warning

The connector is technically compatible with Oracle Database Standard Edition (SE/SE2).
However, Oracle documentation states that “a license to Oracle Database Enterprise Edition
is a prerequisite to license and use Oracle XStream.” Before deploying the connector against
a Standard Edition database, verify your Oracle license agreement to ensure that your use
of XStream is permitted. You’re solely responsible for compliance with your Oracle license
terms.

### 1. Embedded license for 36-month commitment (Snowflake-provided)

Note

In Openflow, this license option is displayed as **Oracle Embedded License**.

Snowflake provides the Oracle XStream license to you directly for a fee. This model
allows you to consume XStream replication without a direct contract with Oracle.
For more information, see
[Embedded license details for 36-month commitment](#label-oracle-embedded-license-details-36) and the
[Openflow Connector for Oracle Addendum](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-oracle-terms/).

| Term | Details |
| --- | --- |
| Billing | Monthly license fees and Support & Maintenance (S&M) fees are drawn from your Snowflake Capacity. |
| Commitment | Activation initiates a non-cancelable 36-month term (after the 60-day trial). |
| Lifecycle | - **Post-term (36+ months)**: After the initial 36-month term, the license fee   drops to $0, but the S&M fee auto-renews in 12-month increments, billed monthly. - **Lock-out risk**: If you opt out of S&M renewal, the connector will be   permanently locked when S&M coverage ends. Unlocking the connector requires   purchasing a new Embedded License, which triggers a new 36-month commitment   at full price. |
| Management UI | All license actions (Start/Cancel Trial, Monitor Usage, Opt-out) are performed by the ORGADMIN in Snowsight under **Admin** » **Terms** » **Openflow for Oracle**. For step-by-step instructions, see [Openflow Connector for Oracle: Enable and manage commercial terms](/user-guide/data-integration/openflow/connectors/oracle/manage-commercial-terms). |
| Restrictions | The following customers are ineligible:   - Customers purchasing Snowflake through the GCP Marketplace. - Customers contracted with Snowflake through a third-party reseller. |

Expand

Show lessSee more

### 2. Embedded license for 12-month commitment (Snowflake-provided)

Note

In Openflow, this license option is displayed as **Oracle Embedded License (Public Sector)**.

Snowflake provides the Oracle XStream license to you directly for a fee. This model
allows you to consume XStream replication without a direct contract with Oracle.
For more information, see
[Embedded license details for 12-month commitment](#label-oracle-embedded-license-details-12) and the
[Openflow Connector for Oracle Addendum](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-oracle-terms/).

| Term | Details |
| --- | --- |
| Billing | One-time license fee and annual Support & Maintenance (S&M) fees are drawn from your Snowflake Capacity. |
| Commitment | Activation initiates a non-cancelable 12-month term (after the 60-day trial), with license fees paid upfront in full and S&M fees billed annually. |
| Lifecycle | - **Post-term (12+ months)**: After the initial 12-month term, the license fee   drops to $0, but the S&M fee auto-renews in 12-month increments, billed annually. - **Lock-out risk**: If you opt out of S&M renewal, the connector will be   permanently locked when S&M coverage ends. Unlocking the connector requires   purchasing a new Embedded License, which triggers a new 12-month commitment   at full price. |
| Management UI | All license actions (Start/Cancel Trial, Monitor Usage, Opt-out) are performed by the ORGADMIN in Snowsight under **Admin** » **Terms** » **Openflow for Oracle**. For step-by-step instructions, see [Openflow Connector for Oracle: Enable and manage commercial terms](/user-guide/data-integration/openflow/connectors/oracle/manage-commercial-terms). |
| Restrictions | The following customers are ineligible:   - Customers purchasing Snowflake through the GCP Marketplace. |

Expand

Show lessSee more

### 3. Independent license (Bring Your Own License, BYOL)

You provide your own Oracle license that includes XStream entitlements (for example, Oracle
GoldenGate license). For more information, see
[Independent license (BYOL) details](#label-oracle-byol-license-details).

| Term | Details |
| --- | --- |
| Billing | No additional licensing fees from Snowflake. Standard storage and compute costs (for example, Openflow Compute) will apply. |
| Compliance | You are solely responsible for compliance with your Oracle license. |
| Usage | Mandatory for GCP Marketplace customers. |

Expand

Show lessSee more

## Choosing an Oracle XStream licensing model

The Openflow Connector for Oracle requires a paid license for Oracle XStream services. Three licensing
models are available:

- Oracle Embedded License (36-month commitment)
- Oracle Embedded License (12-month commitment)
- Independent Oracle License (Bring Your Own License, BYOL)

Use the following table to determine the appropriate model for your organization.

| Consideration | Oracle Embedded License (36-month commitment) | Oracle Embedded License (12-month commitment) | Independent License (BYOL) |
| --- | --- | --- | --- |
| Who is it for? | Customers who need to license Oracle XStream technology directly through their Snowflake agreement and prefer a monthly payment schedule over 36 months. | Customers who need to license Oracle XStream technology through their Snowflake agreement but can’t agree to a multi-year commitment or prefer an upfront payment option instead of monthly payments. | Customers who already have an Oracle GoldenGate license or another Oracle agreement that provides entitlement for XStream. |
| Billing | Billed monthly through Snowflake based on the number of processor cores on your source Oracle DB. Involves a non-cancelable 36-month commitment. Also billed monthly for support and maintenance services.  Additionally, standard storage and compute costs (for example, Openflow Compute) will apply. | Billed upfront through Snowflake based on the number of processor cores on your source Oracle DB. Involves a non-cancelable 12-month commitment where all license fees are paid upfront in full. Also billed upfront for support and maintenance services annually.  Additionally, standard storage and compute costs (for example, Openflow Compute) will apply. | No additional licensing or support and maintenance fees for Oracle XStream services from Snowflake. You are responsible for all licensing and compliance directly with Oracle.  Standard storage and compute costs (for example, Openflow Compute) will apply. |
| Configuration | Requires you to input your Oracle DB’s CPU core count and Oracle’s licensing factor for its processors in the connector parameters. | Requires you to input your Oracle DB’s CPU core count and Oracle’s licensing factor for its processors in the connector parameters. | Does not require you to provide CPU core information to Snowflake. |
| Trial period | Includes a 60-day free trial for up to 16 licensed cores. Billing commences automatically on the 61st day. | Includes a 60-day free trial for up to 16 licensed cores. Billing commences automatically on the 61st day. | No trial period is offered through Snowflake. Your use is subject to your existing Oracle agreement. |

Expand

Show lessSee more

## Embedded license details for 36-month commitment

By choosing this option, you are procuring the right to use Oracle XStream technology
with the connector through Snowflake. Be aware of the following key terms:

### Billing

Oracle XStream services are billed monthly and drawn from your Snowflake capacity
balance. The fee has two components: a license fee and a Support & Maintenance
(S&M) fee. The license fee is calculated based on the number of processor cores
in your source Oracle database, multiplied by the Oracle Processor Licensing Factor.

### Commitment

The first 60 days are free for up to 16 licensed cores. However, activating the
connector beyond the 60-day trial initiates a non-cancelable 36-month billing term.

- **Automatic conversion**: Billing commences automatically on Day 61. To avoid
  charges, you must cancel the trial in the
  **Admin** » **Terms** » **Openflow for Oracle** dashboard before
  Day 60.
- **Lock-in**: If your Snowflake agreement is terminated during this term,
  the entire remaining balance for the 36-month term becomes due immediately.

### Post-term renewal and penalties

After the initial 36-month term, the license fee becomes $0 but the Support & Maintenance
(S&M) fee continues.

- **Opt-out consequence**: You can opt out of S&M renewal through the dashboard in
  **Admin** » **Terms** » **Openflow for Oracle**. However, if S&M
  coverage stops, the connector processors are locked. To resume operations, you
  must purchase a new Embedded License, which resets the 36-month full-price
  commitment.

### Requirements

You are responsible for accurately reporting the number of processor cores and the
correct licensing factor in the connector configuration. This information must be kept
current if your source database hardware changes.

### Configuration

To configure the Embedded License (36-month commitment):

- Review and accept the
  [Openflow Connector for Oracle Addendum](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-oracle-terms/)
  terms presented in the UI.
- Select the **Oracle Embedded License** tile for the 36-month commitment.
- Enter the CPU core count details for your source Oracle database:
  **Oracle Database Processor Cores** (the total number of physical cores on the
  source database server) and **Oracle Database Processor Multiplier** (the Oracle
  processor licensing factor, for example, 0.5 for Intel processors). Consult the
  Oracle Processor Core Factor Table for the correct value.

## Embedded license details for 12-month commitment

By choosing this option, you are procuring the right to use Oracle XStream technology
with the connector through Snowflake under a 12-month, upfront-billed commitment.
Be aware of the following key terms:

### Billing

Oracle XStream services are billed upfront and drawn from your Snowflake capacity
balance. The fee has two components: a license fee and a Support & Maintenance
(S&M) fee. The license fee is calculated based on the number of processor cores
in your source Oracle database, multiplied by the Oracle Processor Licensing Factor.

### Commitment

The first 60 days are free for up to 16 licensed cores. However, activating the
connector beyond the 60-day trial initiates a non-cancelable 12-month billing term.

- **Automatic conversion**: Billing commences automatically on Day 61. To avoid
  charges, you must cancel the trial in the
  **Admin** » **Terms** » **Openflow for Oracle** dashboard before
  Day 60.
- **Lock-in**: If your Snowflake agreement is terminated during this term,
  the entire remaining balance for the 12-month term becomes due immediately.

### Post-term renewal and penalties

After the initial 12-month term, the license fee becomes $0 but the Support & Maintenance
(S&M) fee continues on an annual basis.

- **Opt-out consequence**: You can opt out of S&M renewal through the dashboard in
  **Admin** » **Terms** » **Openflow for Oracle**. However, if S&M
  coverage stops, the connector processors are locked. To resume operations, you
  must purchase a new Embedded License, which resets the 12-month full-price
  commitment.

### Requirements

You are responsible for accurately reporting the number of processor cores and the
correct licensing factor in the connector configuration. This information must be kept
current if your source database hardware changes.

### Configuration

To configure the Embedded License (12-month commitment):

- Review and accept the
  [Openflow Connector for Oracle Addendum](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-oracle-terms/)
  terms presented in the UI.
- Select the **Oracle Embedded License (Public Sector)** tile for the 12-month commitment.
- Enter the CPU core count details for your source Oracle database:
  **Oracle Database Processor Cores** (the total number of physical cores on the
  source database server) and **Oracle Database Processor Multiplier** (the Oracle
  processor licensing factor, for example, 0.5 for Intel processors). Consult the
  Oracle Processor Core Factor Table for the correct value.

## Independent license (BYOL) details

This option is for customers who have already licensed the necessary Oracle technology.

### Requirements

You are solely responsible for ensuring that your use of the connector complies with
the terms of your existing Oracle license agreement. Snowflake doesn’t validate or
audit your Oracle entitlements.

### Configuration

To configure the Independent License (BYOL):

- Review and accept the
  [Openflow Connector for Oracle Addendum](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-oracle-terms/)
  terms presented in the UI.
- Select the **Independent License** type.

When configuring the connector, proceed without entering any core
count or billing-related information.

## Openflow requirements

The following Openflow runtime requirements apply to the Openflow Connector for Oracle:

- Choose the runtime size based on the sustained replication workload. For sizing guidance and how to run multiple connectors on one runtime, see [Runtime sizing](/user-guide/data-integration/openflow/connectors/oracle/setup-connector#label-oracle-runtime-sizing).
- The connector doesn’t support multi-node Openflow runtimes. Configure the
  runtime for this connector with **Min nodes** and **Max nodes** set to `1`.

## Supported Oracle versions and platforms

The following Oracle database versions and platforms are supported:

- Oracle database versions 11g and later
- On-premises servers
- Oracle Exadata
- OCI VM/Bare Metal
- AWS Custom RDS for Oracle
- AWS Standard Single-tenant RDS for Oracle

## Data Guard and standby support

You can keep replication load off the primary Oracle database by connecting to a
Data Guard standby. Which topology you need depends on whether the standby is
physical or logical.

### Active Data Guard (physical standby)

Active Data Guard is a *physical* standby: a read-only copy of the primary. You
can’t create an XStream outbound server on it, because XStream needs a writable
database for the metadata.

The connector still works with Active Data Guard. Use the physical standby for
snapshot load (`Oracle Connection URL`). For incremental (CDC) load, create the
XStream outbound server on a writable database (`XStream Out Server URL`): the
primary, or a separate
[downstream capture](https://docs.oracle.com/en/database/oracle/oracle-database/19/xstrm/xstream-out-concepts.html)
database if you want to keep CDC off the primary as well.

When you run the snapshot against Active Data Guard, set **Snapshot Fetching
Strategy** to `SEQUENTIAL_BY_PRIMARY_KEY`. The default `CONCURRENT_BY_ROWID`
strategy uses parallel tasks to split a table into ranges, which isn’t allowed
on a read-only standby.

### Logical standby

A *logical* standby is open read-write and applies changes from the primary with
SQL Apply. The connector can use a logical standby for both snapshot and CDC, so
you don’t need an additional database for XStream.

Before you create the outbound server or start the connector, set Database Guard
to `STANDBY`. Logical standbys default to `ALL`, which blocks the XStream client
with `ORA-16224: Database Guard is enabled`.

For setup steps, see
[Data Guard or standby capture (optional)](/user-guide/data-integration/openflow/connectors/oracle/setup-oracledb#label-oracle-standby-setup).

## Limitations

The following limitations apply to the Openflow Connector for Oracle:

- AWS Standard Multi-tenant RDS for Oracle isn’t supported.
- Oracle Autonomous Databases (ATP/ADW) aren’t supported.
- Oracle SaaS offerings such as Oracle Fusion Cloud Applications and NetSuite
  aren’t supported.
- Active Data Guard physical standbys are read-only, so create the XStream
  outbound server on the primary, a logical standby, or a separate downstream
  capture database. For details, see
  [Data Guard and standby support](#label-oracle-standby-data-guard-support).
- The connector requires Openflow deployment version 0.55.0 or later for BYOC.
- The Openflow runtime must be created after the required Openflow deployment
  version is installed.
- Each replicated table must have a primary key, a qualifying unique constraint, a qualifying
  unique index, or a user-declared logical key. For more information, see
  [How the connector chooses a replication key](#label-oracle-replication-key-selection).
- The connector supports common source table schema changes during replication, such as adding, dropping, and renaming columns. See [Schema changes](#label-database-schema-changes) for the full list and a few unsupported change types.
- Schema changes (such as ALTER TABLE statements that add or drop columns) aren’t supported
  while re-reading the redo logs from the earliest position. If any table’s schema was
  altered between the earliest available SCN and the current position, that table should
  be removed from replication and re-added with a fresh snapshot instead.
- The connector doesn’t detect at runtime when you drop or modify the primary key,
  unique constraint, or unique index that it uses as the replication key. This limitation also
  applies to renaming a replication-key column. After any such change,
  restart replication for the affected table: see
  [Restart table replication](/user-guide/data-integration/openflow/connectors/oracle/maintenance#label-of-oracle-restart-table-replication).
- When a logical-key value changes on the source, the connector doesn’t soft-delete
  the old row, which results in duplicate active rows in the destination. For more information,
  see [Limitation: Changes to a logical-key value](/user-guide/data-integration/openflow/connectors/oracle/setup-connector#label-oracle-logical-key-value-change).
- Updates that modify only a part of a large object (`LOB`) value by using the
  `DBMS_LOB` package, for example `DBMS_LOB.WRITEAPPEND`, `DBMS_LOB.WRITE`,
  `DBMS_LOB.ERASE`, or `DBMS_LOB.TRIM`, aren’t supported. Oracle XStream reports
  only the part of the `LOB` value that changed, but the connector needs the
  entire value to reconcile the merge query, so affected `LOB` columns are
  replicated as `NULL` in Snowflake. A common pattern that triggers this is
  inserting a row with `EMPTY_CLOB()` (or `EMPTY_BLOB()`) and then populating
  the `LOB` by using `DBMS_LOB.WRITEAPPEND`. When a `LOB` is written inline in
  a single INSERT or UPDATE statement, it is replicated correctly. For small
  `LOB` values, `DBMS_LOB.WRITEAPPEND` may produce an UPDATE LCR with the
  entire value, in which case the row is replicated correctly. When the
  connector observes an unsupported partial `LOB` operation, it logs a
  WARN-level message identifying the source table and primary key of the
  affected row so the change can be reconciled manually.
- The connector doesn’t support the truncate table operation. `TRUNCATE` statements on the source are ignored, and the corresponding row deletions are not applied to the destination table.

## How the connector works

The following sections describe how the connector works in different contexts,
including replication, schema changes, and data retention.

### How tables are replicated

The name of the destination schema is determined by the `Destination Schema Pattern` parameter. For more information, see [Snowflake Destination Parameters](/user-guide/data-integration/openflow/connectors/oracle/setup-connector#label-oracle-snowflake-destination-parameters). By default, the destination schema name is the source database name and source schema name joined by an underscore, so the fully qualified name of a destination table is:

`<destination_database>.<source_database_name>_<source_schema_name>.<source_table_name>`

The tables are replicated in the following stages:

1. Schema introspection: The connector discovers the columns in the source
   table, including the column names and types, then validates them against
   Snowflake’s and the connector’s [Limitations](#limitations). Validation failures cause
   this stage to fail, and the cycle completes. After successful completion
   of this stage, the connector creates an empty destination table in Snowflake.
2. Snapshot load: The connector copies all data available in the source table
   into the destination table. If this stage fails, then no more data is
   replicated. After successful completion, the data from the source table is
   available in the destination table.
3. Incremental load: The connector tracks
   changes in the source table and applies those changes to the destination table.
   This process continues until the table is removed from replication. Failure at this stage
   permanently stops replication of the source table until the issue is resolved.

### Schema changes

During incremental replication, the connector detects many source table schema changes and updates the destination table automatically. Unsupported changes stop replication for the affected table until you restart it.

#### Supported changes

The connector supports the following schema changes:

- **Add column.** The connector adds the column to the destination table and replicates values for new and updated rows. Existing rows aren’t backfilled; the new column is NULL for rows that existed before the change.
- **Drop column.** The connector renames the destination column with a `__SNOWFLAKE_DELETED` suffix to preserve historical values. For details, see [Dropped columns](#dropped-columns).
- **Rename column.** The connector treats a rename as dropping the original column and adding a new one. The connector retains the original column under a suffixed name; for example, a column named `A` becomes `A__SNOWFLAKE_DELETED`. For query patterns, see [Renamed columns](#renamed-columns).
- **Compatible type change.** The connector keeps replication running with the destination column type unchanged when you change a column to a source type that maps to the same Snowflake data type (for example, `INT` to `BIGINT`, both mapped to `NUMBER`).
- **Re-add a previously dropped column.** The connector adds the column as a new destination column alongside the existing soft-deleted column (for example, `A` and `A__SNOWFLAKE_DELETED`).

If you drop a column that was previously dropped and soft-deleted, replication for the affected table fails because the soft-deleted column name is already taken.

#### Unsupported changes

The connector doesn’t support the following schema changes. When one occurs, replication stops for the affected table:

- **Primary key definition change.** Adding or removing primary key columns, or changing which columns form the primary key.
- **Incompatible type change.** When the new source type maps to a different Snowflake data type (for example, `INT` to `VARCHAR`, mapped to `NUMBER` and `TEXT` respectively).
- **Numeric precision or scale change.** For example, changing `NUMERIC(7,2)` to `NUMERIC(6,3)`.
- **Character column length change.** For example, changing `VARCHAR(50)` to `VARCHAR(100)`.

To recover, restart replication for the affected table: see [Restart table replication](/user-guide/data-integration/openflow/connectors/oracle/maintenance#label-of-oracle-restart-table-replication).

Note

For incompatible type changes, the connector might report an Oracle parameter type conflict before the destination table is updated.

The same soft-delete mechanism applies when you change a table’s Column Filter JSON. For details, see [Replicate a subset of columns in a table](/user-guide/data-integration/openflow/connectors/oracle/setup-connector#label-oracle-connector-replication-subset-of-columns).

### How the connector chooses a replication key

The connector uses one column or set of columns from each source table as the
replication key. The replication key uniquely identifies a row, drives the MERGE
operation that applies CDC changes to the destination, and orders rows during the
snapshot load.

For each table, the connector resolves the replication key in this order:

1. **User-declared logical key.** If the connector is configured with a Table Key
   Configuration Service that lists the table, the connector uses those columns as the
   replication key, overriding any primary key, unique constraint, or unique index on the table. For more information, see
   [Specify a logical key for a table](/user-guide/data-integration/openflow/connectors/oracle/setup-connector#label-oracle-logical-key).
2. **Primary key.** The columns of the table’s enabled primary key constraint.
3. **Unique constraint or unique index.** If the table has no primary key, the
   connector looks for a qualifying unique constraint or unique index, as described
   in [Qualifying unique constraints and unique indexes](#label-oracle-replication-key-uk-criteria).
4. **None.** If no qualifying key is found, the connector can’t replicate the
   table. To resolve this, either add a primary key to the table, modify an existing
   constraint or index so it qualifies (see the following criteria), or declare a logical
   key on columns that uniquely identify rows. For diagnostic steps, see
   [A table fails because the connector can’t find a replication key](/user-guide/data-integration/openflow/connectors/oracle/troubleshoot#label-oracle-no-replication-key) in the troubleshooting topic.

#### Qualifying unique constraints and unique indexes

The connector evaluates a unique constraint as a candidate replication key only when:

- The constraint type is `UNIQUE` and `STATUS = ENABLED` in `ALL_CONSTRAINTS`.
- The constraint isn’t initially deferred (`DEFERRED = IMMEDIATE`). Constraints
  declared `DEFERRABLE INITIALLY IMMEDIATE` qualify; `DEFERRABLE INITIALLY DEFERRED`
  doesn’t.
- All columns covered by the constraint are `NOT NULL`.

The connector evaluates a unique index as a candidate replication key only when:

- `UNIQUENESS = UNIQUE` and the index isn’t `UNUSABLE` in `ALL_INDEXES`.
- `INDEX_TYPE = NORMAL` (a standard B-tree index). Bitmap and function-based unique
  indexes are excluded.
- The index isn’t the implementation of a primary or unique constraint
  (constraint-backed indexes are evaluated through the constraint, not separately).
- All columns covered by the index are `NOT NULL`.

Note

`LOB`, `CLOB`, `NCLOB`, `LONG`, and similar large-object columns can’t appear
in unique constraints or unique indexes in Oracle, so they never qualify as
replication-key columns.

#### Tiebreakers

When more than one candidate qualifies, the connector picks one deterministically using
the following preferences, in order:

1. Among all candidates, a unique constraint is preferred over a unique index.
2. Among candidates of the same type, the candidate with the fewest columns is preferred.
3. Among candidates with the same column count, the candidate with the most numeric
   columns is preferred. The connector counts the following Oracle types as numeric:
   `NUMBER`, `INTEGER`, `INT`, `SMALLINT`, `FLOAT`, `DOUBLE`, `BINARY_FLOAT`,
   `BINARY_DOUBLE`.
4. If a tie remains, the candidate with the lowest constraint or index name in
   alphabetical order is selected.

If you want a specific column set used regardless of the tiebreaker outcome, declare it
as a logical key. For more information, see [Specify a logical key for a table](/user-guide/data-integration/openflow/connectors/oracle/setup-connector#label-oracle-logical-key).

#### Replication key examples

The following table has no primary key but has a unique constraint on a `NOT NULL`
column. The constraint qualifies, and the connector replicates the table using the
constraint as the replication key:

Copy code

```
CREATE TABLE customers (
    email      VARCHAR2(255) NOT NULL,
    name       VARCHAR2(100),
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    CONSTRAINT uk_customers_email UNIQUE (email)
);
```

The following table has no primary key and no unique constraint, but a unique B-tree
index on a `NOT NULL` column. The index qualifies, and the connector replicates the
table using the index as the replication key:

Copy code

```
CREATE TABLE sessions (
    session_id VARCHAR2(64) NOT NULL,
    user_id    NUMBER,
    created_at TIMESTAMP
);

CREATE UNIQUE INDEX idx_sessions_id ON sessions (session_id);
```

The following table doesn’t qualify for automatic replication-key selection: the
unique-constraint column is nullable. To replicate this table, add a `NOT NULL`
constraint, replace the column with one that’s `NOT NULL`, or specify a logical
key:

Copy code

```
CREATE TABLE products (
    sku  VARCHAR2(50),
    name VARCHAR2(100),
    CONSTRAINT uk_products_sku UNIQUE (sku)
);
```

### Changes to a replication key value

When a source update changes the replication key value of an existing row, the
connector can’t update the destination row in place because the row’s identity
changes. Instead, it splits the source update into two operations on the
destination table:

1. The destination row keyed by the **old** value is soft-deleted: its
   `_SNOWFLAKE_DELETED` metadata column is set to `TRUE`.
2. A new destination row is inserted keyed by the **new** value, with the
   updated payload and `_SNOWFLAKE_DELETED` set to `FALSE`.

The destination table therefore contains two rows after the change: the
original row, soft-deleted, and a new row under the new key value. To query only
current rows, filter on `_SNOWFLAKE_DELETED = FALSE`.

This behavior applies when the replication key is a primary key or an
auto-detected unique constraint or unique index. User-declared logical keys
behave differently: see the limitation described in
[Limitation: Changes to a logical-key value](/user-guide/data-integration/openflow/connectors/oracle/setup-connector#label-oracle-logical-key-value-change).

### Oversized values

By default, the connector replicates individual values up to **16 MB**. When the connector encounters a larger value, it marks the associated table as permanently failed and stops replicating it. To change how the connector handles oversized values (for example, to replace them with `NULL` instead), modify the **Oversized Value Strategy** destination parameter.

If your Snowflake account has the `ENABLE_OPENFLOW_CDC_ORACLE_SSV2` parameter set to `true`, the per-value limit can be raised from 16 MB to **128 MB**.

For details and instructions on enabling the 128 MB per-value limit, see [Increase the oversized value limit](/user-guide/data-integration/openflow/connectors/oracle/maintenance#label-of-oracle-increase-oversized-value-limit).

### Error handling for invalid rows

An *invalid row* is a row that Snowflake rejects during ingestion because it can’t be written to the destination table, for example, a value that can’t be converted to the destination column’s type, or a missing required column. The **Error Handling Strategy** parameter controls what the connector does when it encounters an invalid row:

- **Fail Table** (default): On the first invalid row, the connector marks the table as permanently failed and stops replicating it, preserving strict, all-or-nothing replication. After you fix the source data, resume replication as described in [Restart table replication](/user-guide/data-integration/openflow/connectors/oracle/maintenance#label-of-oracle-restart-table-replication).
- **Log Errors and Continue**: The connector keeps replicating the valid rows and records each rejected row, together with its original payload and error details, in the table’s *error table*. The table isn’t marked as failed.

To change the strategy, set the **Error Handling Strategy** parameter. For more information, see [Snowflake Destination Parameters](/user-guide/data-integration/openflow/connectors/oracle/setup-connector#label-oracle-snowflake-destination-parameters).

#### How rejected rows are captured

The connector loads data with Snowpipe Streaming, so error logging behaves exactly as described in [Error logging in Snowpipe Streaming](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables). When you select **Log Errors and Continue**, the connector creates new destination and journal tables with the [`ERROR_LOGGING`](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables#turn-on-error-logging) property set to `TRUE`, so rejected rows are captured in a dedicated error table instead of aborting the load. The error table stores the original payload sent to Snowflake before any transformation, along with error details.

Query a table’s error table with the `ERROR_TABLE` table function:

Copy code

```
SELECT * FROM ERROR_TABLE(<destination_database>.<schema>.<table>) ORDER BY timestamp;
```

Where a rejected row lands depends on the replication stage:

- **Snapshot load**: The rejected row is written to the destination table’s error table.
- **Incremental (CDC) load**: The rejected row is written to the journal table’s error table, because CDC changes are first written to the journal table before they’re merged into the destination table.

The connector enables error logging only on tables that it creates after you select **Log Errors and Continue**. To capture rejected rows for tables that were already being replicated, enable error logging on their existing destination and journal tables with the stored procedure in [Enable error logging on an existing schema](/user-guide/data-integration/openflow/connectors/oracle/maintenance#label-of-oracle-enable-error-logging-existing-schema).

Note

When the connector encounters invalid rows, it emits a `WARN` log entry that includes the number of rejected rows. Use these entries to monitor rejected-row activity.

#### Consume rejected rows

To process rejected rows programmatically, create a stream on the error table and consume it like any other Snowflake stream. For more information, see [Streams on error tables](/user-guide/data-load-overview#streams-on-error-tables).

# Understanding data retention

The connector follows a data retention philosophy where customer data is never automatically deleted.
You maintain full ownership and control over your replicated data, and the connector preserves historical
information rather than permanently removing it.

This approach has the following implications:

- Rows deleted from the source table are soft-deleted in the destination table rather than physically removed.
- Columns dropped from the source table are renamed in the destination table rather than dropped.
- Journal tables are retained indefinitely and are not automatically cleaned up.

## Destination table metadata columns

Each destination table includes the following metadata columns that track replication information:

| Column name | Type | Description |
| --- | --- | --- |
| `_SNOWFLAKE_INSERTED_AT` | TIMESTAMP\_NTZ | The timestamp when the row was originally inserted into the destination table. |
| `_SNOWFLAKE_UPDATED_AT` | TIMESTAMP\_NTZ | The timestamp when the row was last updated in the destination table. |
| `_SNOWFLAKE_DELETED` | BOOLEAN | Indicates whether the row was deleted from the source table. When `true`, the row has been soft-deleted and no longer exists in the source. |

Expand

Show lessSee more

## Soft-deleted rows

When a row is deleted from the source table, the connector does not physically remove it from the
destination table. Instead, the row is marked as deleted by setting the `_SNOWFLAKE_DELETED` metadata
column to `true`.

This approach allows you to:

- Retain historical data for auditing or compliance purposes.
- Query deleted records when needed.
- Decide when and how to permanently remove data based on your requirements.

To query only active (non-deleted) rows, filter on the `_SNOWFLAKE_DELETED` column:

Copy code

```
SELECT * FROM my_table WHERE _SNOWFLAKE_DELETED = FALSE;
```

To query deleted rows:

Copy code

```
SELECT * FROM my_table WHERE _SNOWFLAKE_DELETED = TRUE;
```

## Dropped columns

When a column is dropped from the source table, the connector does not drop the corresponding column
from the destination table. Instead, the column is renamed by appending the `__SNOWFLAKE_DELETED` suffix
to preserve historical values.

For example, if a column named `EMAIL` is dropped from the source table, it is renamed to
`EMAIL__SNOWFLAKE_DELETED` in the destination table. Rows that existed before the column was dropped
retain their original values, while rows added after the drop have `NULL` in this column.

You can still query historical values from the renamed column:

Copy code

```
SELECT EMAIL__SNOWFLAKE_DELETED FROM my_table;
```

## Renamed columns

Due to limitations in CDC (Change Data Capture) mechanisms, the connector cannot distinguish between
a column being renamed and a column being dropped followed by a new column being added. As a result,
when you rename a column in the source table, the connector treats this as two separate operations:
dropping the original column and adding a new column with the new name.

For example, if you rename a column from `A` to `B` in the source table, the destination table
will contain:

- `A__SNOWFLAKE_DELETED`: Contains values from before the rename. Rows added after the rename have
  `NULL` in this column.
- `B`: Contains values from after the rename. Rows that existed before the rename have `NULL`
  in this column.

### Querying renamed columns

To retrieve data from both the original and renamed columns as a single unified column, use a
`COALESCE` or `CASE` expression:

Copy code

```
SELECT
    COALESCE(B, A__SNOWFLAKE_DELETED) AS A_RENAMED_TO_B
FROM my_table;
```

Alternatively, using a `CASE` expression:

Copy code

```
SELECT
    CASE
        WHEN B IS NOT NULL THEN B
        ELSE A__SNOWFLAKE_DELETED
    END AS A_RENAMED_TO_B
FROM my_table;
```

### Creating a view for renamed columns

Rather than manually modifying the destination table, you can create a view that presents the renamed
column as a single unified column. This approach is recommended because it preserves the original data
and avoids potential issues with ongoing replication.

Copy code

```
CREATE VIEW my_table_unified AS
SELECT
    *,
    COALESCE(B, A__SNOWFLAKE_DELETED) AS A_RENAMED_TO_B
FROM my_table;
```

Important

Manually modifying the destination table structure (such as dropping or renaming columns) is not
recommended, as it may interfere with ongoing replication and cause data inconsistencies.

## Journal tables

During incremental replication, changes from the source database are first written to journal tables
before being merged into the destination tables. The connector does not automatically remove data from
journal tables, as this data may be useful for auditing, debugging, or reprocessing purposes.

Journal tables are created in the same schema as their corresponding destination tables and follow
this naming convention:

`<TABLE_NAME>_JOURNAL_<timestamp>_<number>`

Where:

- `<TABLE_NAME>` is the name of the destination table.
- `<timestamp>` is the creation timestamp in Unix epoch format (seconds since January 1, 1970),
  ensuring uniqueness.
- `<number>` starts at 1 and increments whenever the destination table schema changes, either due to
  schema changes in the source table or modifications to column filters.

For example, if your destination table is `SALES.ORDERS`, the journal table might be named
`SALES.ORDERS_JOURNAL_1705320000_1`.

Important

Do not drop journal tables while replication is in progress. Removing an active journal table may
cause data loss or replication failures. Only drop journal tables after the corresponding source
table has been fully removed from replication.

### Managing journal table storage

If you need to manage storage costs by removing old journal data, you can create a Snowflake task
that periodically cleans up journal tables for tables that are no longer being replicated.

Before implementing journal cleanup, verify that:

- The corresponding source tables have been fully removed from replication.
- You no longer need the journal data for auditing or processing purposes.

For information on creating and managing tasks for automated cleanup, see
[Introduction to tasks](/user-guide/tasks-intro).

## Next steps

After reviewing this topic, consider the following next steps:

- Review [Openflow Connector for Oracle: Enable and manage commercial terms](/user-guide/data-integration/openflow/connectors/oracle/manage-commercial-terms) to enable the connector, accept the Oracle
  XStream terms, and configure your licensing model.
- Review [Openflow Connector for Oracle: Data mapping](/user-guide/data-integration/openflow/connectors/oracle/data-mapping) to understand how the connector maps data types
  to Snowflake data types.
- Review [Set up tasks for the Openflow Connector for Oracle](/user-guide/data-integration/openflow/connectors/oracle/setup-tasks) to set up the connector.
