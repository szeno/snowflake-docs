# CREATE INTERACTIVE TABLE

Feature — Generally Available

This feature is generally available in select Amazon Web Services (AWS), Google Cloud
Platform (GCP), and Microsoft Azure regions only. For details, see
[Region availability](/user-guide/interactive-cloud-availability#label-interactive-region-availability).

Creates a new [interactive table](/user-guide/interactive) in the current/specified schema or
replaces an existing table. Interactive tables are optimized for low-latency, interactive queries
and provide the best performance when queried using interactive warehouses.

Interactive tables support a more limited set of SQL operations than standard tables and are
designed for high-concurrency, real-time query workloads such as dashboards and data-powered APIs.

Note

When you create an interactive table, you must define a CLUSTER BY clause on one or more columns
that are used in the WHERE clauses for your most time-critical queries.

You can also use the following CREATE INTERACTIVE TABLE variants:

- [Variant syntax: Static interactive table](#label-create-interactive-table-static) (creates a static interactive table populated from a query)
- [Variant syntax: Dynamic interactive table](#label-create-interactive-table-dynamic) (creates a dynamic interactive table with automatic refresh)

For the full CREATE TABLE syntax used for standard Snowflake tables, see [CREATE TABLE](/sql-reference/sql/create-table).

Tip

Before creating and using interactive tables, you should become familiar with the
[limitations and use cases](/user-guide/interactive). Interactive tables work best with simple SELECT statements with selective WHERE clauses.

See also:
:   [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse), [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse), [SHOW INTERACTIVE TABLES](/sql-reference/sql/show-interactive-tables), [SHOW TABLES](/sql-reference/sql/show-tables), [SHOW WAREHOUSES](/sql-reference/sql/show-warehouses), [DROP TABLE](/sql-reference/sql/drop-table)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] INTERACTIVE TABLE [ IF NOT EXISTS ] <table_name>
  (
    <col_name> <col_type>
      [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col_name> , <cond_col1> , ... ) ] ]
      [ , <col_name> <col_type> [ ... ] ]
  )
  CLUSTER BY ( <expr> [ , <expr> , ... ] )
  [ TARGET_LAG = '<num> { seconds | minutes | hours | days }' ]
  [ WAREHOUSE = <warehouse_name> ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ [ WITH ] AGGREGATION POLICY <policy_name> [ ENTITY KEY ( <col_name> [ , <col_name> ... ] ) ] ]
  [ [ WITH ] JOIN POLICY <policy_name> [ ALLOWED JOIN KEYS ( <col_name> [ , ... ] ) ] ]
  [ [ WITH ] STORAGE LIFECYCLE POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  AS <query>
```

## Required parameters

`table_name`
:   Specifies the identifier (i.e. name) for the interactive table; must be unique for the schema in
    which the table is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or
    special characters unless the entire identifier string is enclosed in double quotes (e.g.
    `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`CLUSTER BY ( expr [ , expr , ... ] )`
:   Specifies one or more columns or column expressions in the table as the clustering key. Choose
    clustering columns that are used in the WHERE clauses of your most time-critical queries, as this
    significantly affects query performance.

    The clustering key can use up to 1 KB total across all columns in the CLUSTER BY clause.

    For more details about choosing effective clustering keys, see [Clustering Keys & Clustered Tables](/user-guide/tables-clustering-keys).

`AS query`
:   Specifies the [SELECT statement](/sql-reference/constructs) that populates the interactive
    table. This query must be specified last in the CREATE INTERACTIVE TABLE statement, regardless of
    other parameters included.

    The query follows CREATE TABLE AS SELECT (CTAS) patterns and defines the data and schema for the
    interactive table.

`col_name`
:   Specifies the column identifier (i.e. name). Column identifiers must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier string is enclosed in double quotes.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`col_type`
:   Specifies the data type for the column.

    For details about the data types that can be specified for table columns, see [SQL data types reference](/sql-reference-data-types).

## Optional parameters

`MASKING POLICY policy_name`
:   Specifies the [masking policy](/user-guide/security-column-intro) to set on a column.

`USING ( col_name , cond_col_1 ... )`
:   Specifies the arguments to pass into the conditional masking policy SQL expression.

    The first column in the list specifies the column for the policy conditions to mask or tokenize the data and must match the
    column to which the masking policy is set.

    The additional columns specify the columns to evaluate to determine whether to mask or tokenize the data in each row of the query result
    when a query is made on the first column.

    If the USING clause is omitted, Snowflake treats the conditional masking policy as a normal
    [masking policy](/user-guide/security-column-intro).

`OR REPLACE`
:   Specifies to replace the interactive table if it already exists in the schema. This is equivalent
    to using [DROP TABLE](/sql-reference/sql/drop-table) on the existing table and then creating a new table with the same name.

`IF NOT EXISTS`
:   Specifies to create the interactive table only if it does not already exist in the schema. If a
    table with the same name already exists, the statement succeeds without creating a new table.

    Note

    The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive and cannot both be used in the
    same statement.

`TARGET_LAG = 'num { seconds | minutes | hours | days }'`
:   Specifies the maximum lag time for automatic refresh of the interactive table. When specified, the
    interactive table becomes a dynamic interactive table that automatically refreshes to stay within
    the specified lag time of the source data.

    - The minimum value is 60 seconds (1 minute).
    - If no unit is specified, the number represents seconds.
    - If TARGET\_LAG is not specified, the table is created as a static interactive table.

    When TARGET\_LAG is specified, the WAREHOUSE parameter is also required.

`WAREHOUSE = warehouse_name`
:   **Required when TARGET\_LAG is specified.** Specifies the standard warehouse used for refresh operations when TARGET\_LAG is set. This must be a standard warehouse, not an interactive warehouse.

`COMMENT = 'string_literal'`
:   Specifies a comment for the interactive table.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`ROW ACCESS POLICY policy_name ON ( col_name [ , col_name ... ] )`
:   Specifies the [row access policy](/user-guide/security-row-intro) to set on a table.

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`AGGREGATION POLICY policy_name [ ENTITY KEY ( col_name [ , col_name ... ] ) ]`
:   Specifies an [aggregation policy](/user-guide/aggregation-policies) to set on a table. You can apply one or more aggregation
    policies on a table.

    Use the optional ENTITY KEY parameter to define which columns uniquely identify an entity within the table. For more information, see
    [Implementing entity-level privacy with aggregation policies](/user-guide/aggregation-policies-entity-privacy). You can specify one or more entity keys for an aggregation policy.

`JOIN POLICY policy_name [ ALLOWED JOIN KEYS ( col_name [ , ... ] ) ]`
:   Specifies the [join policy](/user-guide/join-policies) to set on a table.

    Use the optional ALLOWED JOIN KEYS parameter to define which columns are allowed to be used as joining columns when
    this policy is in effect. For more information, see [Join policies](/user-guide/join-policies).

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`STORAGE LIFECYCLE POLICY policy_name ON ( col_name [ , col_name ... ] )`
:   Specifies a [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies)
    to attach to the table.

    The columns specified in the ON clause must match the argument count and data types defined in the
    policy function signature. Snowflake uses these columns to evaluate the policy expression and
    determine which rows to archive or expire.

    Important

    If you attach an archival storage policy to a table, the table is permanently assigned to the specified archive tier for its lifetime. You can’t change the archive tier by applying a new policy. For example, you can’t specify a policy created with a COOL archive tier in ALTER TABLE…DROP STORAGE LIFECYCLE POLICY and then subsequently alter the table to add a policy created with a COLD archive tier. To alter the archive tier for a table, contact Snowflake Support to request deletion of the currently archived data. For additional considerations, see [Archival storage policies](/user-guide/storage-management/storage-lifecycle-policies#label-slp-archive-limitations).

    For more information about creating and managing storage lifecycle policies, see
    [Create and manage storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies-create-manage).

    This parameter is not supported by the CREATE OR ALTER variant syntax.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTERACTIVE TABLE | Schema | Required to create an interactive table in the schema. |
| SELECT | Table, external table, view | Required on queried tables and/or views in the AS SELECT clause. |
| APPLY | Masking policy, row access policy, tag, storage lifecycle policy | Required only when applying a masking policy, row access policy, object tags, storage lifecycle policy, or any combination of these [governance](/guides-overview-govern) features when creating tables. |
| USAGE | Database, Schema | Required on the database and schema containing the interactive table. |
| USAGE | Warehouse | Required on the warehouse specified in the WAREHOUSE parameter (when TARGET\_LAG is used). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- Interactive tables must be created using a standard warehouse, not an interactive warehouse.
- The CLUSTER BY clause is required for all interactive tables and significantly affects query performance. Choose clustering columns carefully based on your most common WHERE clause patterns.
- Interactive tables provide the best performance when queried through interactive warehouses. To get optimal performance for an interactive table:

  1. Create an interactive warehouse
  2. Associate the interactive table with the interactive warehouse using ALTER WAREHOUSE … ADD TABLES
  3. Resume the interactive warehouse
  4. Use the interactive warehouse to query the interactive table
- Interactive tables support a limited set of SQL operations compared to standard tables:

  - SELECT statements with WHERE clauses are optimized.
  - Simple GROUP BY operations are supported.
  - DML operations (INSERT, UPDATE, DELETE) are not supported. The only allowed DML operation is INSERT OVERWRITE.
  - Complex query operations may have limited performance benefits.
- Dynamic interactive tables (with TARGET\_LAG) automatically refresh using the specified standard warehouse. The lag time balances data freshness with compute costs.
- Static interactive tables don’t automatically refresh. They require manual updates to reflect
  changes in source data. To do so, run a CREATE OR REPLACE command or an INSERT OVERWRITE command
  on the interactive table.
- A single masking policy that uses conditional columns can be applied to multiple tables provided that the column structure of the table
  matches the columns specified in the policy.
- When creating a table with a masking policy on one or more table columns, or a row access policy added to the table, use the
  [POLICY\_CONTEXT](/sql-reference/functions/policy_context) function to simulate a query on the column(s) protected by a masking policy and the table
  protected by a row access policy.
- Interactive tables store additional metadata and index information to accelerate queries, but this is compressed and has minimal impact on storage size.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- For creating a table with the WITH STORAGE LIFECYCLE POLICY clause:

  - You must have the necessary privileges to apply the policy. For information about required privileges, see
    [Storage lifecycle policy privileges](/user-guide/security-access-control-privileges#label-security-access-control-slp-privileges).
  - A table can have only one attached storage lifecycle policy.
  - The number of columns must match the argument count in the policy function signature, and the column data must be compatible with the argument types.
  - Associated policies aren’t affected if you rename table columns. Snowflake associates policies to tables by using the column IDs.
  - In order to evaluate and apply storage lifecycle policy expressions, Snowflake internally and temporarily bypasses any governance policies on a table.

## Variant syntax: Static interactive table

Creates a static interactive table that is populated once from the source query:

Copy code

```
CREATE [ OR REPLACE ] INTERACTIVE TABLE <table_name>
  CLUSTER BY ( <expr> [ , <expr> , ... ] )
  [ COMMENT = '<string_literal>' ]
  AS <query>
```

Static interactive tables don’t automatically refresh. They require manual updates to reflect
changes in source data. To do so, run a CREATE OR REPLACE command or an INSERT OVERWRITE command on
the interactive table.

## Variant syntax: Dynamic interactive table

Creates a dynamic interactive table that automatically refreshes based on the specified lag time:

Copy code

```
CREATE [ OR REPLACE ] INTERACTIVE TABLE <table_name>
  CLUSTER BY ( <expr> [ , <expr> , ... ] )
  TARGET_LAG = '<num> { seconds | minutes | hours | days }'
  WAREHOUSE = <warehouse_name>
  [ COMMENT = '<string_literal>' ]
  AS <query>
```

Dynamic interactive tables automatically refresh to stay within the specified TARGET\_LAG of the source data, using the specified standard warehouse for refresh operations.

## Examples

The following examples show different ways that you can create interactive tables,
along with specifying the source of their data and how to refresh the data.

### Basic static interactive table

Create a static interactive table from existing order data, clustered by customer and date for optimal query performance:

Copy code

```
CREATE INTERACTIVE TABLE orders_interactive
  CLUSTER BY (customer_id, order_date)
  COMMENT = 'Interactive table for real-time order analytics'
AS
  SELECT customer_id, order_date, product_id, quantity, total_amount
  FROM orders_staging
  WHERE order_date >= '2024-01-01';
```

### Dynamic interactive table with auto-refresh

Create a dynamic interactive table that refreshes every 5 minutes to provide near real-time sales summaries:

Copy code

```
CREATE INTERACTIVE TABLE sales_summary_interactive
  CLUSTER BY (region, product_category)
  TARGET_LAG = '5 minutes'
  WAREHOUSE = refresh_warehouse
  COMMENT = 'Real-time sales dashboard data'
AS
  SELECT
    region,
    product_category,
    SUM(sales_amount) as total_sales,
    COUNT(*) as transaction_count,
    AVG(sales_amount) as avg_sale
  FROM sales_data
  GROUP BY region, product_category;
```

### Multi-column clustering for complex queries

Create an interactive table with multi-column clustering optimized for various query patterns:

Copy code

```
CREATE INTERACTIVE TABLE customer_analytics_interactive
  CLUSTER BY (customer_tier, region, signup_date)
  TARGET_LAG = '10 minutes'
  WAREHOUSE = analytics_warehouse
AS
  SELECT
    customer_id,
    customer_tier,
    region,
    signup_date,
    total_orders,
    lifetime_value,
    last_order_date
  FROM customer_metrics
  WHERE customer_tier IN ('GOLD', 'PLATINUM', 'DIAMOND');
```

### Replace existing interactive table

Replace an existing interactive table with updated clustering and refresh settings:

Copy code

```
CREATE OR REPLACE INTERACTIVE TABLE product_performance_interactive
  CLUSTER BY (category, brand, launch_date)
  TARGET_LAG = '2 minutes'
  WAREHOUSE = fast_refresh_warehouse
AS
  SELECT
    product_id,
    category,
    brand,
    launch_date,
    units_sold,
    revenue,
    customer_rating
  FROM product_sales_view
  WHERE launch_date >= DATEADD('month', -6, CURRENT_DATE());
```
