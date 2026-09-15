# Access externally managed Apache Iceberg™ tables in a catalog-linked database with an external engine through Snowflake Horizon Catalog

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

This topic describes how to access externally managed Apache Iceberg™ tables in a
[catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database) through Snowflake Horizon Catalog by using
external query engines.

With this feature, you can use the Horizon Iceberg REST Catalog (IRC) API to read and perform DML and DDL operations on Iceberg tables
within a catalog-linked database from external engines such as Apache Spark™, Trino, DuckDB, or PyIceberg. This extends the
existing [Horizon IRC support for Snowflake-managed Iceberg tables](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon)
to include externally managed tables that are synced into Snowflake through a catalog-linked database.

## Overview

Snowflake Horizon Catalog provides universal governance across both Snowflake-managed and externally managed Iceberg tables. By
pointing your external engines to the Horizon IRC endpoint, you can:

- Use a single catalog endpoint to access both Snowflake-managed and externally managed Iceberg tables.
- Enforce Snowflake RBAC policies consistently, regardless of where the table is managed.
- Read from and perform DML operations on externally managed tables without duplicating governance configurations across multiple
  systems.

## Prerequisites

Before you access externally managed tables in a catalog-linked database through Horizon Iceberg REST Catalog APIs, you must
complete the following:

- Set up a catalog-linked database. For instructions, see
  [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database).
- Configure access to Iceberg tables with an external engine through Horizon Catalog. For instructions, see
  [Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).
