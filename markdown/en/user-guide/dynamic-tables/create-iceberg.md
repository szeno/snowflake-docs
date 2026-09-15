# Create a dynamic Apache Iceberg™ table

A dynamic Apache Iceberg™ table stores its output in Iceberg format on Snowflake-managed external storage. It supports the same refresh modes and scheduling as a regular dynamic table, but external engines such as Spark and Trino can also read the data directly.

For the full syntax reference, see [CREATE DYNAMIC ICEBERG TABLE](/sql-reference/sql/create-dynamic-table#label-create-dt-iceberg-syntax).

## Prerequisites

Before you create a dynamic Iceberg table, set up an external volume. The external volume defines
the cloud storage location where Snowflake writes Iceberg data and metadata files.
For setup instructions, see
[Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

## Create a dynamic Iceberg table with Snowflake-managed storage

The CREATE statement requires three Iceberg-specific parameters: EXTERNAL\_VOLUME, CATALOG, and
BASE\_LOCATION. This example creates a dynamic Iceberg table that reads from the `raw_orders`
base table:

Copy code

```
CREATE OR REPLACE DYNAMIC ICEBERG TABLE dt_orders_iceberg
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    EXTERNAL_VOLUME = 'my_external_volume'
    CATALOG = 'SNOWFLAKE'
    BASE_LOCATION = 'dt_orders_iceberg'
    REFRESH_MODE = INCREMENTAL
AS
    SELECT
        order_id,
        customer_id,
        order_date,
        TRIM(UPPER(product_name)) AS product_name,
        quantity,
        unit_price,
        quantity * unit_price AS line_total,
        order_status
    FROM raw_orders
    WHERE order_status != 'returned';
```

To use [Snowflake storage for Iceberg tables](/user-guide/tables-iceberg-internal-storage),
you can omit EXTERNAL\_VOLUME, CATALOG, and BASE\_LOCATION:

Note

Snowflake storage for Iceberg tables is available only on AWS and Azure. It isn’t available
in government regions or in the People’s Republic of China.

Copy code

```
-- Same definition as above, but without explicit storage parameters
CREATE OR REPLACE DYNAMIC ICEBERG TABLE dt_orders_iceberg_managed
    TARGET_LAG = '10 minutes'
    WAREHOUSE = transform_wh
    -- No EXTERNAL_VOLUME, CATALOG, or BASE_LOCATION needed
    REFRESH_MODE = INCREMENTAL
AS
    SELECT ... FROM raw_orders ...;  -- same columns as explicit storage example above
```

For full parameter details including PARTITION\_BY, TARGET\_FILE\_SIZE, and PATH\_LAYOUT, see
[CREATE DYNAMIC ICEBERG TABLE](/sql-reference/sql/create-dynamic-table#label-create-dt-iceberg-syntax).

### Verify the dynamic Iceberg table

Confirm the table exists and check the `is_iceberg` flag:

Copy code

```
SHOW DYNAMIC TABLES LIKE 'dt_orders_iceberg';
```

```
+--------------------+-----+--------------+------+------------------+------------+
| name               | ... | refresh_mode | rows | scheduling_state | is_iceberg |
+--------------------+-----+--------------+------+------------------+------------+
| DT_ORDERS_ICEBERG  | ... | INCREMENTAL  |    4 | RUNNING          | true       |
+--------------------+-----+--------------+------+------------------+------------+
```

The `is_iceberg` column reads `true` for dynamic Iceberg tables and `false` for
regular dynamic tables.

You can also use CREATE OR ALTER to create a dynamic Iceberg table if it doesn’t exist or alter an existing one in place. For syntax and limitations, see [CREATE OR ALTER DYNAMIC ICEBERG TABLE](/sql-reference/sql/create-dynamic-table#label-create-or-alter-dit-syntax).

## Grant access with future grants

Future grants for dynamic Iceberg tables use DYNAMIC TABLES, not ICEBERG TABLES. The following
syntax grants privileges on any dynamic Iceberg tables created in the schema:

Copy code

```
GRANT <privilege> ON FUTURE DYNAMIC TABLES IN SCHEMA mydb.myschema TO ROLE transform_role;
```

Using ON FUTURE ICEBERG TABLES does not apply to dynamic Iceberg tables:

Copy code

```
-- This does NOT grant access to dynamic Iceberg tables:
GRANT <privilege> ON FUTURE ICEBERG TABLES IN SCHEMA mydb.myschema TO ROLE transform_role;
```

## Limitations

Dynamic Iceberg tables have additional limitations:

| Limitation | Detail |
| --- | --- |
| IF NOT EXISTS not supported | The IF NOT EXISTS clause is not supported. Attempting to use it results in a syntax error. Use CREATE OR REPLACE instead. |
| No ALTER DYNAMIC ICEBERG TABLE | ALTER DYNAMIC ICEBERG TABLE does not exist as a command. Use ALTER DYNAMIC TABLE for refresh properties and ALTER ICEBERG TABLE for storage properties. |
| Clone support | You can clone a dynamic Iceberg table to a new dynamic Iceberg table or to a Snowflake-managed Iceberg table, but not to a regular table. See [Clone a dynamic Iceberg table](/user-guide/dynamic-tables/cloning#label-dynamic-tables-clone-iceberg). |
| SNOWFLAKE catalog only | The CATALOG parameter must be `'SNOWFLAKE'`. External catalogs (Snowflake Open Catalog, AWS Glue) are not supported. |
| Backup exclusion | Dynamic Iceberg tables are not included in database or schema backups. |
| Backfill not supported | Using backfill on dynamic Iceberg tables is not supported. |

Expand

Show lessSee more

Dynamic Iceberg tables support the same data types as regular Iceberg tables.
For the full mapping, see [Supported data types](/user-guide/tables-iceberg-data-types#label-tables-iceberg-data-type-mapping-table).

## What’s next

- Learn about refresh modes for your dynamic table: [Dynamic table refresh modes](/user-guide/dynamic-tables/refresh-modes)
- Monitor refresh history and troubleshoot failures: [Monitor dynamic tables](/user-guide/dynamic-tables/monitoring)
- Understand Iceberg table storage options: [Apache Iceberg™ tables](/user-guide/tables-iceberg)
- For storage and compute cost considerations, see [Understanding costs for dynamic tables](/user-guide/dynamic-tables/cost).
- To optimize refresh queries, see [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).
