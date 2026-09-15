# Snowflake Open Catalog overview

Feature — Generally Available

Not available in government regions.

Note

New customers should use [Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon)
for Apache Iceberg™ tables and multi-engine interoperability with Iceberg. Customers who
haven’t previously created a Snowflake Open Catalog account can’t sign up for their first Open
Catalog account.

Existing Snowflake Open Catalog customers can continue to use and can create additional
Open Catalog accounts if necessary.

Snowflake Open Catalog is a catalog implementation for Apache Iceberg™ tables and is built on the open source Apache Iceberg™ REST protocol. Snowflake Open Catalog is a managed service for [Apache Polaris™](https://github.com/apache/polaris).

With Open Catalog, you can provide centralized, secure read and write access to your Iceberg tables across different REST-compatible query engines.

Open Catalog is currently offered as a service hosted in Snowflake-managed infrastructure.

[![Conceptual diagram of Open Catalog.](/static/images/user-guide/opencatalog/img/overview.svg "Open Catalog overview")](/static/images/user-guide/opencatalog/img/overview.svg)

## Account availability

Customers who haven’t previously created a Snowflake Open Catalog account can’t sign up for their first Open Catalog account. New customers
should use [Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon) for Apache
Iceberg™ tables and multi-engine interoperability with Iceberg.

Existing Snowflake Open Catalog customers who already have at least one Open Catalog account can continue using Open Catalog and can create
additional Open Catalog accounts if necessary. For instructions, see [Create a Snowflake Open Catalog account](./create-open-catalog-account).

## Key concepts

This section introduces key concepts associated with using Open Catalog hosted in Snowflake.

In the following diagram, a sample [Open Catalog structure](overview#catalog) with nested [namespaces](overview#namespace) is shown for Catalog1. No tables
or namespaces have been created yet for Catalog2 or Catalog3.

[![Diagram that shows an example Open Catalog structure.](/static/images/user-guide/opencatalog/img/sample-catalog-structure.svg "Sample Open Catalog structure")](/static/images/user-guide/opencatalog/img/sample-catalog-structure.svg)

### Catalog

In Open Catalog, you can create one or more catalog resources to organize Iceberg tables.

Configure your catalog by setting values in the storage configuration for Amazon S3, Azure, or Google Cloud Storage. An Iceberg catalog enables a
query engine to manage and organize tables. The catalog forms the first architectural layer in the [Apache Iceberg™ table specification](https://iceberg.apache.org/spec/#overview) and must support the following tasks:

- Storing the current metadata pointer for one or more Iceberg tables. A metadata pointer maps a table name to the location of that table’s
  current metadata file.
- Performing atomic operations so that you can update the current metadata pointer for a table to the metadata pointer of a new version of
  the table.

To learn more about Iceberg catalogs, see the [Apache Iceberg™ documentation](https://iceberg.apache.org/terms/#catalog).

#### Catalog types

A catalog can be one of the following two types:

- Internal: The catalog is managed by Open Catalog. A third-party query engine can read and write to tables from this catalog. In addition,
  Snowflake can also read and write to tables from this catalog.
- External: The catalog is externally managed by another Iceberg catalog provider (for example, Snowflake, Glue, Dremio Arctic). Tables from
  this catalog are synced to Open Catalog. These tables are read-only in Open Catalog. In the current release, only a Snowflake external
  catalog is provided.

A catalog is configured with a storage configuration that can point to Amazon S3, Azure Storage, or Cloud Storage from Google.

To create a new catalog, see [Create a catalog](create-catalog "Sample Open Catalog structure").

### Namespace

You create *namespaces* to logically group Iceberg tables within a catalog. A catalog can have multiple namespaces. You can also create
nested namespaces. Iceberg tables belong to namespaces.

### Apache Iceberg™ tables and catalogs

In an internal catalog, an Iceberg table is registered in Open Catalog, but read and written via query engines. The table data and
metadata is stored in your external cloud storage. The table uses Open Catalog as the Iceberg catalog.

Important

If you drop a table in Snowflake Open Catalog without purging it, don’t create a new table with the same name and location as the dropped
table. If you do, a user could gain access to the original table’s data when they shouldn’t have permission to access it. For example, if
you drop but don’t purge Table1 where its storage directory location is /MyCatalog/Schema1/Table1, don’t create a new Table1 within
the same Table1 storage directory. When you drop a table without purging it, its data is retained in the external cloud storage.

If you have tables that use Snowflake as the Iceberg catalog (Snowflake-managed tables), you can sync these tables to an external
catalog in Open Catalog. If you sync this catalog to Open Catalog, it appears as an external catalog in Open Catalog. The table data and
metadata is stored in your external cloud storage. The Snowflake query engine can read from or write to these tables. However, the other query
engines can only read from these tables.

Important

To ensure that the access privileges defined for a catalog are enforced correctly, the following conditions must be met:

- A directory only contains the data files that belong to a single table.
- A directory hierarchy matches the namespace hierarchy for the catalog.

For example, if a catalog includes the following items:

- Top-level namespace `namespace1`
- Nested namespace `namespace1a`
- A `customers` table grouped under nested namespace `namespace1a`
- An `orders` table grouped under nested namespace `namespace1a`

The directory hierarchy for the catalog must be:

- `/namespace1/namespace1a/customers/<files for the customers table *only*>`
- `/namespace1/namespace1a/orders/<files for the orders table *only*>`

These conditions apply to both internal and external catalogs, including external catalogs that contain
[Snowflake-managed Apache Iceberg™ tables](https://docs.snowflake.com/en/user-guide/tables-iceberg). When you create a table in an
internal catalog, Open Catalog prohibits you from creating the table within the directory or subdirectory for an existing table. When you
create Snowflake-managed Iceberg tables in an external catalog, Open Catalog doesn’t prohibit overlapping directory locations. Therefore,
when you create these tables, use the BASE\_LOCATION parameter to specify a unique parent directory for each table. For more information, see
[CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](https://docs.snowflake.com/en/sql-reference/sql/create-iceberg-table-snowflake).

For more information about internal and external catalogs, see [Catalog types](./overview#catalog-types).

### Service principal

A service principal is an entity that you create in Open Catalog. Each service principal encapsulates credentials that you use to connect
to Open Catalog.

Query engines use service principals to connect to catalogs.

Open Catalog generates a Client ID and Client Secret pair for each service principal.

The following table displays example service principals that you might create in Open Catalog:

| Service connection name | Purpose |
| --- | --- |
| Flink ingestion | For Apache Flink® to ingest streaming data into Apache Iceberg™ tables. |
| Spark ETL pipeline | For Apache Spark™ to run ETL pipeline jobs on Iceberg tables. |
| Snowflake data pipelines | For Snowflake to run data pipelines for transforming data in Apache Iceberg™ tables. |
| Trino BI dashboard | For Trino to run BI queries for powering a dashboard. |
| Snowflake AI team | For Snowflake to run AI jobs on data in Apache Iceberg™ tables. |

Expand

Show lessSee more

### Service connection

A service connection represents a REST-compatible engine (such as Apache Spark™, Apache Flink®, or Trino) that can read from and write to Open
Catalog. When creating a new service connection, the Open Catalog administrator grants the service principal that is created with the new service
connection either a new or existing principal role. A principal role is a resource in Open Catalog that you can use to logically group Open
Catalog service principals together and grant privileges on securable objects. For more information, see [Principal role](access-control#principal-role "Principal role"). Open Catalog uses a role-based access control (RBAC) model to grant service principals access to resources. For more information,
see [Access control](access-control "Access control"). For a diagram of this model, see [RBAC model](access-control#rbac-model "RBAC model").

If the Open Catalog administrator grants the service principal for the new service connection a new principal role, the service principal
doesn’t have any privileges granted to it yet. When securing the catalog that the new service connection will connect to, the Open
Catalog administrator grants privileges to catalog roles and then grants these catalog roles to the new principal role. As a result, the service
principal for the new service connection has these privileges. For more information about catalog roles, see [Catalog role](access-control#catalog-role "Catalog role").

If the Open Catalog administrator grants an existing principal role to the service principal for the new service connection, the service principal
is bestowed with the privileges granted to the catalog roles that are granted to the existing principal role. If needed, the Open Catalog
administrator can grant additional catalog roles to the existing principal role or remove catalog roles from it to adjust the privileges
bestowed to the service principal. For an example of how RBAC works in Open Catalog, see [RBAC example](access-control#rbac-example "RBAC example").

### Storage configuration

A storage configuration stores a generated identity and access management (IAM) entity for your external cloud storage and is created
when you create a catalog. The storage configuration is used to set the values to connect Open Catalog to your cloud storage. During the
catalog creation process, an IAM entity is generated and used to create a trust relationship between the cloud storage provider and Open
Catalog.

When you create a catalog, you supply the following information about your external cloud storage:

| Cloud storage provider | Information |
| --- | --- |
| Amazon S3 | - Default base location for your Amazon S3 bucket - Locations for your Amazon S3 bucket - S3 role ARN - External ID (optional) |
| Cloud Storage from Google | - Default base location for your Cloud Storage from Google bucket - Locations for your Cloud Storage from Google bucket |
| Azure | - Default base location for your Microsoft Azure container - Locations for your Microsoft Azure container - Azure tenant ID |

Expand

Show lessSee more

## Example workflow

In the following example workflow, Bob creates an Apache Iceberg™ table named Table1 and Alice reads data from Table1.

1. Bob uses Apache Spark™ to create the Table1 table under the Namespace1 namespace in the Catalog1 catalog and insert values into Table1.

   Bob can create Table1 and insert data into it because he is using a service connection with a service principal that has
   the privileges to perform these actions.
2. Alice uses Snowflake to read data from Table1.

   Alice can read data from Table1 because she is using a service connection with a service principal with a catalog integration that
   has the privileges to perform this action. Alice creates an externally managed table in Snowflake to read data from Table1.

[![Diagram that shows an example workflow for Open Catalog](/static/images/user-guide/opencatalog/img/example-workflow.svg "Example workflow for Open Catalog")](/static/images/user-guide/opencatalog/img/example-workflow.svg)

## Security and access control

This section describes security and access control.

### Credential vending

Credential vending simplifies access control in Open Catalog by centralizing access management for the following items:

- The metadata within Open Catalog
- The storage location to your Apache Iceberg tables

When credential vending is enabled for a catalog, Open Catalog provides the query engine executing the query with a temporary storage
credential. This credential allows the query engine to access an Iceberg table’s underlying directory location. If you enable credential
vending, you don’t have to manage storage access separately, outside of Open Catalog.

#### Credential vending for external catalogs

You have the option to enable credential vending for each external catalog. If you don’t enable credential vending for a catalog, you must
provide your own storage credential separately to the query engine, outside of Open Catalog.

Before you enable credential vending for an external catalog, be aware that Open Catalog doesn’t prevent Iceberg tables in the catalog from
having overlapping storage directory locations. When tables have overlapping storage directory locations, a user could gain access to tables
that they shouldn’t have permission to access. Before you enable credential vending for an external catalog, ensure your tables in the
catalog don’t have overlapping storage directory locations.

For example, consider the following directory locations:

- Storage directory location for Table1 is `/MyCatalog/Schema1/Table1`.
- Storage directory location for Table2 is `/MyCatalog/Schema1/Table1/Table2`.

Users with vended credentials to Table1 will also have access to the storage location for Table2.

Here’s an example of how to resolve the overlapping storage directory locations:

- Storage directory location for Table1 is `/MyCatalog/Schema1/Table1`.
- Storage directory location for Table2 is `/MyCatalog/Schema1/Table2`.

To enable credential vending for an external catalog, see [Enable credential vending for an external catalog](./enable-credential-vending-external-catalog).

#### Credential vending for internal catalogs

Credential vending for internal catalogs is enabled by default when you create the catalog. You don’t need to enable it. When you create a
table in an internal catalog, Open Catalog prohibits you from creating the table within the directory or subdirectory for an existing table.

### Identity and access management (IAM)

Open Catalog uses the identity and access management (IAM) entity to securely connect to your storage for accessing table data, Iceberg
metadata, and manifest files that store the table schema, partitions, and other metadata. Open Catalog retains the IAM entity for your
storage location.

### Access control

Open Catalog enforces the access control that you configure across all tables registered with the service and governs security for all
queries from query engines in a consistent manner.

Open Catalog uses a role-based access control (RBAC) model that lets you centrally configure access for Open Catalog service principals
to catalogs, namespaces, and tables.

Open Catalog RBAC uses two different role types to delegate privileges:

- **Principal roles:** Granted to Open Catalog service principals and
  analogous to roles in other access control systems that you grant to service principals.
- **Catalog roles:** Configured with certain privileges on Open Catalog resources and granted to principal roles.

For more information, see [Access control](access-control "Access control").

## Billing

Open Catalog is currently free to use with general availability. Billing will begin in the first half of 2026.

When billing begins, Snowflake bills your account for the requests to the REST APIs supported by the Open Catalog service. For more
information, see the Serverless Feature Table in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

Snowflake does not bill your account for Iceberg tables stored outside of Snowflake. Your cloud storage provider bills you directly for data storage usage.

## Legal notices

Apache®, Apache Iceberg™, Apache Spark™, Apache Flink®, and Flink® are either registered trademarks or trademarks of the Apache Software Foundation in the United States and/or other countries.
