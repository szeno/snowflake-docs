# Snowflake storage for Apache Iceberg™ tables

Snowflake storage is the recommended way to store data for [Snowflake-managed Iceberg tables](/user-guide/tables-iceberg#label-tables-iceberg-snowflake-as-catalog).
With this option, Snowflake stores and manages the Iceberg table files for you, so you don’t need to configure or
grant access to external cloud storage.

If you need to keep table files in your own cloud storage or want to use an external Iceberg catalog,
use [external volume storage](/user-guide/tables-iceberg-managing-external-volumes) instead.
For a comparison of both storage options, see [Storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-storage).

This feature works with the [Snowflake Horizon Catalog](/user-guide/snowflake-horizon),
so you can use an external query engine to connect to an Iceberg table that uses Snowflake storage.
For more information, see [Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon). In addition, you can
query these same tables in Snowflake.

Note

This feature is currently available only for accounts hosted on Amazon Web Services (AWS) or Azure.
This feature is not available in government regions or in the People’s Republic of China.

## How Snowflake storage works

When you create an Iceberg table with Snowflake storage, Snowflake manages all data and metadata files internally.
You don’t need to configure an external volume or grant Snowflake access to your cloud storage.

### Create an Iceberg table with Snowflake storage

Copy code

```
CREATE ICEBERG TABLE my_iceberg_table_defaults (col1 int)
  CATALOG = SNOWFLAKE
  EXTERNAL_VOLUME = SNOWFLAKE_MANAGED;
```

Explicit `TRANSIENT` table with Snowflake-managed storage:

Copy code

```
CREATE TRANSIENT ICEBERG TABLE my_iceberg_table_internal (col1 int)
  CATALOG = SNOWFLAKE
  EXTERNAL_VOLUME = SNOWFLAKE_MANAGED;
```

- `CATALOG` must be `SNOWFLAKE` for this storage model. If your account default catalog is Snowflake, you can omit `CATALOG`.
- `EXTERNAL_VOLUME` must be `SNOWFLAKE_MANAGED` when you are using Snowflake storage. If your default external volume
  is `SNOWFLAKE_MANAGED`, you can omit `EXTERNAL_VOLUME`.

### The `SNOWFLAKE_MANAGED` external volume

`EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'` selects Snowflake-provided storage for the table. `SNOWFLAKE_MANAGED` is a reserved
value, not a user-created [external volume](/sql-reference/sql/create-external-volume) object. You don’t run `CREATE EXTERNAL VOLUME`
for this path.

For Iceberg tables that store files in **your** cloud storage instead, you create an external volume, grant `USAGE`, and set
`EXTERNAL_VOLUME` to that volume’s name. For instructions, see [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

### Permanent and transient tables

Iceberg tables that use Snowflake storage can be permanent or transient:

- **Permanent** (default): Table data is protected by [Fail-safe](/user-guide/data-failsafe),
  the same 7-day data recovery feature that Snowflake provides for standard tables.
- **Transient**: Table data is not protected by Fail-safe. Storage and time travel behavior follow
  [transient tables](/user-guide/tables-temp-transient#label-table-type-transient) in Snowflake. Transient tables don’t incur Fail-safe storage costs.

Use the `TRANSIENT` keyword in the [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table-snowflake) statement
to create a transient Iceberg table.

Note

Transient Iceberg tables are only supported with Snowflake storage. You can’t create a transient Iceberg table
that uses a customer-managed external volume.

Tip

To check whether an existing Iceberg table is permanent or transient, run [SHOW TABLES](/sql-reference/sql/show-tables)
and look at the `kind` column. The value is `TRANSIENT` for transient tables and `TABLE` for permanent tables.

### Default catalog and external volume

If you omit `CATALOG` and `EXTERNAL_VOLUME` on the statement, Snowflake resolves them from schema, database, and account
defaults (schema overrides database, database overrides account). When the effective catalog is Snowflake (`CATALOG = 'SNOWFLAKE'`),
the default external volume is `SNOWFLAKE_MANAGED` unless a different default is set at a lower level. For more information, see
[Set a default catalog at the account, database, or schema level](/user-guide/tables-iceberg-configure-catalog-integration#label-tables-iceberg-configure-catalog-set-level) and [Set a default external volume at the account, database, or schema level](/user-guide/tables-iceberg-configure-external-volume#label-tables-iceberg-configure-external-volume-set-level).

When you set `CATALOG = 'SNOWFLAKE'` explicitly, the default external volume is `SNOWFLAKE_MANAGED` unless you override it with
`EXTERNAL_VOLUME` or a schema, database, or account default that names another volume.

## Replication

You can replicate Iceberg tables that use Snowflake storage by using a failover or replication group.
To enable replication for these tables, you must first enable replication for Snowflake-managed Iceberg tables
by following the steps in [Configure replication for Snowflake-managed Apache Iceberg™ tables](/user-guide/tables-iceberg-replication).

Unlike standard Snowflake-managed Iceberg tables, you don’t need to include `EXTERNAL VOLUMES` in the
`OBJECT_TYPES` list of your failover or replication group. Snowflake automatically manages the storage for
replicated tables that use the `SNOWFLAKE_MANAGED` external volume.

For example, create a failover group that replicates a database containing Iceberg tables that use Snowflake storage:

Copy code

```
CREATE FAILOVER GROUP my_iceberg_fg
  OBJECT_TYPES = DATABASES
  ALLOWED_DATABASES = my_iceberg_database
  ALLOWED_ACCOUNTS = myorg.my_account_1;
```

### Considerations for replication

- Replication to accounts hosted on Google Cloud Platform (GCP) isn’t supported. Snowflake skips Iceberg tables that
  use Snowflake storage during refresh operations when the target account is hosted on GCP.
- If you created Iceberg tables during the private preview using an external volume other than `SNOWFLAKE_MANAGED`,
  Snowflake automatically migrates the replicated table on the secondary account to use the `SNOWFLAKE_MANAGED`
  volume. Note the following about this migration:
  - If you include `EXTERNAL VOLUMES` in the `OBJECT_TYPES` list of the failover or replication group,
    the private preview external volume is replicated to the secondary account, but it isn’t attached to the table.
    All usages of the private preview external volume on the secondary account are blocked.
  - Snowflake recommends that you drop any Iceberg tables that use a private preview external volume and recreate them
    using `EXTERNAL_VOLUME = SNOWFLAKE_MANAGED` before you enable replication.

## Billing

Snowflake bills your account for the following usage:

### Storage cost

- Snowflake charges for every byte stored in Snowflake.

  Snowflake aggregates the storage usage for Iceberg
  tables that use Snowflake storage in the `STORAGE_BYTES` column of the [STORAGE\_USAGE view](/sql-reference/account-usage/storage_usage), together
  with storage usage for non-Iceberg tables.
  Only files that are committed to the catalog are included in `STORAGE_BYTES`. Snowflake doesn’t bill for abandoned commits.

  The cost for this storage cost usage is described in Table 3(a) of the
  [Snowflake service consumption table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) on the Snowflake website.

### Request cost

Note

Any time you use a query engine through Horizon Catalog to access Iceberg tables that are stored in Snowflake, the query engine is
considered an external query engine. When you use an external query engine to access these tables, Snowflake bills your account for this access.

The following list describes some cases where external query engines access Iceberg tables that are stored in Snowflake:

- Snowflake engines that access the table through Horizon Catalog from another Snowflake account. For example, if a table is managed by Snowflake account A but you access
  the table from the Snowflake engine in account B through Horizon Catalog, you are charged for this access. You are charged for this access because
  the Snowflake engine in account B is an external query engine.
- Third-party query engines that you deploy within the Snowflake network by using Snowflake Container Services.
  When you use these engines through Horizon Catalog to access the table, the engine is external and
  their requests are billed in the same way as other third-party query engines.
- Third-party query engines that you deploy outside of Snowflake that you use to connect to the table through Horizon Catalog.

Snowflake doesn’t bill your account when you use the Snowflake query engine to *directly* access these Iceberg tables, which
means you don’t access them through Horizon Catalog. For example, if a table is managed by account A and you
use the Snowflake engine in account A to access the table, you aren’t charged for this access.

- When you use an external query engine through Snowflake Horizon Catalog to access Iceberg tables that use Snowflake storage, Snowflake
  bills your account a per-request fee for each HTTP request sent to the underlying storage system. The rate depends on the request type:

  - PUT, COPY, POST, PATCH and LIST operations, which are billed as “class 1”.
  - GET and SELECT operations, which are billed as “class 2”.

  To view the request counts for these operation types, use the
  [STORAGE\_REQUEST\_HISTORY](/sql-reference/account-usage/storage_request_history) Account Usage view.
  This usage is billed under the `STORAGE_REQUEST-1` and `STORAGE_REQUEST-2` SKUs on the billing report.

  This rate is described in Table 3(g) of the [Snowflake service consumption table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

### Data transfer cost

- When you use an external query engine through Horizon Catalog to access the table from a different region or with another cloud provider,
  a standard data transfer charge is billed on a per-byte basis.

  This data transfer charge is described in Tables 4(a), 4(b), and 4(c) of the
  [Snowflake service consumption table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

  For more information, see [Understanding data transfer cost](/user-guide/cost-understanding-data-transfer).

### Storage optimization cost

For Iceberg tables that use Snowflake storage, data compaction is bundled (no separate compaction
charge) for tables that are written *only* by Snowflake. While a table is written only by Snowflake,
the [ICEBERG\_STORAGE\_OPTIMIZATION\_HISTORY](/sql-reference/account-usage/iceberg_storage_optimization_history)
view reports `0` in the `CREDITS_USED` column for that table.

A table starts being charged for compaction once an external engine performs DML or DDL on the
table through the Iceberg REST Catalog (IRC) on or after May 21, 2026. From that point on, compaction
charges for that table appear in the `CREDITS_USED` column of the `ICEBERG_STORAGE_OPTIMIZATION_HISTORY`
view.

To disable data compaction, see [Set data compaction](/user-guide/tables-iceberg-manage#label-tables-iceberg-manage-set-data-compaction).

## Private connectivity

When you use an external query engine to access Iceberg tables that use Snowflake storage, you can configure
private connectivity so that traffic doesn’t traverse the public internet.

For setup instructions, see [To Snowflake-managed storage volumes](/user-guide/private-connectivity-inbound#label-private-connect-managed-volumes).

## Considerations and limitations

Consider the following when you work with Iceberg tables that use Snowflake storage.

Note

When you use an external query engine to access Iceberg tables that use Snowflake storage, additional considerations apply.
For more information, see [Considerations for accessing Iceberg tables with an external query engine](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-considerations).

### Cloud provider support

This feature is currently available only for accounts hosted on Amazon Web Services (AWS) or Microsoft Azure.
This feature is not available in government regions or in the People’s Republic of China.

### Encryption

Iceberg tables that use Snowflake storage support only server-side encryption (SSE).
Customer-managed keys (CMK) are not supported, even if your account has
[Tri-Secret Secure](/user-guide/security-encryption-tss) enabled.

Important

Starting May 26, 2026, accounts that have Tri-Secret Secure enabled may not be able to
create Iceberg tables that use Snowflake storage. Affected accounts receive an error
that directs them to contact Snowflake Support to enable the feature.

To enable your account, an account administrator must contact
[Snowflake Support](/user-guide/contacting-support) to start the enablement process.

### Cloning behavior

Warning

The Iceberg table that you create uses catalog-vended credentials. When you clone an Iceberg table that uses catalog-vended credentials, the cloned table
shares the same base location as the source table. The same credentials can be used to access the shared base location, so the cloned table has write
access to the source table.

For tables that use Snowflake-managed storage (`EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'`), `CREATE ICEBERG TABLE ... CLONE` succeeds only when the
source table and the new table are **both** transient or **both** permanent. If one is transient and the other is permanent, the statement fails.

| Source table | Clone | Result |
| --- | --- | --- |
| Transient | Transient | Supported |
| Permanent | Permanent | Supported |
| Transient | Permanent | Not supported |
| Permanent | Transient | Not supported |

Expand

Show lessSee more

For command syntax and more cloning behavior, see [CREATE ICEBERG TABLE … CLONE](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-clone-syntax) in [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-snowflake)
and [Cloning and Apache Iceberg™ tables](/user-guide/object-clone#label-cloning-and-iceberg-tables).

### Ingesting data

You can ingest data into Iceberg tables that use Snowflake storage using the following methods:

- **Snowpipe**: Use [Snowpipe](/user-guide/data-load-snowpipe-intro) to load data from files in cloud storage
  using [COPY INTO](/sql-reference/sql/copy-into-table). Snowpipe works with both permanent and transient Iceberg tables.
- **Snowpipe Streaming**: Use [Snowpipe Streaming high-performance](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview)
  to ingest streaming data. Snowpipe Streaming works with both permanent and transient Iceberg tables.
