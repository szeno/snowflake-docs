# CREATE INTERACTIVE WAREHOUSE

Feature — Generally Available

This feature is generally available in select Amazon Web Services (AWS), Google Cloud
Platform (GCP), and Microsoft Azure regions only. For details, see
[Region availability](/user-guide/interactive-cloud-availability#label-interactive-region-availability).

Creates a new interactive [virtual warehouse](/user-guide/warehouses-overview) optimized for low-latency, high-concurrency workloads with interactive tables.

Interactive warehouses are designed to deliver optimal query performance when working with interactive tables, which provide
fast query responses for frequently accessed data through intelligent caching and optimization.

See also:
:   [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse), [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse), [DESCRIBE WAREHOUSE](/sql-reference/sql/desc-warehouse), [DROP WAREHOUSE](/sql-reference/sql/drop-warehouse), [SHOW WAREHOUSES](/sql-reference/sql/show-warehouses), [SHOW INTERACTIVE TABLES](/sql-reference/sql/show-interactive-tables), [CREATE INTERACTIVE TABLE](/sql-reference/sql/create-interactive-table)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] INTERACTIVE WAREHOUSE [ IF NOT EXISTS ] <name>
       [ TABLES ( <table_name> [ , <table_name> ... ] ) ]
       [ [ WITH ] objectProperties ]
       [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
       [ objectParams ]
```

Where:

> Copy code
>
> ```
> objectProperties ::=
>   WAREHOUSE_SIZE = { XSMALL | SMALL | MEDIUM | LARGE | XLARGE | XXLARGE | XXXLARGE | X4LARGE }
>   MAX_CLUSTER_COUNT = <num>
>   MIN_CLUSTER_COUNT = <num>
>   AUTO_SUSPEND = { <num> | NULL }
>   AUTO_RESUME = { TRUE | FALSE }
>   INITIALLY_SUSPENDED = { TRUE | FALSE }
>   RESOURCE_MONITOR = <monitor_name>
>   COMMENT = '<string_literal>'
> ```
>
> Copy code
>
> ```
> objectParams ::=
>   MAX_CONCURRENCY_LEVEL = <num>
>   STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = <num>
>   STATEMENT_TIMEOUT_IN_SECONDS = <num>
> ```

## Parameters

`name`
:   Specifies the identifier for the interactive warehouse. The identifier must be unique within your account.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TABLES ( ... )`
:   Optionally specifies a comma-separated list of interactive table names to immediately associate with the interactive warehouse.
    Using this clause starts the cache-warming process for the specified tables when the warehouse is created.

    `table_name`
    :   Specifies the identifier for an interactive table to associate with the warehouse. You can specify multiple table names separated by commas.

        Note

        - All specified tables must be interactive tables created with the `INTERACTIVE` keyword.
        - If this clause is omitted, you can associate interactive tables later using [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) with the `ADD TABLES` clause.
        - Cache warming may take significant time depending on the size of the data.

`WAREHOUSE_SIZE = string_constant`
:   Specifies the size of the interactive warehouse. Interactive warehouses support specific sizes optimized for interactive workloads.

    Valid values:
    :   - `XSMALL` , `'X-SMALL'`
        - `SMALL`
        - `MEDIUM`
        - `LARGE`
        - `XLARGE` , `'X-LARGE'`
        - `XXLARGE` , `X2LARGE` , `'2X-LARGE'`
        - `XXXLARGE` , `X3LARGE` , `'3X-LARGE'`
        - `X4LARGE` , `'4X-LARGE'`

    Default:
    :   `XSMALL`

    Note

    - To use a value that contains a hyphen (for example, `'2X-LARGE'`), you must enclose the value in single quotes, as shown.
    - Choose a warehouse size to match your workload requirements. You can adjust the
      `MIN_CLUSTER_COUNT` and `MAX_CLUSTER_COUNT` properties to optimize for concurrency.

`MAX_CLUSTER_COUNT = num`
:   Specifies the maximum number of clusters for a multi-cluster interactive warehouse.

    Valid values:
    :   `1` to `10` (depending on warehouse size)

    Default:
    :   `1` (single-cluster warehouse)

`MIN_CLUSTER_COUNT = num`
:   Specifies the minimum number of clusters for a multi-cluster interactive warehouse.

    Valid values:
    :   `1` to the value of MAX\_CLUSTER\_COUNT

    Default:
    :   `1`

`AUTO_SUSPEND = { num | NULL }`
:   Specifies the number of seconds of inactivity after which the interactive warehouse is automatically suspended.

    The minimum value for interactive warehouses is `86400` (24 hours). If you specify a value less
    than 86400, Snowflake uses 86400. Setting the value to `NULL` disables auto-suspend.

    Default:
    :   `NULL` (auto-suspend is disabled)

`AUTO_RESUME = { TRUE | FALSE }`
:   Specifies whether to automatically resume the interactive warehouse when a SQL statement is
    submitted to it.

    Default:
    :   `FALSE`

`INITIALLY_SUSPENDED = { TRUE | FALSE }`
:   Specifies whether the interactive warehouse is created in a suspended state.

    Default:
    :   `FALSE`

`RESOURCE_MONITOR = monitor_name`
:   Specifies the identifier of a resource monitor to assign to the interactive warehouse for credit usage control.

    Valid values:
    :   Any existing resource monitor

    Default:
    :   No value (no resource monitor assigned)

`COMMENT = 'string_literal'`
:   Specifies a comment for the interactive warehouse.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`MAX_CONCURRENCY_LEVEL = num`
:   Specifies the concurrency level for SQL statements executed by the interactive warehouse cluster.

`STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = num`
:   Specifies the time, in seconds, a SQL statement can be queued before being canceled.

`STATEMENT_TIMEOUT_IN_SECONDS = num`
:   Specifies the time, in seconds, after which a running SQL statement is canceled.
    Interactive warehouses have a maximum timeout interval of five seconds.
    If you specify a value greater than five seconds, Snowflake caps the timeout at five seconds.

    For example, if you set `STATEMENT_TIMEOUT_IN_SECONDS = 30`, Snowflake uses the value `5`.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE WAREHOUSE | Account | Required to create any warehouse, including interactive warehouses. |
| USAGE | Interactive Table | Required on each interactive table specified in the `TABLES` clause, if used. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- Interactive warehouses are created in a running state by default. To create a warehouse in a suspended state, set `INITIALLY_SUSPENDED = TRUE`.
- When you specify the TABLES clause, cache warming begins immediately for the specified
  interactive tables. This process may take significant time depending on data size.
- Interactive warehouses can query any table type (standard tables, Iceberg tables, dynamic tables, and interactive tables) directly,
  without copying or transforming data. For more information, see .
- Interactive warehouses support auto-suspend and auto-resume. The minimum AUTO\_SUSPEND value
  is 86400 seconds (24 hours). For more information, see [Resuming and suspending an interactive warehouse](/user-guide/interactive#label-interactive-resume-and-suspend-a-warehouse).
- Interactive warehouses support multi-cluster configuration for handling high-concurrency workloads.
- If you don’t specify the `TABLES` clause during creation, you can associate interactive tables
  later using [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) with the ADD TABLES clause.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Billing and pricing

For information about billing and pricing considerations for interactive warehouses, see
[Cost and billing considerations](/user-guide/interactive#label-interactive-cost).

## Examples

Create an interactive warehouse associated with specific interactive tables:

Copy code

```
CREATE OR REPLACE INTERACTIVE WAREHOUSE sales_interactive_wh
  TABLES (orders, customers, products)
  WAREHOUSE_SIZE = 'MEDIUM'
  COMMENT = 'Interactive warehouse for sales team analytics';
```

Create an interactive warehouse without associated tables (to be added later):

Copy code

```
CREATE INTERACTIVE WAREHOUSE analytics_interactive_wh
  WAREHOUSE_SIZE = 'LARGE'
  MAX_CLUSTER_COUNT = 3
  MIN_CLUSTER_COUNT = 3;
```

Create an interactive warehouse with resource monitoring:

Copy code

```
CREATE INTERACTIVE WAREHOUSE dev_interactive_wh
  WAREHOUSE_SIZE = 'XSMALL'
  RESOURCE_MONITOR = dev_resource_monitor
  COMMENT = 'Development interactive warehouse';
```

Resume an interactive warehouse and associate tables with it:

Copy code

```
-- Resume the warehouse
ALTER WAREHOUSE sales_interactive_wh RESUME;

-- Add additional tables if needed
ALTER WAREHOUSE sales_interactive_wh ADD TABLES (inventory);
```
