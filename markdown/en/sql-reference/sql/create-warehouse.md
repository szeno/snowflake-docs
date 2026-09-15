# CREATE WAREHOUSE

Creates a new [virtual warehouse](/user-guide/warehouses-overview) in the system.

Initial creation of a virtual warehouse might take some time to provision the compute resources, unless the warehouse is created initially
in a `SUSPENDED` state.

This command supports the following variants:

- [CREATE OR ALTER WAREHOUSE](#label-create-or-alter-warehouse-syntax): Creates a new warehouse if it doesn’t exist or alters an existing warehouse.

See also:
:   [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse), [DESCRIBE WAREHOUSE](/sql-reference/sql/desc-warehouse), [DROP WAREHOUSE](/sql-reference/sql/drop-warehouse), [SHOW WAREHOUSES](/sql-reference/sql/show-warehouses)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] WAREHOUSE [ IF NOT EXISTS ] <name>
       [ [ WITH ] objectProperties ]
       [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
       [ objectParams ]
```

Where:

> Copy code
>
> ```
> objectProperties ::=
>   WAREHOUSE_TYPE = { STANDARD | 'SNOWPARK-OPTIMIZED' | ADAPTIVE }
>   WAREHOUSE_SIZE = { XSMALL | SMALL | MEDIUM | LARGE | XLARGE | XXLARGE | XXXLARGE | X4LARGE | X5LARGE | X6LARGE }
>   GENERATION = { '1' | '2' }
>   RESOURCE_CONSTRAINT = { STANDARD_GEN_1 | STANDARD_GEN_2 | MEMORY_1X | MEMORY_1X_x86 | MEMORY_16X | MEMORY_16X_x86 | MEMORY_64X | MEMORY_64X_x86 }
>   MAX_CLUSTER_COUNT = <num>
>   MIN_CLUSTER_COUNT = <num>
>   SCALING_POLICY = { STANDARD | ECONOMY }
>   AUTO_SUSPEND = { <num> | NULL }
>   AUTO_RESUME = { TRUE | FALSE }
>   INITIALLY_SUSPENDED = { TRUE | FALSE }
>   RESOURCE_MONITOR = <monitor_name>
>   COMMENT = '<string_literal>'
>   ENABLE_QUERY_ACCELERATION = { TRUE | FALSE }
>   QUERY_ACCELERATION_MAX_SCALE_FACTOR = <num>
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

## Variant syntax

### CREATE OR ALTER WAREHOUSE

Creates a new warehouse if it doesn’t already exist, or transforms an existing warehouse into the warehouse defined in the statement.
A CREATE OR ALTER WAREHOUSE statement follows the syntax rules of a CREATE WAREHOUSE statement and has the same limitations as an
[ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) statement.

The following modifications are supported when altering a warehouse:

- Changing warehouse properties and parameters. For example, WAREHOUSE\_TYPE, AUTO\_RESUME or MAX\_CLUSTER\_COUNT.

For more information, see [CREATE OR ALTER WAREHOUSE usage notes](#label-create-or-alter-warehouse-usage-notes) and [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

Copy code

```
CREATE OR ALTER WAREHOUSE <name>
     [ [ WITH ] objectProperties ]
     [ objectParams ]

objectProperties ::=
  WAREHOUSE_TYPE = { STANDARD | 'SNOWPARK-OPTIMIZED' | ADAPTIVE }
  WAREHOUSE_SIZE = { XSMALL | SMALL | MEDIUM | LARGE | XLARGE | XXLARGE | XXXLARGE | X4LARGE | X5LARGE | X6LARGE }
  GENERATION = { '1' | '2' }
  RESOURCE_CONSTRAINT = { STANDARD_GEN_1 | STANDARD_GEN_2 | MEMORY_1X | MEMORY_1X_x86 | MEMORY_16X | MEMORY_16X_x86 | MEMORY_64X | MEMORY_64X_x86 }
  MAX_CLUSTER_COUNT = <num>
  MIN_CLUSTER_COUNT = <num>
  SCALING_POLICY = { STANDARD | ECONOMY }
  AUTO_SUSPEND = { <num> | NULL }
  AUTO_RESUME = { TRUE | FALSE }
  INITIALLY_SUSPENDED = { TRUE | FALSE }
  RESOURCE_MONITOR = <monitor_name>
  COMMENT = '<string_literal>'
  ENABLE_QUERY_ACCELERATION = { TRUE | FALSE }
  QUERY_ACCELERATION_MAX_SCALE_FACTOR = <num>

objectParams ::=
  MAX_CONCURRENCY_LEVEL = <num>
  STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = <num>
  STATEMENT_TIMEOUT_IN_SECONDS = <num>
```

## Required parameters

`name`
:   Identifier for the virtual warehouse; must be unique for your account.

    In addition, the identifier must start with an alphabetic character and can’t contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional properties (`objectProperties`)

`WAREHOUSE_TYPE = { STANDARD | 'SNOWPARK-OPTIMIZED' | ADAPTIVE }`
:   Specifies the warehouse type.

    Valid values:
    :   - `STANDARD`, `'STANDARD'`
        - `'SNOWPARK-OPTIMIZED'`
        - `ADAPTIVE`, `'ADAPTIVE'`

    Default:
    :   `STANDARD`

    Note

    - To use a value that contains a hyphen (`'SNOWPARK-OPTIMIZED'`), you must enclose the value in single quotes, as shown.
    - For [Adaptive Warehouses](/user-guide/warehouses-adaptive), use `ADAPTIVE`. See
      [SQL reference](/user-guide/warehouses-adaptive#label-create-adaptive-warehouse-syntax) for supported properties.

`WAREHOUSE_SIZE = \{ XSMALL | SMALL | MEDIUM | LARGE | XLARGE | XXLARGE | XXXLARGE | X4LARGE | X5LARGE | X6LARGE \}`
:   Specifies the size of the virtual warehouse. The size determines the amount of compute resources in each cluster in the warehouse and,
    therefore, the number of credits consumed while the warehouse is running.

    Valid values:
    :   | Supported Values | Synonyms |
        | --- | --- |
        | `XSMALL` | `'X-SMALL'` |
        | `SMALL` |  |
        | `MEDIUM` |  |
        | `LARGE` |  |
        | `XLARGE` | `'X-LARGE'` |
        | `XXLARGE` | `X2LARGE`, `'2X-LARGE'` |
        | `XXXLARGE` | `X3LARGE`, `'3X-LARGE'` |
        | `X4LARGE` | `'4X-LARGE'` |
        | `X5LARGE` | `'5X-LARGE'` |
        | `X6LARGE` | `'6X-LARGE'` |
        | Default:  `XSMALL` |

        Expand

        Show lessSee more

        - X5LARGE and X6LARGE sizes for Snowpark-optimized warehouses are only supported with the MEMORY\_16X resource constraint.
        - X5LARGE and X6LARGE sizes aren’t supported for standard warehouses that use the STANDARD\_GEN\_2 resource constraint.
        - The default size for Snowpark-optimized warehouses is MEDIUM.
        - To use a value that contains a hyphen (for example, `'2X-LARGE'`), you must enclose the value in single quotes, as shown.

`GENERATION = { '1' | '2' }`
:   Specifies the warehouse generation for standard warehouses. This parameter provides a simplified way to set the warehouse generation,
    instead of using RESOURCE\_CONSTRAINT = STANDARD\_GEN\_1 or STANDARD\_GEN\_2.

    Valid values:
    :   - `'1'`: Uses generation 1 compute resources. Equivalent to
          `RESOURCE_CONSTRAINT = STANDARD_GEN_1`.
        - `'2'`: Uses generation 2 compute resources. Equivalent to
          `RESOURCE_CONSTRAINT = STANDARD_GEN_2`.

    Default:
    :   `'2'` (generation 2 compute resources)

    Note

    - Values must be enclosed in single quotes (for example, `'1'`, not `1`).
    - GENERATION applies only to standard warehouses (`WAREHOUSE_TYPE = STANDARD`).
    - When both GENERATION and RESOURCE\_CONSTRAINT are specified, any mismatch results in an error.
    - You can’t use GENERATION with Snowpark-optimized warehouses or memory-based resource constraints (MEMORY\_1X, MEMORY\_16X, MEMORY\_64X).

`RESOURCE_CONSTRAINT = { STANDARD_GEN_1 | STANDARD_GEN_2 | MEMORY_1X | MEMORY_1X_x86 | MEMORY_16X | MEMORY_16X_x86 | MEMORY_64X | MEMORY_64X_x86 }`

> [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
>
> The 1 TB resource constraints (MEMORY\_64X and MEMORY\_64X\_x86) are available as a preview feature.
> The 1 TB constraints are available only on the Amazon Web Services (AWS) cloud platform.
>
> All other MEMORY\_\* resource constraint sizes are generally available and are available for all cloud platforms.
>
> Specifies the memory and CPU architecture for [Snowpark-optimized warehouses](/user-guide/warehouses-snowpark-optimized),
> or generation 1 or [generation 2 capabilities for standard warehouses](/user-guide/warehouses-gen2).
>
> The following table includes the valid values for the property, available memory, CPU architecture, and the minimum warehouse
> size required for the `resource_constraint` setting.
> For more information about regions and cloud service providers where generation 2 standard warehouses
> are available, see [Snowflake generation 2 standard warehouses](/user-guide/warehouses-gen2).
>
> > Valid values:
> >
> > | Value | Memory (up to) | CPU architecture | Min warehouse size required | Max warehouse size |
> > | --- | --- | --- | --- | --- |
> > | `STANDARD_GEN_1` | 16 GB | Standard | XSMALL | X6LARGE |
> > | `STANDARD_GEN_2` | 16 GB | Standard (generation 2) | XSMALL | X4LARGE |
> > | `MEMORY_1X` | 16 GB | Standard | XSMALL | X4LARGE |
> > | `MEMORY_1X_x86` | 16 GB | x86 | XSMALL | X4LARGE |
> > | `MEMORY_16X` | 256 GB | Standard | MEDIUM | X6LARGE |
> > | `MEMORY_16X_x86` | 256 GB | x86 | MEDIUM | X4LARGE |
> > | `MEMORY_64X` | 1 TB | Standard | LARGE | X4LARGE |
> > | `MEMORY_64X_x86` | 1 TB | x86 | LARGE | X4LARGE |
> >
> > Expand
> >
> > Show lessSee more
> >
> > Default value:
> > :   `MEMORY_16X` for Snowpark-optimized warehouses. For standard warehouses, the default depends on
> >     Gen2 support for your cloud service provider region and whether your organization was created after
> >     Gen2 support became available in that region. For more information, see
> >     [Default value for the GENERATION for standard warehouses](/user-guide/warehouses-gen2#label-gen-2-standard-warehouses-default-generation).
> >
> > Tip
> >
> > For standard warehouses, consider using the GENERATION parameter instead of STANDARD\_GEN\_1 and STANDARD\_GEN\_2 values.
> > The GENERATION parameter provides a simpler way to specify the warehouse generation.
> > Specify `GENERATION = '2'` or `GENERATION = '1'`. The quotes are required around the
> > generation number.

`MAX_CLUSTER_COUNT = num`
:   Specifies the maximum number of clusters for a multi-cluster warehouse. For a single-cluster warehouse, this value is always `1`.

    Valid values:
    :   `1` to an upper limit that varies depending on warehouse size.

        Note that specifying a value greater than `1` indicates the warehouse is a multi-cluster warehouse; however, the value can only be set
        to a higher value in [Snowflake Enterprise Edition](/user-guide/intro-editions) (or higher).

        For more information, including the upper limit for each warehouse size, see [Multi-cluster warehouses](/user-guide/warehouses-multicluster).

    Default:
    :   `1` (single-cluster warehouse)

    Tip

    For Snowflake Enterprise Edition (or higher), we recommend always setting the value greater than `1` to help maintain
    high-availability and optimal performance of a multi-cluster warehouse. This also helps ensure continuity in the unlikely event that a
    cluster fails.

`MIN_CLUSTER_COUNT = num`
:   Specifies the minimum number of clusters for a multi-cluster warehouse (only applies to multi-cluster warehouses).

    Valid values:
    :   `1` to the value of `MAX_CLUSTER_COUNT`. The upper limit for `MAX_CLUSTER_COUNT` varies depending on the warehouse size.

        `MIN_CLUSTER_COUNT` must be equal to or less than `MAX_CLUSTER_COUNT`:

        - If both parameters are equal, the warehouse runs in Maximized mode.
        - If `MIN_CLUSTER_COUNT` is less than `MAX_CLUSTER_COUNT`, the warehouse runs in Auto-scale mode.

        For more information, including the upper limit for each warehouse size, see [Multi-cluster warehouses](/user-guide/warehouses-multicluster).

    Default:
    :   `1`

`SCALING_POLICY = { STANDARD | ECONOMY }`
:   Specifies the policy for automatically starting and shutting down clusters in a multi-cluster warehouse running in Auto-scale mode.

    Valid values:
    :   - `STANDARD`: Minimizes queuing by starting clusters.
        - `ECONOMY`: Conserves credits by favoring keeping running clusters fully loaded.

        For a more detailed description, see [Setting the scaling policy for a multi-cluster warehouse](/user-guide/warehouses-multicluster#label-mcw-scaling-policies).

    Default:
    :   `STANDARD`

`AUTO_SUSPEND = { num | NULL }`
:   Specifies the number of seconds of inactivity after which a warehouse is automatically suspended.

    Valid values:
    :   Any integer `0` or greater, or `NULL`:

        - The background process that suspends a warehouse runs approximately every 30 seconds and, therefore, the setting for
          this property isn’t intended for enabling precise control over warehouse suspension.
        - Setting a value less than 30, or a value that isn’t a multiple of 30, is allowed but might not result in the expected
          behavior due to the 30-second poll interval for warehouse suspension.
        - Setting a `0` or `NULL` value means the warehouse never suspends.

    Default:
    :   `600` (the warehouse suspends automatically after 10 minutes of inactivity)

    Important

    Setting `AUTO_SUSPEND` to `0` or `NULL` is not recommended, unless your query workloads require a continually
    running warehouse. Note that this can result in significant consumption of credits (and corresponding charges), particularly for
    larger warehouses.

`AUTO_RESUME = { TRUE | FALSE }`
:   Specifies whether to automatically resume a warehouse when a SQL statement (for example, query) is submitted to it.

    Valid values:
    :   - `TRUE`: The warehouse resumes when a new query is submitted.
        - `FALSE`: The warehouse only resumes when explicitly resumed using [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) or through the Snowflake web
          interface.

    Default:
    :   `TRUE` (the warehouse resumes automatically when a SQL statement is submitted to it)

`INITIALLY_SUSPENDED = { TRUE | FALSE }`
:   Specifies whether the warehouse is created initially in the ‘Suspended’ state.

    Valid values:
    :   - `TRUE`: The warehouse is created, but suspended.
        - `FALSE`: The warehouse starts running after it is created.

    Default:
    :   `FALSE`

`RESOURCE_MONITOR = monitor_name`
:   Specifies the name of a resource monitor that is explicitly assigned to the warehouse. When a resource monitor is explicitly assigned
    to a warehouse, the monitor controls the monthly credits used by the warehouse (and all other warehouses to which the monitor is
    assigned).

    Valid values:
    :   Any existing resource monitor.

        For more details, see [Working with resource monitors](/user-guide/resource-monitors).

    Default:
    :   No value (no resource monitor assigned to the warehouse)

    Tip

    To view all resource monitors and their identifiers, use the [SHOW RESOURCE MONITORS](/sql-reference/sql/show-resource-monitors) command.

`COMMENT = 'string_literal'`
:   Specifies a comment for the warehouse.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

### Query acceleration properties

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

`ENABLE_QUERY_ACCELERATION = { TRUE | FALSE }`
:   Specifies whether to enable the [query acceleration service](/user-guide/query-acceleration-service) for queries that rely on this
    warehouse for compute resources.

    > Valid values:
    > :   - `TRUE` Enables Query Acceleration
    >     - `FALSE` Disables Query Acceleration
    >
    > Default:
    > :   - `FALSE` for single-cluster Gen1 warehouses
    >     - `TRUE` for [Gen2](/user-guide/warehouses-gen2) and [multi-cluster](/user-guide/warehouses-multicluster) warehouses

`QUERY_ACCELERATION_MAX_SCALE_FACTOR = num`
> Specifies the maximum scale factor for leasing compute resources for query acceleration. The scale factor is used as a multiplier based
> on [warehouse size](/user-guide/warehouses-overview#label-warehouse-size).
>
> Setting the QUERY\_ACCELERATION\_MAX\_SCALE\_FACTOR to 0 eliminates the limit and allows queries to lease as many resources as necessary and
> as available to service the query.
>
> Regardless of the QUERY\_ACCELERATION\_MAX\_SCALE\_FACTOR value, the amount of available compute resources for query acceleration is bound by
> the available resources in the service and the number of other concurrent requests. For more details, refer to
> [Adjusting the scale factor](/user-guide/query-acceleration-service#label-query-acceleration-scale-factor).
>
> Valid values:
> :   `0` to `100`
>
> Default:
> :   `8`, or `2` when Snowflake automatically enables query acceleration for [Gen2](/user-guide/warehouses-gen2) or
>     [multi-cluster](/user-guide/warehouses-multicluster) warehouses at creation time

## Optional parameters (`objectParams`)

`MAX_CONCURRENCY_LEVEL = num`
:   Object parameter that specifies the concurrency level for SQL statements (that is, queries and DML) executed by a warehouse cluster.

    For a detailed description of this parameter, see [MAX\_CONCURRENCY\_LEVEL](/sql-reference/parameters#label-max-concurrency-level).

`STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = num`
:   Object parameter that specifies the time, in seconds, a SQL statement (query, DDL, DML, and so on) can be queued on a warehouse before it is
    canceled by the system.

    For a detailed description of this parameter, see [STATEMENT\_QUEUED\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-queued-timeout-in-seconds).

`STATEMENT_TIMEOUT_IN_SECONDS = num`
:   Object parameter that specifies the time, in seconds, after which a running SQL statement (query, DDL, DML, and so on) is canceled by the system.

    For a detailed description of this parameter, see [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE WAREHOUSE | Account | Only the SYSADMIN role, or a higher role, has this privilege by default. The privilege can be granted to additional roles as needed. |
| OWNERSHIP | Warehouse | Required to execute a [CREATE OR ALTER WAREHOUSE](#label-create-or-alter-warehouse-syntax) statement for an *existing* warehouse.  OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## General usage notes

- Creating a virtual warehouse automatically sets it as the warehouse in use for the current session (equivalent to using the
  [USE WAREHOUSE](/sql-reference/sql/use-warehouse) command for the warehouse).

  To change the warehouse in use for the current session, execute an explicit USE WAREHOUSE statement after the
  CREATE WAREHOUSE statement. For example, create warehouse `my_wh` but continue to use the current warehouse, not `my_wh`,
  to execute additional statements:

  Copy code

  ```
  SET current_wh_name = (SELECT CURRENT_WAREHOUSE());

  CREATE OR REPLACE WAREHOUSE my_wh
    WAREHOUSE_SIZE = 'XSMALL';

  USE WAREHOUSE IDENTIFIER($current_wh_name);
  ```
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- Using `OR REPLACE` is the equivalent of using [DROP WAREHOUSE](/sql-reference/sql/drop-warehouse) on the existing warehouse and then
  creating a new warehouse with the same name.

  CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

  Any queries running on the dropped warehouse are aborted.
- The `OR REPLACE` and `IF NOT EXISTS` clauses are mutually exclusive. They can’t both be used in the same statement.
- Initial creation and resumption of a Snowpark-optimized virtual warehouse may take longer than standard warehouses.

## CREATE OR ALTER WAREHOUSE usage notes

**Limitations**

- All limitations of the [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) command apply.
- The INITIALLY\_SUSPENDED property can’t be altered (SET or UNSET).

**Warehouse parameters and properties**

- The absence of a property or parameter that was previously set in the modified warehouse definition results in unsetting it.
- Unsetting an explicit parameter value results in setting it to the default parameter value.

**Data governance**

- Setting or unsetting a tag or policy on a warehouse using a CREATE OR ALTER WAREHOUSE statement is *not* supported.
- Existing policies or tags can’t be altered by a CREATE OR ALTER WAREHOUSE statement and remain unchanged.

## Billing and pricing

For information on Snowpark-optimized warehouse credit consumption, see
`Table 1` in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Examples

### Basic examples

Create an X-Large warehouse:

> Copy code
>
> ```
> CREATE OR REPLACE WAREHOUSE my_wh WITH WAREHOUSE_SIZE = 'X-LARGE';
> ```

Create a Large warehouse in a suspended state:

> Copy code
>
> ```
> CREATE OR REPLACE WAREHOUSE my_wh WAREHOUSE_SIZE = LARGE INITIALLY_SUSPENDED = TRUE;
> ```

Create an X-Large Snowpark-optimized warehouse named `so_warehouse` with 256 GB memory for
Snowpark workloads that require x86 Python:

Copy code

```
CREATE WAREHOUSE so_warehouse WITH
  WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED'
  WAREHOUSE_SIZE = XLARGE
  RESOURCE_CONSTRAINT = 'MEMORY_16X_x86';
```

Create a Large generation 2 standard warehouse:

Copy code

```
CREATE WAREHOUSE gen2_wh WITH
  WAREHOUSE_SIZE = LARGE
  GENERATION = '2';
```

### CREATE OR ALTER WAREHOUSE examples

#### Create a simple warehouse

The following example shows how to use CREATE OR ALTER WAREHOUSE to create a Snowpark-optimized
warehouse, then modify its AUTO\_RESUME setting.

Copy code

```
CREATE OR ALTER WAREHOUSE so_warehouse
  WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED'
  WAREHOUSE_SIZE = 'X-LARGE'
  RESOURCE_CONSTRAINT = 'MEMORY_16X_x86'
  AUTO_RESUME = TRUE
  COMMENT = 'Snowpark warehouse for ingestion';

CREATE OR ALTER WAREHOUSE so_warehouse
  WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED'
  WAREHOUSE_SIZE = 'X-LARGE'
  RESOURCE_CONSTRAINT = 'MEMORY_16X_x86'
  AUTO_RESUME = FALSE
  COMMENT = 'Snowpark warehouse for ingestion (disabled for auto-resume)';
```

#### Create a Gen1 warehouse and alter it to Gen2

The following example demonstrates how CREATE OR ALTER WAREHOUSE works with the GENERATION
parameter, first creating a warehouse with generation 1 resources, then altering it to use
generation 2 resources.

Copy code

```
-- Create a new warehouse with GENERATION = '1'
CREATE OR ALTER WAREHOUSE test_gen_warehouse
  WITH WAREHOUSE_SIZE = XSMALL
    GENERATION = '1'
    AUTO_SUSPEND = 60
    INITIALLY_SUSPENDED = TRUE;

-- Verify that it was created
SHOW WAREHOUSES LIKE 'test_gen_warehouse'
  ->> SELECT "name", "resource_constraint" FROM $1;

-- Alter it to GENERATION = '2'
CREATE OR ALTER WAREHOUSE test_gen_warehouse
  WITH WAREHOUSE_SIZE = SMALL
    GENERATION = '2'
    AUTO_SUSPEND = 120;

-- Verify that it was altered
SHOW WAREHOUSES LIKE 'test_gen_warehouse'
  ->> SELECT "name", "resource_constraint" FROM $1;

-- Clean up when done
DROP WAREHOUSE test_gen_warehouse;
```