- To use credentials vended by Horizon Catalog, ensure your catalog-linked database has an EXTERNAL\_VOLUME configured.
  Credential vending for externally managed tables is disabled by default. For more information, see
  [Credential vending](#label-cld-horizon-irc-credential-vending).
- Access to externally managed Iceberg tables that aren’t within a catalog-linked database isn’t currently supported through the
  Horizon Iceberg REST Catalog APIs.

## Supported operations

The following Horizon IRC operations are supported for tables in a catalog-linked database:

| Operation | Description |
| --- | --- |
| `listNamespaces` | List the namespaces (schemas) available in the catalog-linked database. |
| `getNamespace` | Retrieve metadata for a specific namespace. |
| `listTables` | List the tables within a namespace. |
| `loadTable` | Load table metadata, enabling read access from external engines. |
| `updateTable` | Update table state, enabling DML operations (such as append, overwrite, delete, and alter table) from external engines. |
| `namespaceExists` | Check whether a specific namespace exists in the catalog-linked database. |
| `tableExists` | Check whether a specific table exists within a namespace. |
| `createTable` | Create a table in the remote catalog and materialize the corresponding Snowflake table object. |
| `registerTable` | Register an existing table in the remote catalog and materialize the corresponding Snowflake table object. |
| `dropTable` | Drop a table from the remote catalog and drop the corresponding Snowflake table object. |
| `renameTable` | Rename a table in the remote catalog and update the corresponding Snowflake table object. |
| `createNamespace` | Create a namespace in the remote catalog and create the corresponding Snowflake schema. |
| `dropNamespace` | Drop a namespace from the remote catalog and drop the corresponding Snowflake schema. |

Expand

Show lessSee more

Together, these operations enable read, DML, and DDL capabilities for external engines through Horizon IRC.

Note

Each operation also depends on support in your remote catalog. If your remote catalog doesn’t implement the corresponding
Iceberg REST operation, that operation isn’t available through Horizon IRC. For example, if your remote catalog doesn’t
support `registerTable`, you can’t register tables through Horizon IRC.

## Connect an external engine to a catalog-linked database

To access tables in a catalog-linked database through Horizon IRC, use the same connection workflow described in
[Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).
When you configure your external engine, specify the catalog-linked database name as the warehouse property.

The name that you pass must match the Snowflake identifier exactly: the form returned by `SHOW DATABASES`,
`SHOW NAMESPACES`, or `SHOW TABLES`. If the database was created without quotes (the common case), use the
upper-cased form. If it was created with a quoted identifier, use the exact case it was created with. A mismatch
returns a 404 error.

### Example: Spark configuration

The following example shows how to configure Apache Spark™ to connect to a catalog-linked database through Horizon IRC:

Copy code

```
CATALOG_URI = "https://<account_identifier>.snowflakecomputing.com/polaris/api/catalog"
HORIZON_SESSION_ROLE = "session:role:<role>"
CATALOG_NAME = "<database_name>"  # must match the Snowflake identifier as returned by SHOW DATABASES
ICEBERG_VERSION = "1.10.1"

spark = (
    SparkSession.builder
    .appName("HorizonCLDAccess")
    .master("local[*]")
    .config(
        "spark.jars.packages",
        "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:{ICEBERG_VERSION},"
        "org.apache.iceberg:iceberg-aws-bundle:{ICEBERG_VERSION}"
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
- `<role>` is the Snowflake role that has the appropriate privileges on the catalog-linked database and its tables.
- `<database_name>` is the name of your catalog-linked database. It must match the Snowflake identifier exactly: the
  form returned by `SHOW DATABASES`, `SHOW NAMESPACES`, or `SHOW TABLES`. Unquoted identifiers resolve to upper case;
  quoted identifiers preserve the exact case that was used at creation.
- `<your_PAT_token>` is the programmatic access token (PAT) for authentication. For more authentication options, see
  [Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).

## Access tables

After configuring your external engine, you can access tables in the catalog-linked database.

### List namespaces

Copy code

```
spark.sql("SHOW NAMESPACES").show()
```

### List tables in a namespace

Copy code

```
spark.sql("USE NAMESPACE <namespace_name>")
spark.sql("SHOW TABLES").show()
```

### Query a table

Copy code

```
spark.sql("SELECT * FROM <namespace_name>.<table_name>").show()
```

### Write to a table (DML)

Copy code

```
spark.sql("INSERT INTO <namespace_name>.<table_name> VALUES (1, 'example')")
```

Copy code

```
spark.sql("UPDATE <namespace_name>.<table_name> SET col1 = 'new_value' WHERE col2 = 100")
```

Copy code

```
spark.sql("DELETE FROM <namespace_name>.<table_name> WHERE col1 = 'obsolete'")
```

Note

DML operations aren’t supported when ALLOWED\_WRITE\_OPERATIONS is configured as READ\_ONLY on the catalog-linked database.

## Configure access control

To access tables in a catalog-linked database through Horizon IRC, the role specified in the session scope must have the
appropriate privileges:

- **Read access**: The role must have USAGE on the catalog-linked database, USAGE on the schema, and the privileges described in
  [Configure read access to your Iceberg tables](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon#configure-read-access-to-your-iceberg-tables)
  on the table.
- **Write access (DML)**: The role must have the privileges described in
  [Configure write access to your Iceberg tables](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon#configure-write-access-to-your-iceberg-tables)
  on the tables.

For more information, see
[Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).

## Data protection policies

A table in a catalog-linked database can be protected by Snowflake data protection policies, such as a row access policy or a
masking policy. An external engine that reads table files directly can’t evaluate those policies, so Horizon IRC doesn’t serve
data for a protected table on that path.

To query a protected table from Apache Spark™, use the Snowflake Connector for Spark, which routes the query through Snowflake
so that policies are enforced consistently. For more information, see
[Enforce data protection policies on Apache Iceberg tables accessed from Spark](/user-guide/spark-connector#label-spark-connector-enforce-access-polices-on-apache-iceberg-tables)
and
[Enforce data protection policies when querying Apache Iceberg™ tables from Apache Spark™](/user-guide/tables-iceberg-query-using-external-query-engine-snowflake-horizon-enforce-access-policies).

## Credential vending

When an external engine requests vended credentials, Horizon Catalog returns a temporary cloud storage credential that lets the
engine read and write an externally managed Iceberg table’s files directly. The credential is scoped to the object storage
prefix under which the table’s files reside, and your cloud provider evaluates it at the storage layer, independently of
Snowflake role-based access control. Any object stored beneath that prefix is therefore within the credential’s scope for its
lifetime. Because your remote catalog supplies the location of an externally managed table rather than Snowflake assigning it,
Snowflake can’t guarantee that the prefix contains only the files that belong to the requested table. If a credential were
disclosed outside its intended use, its scope would extend to the files of any other table stored under the same prefix,
including Snowflake-managed Iceberg tables.

Warning

Credential vending for externally managed tables is disabled by default. Evaluate the risk of credential misuse or disclosure
described above before you enable it. Snowflake recommends that you enable it only on the catalog-linked databases that require
it. Before you enable it, review the storage layout behind the database and confirm that the location contains only the tables
that you intend external engines to access, and that no table in your remote catalog is registered at a location that encloses
another table’s files.

To enable credential vending for a catalog-linked database, set the `ENABLE_HORIZON_IRC_UNMANAGED_CREDENTIAL_VENDING` parameter.

Copy code

```
ALTER DATABASE <database_name>
  SET ENABLE_HORIZON_IRC_UNMANAGED_CREDENTIAL_VENDING = TRUE;
```

Note

While the parameter is set to `FALSE`, external engines can continue to browse namespaces and load table metadata through
Horizon Catalog. Only requests that ask for vended credentials are declined.

## Limitations

The following operations and configuration combinations for catalog-linked databases aren’t supported through Horizon IRC:

| Limitation | Details |
| --- | --- |
| Nested namespaces | Access to catalog-linked databases with nested namespaces (where NAMESPACE\_MODE is configured for nested namespace support) isn’t supported. |
| Non-Iceberg table formats | Access to catalog-linked databases that contain non-Iceberg table formats (such as Delta) isn’t supported. |
| Catalog-vended credentials without an external volume | Access to catalog-linked databases where credentials are vended by the remote catalog (that is, the catalog-linked database doesn’t have an EXTERNAL\_VOLUME configured) and the `loadTable` request is configured with `vended-credentials` mode isn’t supported. |

Expand

Show lessSee more

## Considerations

### Case sensitivity and identifier resolution

Horizon IRC resolves table and namespace identifiers the same way that your remote catalog resolves them. If your
catalog-linked database connects to a catalog that resolves identifiers case-sensitively, such as Apache Polaris™ or
Snowflake Open Catalog, Horizon IRC also resolves them case-sensitively. If it connects to a catalog that resolves
identifiers case-insensitively, such as AWS Glue or Databricks Unity Catalog, Horizon IRC resolves them
case-insensitively.

For details, see
[Requirements for identifier resolution in a catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database#requirements-for-identifier-resolution-in-a-catalog-linked-database).

### Considerations for catalog-linked databases

All considerations for using a catalog-linked database also apply when accessing tables through Horizon IRC. For the full list,
see [Considerations for using a catalog-linked database for Iceberg tables](/user-guide/tables-iceberg-catalog-linked-database#considerations-for-using-a-catalog-linked-database-for-iceberg-tables).
