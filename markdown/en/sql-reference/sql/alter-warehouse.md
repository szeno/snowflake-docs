# ALTER WAREHOUSE

Suspends or resumes a [virtual warehouse](/user-guide/warehouses-overview),
or aborts all queries (and other SQL statements) for a warehouse. Can also be used to rename or
set/unset the properties for a warehouse.

See also:
:   [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse), [DESCRIBE WAREHOUSE](/sql-reference/sql/desc-warehouse), [DROP WAREHOUSE](/sql-reference/sql/drop-warehouse), [SHOW WAREHOUSES](/sql-reference/sql/show-warehouses)

## Syntax

Copy code

```
ALTER WAREHOUSE [ IF EXISTS ] [ <name> ] { SUSPEND | RESUME [ IF SUSPENDED ] }

ALTER WAREHOUSE [ IF EXISTS ] <name> { ENABLE | DISABLE }

ALTER WAREHOUSE [ IF EXISTS ] [ <name> ] ABORT ALL QUERIES

ALTER WAREHOUSE [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER WAREHOUSE [ IF EXISTS ] <name> SET [ objectProperties ]
                                         [ objectParams ]

ALTER WAREHOUSE [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER WAREHOUSE [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER WAREHOUSE [ IF EXISTS ] <name> UNSET { <property_name> | <param_name> } [ , ... ]

ALTER WAREHOUSE [ IF EXISTS ] <name> UNSET DCM PROJECT

ALTER WAREHOUSE [ IF EXISTS ] <name> ADD TABLES ( <table_name> [ , <table_name> ... ] )

ALTER WAREHOUSE [ IF EXISTS ] <name> DROP TABLES ( <table_name> [ , <table_name> ... ] )
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
>   WAIT_FOR_COMPLETION = { TRUE | FALSE }
>   MAX_CLUSTER_COUNT = <num>
>   MIN_CLUSTER_COUNT = <num>
>   SCALING_POLICY = { STANDARD | ECONOMY }
>   AUTO_SUSPEND = { <num> | NULL }
>   AUTO_RESUME = { TRUE | FALSE }
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

## Properties/parameters

`name`
:   Specifies the identifier for the warehouse to alter. If the identifier contains spaces or special characters, the entire string must be enclosed
    in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Note

    A warehouse identifier is required or optional depending on the following:

    - When resuming/suspending a warehouse or aborting queries for a warehouse, if a warehouse is currently in use for the session, the identifier
      can be omitted.
    - When renaming a warehouse or performing any other operations on a warehouse, the identifier must be specified.

`{ SUSPEND | RESUME [ IF SUSPENDED ] }`
:   Specifies the action to perform on the warehouse:

    - `SUSPEND` removes all compute nodes from a warehouse and puts the warehouse into a ‘Suspended’ state.
    - `RESUME [ IF SUSPENDED ]` brings a suspended warehouse to a usable ‘Running’ state by provisioning compute resources.

      The optional `IF SUSPENDED` clause specifies whether the ALTER WAREHOUSE command completes successfully when resuming a warehouse that
      is already running:

      - If omitted, the command fails and returns an error if the warehouse is already running.
      - If specified, the command completes successfully regardless of whether the warehouse is running.

`{ ENABLE | DISABLE }`
:   Enables or disables an [Adaptive Warehouse](/user-guide/warehouses-adaptive). Applies only when
    `WAREHOUSE_TYPE` is `ADAPTIVE`.

    - `ENABLE` allows the warehouse to accept new jobs for execution.
    - `DISABLE` rejects new jobs submitted to the warehouse. Queries already running on the warehouse
      can continue to completion.

    For more information, see [Enable or disable an Adaptive Warehouse](/user-guide/warehouses-adaptive#label-adaptive-warehouse-enable-disable).

`ABORT ALL QUERIES`
:   Aborts all the queries currently running or queued on the warehouse.

`RENAME TO new_name`
:   Specifies a new identifier for the warehouse; must be unique for your account.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Specifies one or more properties/parameters to set for the warehouse (separated by blank spaces, commas, or new lines).

    Note

    Only some properties apply to an [interactive warehouse](/user-guide/interactive).
    For the list of properties that you can use, see [CREATE INTERACTIVE WAREHOUSE](/sql-reference/sql/create-interactive-warehouse).

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

    `WAREHOUSE_SIZE = string_constant`
    :   Specifies the size of the virtual warehouse. The size determines the amount of compute resources in each cluster and, therefore,
        the number of credits consumed while the warehouse is running.

        For more information, see [Resizing a warehouse](/user-guide/warehouses-tasks#label-resizing-a-warehouse).

        Valid values:
        :   - `XSMALL`, `'X-SMALL'`
            - `SMALL`
            - `MEDIUM`
            - `LARGE`
            - `XLARGE`, `'X-LARGE'`
            - `XXLARGE`, `X2LARGE`, `'2X-LARGE'`
            - `XXXLARGE`, `X3LARGE`, `'3X-LARGE'`
            - `X4LARGE`, `'4X-LARGE'`
            - `X5LARGE`, `'5X-LARGE'`
            - `X6LARGE`, `'6X-LARGE'`

        Default:
        :   `XSMALL`

        Note

        - The default size for Snowpark-optimized warehouses is MEDIUM.
        - X5LARGE and X6LARGE sizes for Snowpark-optimized warehouses are only supported with the MEMORY\_16X resource constraint.
        - X5LARGE and X6LARGE sizes aren’t supported for standard warehouses that use the STANDARD\_GEN\_2 resource constraint.
        - To use a value that contains a hyphen (for example, `'2X-LARGE'`), you must enclose the value in single quotes, as shown.
        - To block the immediate return of the ALTER WAREHOUSE command until the resize is complete, add the
          [WAIT\_FOR\_COMPLETION](/sql-reference/sql/alter-warehouse#label-alter-warehouse-wait-for-completion) parameter.
        - The upper limit for the MAX\_CLUSTER\_COUNT property depends on the warehouse size. When you change WAREHOUSE\_SIZE
          to a value higher than `MEDIUM`, you might need to reduce MAX\_CLUSTER\_COUNT at the same time. For the upper limit
          on MAX\_CLUSTER\_COUNT for each warehouse size, see [Upper limit on number of clusters for a multi-cluster warehouse](/user-guide/warehouses-multicluster#label-max-cluster-size-limit-per-warehouse-size).
        - Larger warehouse sizes 5X-Large and 6X-Large are generally available in all Amazon Web Services (AWS) and Microsoft Azure regions.

          Larger warehouse sizes are in preview in US Government regions (requires FIPS support on ARM).

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
        - For standard warehouses, the default depends on Gen2 support for your cloud service provider region and whether your organization was created after Gen2 support became available in that region. For more information, see [Default value for the GENERATION for standard warehouses](/user-guide/warehouses-gen2#label-gen-2-standard-warehouses-default-generation).
        - GENERATION applies only to standard warehouses (WAREHOUSE\_TYPE = STANDARD).
        - When both GENERATION and RESOURCE\_CONSTRAINT are specified, any mismatch results in an error.
        - You can’t use GENERATION with Snowpark-optimized warehouses or memory-based resource constraints.

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

    `WAIT_FOR_COMPLETION = { TRUE | FALSE }`
    :   When resizing a warehouse, you can use this parameter to block the return of the ALTER WAREHOUSE command until the resize has finished
        provisioning all its compute resources. Blocking the return of the command when resizing to a larger warehouse serves to notify you
        that your compute resources have been fully provisioned and the warehouse is now ready to execute queries using all the new resources.

        Valid values:
        :   - `TRUE`: The ALTER WAREHOUSE command will block until the warehouse resize completes.
            - `FALSE`: The ALTER WAREHOUSE command returns immediately, before the warehouse resize completes.

        Default:
        :   FALSE

        Note

        - The value of this parameter isn’t persisted and must be set to TRUE on every execution if you want the warehouse resizing to
          complete before this command returns.
        - If set to `TRUE` and you abort the ALTER WAREHOUSE command, only the waiting is aborted and the warehouse resize will go
          through. To resize the warehouse back to its original size, you will need to execute another ALTER WAREHOUSE command.
        - This parameter must be used with the WAREHOUSE\_SIZE parameter, otherwise an exception will be thrown.

    `MAX_CLUSTER_COUNT = num`
    :   Specifies the maximum number of clusters for a multi-cluster warehouse. For a single-cluster warehouse, this value is always `1`.

        Valid values:
        :   `1` to an upper limit that varies depending on warehouse size.

            Note that specifying a value greater than `1` indicates the warehouse is a multi-cluster warehouse; however, the value can
            only be set to a higher value in [Snowflake Enterprise Edition](/user-guide/intro-editions) (or higher).

            - The upper limit for the MAX\_CLUSTER\_COUNT property depends on the warehouse size. When you change WAREHOUSE\_SIZE
              to a value higher than MEDIUM, you might need to reduce MAX\_CLUSTER\_COUNT at the same time. For the upper limit
              on MAX\_CLUSTER\_COUNT for each warehouse size, see [Upper limit on number of clusters for a multi-cluster warehouse](/user-guide/warehouses-multicluster#label-max-cluster-size-limit-per-warehouse-size).

            For more information about multi-cluster warehouses, see [Multi-cluster warehouses](/user-guide/warehouses-multicluster).

        Default:
        :   `1` (single-cluster warehouse)

        Tip

        For Snowflake Enterprise Edition (or higher), we recommend always setting the value greater than `1` to help maintain
        high-availability and optimal performance of the (multi-cluster) warehouse. This also helps ensure continuity in the unlikely event
        that a cluster fails.

    `MIN_CLUSTER_COUNT = num`
    :   Specifies the minimum number of clusters for a multi-cluster warehouse.

        Valid values:
        :   `1` to the value of MAX\_CLUSTER\_COUNT. The upper limit for MAX\_CLUSTER\_COUNT varies depending on the warehouse size.

            MIN\_CLUSTER\_COUNT must be equal to or less than MAX\_CLUSTER\_COUNT:

            - If both parameters are equal, the warehouse runs in Maximized mode.
            - If MIN\_CLUSTER\_COUNT is less than MAX\_CLUSTER\_COUNT, the warehouse runs in Auto-scale mode.

            For more information, including the upper limit for each warehouse size, see [Multi-cluster warehouses](/user-guide/warehouses-multicluster).

        Default:
        :   `1`

    `SCALING_POLICY = { STANDARD | ECONOMY }`
    :   Object parameter that specifies the policy for automatically starting and shutting down clusters in a multi-cluster warehouse
        running in Auto-scale mode.

        For a detailed description of this parameter, see [Setting the scaling policy for a multi-cluster warehouse](/user-guide/warehouses-multicluster#label-mcw-scaling-policies).

    `AUTO_SUSPEND = { num | NULL }`
    :   Specifies the number of seconds of inactivity after which a warehouse is automatically suspended.

        Valid values:
        :   Any integer `0` or greater, or `NULL`:

            - The background process that suspends a warehouse runs approximately every 30 seconds and therefore, the setting for
              this property isn’t intended for enabling precise control over warehouse suspension.
            - Setting a value less than 30, or a value that isn’t a multiple of 30, is allowed but might not result in the expected
              behavior due to the 30 second poll interval for warehouse suspension.
            - Setting a `0` or `NULL` value means the warehouse never suspends.

        Default:
        :   `600` (the warehouse suspends automatically after 10 minutes of inactivity)

        Important

        Setting `AUTO_SUSPEND` to `0` or `NULL` is not recommended, unless your query workloads require a continually running
        warehouse. Note that this can result in significant consumption of credits (and corresponding charges), particularly for larger warehouses.

        For more details, see [Warehouse considerations](/user-guide/warehouses-considerations).

    `AUTO_RESUME = { TRUE | FALSE }`
    :   Specifies whether to automatically resume a warehouse when a SQL statement (for example, query) is submitted to it. If `FALSE`, the warehouse
        only starts again when explicitly resumed using [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) or through the Snowflake web interface.

        Valid values:
        :   - `TRUE`: The warehouse resumes when a new query is submitted.
            - `FALSE`: The warehouse only resumes when explicitly resumed using [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) or through the Snowflake web interface.

        Default:
        :   `TRUE` (the warehouse resumes automatically when a SQL statement is submitted to it)

    `INITIALLY_SUSPENDED = { TRUE | FALSE }`
    :   Not applicable when altering a warehouse

    `RESOURCE_MONITOR = monitor_name`
    :   Specifies the identifier of a resource monitor that is explicitly assigned to the warehouse. When a resource monitor is explicitly assigned
        to a warehouse, the monitor controls the monthly credits used by the warehouse (and all other warehouses to which the monitor is assigned).

        Valid values:
        :   Any existing resource monitor.

            For more details, see [Working with resource monitors](/user-guide/resource-monitors).

        Default:
        :   No value (no resource monitor assigned to the warehouse)

        Tip

        To view all resource monitors and their identifiers, use the [SHOW RESOURCE MONITORS](/sql-reference/sql/show-resource-monitors) command.

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the warehouse.

    `MAX_CONCURRENCY_LEVEL = num`
    :   Object parameter that specifies the concurrency level for SQL statements (that is, queries and DML) executed by a warehouse cluster. When
        the level is reached:

        > - For a single-cluster warehouse or a multi-cluster warehouse (in Maximized mode), additional statements are queued until resources
        >   are available.
        > - For a multi-cluster warehouse (in Auto-scale mode), additional clusters are started.

        This parameter can be used in conjunction with `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS` to ensure a warehouse is never backlogged.

        For a detailed description of this parameter, see [MAX\_CONCURRENCY\_LEVEL](/sql-reference/parameters#label-max-concurrency-level).

    `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = num`
    :   Object parameter that specifies the time, in seconds, a SQL statement (query, DDL, DML, and so on) can be queued on a warehouse before it is
        canceled by the system.

        This parameter can be used in conjunction with `MAX_CONCURRENCY_LEVEL` to ensure a warehouse is never backlogged.

        For a detailed description of this parameter, see [STATEMENT\_QUEUED\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-queued-timeout-in-seconds).

    `STATEMENT_TIMEOUT_IN_SECONDS = num`
    :   Object parameter that specifies the time, in seconds, after which a running SQL statement (query, DDL, DML, and so on) is canceled by the system.

        For a detailed description of this parameter, see [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds).

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `ENABLE_QUERY_ACCELERATION = { TRUE | FALSE }`
    :   Specifies whether to enable the [query acceleration service](/user-guide/query-acceleration-service) for queries that rely on
        this warehouse for compute resources.

        > [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Enterprise Edition Feature](/user-guide/intro-editions)
        >
        > Query acceleration service requires Enterprise Edition (or higher).
        > To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
        >
        > Valid values:
        > :   - `TRUE` Enables Query Acceleration
        >     - `FALSE` Disables Query Acceleration
        >
        > Default:
        > :   Unchanged. The warehouse retains its current setting if you omit this parameter in the ALTER WAREHOUSE statement.
        >
        >     For defaults when you **create** a warehouse, see the Query acceleration properties in
        >     [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse).

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

`UNSET ...`
:   > Specifies one (or more) properties and/or parameters to unset for the database, which resets them to the defaults:
    >
    > - `property_name`
    > - `param_name`
    >   - `TAG tag_name [ , tag_name ... ]`
    >
    > You can reset multiple properties/parameters with a single ALTER statement; however, each property/parameter must be separated by
    > a comma. Also, when resetting a property/parameter, you only specify the name; no value is required.

    Note

    `UNSET` can be used to unset all the properties and parameters for a warehouse, except `WAREHOUSE_SIZE`, which can only
    be changed using `SET`.

`UNSET DCM PROJECT`

> Detaches the warehouse from the [DCM project](/user-guide/dcm-projects/dcm-projects-overview) that currently manages it.
> The command removes the association between the warehouse and the DCM project without dropping the warehouse. See [Detach objects from a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-detach-object) for more information.

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.
Currently, this feature is only available on Amazon Web Services (AWS).

`ADD TABLES ( table_name[, ...] )`
:   Associates one or more [interactive tables with an interactive warehouse](/user-guide/interactive). This action initiates the cache-warming process for the specified
    tables.

    Note

    - This clause only applies to interactive warehouses created with the INTERACTIVE keyword.
    - If an interactive table is already associated with the warehouse, the command succeeds but has no effect.
    - An interactive table can be associated with multiple interactive warehouses.
    - Cache warming may take significant time depending on the size of the data.

    `table_name`
    :   Specifies the identifier for an interactive table to associate with the warehouse. You can
        specify multiple table names separated by commas.

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.
Currently, this feature is only available on Amazon Web Services (AWS).

`DROP TABLES ( table_name[, ...] )`
:   Removes the association between one or more [interactive tables and an interactive warehouse](/user-guide/interactive). This action stops using the cache for the specified
    tables, but does not drop the tables themselves.

    Note

    - This clause only applies to interactive warehouses created with the INTERACTIVE keyword.
    - The interactive tables continue to exist after this operation. This clause does not
      perform a DROP TABLE operation.

    `table_name`
    :   Specifies the identifier for an interactive table to disassociate from the warehouse. You can
        specify multiple table names separated by commas.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY | Tag | Enables setting a tag on a warehouse. |
| MANAGE ATTACHED TABLES | Warehouse | Enables the ADD TABLES and DROP TABLES clauses on an interactive warehouse to manage which tables are cached by the warehouse. Does not grant other warehouse modification operations. The MODIFY privilege also authorizes these operations. Applies to interactive warehouses only. |
| MODIFY | Warehouse | Enables altering any properties of a warehouse, including changing its size. Required to assign a warehouse to a resource monitor. Only the ACCOUNTADMIN role can assign warehouses to resource monitors. |
| MONITOR | Warehouse | Enables viewing current and past queries executed on a warehouse as well as usage statistics on that warehouse. |
| OPERATE | Warehouse | Enables changing the state of a warehouse (stop, start, suspend, resume), and enables viewing current and past queries executed on a warehouse, and aborting any executing queries. |
| USAGE | Warehouse | Enables using a virtual warehouse and, as a result, executing queries on the warehouse. If the warehouse is configured to auto-resume when a SQL statement (for example, query) is submitted to it, the warehouse resumes automatically and executes the statement. |

Expand

Show lessSee more

Tip

The granting of the global MANAGE WAREHOUSES privilege is equivalent to granting the MODIFY, MONITOR, and OPERATE
privileges on all warehouses in an account. You can grant this
privilege to a role whose purpose includes managing a warehouse to simplify your Snowflake access control management.

For details, refer to [Delegating warehouse management](/user-guide/warehouses-tasks#label-grant-manage-warehouses-privilege).

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- A warehouse does not need to be suspended to set or change any of its properties. You can change the warehouse type
  and resource constraint properties while the warehouse is running.
- When the warehouse size is changed, the change doesn’t impact any statements, including queries, that are currently executing. Once the
  statements complete, and the compute resources are fully provisioned, the new size is used for all subsequent statements.
- Suspending a warehouse does not abort any queries being processed by the warehouse at the time it is suspended. Instead, the
  warehouse completes the queries, then shuts down the compute resources used to process the queries. During this time period, the warehouse
  is in *quiescing* mode. When all the compute resources are shut down, the warehouse’s status changes to Suspended.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- Resuming a Snowpark-optimized virtual warehouse may take longer than for standard warehouses.
- Snowpark-optimized warehouses don’t support [Query Acceleration](/user-guide/query-acceleration-service).
- Specifying the `IF EXISTS` clause requires the role in use or a role in the active role hierarchy to have the appropriate
  [warehouse privileges](/user-guide/security-access-control-privileges#label-warehouse-privileges) on the warehouse.
- The ADD TABLES and DROP TABLES clauses only apply to interactive warehouses created with the
  INTERACTIVE keyword. These clauses are not available for standard or Snowpark-optimized
  warehouses. To run these clauses, a role must have the MANAGE ATTACHED TABLES or MODIFY privilege
  on the warehouse, or the MANAGE WAREHOUSES privilege on the account.

## Billing and pricing

For information on Snowpark-optimized warehouse credit consumption, see
`Table 1` in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

For information about billing and pricing considerations for interactive warehouses, see
[Cost and billing considerations](/user-guide/interactive#label-interactive-cost).

Tip

For information about cost implications of changing the RESOURCE\_CONSTRAINT property, see
[considerations for changing RESOURCE\_CONSTRAINT while a warehouse is running or suspended](/user-guide/warehouses-gen2#label-gen-2-standard-warehouses-altering).

## Examples

Rename warehouse `wh1` to `wh2`:

Copy code

```
ALTER WAREHOUSE IF EXISTS wh1 RENAME TO wh2;
```

Resume a warehouse named `my_wh` and then change the size of the warehouse while it is running:

Copy code

```
ALTER WAREHOUSE my_wh RESUME;

ALTER WAREHOUSE my_wh SET warehouse_size=MEDIUM;
```

Modify the memory resources to 256 GB and set the CPU architecture to x86 for Snowpark-optimized warehouse `so_warehouse`:

Copy code

```
ALTER WAREHOUSE so_warehouse SET
  RESOURCE_CONSTRAINT = 'MEMORY_16X_x86';
```

Change a warehouse to use generation 2 compute resources:

Copy code

```
ALTER WAREHOUSE my_wh SET GENERATION = '2';
```

Associate interactive tables with an interactive warehouse:

Copy code

```
ALTER WAREHOUSE interactive_demo ADD TABLES (orders, customers);
```

Remove interactive tables from an interactive warehouse:

Copy code

```
ALTER WAREHOUSE interactive_demo DROP TABLES (orders, customers);
```
