# Use Apache Iceberg™ tables with Snowflake Open Catalog in Snowflake

Note

New customers should use [Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon)
for Apache Iceberg™ tables and multi-engine interoperability with Iceberg. Customers who
haven’t previously created a Snowflake Open Catalog account can’t sign up for their first Open
Catalog account.

Existing Snowflake Open Catalog customers can continue to use and can create additional
Open Catalog accounts if necessary.

Use Apache Iceberg™ tables in Snowflake to work with Snowflake Open Catalog.

## What is Snowflake Open Catalog?

Open Catalog is a catalog implementation for Iceberg built on the open source Apache Iceberg REST protocol. To learn more,
see the [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview) documentation.

Snowflake supports the following options for working with Open Catalog:

- [Query a table registered in Snowflake Open Catalog using Snowflake](/user-guide/tables-iceberg-open-catalog-query).
- [Write to a table registered in Open Catalog using Snowflake](/user-guide/tables-iceberg-externally-managed-writes).
- [Sync a Snowflake-managed Iceberg table with Open Catalog](/user-guide/tables-iceberg-open-catalog-sync).

## Considerations

When using Snowflake with Open Catalog, be aware of the following considerations:

**Storage**

- Just like [Snowflake-managed Iceberg tables](/user-guide/tables-iceberg#label-tables-iceberg-snowflake-as-catalog), you store Iceberg tables managed by Open Catalog
  in external cloud storage.
- Iceberg tables in Snowflake use an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) to provide access to your cloud storage,
  while tables managed by Open Catalog use a [storage configuration](https://other-docs.snowflake.com/en/opencatalog/overview#storage-configuration).

**Configuration for syncing Snowflake-managed Iceberg tables**

- To sync a Snowflake-managed table with Open Catalog, you must first create an external volume in Snowflake and then create an external
  catalog in Open Catalog that points to the same location as the external volume. For more information, see
  [Sync a Snowflake-managed table with Snowflake Open Catalog](/user-guide/tables-iceberg-open-catalog-sync).

**Table access**

- Snowflake-managed Iceberg tables that you sync with Open Catalog are read-only in Open Catalog.
- Snowflake can query but can’t write to tables managed by Open Catalog.

## Terminology differences

This section summarizes the key differences in terminology between Snowflake and Open Catalog.

| Snowflake term | Open Catalog term |
| --- | --- |
| [Database](/guides-overview-db) | Open Catalog uses *catalogs*, which are like databases in Snowflake. In Open Catalog, you create one or more catalog resources to organize Iceberg tables under namespaces. For more information, see [Catalog](https://other-docs.snowflake.com/en/opencatalog/overview#catalog) in the Open Catalog documentation.  When you sync a Snowflake-managed table with Open Catalog, Snowflake syncs the table with the catalog associated with the table’s catalog integration using two parent namespaces. The namespaces correspond to the table’s database and schema in Snowflake. For example, if you have a `db1.public.table1` Iceberg table registered in Snowflake and you specify `catalog1` in the catalog integration, it gets synced to Open Catalog with the following fully qualified name: `catalog1.db1.public.table1`. |
| [Schema](/sql-reference/ddl-database) | In Open Catalog, the concepts of schema and namespace are synonymous and can be used interchangeably.  **Namespace** is displayed in the Open Catalog user interface. Open Catalog uses namespaces to hold a collection of objects and the term *namespace* is primarily used in the Open Catalog documentation. For more information about namespaces, see [Namespace](/user-guide/tables-iceberg-open-catalog#label-terminology-differences-namespace).  However, if you’re using a third-party query engine, such as Apache Spark, and you run the CREATE SCHEMA or CREATE DATABASE command, you create a namespace in Open Catalog. You can also run the CREATE NAMESPACE command to create a namespace. |
| [Namespace](/sql-reference/ddl-database) | Like Snowflake, Open Catalog also uses namespaces but with key differences compared to how Snowflake uses namespaces.  A catalog in Open Catalog comprises top-level namespaces, which you define, along with any number of nested namespaces beneath them, which you also define.  Nested namespaces allow you to register tables with the same name within the same catalog. For example, a catalog named `customers` can contain the following `customerdata` tables, which are grouped under a top-level namespace `<region>` and a nested namespace `<state>`:   - `customers.northeast.maine.customerdata` - `customers.northeast.vermont.customerdata`   Also, in Open Catalog, you can group tables under any namespace in the namespace hierarchy, including top-level namespaces.  For more information about namespaces, including a conceptual diagram of a sample Open Catalog structure, see [key concepts of Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview#key-concepts). |
| [Role](/user-guide/security-access-control-overview#label-access-control-overview-roles) | In Open Catalog, *principal roles* are like roles in Snowflake but with key differences. You don’t grant privileges to a principal role. Instead, you grant privileges to a catalog role, which you then grant to a principal role, and then you grant the principal role to a service principal, thus bestowing the privileges on the service principal. Also, you can’t assign principal roles to other principal roles. You can only grant one principal role to a service principal.  You can use a principal role to logically group service principals together. The scope of a principal role is across all catalogs. Also, there aren’t different types of principal roles. For more information, see [Principal role](https://other-docs.snowflake.com/en/opencatalog/access-control#principal-role) in the Open Catalog documentation. |
| [Database role](/user-guide/security-access-control-overview#label-access-control-overview-role-types) | Open Catalog uses *catalog roles*, which are like database roles in Snowflake. Catalog roles specify a set of permissions for actions on a catalog or objects in the catalog. The scope of a catalog role is the catalog where it is created.  In Open Catalog, you grant privileges to catalog roles. Next, you grant catalog roles to principal roles, and then you grant principal roles to service principals, which grants access to resources. You can grant multiple catalog roles to a principal role but only one principal role to a service principal. For more information, see [Catalog role](https://other-docs.snowflake.com/en/opencatalog/access-control#catalog-role) in the Open Catalog documentation. |
| [User](/user-guide/security-access-control-overview) | In the context of access control, there is no concept of a user in Open Catalog.  In Open Catalog, privileges are bestowed on *service principals*, not users. Query engines use service principals to connect to catalogs. For more information, see [Service principal](https://other-docs.snowflake.com/en/opencatalog/overview#service-principal) in the Open Catalog documentation. |

Expand

Show lessSee more

## Legal Notices

Apache®, Apache Iceberg™, Apache Spark™, Apache Flink®, and Flink® are either registered trademarks or trademarks of the Apache Software
Foundation in the United States and/or other countries.
