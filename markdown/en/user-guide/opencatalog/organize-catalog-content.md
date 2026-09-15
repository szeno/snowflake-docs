# Organize catalog content

Feature — Generally Available

Not available in government regions.

This topic provides instructions for how to create namespaces and tables for an internal catalog in Snowflake Open Catalog.

Important

If you drop a table in Snowflake Open Catalog without purging it, don’t create a new table with the same name and location as the dropped
table. If you do, a user could gain access to the original table’s data when they shouldn’t have permission to access it. For example, if
you drop but don’t purge Table1 where its storage directory location is /MyCatalog/Schema1/Table1, don’t create a new Table1 within
the same Table1 storage directory. When you drop a table without purging it, its data is retained in the external cloud storage.

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

## Organizing catalog content

A catalog admin can use Open Catalog or a third-party query engine to organize catalog content as follows:

| Object | Use |
| --- | --- |
| Namespace | - Open Catalog - Third-party query engine |
| Table | Third-party query engine |

Expand

Show lessSee more

**Note**

> The tables and namespaces for an external catalog are read-only in Open Catalog. If you need to organize catalog content for an external
> catalog, you must use Snowflake. For more information, see [Snowflake-managed Apache Iceberg™ tables](https://docs.snowflake.com/en/user-guide/tables-iceberg).

The example code in this topic shows how to use Apache Spark to organize catalog content. The example code is in PySpark.

## Create a namespace

This section provides instructions for creating top-level or nested namespaces.

**Important**

> When you create a namespace, don’t use periods or spaces in the namespace name.

### Create a top-level namespace

To create a top-level namespace, you can use Apache Spark or Open Catalog.

#### Example: Create a top-level namespace by using Apache Spark

The following example code creates a top-level namespace named `namespace1` in the catalog `catalog1`:

Copy code

```
spark.sql("use catalog1").show()
spark.sql("CREATE NAMESPACE namespace1")
```

#### Create a top-level namespace by using Open Catalog

1. Sign in to Open Catalog.
2. From the menu on the left, select **Catalogs**.
3. From the list of catalogs, select the catalog where you want to create a top-level namespace.
4. Select **+ Namespace**.
5. For **Name**, enter a name for the namespace, and then select **Submit**.

### Create a nested namespace

To create a nested namespace, you can use Apache Spark or Open Catalog.

#### Example: Create a nested namespace by using Apache Spark

The following example code creates a nested namespace named `namespace1a` in the catalog `catalog1`. This nested namespace is created under the
existing top-level namespace `namespace1`:

Copy code

```
spark.catalog.setCurrentCatalog("catalog1")
spark.sql("use catalog1").show()
spark.sql("CREATE NAMESPACE namespace1.namespace1a")
```

#### Create a nested namespace by using Open Catalog

1. Sign in to Open Catalog.
2. From the menu on the left, select **Catalogs**.
3. From the list of catalogs, select the catalog where you want to create a nested namespace.
4. On the **Namespaces** tab, navigate to the parent namespace where you want to create the nested namespace.
5. Select **+ Namespace**.
6. For **Name**, enter a name for the nested namespace, and then select **Submit**.

## Create a table

This section provides examples for creating tables by using Apache Spark.

Important

If you drop a table in Snowflake Open Catalog without purging it, don’t create a new table with the same name and location as the dropped
table. If you do, a user could gain access to the original table’s data when they shouldn’t have permission to access it. For example, if
you drop but don’t purge Table1 where its storage directory location is /MyCatalog/Schema1/Table1, don’t create a new Table1 within
the same Table1 storage directory. When you drop a table without purging it, its data is retained in the external cloud storage.

### Example: Create a table

The following example code creates a `customers` table under nested namespace `namespace1a` in the catalog `catalog1`. It is created with `id` and
`custnum` columns, and the data type for both columns is `integer`:

Copy code

```
spark.sql("use catalog1").show()
spark.sql ("use namespace1.namespace1a")
spark.sql("CREATE OR REPLACE TABLE customers (id int, custnum int) using iceberg")
```

### Example: Insert rows into a table

The following example code inserts a row into the `customers` table:

Copy code

```
spark.sql("use catalog1").show()
spark.sql ("use namespace1.namespace1a")
spark.sql("INSERT INTO customers VALUES (123,456)")
```
