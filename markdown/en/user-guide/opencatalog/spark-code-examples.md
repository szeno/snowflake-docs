# Code examples: Apache Spark™

Feature — Generally Available

Not available in government regions.

This section provides code examples for using Apache Spark™ to do the following tasks in Snowflake Open Catalog:

- Configure a service connection
- Use a catalog
- List catalogs
- List namespaces
- Create a namespace
- Use a namespace
- Drop a namespace
- Create a table
- Query a table
- Show table properties
- List tables
- Drop a table

## Required privileges

To perform the commands included in the code examples, the following privileges must be bestowed to the service principal you use to connect
Spark to Open Catalog:

| Command | Required privilege |
| --- | --- |
| Show Namespaces | NAMESPACE\_LIST |
| Create namespace | NAMESPACE\_CREATE |
| Use namespace | NAMESPACE\_READ\_PROPERTIES |
| Show tables | TABLE\_LIST |
| Create or replace table | - TABLE\_WRITE\_DATA - TABLE\_CREATE |
| Drop namespace | NAMESPACE\_DROP |
| Drop table | TABLE\_DROP |
| Insert into table | TABLE\_WRITE\_DATA |
| Select from table | TABLE\_READ\_DATA |

Expand

Show lessSee more

## Configure a service connection

See [examples of configuring a service connection in Spark](register-service-connection#examples).

## Use catalog

Use the catalog `catalog1`:

Copy code

```
spark.sql("use catalog1").show()
```

## List catalogs

List the catalogs you’re connected to:

Copy code

```
spark.sql("show catalogs").show()
```

## List namespaces

List the namespaces for the catalog you’re connected to:

Copy code

```
spark.sql("show namespaces").show()
```

## Create a namespace

Create the namespace `namespace1`:

Copy code

```
spark.sql("CREATE NAMESPACE namespace1")
```

## Use a namespace

Use the namespace `namespace1`:

Copy code

```
spark.sql("use namespace1").show()
```

## Drop a namespace

Drop the namespace `namespace1` from the catalog:

Copy code

```
spark.sql("DROP NAMESPACE namespace1")
```

## Create a table

Create a `customers` table under the parent namespace `namespace1`:

Copy code

```
spark.sql ("use namespace1");
spark.sql("CREATE OR REPLACE TABLE customers (id int, custnum int) using iceberg")
```

## Query a table

Query the `customers` table:

Copy code

```
spark.sql ("use namespace1");
spark.sql("SELECT * FROM customers").show()
```

## Show table properties

Show the table properties for the `customers` table:

Copy code

```
spark.sql("SHOW TBLPROPERTIES customers").show(50, False)
```

## List tables

List the tables for the catalog you’re connected to:

Copy code

```
spark.sql("show tables").show()
```

## Drop a table

Drop the `customers` table under parent namespace `namespace1`:

Copy code

```
spark.sql ("use namespace1");
spark.sql("DROP TABLE customers")
```
