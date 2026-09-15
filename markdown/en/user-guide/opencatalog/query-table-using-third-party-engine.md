# Query a table in Snowflake Open Catalog using a third-party engine

Feature — Generally Available

Not available in government regions.

This topic provides instructions for using a third-party query engine to query a table in Snowflake Open Catalog.

## Prerequisites

Before you can query a table in Open Catalog, you must do the following:

- [Create a catalog](create-catalog).
- Grant read privileges to the catalog you created. For more
  information, see [Secure catalogs](secure-catalogs).
- [Configure a service connection](configure-service-connection).
- Register the service connection you configured. For more information, see [Register a service connection](register-service-connection).

## Considerations for querying Snowflake-managed Apache Iceberg™ tables

If you use Snowflake and sync a Snowflake-managed Iceberg table to Open Catalog, be aware of the following considerations when querying
the table in Open Catalog:

- [Unquoted identifiers](https://docs.snowflake.com/sql-reference/identifiers-syntax#label-unquoted-identifier): If you create a database, schema,
  or Iceberg table in Snowflake and give it a name that contains letters *without* enclosing the name in double quotes, you must specify the
  name in all caps when you reference it in Open Catalog. For example, if `iceberg_tables.public.table1` is the name in Snowflake, use
  `ICEBERG_TABLES.PUBLIC.TABLE1` in Open Catalog.
- [Double-quoted identifiers](https://docs.snowflake.com/sql-reference/identifiers-syntax#label-delimited-identifier): If you create an object in
  Snowflake with the name in double quotes, when referencing the object in a query in Open Catalog, you must do the following:

  - Enclose the object name with backticks.
  - Specify the object name exactly as it appears in Open Catalog to account for any character that was rendered as a different character,
    when applicable.

  The following example shows the `My 'Identifier'` Snowflake identifier, which was created with double quotes, being referenced in a query in
  Open Catalog:

  Copy code

  ```
  spark.sql ("select * from `My+'Identifier'`.PUBLIC.TABLE1").show()
  ```

  Open Catalog renders the space character in double-quoted Snowflake identifiers as `+`.

## Example: Query a table

The following example code shows how to use Apache Spark to query the `customers` table in the catalog `catalog1`. The `customers` table is located
under `namespace1a`, which is nested under the top-level namespace `namespace1`:

Copy code

```
spark.sql("use catalog1").show()
spark.sql("use namespace1.namespace1a").show()
spark.sql("SELECT * FROM customers").show()
```
