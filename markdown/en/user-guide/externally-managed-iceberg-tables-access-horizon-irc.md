# Access externally managed Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog

Regional availability

- Available on Amazon S3, Google Cloud, or Microsoft Azure in all commercial regions.
- Not available on FedRAMP (Moderate) or FedRAMP (High) deployments.

This topic describes how to access externally managed Apache Iceberg™ tables through Snowflake Horizon Catalog by using
external query engines. The tables can be in a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database)
or in a standard Snowflake database. To create an externally managed table in a standard Snowflake database, see
[Create an Iceberg table in a standard Snowflake database](/user-guide/tables-iceberg-externally-managed-writes#label-tables-iceberg-external-writes-create-table-standard-db).

With this feature, you can use the Horizon Iceberg REST Catalog (IRC) API to access and operate on Iceberg tables from
external engines such as Apache Spark™, Trino, DuckDB, or PyIceberg. This extends the existing
[Horizon IRC support for Snowflake-managed Iceberg tables](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon)
so that one catalog endpoint covers Snowflake-managed tables and externally managed tables.

## Overview

Snowflake Horizon Catalog provides governance for Snowflake-managed and externally managed Iceberg tables. By pointing
your external engines to the Horizon IRC endpoint, you can:

- Use a single catalog endpoint for Snowflake-managed and externally managed Iceberg tables.
- Enforce Snowflake RBAC before a request is sent to the remote catalog.
- Access and operate on externally managed tables without copying governance configuration into each engine.

Where the table lives changes what a catalog operation does:

- In a catalog-linked database, reads, DML, and DDL are sent to the remote catalog, and Snowflake keeps a matching schema
  or table.
- In a standard Snowflake database, reads and DML on an externally managed table are sent to the remote catalog. Other
  catalog operations change the Snowflake object only.

## Prerequisites

Before you access externally managed tables through Horizon IRC, complete the following:

- Create the tables in one of these places:
  - A catalog-linked database. For instructions, see
    [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database).
  - A standard Snowflake database. For instructions, see
    [Create an Iceberg table in a standard Snowflake database](/user-guide/tables-iceberg-externally-managed-writes#label-tables-iceberg-external-writes-create-table-standard-db).
- Configure the external engine for Horizon Catalog. For instructions, see
  [Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).
- To use credentials vended by Horizon Catalog, the database needs an external volume, and the catalog integration must
  use `ACCESS_DELEGATION_MODE = EXTERNAL_VOLUME_CREDENTIALS`. Credential vending for externally managed tables is
  disabled by default. For more information, see [Credential vending](#label-cld-horizon-irc-credential-vending).

## Supported operations

The operations below depend on whether the table is in a catalog-linked database or a standard Snowflake database.

### Catalog-linked database

| Operation | Description |
| --- | --- |
| `listNamespaces` | List the namespaces (schemas) available in the catalog-linked database. |
| `getNamespace` | Retrieve metadata for a specific namespace. |
| `listTables` | List the tables within a namespace. |
| `loadTable` | Load table metadata, enabling read access from external engines. |
| `updateTable` | Update table state, enabling DML operations (such as append, overwrite, delete, and alter table) from external engines. |
| `namespaceExists` | Check whether a specific namespace exists in the catalog-linked database. |
| `tableExists` | Check whether a specific table exists within a namespace. |
| `createTable` | Create a table in the remote catalog and create the corresponding Snowflake table. |
| `dropTable` | Drop a table from the remote catalog and drop the corresponding Snowflake table. |
| `renameTable` | Rename a table in the remote catalog and rename the corresponding Snowflake table. |
| `createNamespace` | Create a namespace in the remote catalog and create the corresponding Snowflake schema. |
| `dropNamespace` | Drop a namespace from the remote catalog and drop the corresponding Snowflake schema. |

Expand

Show lessSee more

Each operation also depends on support in your remote catalog. If your remote catalog doesn’t implement the
corresponding Iceberg REST operation, that operation isn’t available through Horizon IRC.

Note

In a catalog-linked database, DML operations aren’t supported when `ALLOWED_WRITE_OPERATIONS` is configured as
`READ_ONLY`.

### Standard Snowflake database

In a standard database, Horizon IRC behavior depends on the table. `loadTable` and `updateTable` for an externally
managed table are sent to the remote catalog. Every other operation follows Snowflake semantics and doesn’t change the
remote catalog.

| Operation | Description |
| --- | --- |
| `listNamespaces`, `getNamespace`, `namespaceExists` | List or read Snowflake schemas in the database. |
| `listTables`, `tableExists` | List or check Iceberg tables only. Both Snowflake-managed and externally managed Iceberg tables are included. Other table types, such as standard Snowflake tables, aren’t returned. |
| `loadTable` | For a Snowflake-managed table, return Snowflake metadata. For an externally managed table, return metadata from the remote catalog. |
| `updateTable` | For a Snowflake-managed table, update Snowflake metadata. For an externally managed table, commit the change to the remote catalog. |
| `createTable` | Create a Snowflake-managed Iceberg table. This operation doesn’t create an externally managed table. |
| `renameTable` | Rename the Snowflake table only. The remote catalog entry for an externally managed table isn’t renamed. |
| `dropTable` | Drop the Snowflake table only. The remote catalog entry for an externally managed table isn’t dropped. |
| `createNamespace`, `dropNamespace` | Create or drop a Snowflake schema. The remote catalog isn’t changed. |

Expand

Show lessSee more

External engines use the Snowflake database, schema, and table names. Horizon IRC doesn’t expose the table’s name in
the remote catalog.

## Connect an external engine to externally managed Iceberg tables

To access these tables through Horizon IRC, use the same connection workflow described in
[Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).
When you configure your external engine, set the warehouse property to the Snowflake database name. That name is the
catalog-linked database or the standard database that contains the tables.

The name that you pass must match the Snowflake identifier exactly: the form returned by `SHOW DATABASES`. If the
database was created without quotes (the common case), use the upper-cased form. If it was created with a quoted
identifier, use the exact case it was created with. A mismatch returns a 404 error.

### Example: Spark configuration

The following example shows how to configure Apache Spark™ to connect through Horizon IRC:

Copy code

```
CATALOG_URI = "https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog"
HORIZON_SESSION_ROLE = "session:role:<role>"
CATALOG_NAME = "<database_name>"  # Snowflake database name, as returned by SHOW DATABASES
ICEBERG_VERSION = "1.10.1"

spark = (
    SparkSession.builder
    .appName("HorizonExternalIceberg")
    .master("local[*]")
    .config(
        "spark.jars.packages",
        f"org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:{ICEBERG_VERSION},"
        f"org.apache.iceberg:iceberg-aws-bundle:{ICEBERG_VERSION}"
    )
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
    .config("spark.sql.defaultCatalog", CATALOG_NAME)
    .config(f"spark.sql.catalog.{CATALOG_NAME}", "org.apache.iceberg.spark.SparkCatalog")
    .config(f"spark.sql.catalog.{CATALOG_NAME}.type", "rest")
    .config(f"spark.sql.catalog.{CATALOG_NAME}.uri", CATALOG_URI)
    .config(f"spark.sql.catalog.{CATALOG_NAME}.warehouse", CATALOG_NAME)
    .config(f"spark.sql.catalog.{CATALOG_NAME}.credential", "<your_PAT_token>")
    .config(f"spark.sql.catalog.{CATALOG_NAME}.scope", HORIZON_SESSION_ROLE)
    .config(f"spark.sql.catalog.{CATALOG_NAME}.header.X-Iceberg-Access-Delegation", "vended-credentials")
    .config("spark.sql.iceberg.vectorization.enabled", "false")
    .getOrCreate()
)
```

Where:

- `<account_identifier>` is the account identifier for your Snowflake account, in the format
  `<organization_name>-<account_name>`.
- `<role>` is the Snowflake role that has the appropriate privileges on the database and its tables.
- `<database_name>` is the name of your catalog-linked database or standard Snowflake database. It must match the
  Snowflake identifier exactly: the form returned by `SHOW DATABASES`. Unquoted identifiers resolve to upper case;
  quoted identifiers preserve the exact case that was used at creation.
- `<your_PAT_token>` is the programmatic access token (PAT) for authentication. For more authentication options, see
  [Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).

## Access tables

After configuring your external engine, you can access tables in the database. The examples use `SALES.ORDERS`, an
externally managed Iceberg table.

Note

Use the Snowflake table name, not the name of the table in the remote catalog. For a catalog-linked database, table
and namespace names also follow the case rules in
[Case sensitivity and identifier resolution](#label-cld-horizon-irc-identifier-case).

### List namespaces

Copy code

```
spark.sql("SHOW NAMESPACES").show()
```

### List tables in a namespace

Copy code

```
spark.sql("USE NAMESPACE SALES")
spark.sql("SHOW TABLES").show()
```

### Query a table

Copy code

```
spark.sql("SELECT order_id, status FROM SALES.ORDERS LIMIT 10").show()
```

### Write to a table (DML)

Copy code

```
spark.sql("INSERT INTO SALES.ORDERS VALUES (1001, 'shipped')")
```

Copy code

```
spark.sql("UPDATE SALES.ORDERS SET status = 'delivered' WHERE order_id = 1001")
```

Copy code

```
spark.sql("DELETE FROM SALES.ORDERS WHERE order_id = 1001")
```

## Configure access control

The role specified in the session scope must have the appropriate privileges:

- **Read access**: The role must have USAGE on the database, USAGE on the schema, and the privileges described in
  [Configure read access to your Iceberg tables](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon#configure-read-access-to-your-iceberg-tables)
  on the table.
- **Write access (DML)**: The role must have the privileges described in
  [Configure write access to your Iceberg tables](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon#configure-write-access-to-your-iceberg-tables)
  on the tables.
- **DDL**: The role must have the same privileges required to create, rename, or drop the object in Snowflake. For
  creating a table, see the CREATE ICEBERG TABLE privileges in
  [Configure write access to your Iceberg tables](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon#configure-write-access-to-your-iceberg-tables).

For more information, see
[Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).

## Data protection policies

Preview Feature

Access to an externally managed Iceberg table that has a Snowflake data protection policy, such as a row access policy
or a masking policy, is in public preview.

An external engine that reads table files directly can’t evaluate those policies. To query a protected table, use one
of the options in
[Enforce data protection policies on Apache Iceberg™ tables from external query engines](/user-guide/tables-iceberg-query-using-external-query-engine-snowflake-horizon-enforce-access-policies).

For a protected externally managed table, the data served to the external engine can lag the remote catalog by up to
the table’s auto-refresh interval. An unprotected externally managed table returns the latest state from the remote
catalog.

## Credential vending

Credential vending is an Iceberg REST catalog behavior. When an external engine requests vended credentials, the
catalog returns a temporary cloud storage credential so the engine can read and write the table’s files directly.

### When Horizon vends credentials

Horizon vends credentials for an externally managed Iceberg table only when all of the following are true:

- The engine sends the `X-Iceberg-Access-Delegation: vended-credentials` header.
- The catalog integration uses `ACCESS_DELEGATION_MODE = EXTERNAL_VOLUME_CREDENTIALS`.
- The database or table has an external volume that can access the table’s storage locations.
- Credential vending is enabled on the database.
- The table’s storage locations don’t overlap a Snowflake-managed Iceberg table in the same account. A location can’t
  be the same as, a parent of, or under a Snowflake-managed Iceberg table’s location.
- The role has privileges on the table. A role that can write receives read-write credentials. A role that can only
  read receives read-only credentials.

Horizon vends these credentials only on `loadTable`, and on `createTable` when `stage-create` is true. Credential
vending on `createTable` applies only when you create a table in a catalog-linked database that has an external volume.

The credential covers the table location and, when they are set, `write.data.path` and `write.metadata.path`. Your
cloud provider evaluates the credential at the storage layer, independently of Snowflake role-based access control.
Any object under that prefix is within the credential’s scope for its lifetime.

### Before you enable credential vending

Warning

Credential vending for externally managed tables is disabled by default. Because the remote catalog chooses the table
location, Snowflake can’t guarantee that the prefix contains only that table’s files. A disclosed credential can read
or write every object under the prefix, including files that belong to another externally managed table.

Enable credential vending only on the databases that need it. Before you enable it, confirm the following:

- Each externally managed table has its own storage location, and that location doesn’t overlap another externally
  managed table or a Snowflake-managed Iceberg table.
- The external volume can access those locations, and its storage identity has only the permissions the engines need.
- Only trusted users and engines can create tables or change table locations in the remote catalog.
- Before you create or convert a Snowflake-managed Iceberg table, its location doesn’t overlap an externally managed
  table.

The following changes stop credential vending or change what the credential allows.

| Change | Result & how to avoid |
| --- | --- |
| You create a Snowflake-managed Iceberg table in a child folder of an externally managed table. Snowflake appends a random suffix, `.<randomId>`, to `BASE_LOCATION`. `ANALYTICS_VOLUME` uses `s3://analytics/`. For example:   - `SALES.ORDERS` (externally managed) is at `s3://analytics/orders/`. - `MANAGED_ORDERS` (Snowflake-managed) uses `BASE_LOCATION = 'orders/managed_orders'`, so its files are at   `s3://analytics/orders/managed_orders.<randomId>/`, which is under `SALES.ORDERS`.   Copy code  ``` CREATE ICEBERG TABLE MANAGED_ORDERS   CATALOG = 'SNOWFLAKE'   EXTERNAL_VOLUME = 'ANALYTICS_VOLUME'   BASE_LOCATION = 'orders/managed_orders'; ``` | Credential requests for `SALES.ORDERS` fail with 403 Forbidden because `MANAGED_ORDERS` is stored under that table. Keep Snowflake-managed tables out of an externally managed table’s location, preferably on a separate external volume. |
| You convert an externally managed table to a Snowflake-managed table while its location contains another externally managed table. For example:   - `SALES.ORDERS` is at `s3://analytics/orders/`. - `SALES.ARCHIVE` is at `s3://analytics/orders/archive/`, which is under `SALES.ORDERS`.   Copy code  ``` ALTER ICEBERG TABLE SALES.ORDERS CONVERT TO MANAGED; ``` | Credential requests for `SALES.ARCHIVE` fail with 403 Forbidden. Convert only a table whose location doesn’t overlap another table. |
| The remote catalog sets `write.data.path` or `write.metadata.path` under a Snowflake-managed table’s location. For example:   - The Snowflake-managed table is at `s3://analytics/managed/`. - The externally managed table’s `write.data.path` is at `s3://analytics/managed/orders/`. | Credential requests for the externally managed table fail with 403 Forbidden. Limit who can change table locations, and keep the two kinds of tables in separate locations. |
| You disable credential vending. For example:  Copy code  ``` ALTER DATABASE SALES_DB   SET ENABLE_HORIZON_IRC_UNMANAGED_CREDENTIAL_VENDING = FALSE; ``` | Credential requests fail with 405 Not Allowed. Before you disable vending, configure engines with their own storage credentials. |
| You revoke a role’s write privileges on a table. For example:  Copy code  ``` REVOKE INSERT, UPDATE, DELETE ON TABLE SALES.ORDERS FROM ROLE SPARK_WRITER; ``` | The role receives read-only credentials, and writes fail. Without any privileges on the table, the request fails. Review grants before you change them for roles that engines use. |
| You change the storage permissions or trust policy of the external volume’s storage identity. | Credential requests fail, or the cloud provider denies access to the files. After the change, test access with `DESCRIBE EXTERNAL VOLUME` and `SYSTEM$VERIFY_EXTERNAL_VOLUME`. |

Expand

Show lessSee more

### Enable credential vending

To enable credential vending for a database, set the `ENABLE_HORIZON_IRC_UNMANAGED_CREDENTIAL_VENDING` parameter.

Copy code

```
ALTER DATABASE <database_name>
  SET ENABLE_HORIZON_IRC_UNMANAGED_CREDENTIAL_VENDING = TRUE;
```

Note

While the parameter is set to `FALSE`, external engines can continue to browse namespaces and load table metadata through
Horizon Catalog. Only requests that ask for vended credentials are declined.

### Recommendations

- Give each externally managed table its own storage location. Avoid broad prefixes, such as the root of an external
  volume or a namespace directory.
- Use separate external volumes for Snowflake-managed and externally managed Iceberg tables.
- Don’t share the storage behind an external volume with other Snowflake accounts or other systems.
- Grant each engine’s role only the privileges it needs. Use a read-only role for a read-only workload.
- Give the external volume’s storage identity read-only permissions when no engine writes.

## Considerations

### Case sensitivity and identifier resolution

For a catalog-linked database, Horizon IRC resolves table and namespace identifiers the same way that your remote
catalog resolves them. If your catalog-linked database connects to a catalog that resolves identifiers
case-sensitively, such as Apache Polaris™ or Snowflake Open Catalog, Horizon IRC also resolves them case-sensitively.
If it connects to a catalog that resolves identifiers case-insensitively, such as AWS Glue or Databricks Unity Catalog,
Horizon IRC resolves them case-insensitively.

For details, see
[Requirements for identifier resolution in a catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database#requirements-for-identifier-resolution-in-a-catalog-linked-database).

For a standard Snowflake database, identifiers follow
[Snowflake identifier rules](/sql-reference/identifiers-syntax). Use the Snowflake table name.

### Nested namespaces in a catalog-linked database

Horizon IRC uses the same namespace names as the catalog-linked database. It doesn’t show multi-level Iceberg
namespaces as nested namespaces.

- With `NAMESPACE_MODE = IGNORE_NESTED_NAMESPACE` (the default), only first-level namespaces are available.
- With `NAMESPACE_MODE = FLATTEN_NESTED_NAMESPACE`, a nested namespace is available under its flattened schema name.
  For example, if the delimiter is `_`, the remote namespace `accounting.tax` is the schema `accounting_tax`. Query
  `accounting_tax.orders`, not `accounting.tax.orders`.
- To create a nested namespace, create the flattened name. The parent namespace must already exist.

For the parameters and examples, see
[`NAMESPACE_MODE`](/sql-reference/sql/create-database-catalog-linked) for a catalog-linked database.

### Cross-region federation

Cross-region federation isn’t recommended because latency will be high. Latency and errors from the source catalog pass
through Horizon Catalog to the client on every request.

### Table maintenance in the source catalog

Configure table maintenance jobs, such as snapshot expiry, for each externally managed table in the source catalog.
Without that maintenance, table metadata may grow without bound and cause performance and stability problems.

Horizon Catalog rejects a remote catalog response larger than 30 MB. If you need support for a larger response, contact
[Snowflake Support](/user-guide/contacting-support).

### Considerations for catalog-linked databases

All considerations for using a catalog-linked database also apply when accessing tables through Horizon IRC. For the
full list, see
[Considerations for using a catalog-linked database for Iceberg tables](/user-guide/tables-iceberg-catalog-linked-database#considerations-for-using-a-catalog-linked-database-for-iceberg-tables).

## Limitations

The following limits apply when you access externally managed Iceberg tables through Horizon IRC:

- **FedRAMP:** This feature isn’t available on FedRAMP (Moderate) or FedRAMP (High) deployments.
- **Non-Iceberg table formats:** Tables in formats other than Iceberg, such as Delta, aren’t available. In a standard
  database, `listTables` returns Iceberg tables only.
- **Credential vending:** Credential vending is disabled by default. It isn’t supported when the catalog integration
  uses `ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS`. On a catalog-linked database, credential vending on `createTable`
  when `stage-create` is true requires an external volume. For more information, see
  [Credential vending](#label-cld-horizon-irc-credential-vending).
- **`registerTable`:** `registerTable` isn’t supported.
- **`commitTransaction`:** `commitTransaction` (multi-table commit) isn’t supported.
- **Remote catalog latency and errors:** Latency and errors from the source catalog pass through Horizon Catalog to the
  client.
- **Data protection policies:** Access to an externally managed Iceberg table that has a Snowflake data protection
  policy, such as a row access policy or a masking policy, is in public preview.
