# Explore Data Products from SAP® BDC Connect for Snowflake

This topic describes how to use a Zerocopy Connector to list available SAP®
data products, create catalog-linked databases, and query the shared data in
Snowflake.

The connector must be in `CONNECTED` state before performing any of the
steps in this topic.

## In SAP® BDC, choose data products to share with Snowflake

To search for and share data products with Snowflake, users must use the central SAP Business Data Cloud catalog and have a global role that grants them the following privileges:

- BDC Data Packages (read) - To access SAP Business Data Cloud.
- Catalog Asset (read) - To access the catalog and view objects in the Assets and Data Products collections.
- Cloud Data Product (share) - To share data products to target systems.

Users with these privileges can share data products from the SAP Business Data Cloud catalog with the desired SAP Snowflake account to make them available for consumption to specific roles in that account.

To share data products with Snowflake:

1. In the central SAP Business Data Cloud catalog, select data products to share with an SAP Snowflake account
2. From **Catalog & Marketplace**, search for (or use filters) to find the data products to be shared
3. From the search results, select **Share** in the data product to be shared (for example, customer)
   to open the **Manage Share Access** dialog
4. In the **Overview** section, learn more about the data product by reviewing its details and available objects.
5. Under **Target System**:
   1. Choose the Snowflake account with the enrolled Zerocopy Connector to share with (if there is more than one).
   2. Select **Update**.

A message confirms the share process has started. After it finishes, a notification shows the result.

## In Snowflake, list shared data products

To list the data products that SAP® BDC has shared with your Snowflake account,
call the `SYSTEM$ZEROCOPY_CONNECTOR_LIST_SHARES` function:

Copy code

```
SELECT SYSTEM$ZEROCOPY_CONNECTOR_LIST_SHARES('my_db.my_schema.my_sap_connector');
```

The function returns a JSON array. Each element represents one shared data
product:

```
[
  {
    "name": "usid:b077d21c-b7a2-479a-a20e-bba1dbe91034:ns:sap.s4pce:r:SalesOrder:v:1",
    "id": "25c0de58-6e61-4bcc-ba68-c2c15b7a2d4b",
    "display_name": "Sales Order (BDF730, sap.s4pce:apiResource:SalesOrder:v1)",
    "comment": "An agreement between a vendor and a customer to provide products on a specific date.",
    "status": "MOUNTED",
    "catalog_linked_databases": [ { "name": "SALES_ORDER_CLD" } ],
    "properties": {
      "sap.ord.apiResource.ordId": "sap.s4pce:apiResource:SalesOrder:v1",
      "sap.ord.systemInstance.name": "BDF730",
      "sap.ord.systemInstance.id": "30f962e7-791c-41d7-9e72-1534823e8b21"
    }
  }
]
```

To filter and search more easily, parse the JSON output into a tabular format
using `PARSE_JSON` and `LATERAL FLATTEN`:

Copy code

```
WITH raw AS (
  SELECT PARSE_JSON(
    SYSTEM$ZEROCOPY_CONNECTOR_LIST_SHARES('my_db.my_schema.my_sap_connector')
  ) AS json_data
)
SELECT
  f.value:name::STRING                                         AS name,
  f.value:id::STRING                                           AS id,
  f.value:display_name::STRING                                 AS display_name,
  f.value:comment::STRING                                      AS comment,
  f.value:properties['sap.ord.apiResource.ordId']::STRING      AS api_resource_ord_id,
  f.value:properties['sap.ord.systemInstance.name']::STRING    AS system_instance_name,
  f.value:properties['sap.ord.systemInstance.id']::STRING      AS system_instance_id
FROM raw,
LATERAL FLATTEN(INPUT => json_data) f;
```

## Create a Catalog-Linked Database

To mount a shared SAP® data product in Snowflake, create a catalog-linked database using the
`LINKED_ZEROCOPY_CONNECTOR` clause. The role requires `CREATE DATABASE` on
the account and `USAGE` on the connector. The owner of the catalog-linked database can be
different from the owner of the connector.

Copy code

```
CREATE DATABASE my_sales_order
  LINKED_ZEROCOPY_CONNECTOR = (
    CONNECTOR_NAME = 'my_db.my_schema.my_sap_connector',
    SHARE_NAME = 'usid:b077d21c-b7a2-479a-a20e-bba1dbe91034:ns:sap.s4pce:r:SalesOrder:v:1',
    SYNC_INTERVAL_SECONDS = 86400
  );
```

Note

When a catalog-linked database is created, a read-only schema named
`snowflake$` is automatically created within it. This schema contains
[Semantic Views](/user-guide/views-semantic/overview) generated
from the SAP® Core Schema Notation (CSN). Semantic Views add business
meaning to the incoming shared data by defining metrics, entities, and
relationships — enabling consistent business definitions and powering
AI capabilities such as
[Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst)
directly on top of the SAP® data in Snowflake.

Use `SYNC_INTERVAL_SECONDS` to control how frequently Snowflake
automatically discovers schema and table changes from the shared data
product. The value can range from 30 to 86400 seconds (1 day). The
default value for SAP® BDC is 86400 seconds.

You can create multiple catalog-linked databases from the same connector, one per data product
shared from SAP® BDC.

To confirm the database was created, use [SHOW DATABASES](/sql-reference/sql/show-databases):

Copy code

```
SHOW DATABASES LIKE 'MY_SALES_ORDER%';
```

## Explore the Data

List the schemas and tables available in the catalog-linked database:

Copy code

```
SHOW SCHEMAS IN DATABASE my_sales_order;

SHOW TABLES IN DATABASE my_sales_order;
```

Query the data:

Copy code

```
SELECT * FROM my_sales_order.salesorder.salesorder LIMIT 100;
```

You can join tables across multiple catalog-linked databases. For example, to find the top
customers by revenue using data from two shared data products:

Copy code

```
SELECT
  s.salesorder,
  s.soldtoparty,
  c.customername,
  c.country,
  s.totalnetamount
FROM my_sales_order.salesorder.salesorder s
JOIN my_customers.customer.customer c
  ON s.soldtoparty = c.customer
WHERE s.overallsdprocessingstatus != 'C'
ORDER BY s.totalnetamount DESC
LIMIT 10;
```

## Create Table As Select (CTAS)

To persist query results as a native Snowflake table, use CREATE TABLE AS
SELECT (CTAS). Create a new database to hold the results:

Copy code

```
CREATE DATABASE IF NOT EXISTS my_ctas_db;
USE DATABASE my_ctas_db;

CREATE OR REPLACE TABLE top_customers_by_revenue AS
SELECT
  c.customer,
  c.customername,
  c.country,
  c.region,
  c.businesstype,
  COUNT(DISTINCT s.salesorder)           AS num_orders,
  SUM(s.totalnetamount)                  AS total_revenue,
  AVG(s.totalnetamount)                  AS avg_order_amount
FROM my_customers.customer.customer c
JOIN my_sales_order.salesorder.salesorder s
  ON c.customer = s.soldtoparty
WHERE c.deletionindicator = FALSE
GROUP BY 1, 2, 3, 4, 5;

-- Query the result table
SELECT * FROM top_customers_by_revenue LIMIT 10;
```

## Drop a Catalog-Linked Database

All catalog-linked databases must be dropped before you can disconnect or drop the connector.
Catalog-linked databases do not support `UNDROP`.

Copy code

```
DROP DATABASE my_sales_order;
```
