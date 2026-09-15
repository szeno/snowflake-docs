# CREATE DYNAMIC TABLE

Creates a [dynamic table](/user-guide/dynamic-tables/overview), based on a specified query.

This command supports the following variants:

- [CREATE OR ALTER DYNAMIC TABLE](#label-create-or-alter-dt-syntax): Creates a dynamic table if it doesn’t exist or alters an existing dynamic table.
- [CREATE DYNAMIC TABLE FROM BACKUP SET](#label-create-dt-backup-syntax): Restores a dynamic table from a backup.
- [CREATE DYNAMIC TABLE … CLONE](#label-create-dt-clone-syntax): Creates a clone of an existing dynamic table.
- [CREATE DYNAMIC ICEBERG TABLE](#label-create-dt-iceberg-syntax): Creates a dynamic Apache Iceberg™ table.

See also:
:   [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table), [DESCRIBE DYNAMIC TABLE](/sql-reference/sql/desc-dynamic-table), [DROP DYNAMIC TABLE](/sql-reference/sql/drop-dynamic-table), [SHOW DYNAMIC TABLES](/sql-reference/sql/show-dynamic-tables)

Note

Frozen regions were previously named immutability constraints, and the `FROZEN WHERE` clause previously used the syntax `IMMUTABLE WHERE`. The legacy `IMMUTABLE WHERE` syntax continues to be supported, and `SHOW DYNAMIC TABLES` still uses the `immutable_where` column.

## Syntax

Copy code

```
CREATE [ OR REPLACE ] [ TRANSIENT ] DYNAMIC TABLE [ IF NOT EXISTS ] <name> (
    -- Column definition
    <col_name> <col_type>
      [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col_name> , <cond_col1> , ... ) ] ]
      [ [ WITH ] PROJECTION POLICY <policy_name> ]
      [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
      [ COMMENT '<string_literal>' ]
      [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]

    -- Additional column definitions
    [ , <col_name> <col_type> [ ... ] ]

  )
  TARGET_LAG = { '<num> { seconds | minutes | hours | days }' | DOWNSTREAM }
  [ SCHEDULER = DISABLE | ENABLE ]
  WAREHOUSE = <warehouse_name>
  [ INITIALIZATION_WAREHOUSE = <warehouse_name> ]
  [ REFRESH_MODE = { AUTO | FULL | INCREMENTAL | ADAPTIVE | CUSTOM_INCREMENTAL } ]
  [ INITIALIZE = { ON_CREATE | ON_SCHEDULE } ]
  [ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ COMMENT = '<string_literal>' ]
  [ COPY GRANTS ]
  [ COPY TAGS ]
  [ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ [ WITH ] AGGREGATION POLICY <policy_name> [ ENTITY KEY ( <col_name> [ , <col_name> ... ] ) ] ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ REQUIRE USER ]
  [ FROZEN WHERE ( <expr> ) ]
  [ [ WITH ] STORAGE LIFECYCLE POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
  [ BACKFILL FROM <table_name> ]
  [ START AT ({ STREAM => '<stream_name>' | TIMESTAMP => <timestamp> | STATEMENT => <query_id> | OFFSET => -<seconds> }) ]  -- Requires CUSTOM_INCREMENTAL + BACKFILL FROM
  [ EXECUTE AS USER <user_name>
    [ USE SECONDARY ROLES { ALL | NONE | <role> [ , ... ] } ]
  ]
  [ ROW_TIMESTAMP = { TRUE | FALSE } ]
  { AS <query> | REFRESH USING ( <dml_statement> ) }
```

## Variant syntax

### CREATE OR ALTER DYNAMIC TABLE

Copy code

```
CREATE OR ALTER [ TRANSIENT ] DYNAMIC TABLE <name> (
  -- Column definition
  <col_name> <col_type>
    [ COLLATE '<collation_specification>' ]
    [ COMMENT '<string_literal>' ]

  -- Additional column definitions
  [ , <col_name> <col_type> [ ... ] ]
  )
  TARGET_LAG = { '<num> { seconds | minutes | hours | days }' | DOWNSTREAM }
  [ SCHEDULER = DISABLE | ENABLE ]
  WAREHOUSE = <warehouse_name>
  [ INITIALIZATION_WAREHOUSE = <warehouse_name> ]
  [ REFRESH_MODE = { AUTO | FULL | INCREMENTAL | ADAPTIVE | CUSTOM_INCREMENTAL } ]
  [ INITIALIZE = { ON_CREATE | ON_SCHEDULE } ]
  [ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ COMMENT = '<string_literal>' ]
  [ REQUIRE USER ]
  [ FROZEN WHERE ( <expr> ) ]
  [ BACKFILL FROM <table_name> ]
  [ START AT ({ STREAM => '<stream_name>' | TIMESTAMP => <timestamp> | STATEMENT => <query_id> | OFFSET => -<seconds> }) ]  -- Requires CUSTOM_INCREMENTAL + BACKFILL FROM
  [ EXECUTE AS USER <user_name>
    [ USE SECONDARY ROLES { ALL | NONE | <role> [ , ... ] } ]
  ]
  [ ROW_TIMESTAMP = { TRUE | FALSE } ]
  { AS <query> | REFRESH USING ( <dml_statement> ) }
```

Creates a dynamic table if it doesn’t exist, or alters it according to the dynamic table
definition. The CREATE OR ALTER DYNAMIC TABLE syntax follows the rules of a
[CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table) statement and has the same limitations as
an [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table) statement.

For more information, see [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

The definition in a CREATE OR ALTER DYNAMIC TABLE statement represents the complete target state. Any property that isn’t specified is set to its default value, except CHANGE\_TRACKING and ROW\_TIMESTAMP, which are preserved when omitted.

Changes to the following dynamic table properties and parameters trigger a [reinitialization](/user-guide/dynamic-tables/overview#label-dynamic-tables-initialization):

- REFRESH\_MODE
- Changes to the query
- Changes to the column list if it will result in existing columns being renamed
- Removing existing FROZEN WHERE or shrinking the frozen region. For more information, see [Add or remove a frozen region](/user-guide/dynamic-tables/frozen-regions#label-dynamic-tables-frozen-alter).

Changes to the other dynamic table properties and parameters preserve data.

#### CREATE OR ALTER DYNAMIC ICEBERG TABLE

To create or alter a dynamic Iceberg table, use CREATE OR ALTER DYNAMIC ICEBERG TABLE. It follows the same rules as CREATE OR ALTER DYNAMIC TABLE, with the additional Iceberg-specific limitations in the [CREATE OR ALTER DYNAMIC TABLE usage notes](#label-create-or-alter-dt-usage-notes). For the Iceberg-specific parameters, see [CREATE DYNAMIC ICEBERG TABLE](#label-create-dt-iceberg-syntax).

### CREATE DYNAMIC TABLE FROM BACKUP SET

Copy code

```
CREATE DYNAMIC TABLE <name> FROM BACKUP SET <backup_set> IDENTIFIER '<backup_id>'
```

The FROM BACKUP SET clause restores a dynamic table from a backup. You don’t specify other table
properties because they’re all the same as in the backed-up table.

This form doesn’t have a CREATE OR REPLACE clause. You typically either restore the
dynamic table under a new name and recover any data or other objects from this new table,
or rename the original table and then restore the table under the original name.

Note

The backup set is associated with the internal table ID of the original table.
Any more backups you add to the backup set use the original table, even if you
changed its name. If you want to make backups of the newly restored table, create a
new backup set for it.

When you restore a dynamic table from a backup, Snowflake
[automatically initializes](/user-guide/dynamic-tables/overview#label-dynamic-tables-initialization)
the new table during its initial refresh.

For more information about backups, see [Backups for disaster recovery and immutable storage](/user-guide/backups).

`backup_set`
:   Specifies the name of a backup set created for a specific dynamic table.
    You can use the SHOW BACKUP SETS command to locate the right backup set.

`backup_id`
:   Specifies the identifier of a specific backup within that backup set.
    You can use the SHOW BACKUPS IN BACKUP SET command to locate the right identifier within the backup
    set, based on the creation date and time for the backup.

### CREATE DYNAMIC TABLE … CLONE

Creates a new dynamic table with the same column definitions and containing all the
existing data from the source dynamic table, without actually copying the data.

Cloned dynamic tables, whether cloned directly or as part of a cloned database or schema, are suspended by default. In [DYNAMIC\_TABLE\_GRAPH\_HISTORY](/sql-reference/functions/dynamic_table_graph_history),
this appears as CLONED\_AUTO\_SUSPENDED in the SCHEDULING\_STATE column. Any downstream dynamic tables are also suspended, shown as UPSTREAM\_CLONED\_AUTO\_SUSPENDED.
For more information, see [Automatic suspension after 5 consecutive errors](/user-guide/dynamic-tables/manage#label-dynamic-tables-manage-understanding-auto-suspend).

You can also clone a dynamic table as it existed at a specific point in the past. For
more information, see [Cloning considerations](/user-guide/object-clone).

Copy code

```
CREATE [ OR REPLACE ] [ TRANSIENT ] DYNAMIC TABLE <name>
  CLONE <source_dynamic_table>
        [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
  [
    COPY GRANTS
    COPY TAGS
    TARGET_LAG = { '<num> { seconds | minutes | hours | days }' | DOWNSTREAM }
    WAREHOUSE = <warehouse_name>
    EXECUTE AS USER <user_name>
      USE SECONDARY ROLES { ALL | NONE | <role> [ , ... ] }
  ]
```

If the source dynamic table has clustering keys, then the cloned dynamic table has
clustering keys. By default, Automatic Clustering is suspended for the new table, even
if Automatic Clustering was not suspended for the source table.

If the source dynamic table has a storage lifecycle policy attached, the policy attachment is preserved on the clone, consistent with the behavior for standard tables.

For more details about cloning, see [CREATE <object> … CLONE](/sql-reference/sql/create-clone).

### CREATE DYNAMIC ICEBERG TABLE

Creates a new dynamic Iceberg table. For information about Iceberg tables, see
[Apache Iceberg™ tables](/user-guide/tables-iceberg) and [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-snowflake).

Copy code

```
CREATE [ OR REPLACE ] DYNAMIC ICEBERG TABLE <name> (
  -- Column definition
  <col_name> <col_type>
    [ [ WITH ] MASKING POLICY <policy_name> [ USING ( <col_name> , <cond_col1> , ... ) ] ]
    [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
    [ COMMENT '<string_literal>' ]

  -- Additional column definitions
  [ , <col_name> <col_type> [ ... ] ]

)
TARGET_LAG = { '<num> { seconds | minutes | hours | days }' | DOWNSTREAM }
WAREHOUSE = <warehouse_name>
[ EXTERNAL_VOLUME = '<external_volume_name>' ]
[ CATALOG = 'SNOWFLAKE' ]
[ BASE_LOCATION = '<optional_directory_for_table_files>' ]
[ TARGET_FILE_SIZE = '{ AUTO | 16MB | 32MB | 64MB | 128MB }' ]
[ PARTITION BY ( partitionExpression [, partitionExpression , ...] ) ]
[ PATH_LAYOUT = { FLAT | HIERARCHICAL } ]
[ ICEBERG_VERSION = <integer> ]
[ REFRESH_MODE = { AUTO | FULL | INCREMENTAL | ADAPTIVE | CUSTOM_INCREMENTAL } ]
[ FROZEN WHERE ( <expr> ) ]
[ INITIALIZE = { ON_CREATE | ON_SCHEDULE } ]
[ CLUSTER BY ( <expr> [ , <expr> , ... ] ) ]
[ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
[ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
[ COMMENT = '<string_literal>' ]
[ COPY GRANTS ]
[ COPY TAGS ]
[ [ WITH ] ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
[ [ WITH ] STORAGE LIFECYCLE POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] ) ]
[ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
[ REQUIRE USER ]
[ EXECUTE AS USER <user_name>
  [ USE SECONDARY ROLES { ALL | NONE | <role> [ , ... ] } ]
]
{ AS <query> | REFRESH USING ( <dml_statement> ) }
```

Where:

Copy code

```
partitionExpression ::=
  <col_name> -- identity transform
  | BUCKET ( <num_buckets> , <col_name> )
  | TRUNCATE ( <width> , <col_name> )
  | YEAR ( <col_name> )
  | MONTH ( <col_name> )
  | DAY ( <col_name> )
  | HOUR ( <col_name> )
```

To clone a dynamic Iceberg table to a new dynamic Iceberg table, use CREATE DYNAMIC ICEBERG TABLE … CLONE:

Copy code

```
CREATE [ OR REPLACE ] DYNAMIC ICEBERG TABLE <name>
  CLONE <source_dynamic_iceberg_table>
        [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
  [
    COPY GRANTS
    COPY TAGS
    TARGET_LAG = { '<num> { seconds | minutes | hours | days }' | DOWNSTREAM }
    WAREHOUSE = <warehouse_name>
    EXECUTE AS USER <user_name>
      USE SECONDARY ROLES { ALL | NONE | <role> [ , ... ] }
  ]
```

The clone uses the same external volume and catalog as the source, so you can’t specify EXTERNAL\_VOLUME, CATALOG, or BASE\_LOCATION. You can
also clone a dynamic Iceberg table to a Snowflake-managed Iceberg table. For more information, see [Clone a dynamic Iceberg table](/user-guide/dynamic-tables/cloning#label-dynamic-tables-clone-iceberg).

For more information about usage and limitations, see
[Create a dynamic Apache Iceberg™ table](/user-guide/dynamic-tables/create-iceberg).

## Required parameters

`name`
:   Specifies the identifier (that is, name) for the dynamic table; must be unique for the schema in which the dynamic table is created.

    In addition, the identifier must start with an alphabetic character and can’t contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TARGET_LAG = { num { seconds | minutes | hours | days } | DOWNSTREAM }`
:   Specifies the lag for the dynamic table:

    > `'num seconds | minutes | hours | days'`
    > :   Specifies the maximum amount of time that the dynamic table’s content should lag behind changes to the base tables.
    >
    >     For example:
    >
    >     - If the data in the dynamic table should lag by no more than 5 minutes, specify `5 minutes`.
    >     - If the data in the dynamic table should lag by no more than 5 hours, specify `5 hours`.
    >
    >     Must be a minimum of 60 seconds. If the dynamic table depends on another dynamic table, the minimum target lag must
    >     be greater than or equal to the target lag of the dynamic table it depends on.
    >
    > `DOWNSTREAM`
    > :   Specifies that the dynamic table should be refreshed only when dynamic tables that depend on it are refreshed.

    Required when `SCHEDULER = ENABLE`.

    For information on how target lag affects how often refreshes run and the associated costs, see [How Snowflake uses target lag](/user-guide/dynamic-tables/target-lag#label-dt-optimize-target-lag).

`WAREHOUSE = warehouse_name`
:   Specifies the name of the warehouse that provides the compute resources for refreshing the dynamic table.

    You must use a role that has the USAGE privilege on this warehouse in order to create the dynamic table. For limitations and more
    information, see [Privilege quick reference](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges).

    For guidance on choosing a warehouse for optimal refresh performance, see [WAREHOUSE vs INITIALIZATION\_WAREHOUSE](/user-guide/dynamic-tables/warehouse-selection#label-dt-optimize-warehouse).

`{ AS query | REFRESH USING ( dml_statement ) }`
:   Specifies the dynamic table’s content. Provide exactly one of the following:

    - `AS <query>`: For SELECT-based dynamic tables. Specifies the query whose results the dynamic table should contain.
    - `REFRESH USING ( <dml_statement> )`: For [custom incremental dynamic tables](/user-guide/dynamic-tables/custom-incrementalization). Specifies the `MERGE INTO SELF` or `INSERT INTO SELF` statement that Snowflake executes on each refresh. For details, see [REFRESH USING](/sql-reference/sql/create-dynamic-table#label-create-dt-refresh-using).

## Optional parameters

`SCHEDULER = { DISABLE | ENABLE }`
:   Specifies whether the dynamic table is refreshed automatically by Snowflake.

    `DISABLE`
    :   Excludes the dynamic table from automatic background refresh. The table isn’t refreshed on a schedule, either directly or
        through downstream dependencies.

        - Manual control: Refreshing must be triggered manually by using `ALTER DYNAMIC TABLE ... REFRESH`.
        - Isolation: A manual refresh of a disabled table doesn’t automatically refresh its upstream dependencies. This creates an “isolation
          boundary,” allowing external orchestrators, like dbt, to manage specific table refreshes in isolation without triggering the entire
          pipeline.
        - `TARGET_LAG` can’t be defined when `SCHEDULER = DISABLE`.

    `ENABLE`
    :   Enables the automated background refresh schedule for the dynamic table. Snowflake ensures that the table is refreshed alongside its
        dependencies to maintain snapshot consistency. In this mode, Snowflake automatically calculates how often refreshes run based on
        the defined `TARGET_LAG`. With this setting, `TARGET_LAG` must be set.

    If not specified, the dynamic table is scheduler-managed by default. [SHOW DYNAMIC TABLES](/sql-reference/sql/show-dynamic-tables) displays `NULL` for the `SCHEDULER` column when the attribute isn’t explicitly set.

`INITIALIZATION_WAREHOUSE = warehouse_name`
:   Specifies a warehouse to use for all dynamic table [initializations and reinitializations](/user-guide/dynamic-tables/overview#label-dynamic-tables-initialization).

    If this parameter isn’t included in the CREATE DYNAMIC TABLE statement, the dynamic table uses the warehouse that is specified by the
    required WAREHOUSE parameter for all refreshes.

    You must use a role that has the USAGE privilege on this warehouse for you to create the dynamic table. For limitations and more
    information, see [Privilege quick reference](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges).

`TRANSIENT`
:   Specifies that the table is transient.

    Like permanent dynamic tables, [transient](/user-guide/tables-temp-transient) dynamic tables exist until
    they’re explicitly dropped, and are available to any user with the appropriate privileges. Transient dynamic
    tables don’t retain data in fail-safe storage, which helps reduce storage costs, especially for tables that
    refresh frequently. Due to this reduced level of durability, transient dynamic tables are best used for
    transitory data that doesn’t need the same level of data protection and recovery provided by permanent tables.

    Default: No value. If a dynamic table is not declared as `TRANSIENT`, it is permanent.

`REFRESH_MODE = { AUTO | FULL | INCREMENTAL | ADAPTIVE | CUSTOM_INCREMENTAL }`
:   Specifies the [refresh mode](/user-guide/dynamic-tables/refresh-modes) for the dynamic table.

    This property can’t be changed with ALTER DYNAMIC TABLE. To change it, use CREATE OR REPLACE DYNAMIC TABLE or CREATE OR ALTER DYNAMIC TABLE. Some transitions trigger reinitialization (see [Refresh mode transitions](/user-guide/dynamic-tables/modify#label-dynamic-tables-refresh-mode-transitions)).

    > `AUTO`
    > :   When refresh mode is `AUTO`, the system attempts to apply an incremental refresh by default. However, when incremental refresh isn’t
    >     supported or expected to perform well, the dynamic table automatically selects full refresh instead. If a `REFRESH USING` clause is
    >     present, `AUTO` resolves to `CUSTOM_INCREMENTAL`. For more information, see
    >     [ADAPTIVE refresh](/user-guide/dynamic-tables/refresh-modes#label-dynamic-tables-intro-refresh-modes) and [Run your query standalone first](/user-guide/dynamic-tables/refresh-optimization#label-dt-optimize-refresh).
    >
    >     To determine the best mode for your use case, experiment with refresh modes and automatic recommendations. For consistent behavior across
    >     Snowflake releases, explicitly set the refresh mode on all dynamic tables.
    >
    >     To verify the refresh mode for your dynamic tables, see [Check refresh status](/user-guide/dynamic-tables/monitoring#label-dynamic-tables-monitoring-refresh-mode).
    >
    > `FULL`
    > :   Enforces a full refresh of the dynamic table, even if the dynamic table can be incrementally refreshed.
    >
    > `INCREMENTAL`
    > :   Enforces an incremental refresh of the dynamic table. If the query that underlies the dynamic table can’t perform an incremental refresh,
    >     dynamic table creation fails and displays an error message.
    >
    >     For information about how operators affect incremental refresh, see [Optimize queries for incremental refresh](/user-guide/dynamic-tables/refresh-optimization).
    >
    > `ADAPTIVE`
    > :   Uses incremental refresh by default but automatically reinitializes the dynamic table when internal heuristics
    >     detect that an incremental refresh would be significantly more expensive than rebuilding from scratch. After
    >     reinitialization, incremental refreshes resume.
    >
    >     Requires the same incrementalizable query constructs as `INCREMENTAL`. If the query can’t perform an incremental refresh,
    >     dynamic table creation fails and displays an error message.
    >
    >     If an `INITIALIZATION_WAREHOUSE` is configured, reinitializations use that warehouse.
    >
    >     For more information, see [ADAPTIVE refresh](/user-guide/dynamic-tables/refresh-modes#label-dynamic-tables-refresh-adaptive).
    >
    > `CUSTOM_INCREMENTAL`
    > :   The dynamic table uses a user-defined MERGE or INSERT statement (specified in the `REFRESH USING` clause) as its refresh logic. Requires
    >     an explicit column list with both names and types (`( <col_name> <col_type> [ , <col_name> <col_type> ... ] )`) and a `REFRESH USING` clause. `AUTO` resolves to `CUSTOM_INCREMENTAL` when `REFRESH USING` is present.
    >
    >     For more information, see [Custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization).
    >
    > Default: `AUTO`

`REFRESH USING ( dml_statement )`
:   Specifies the DML statement that Snowflake executes on each refresh. The statement must be either `MERGE INTO SELF ...` or
    `INSERT INTO SELF ...`. The `SELF` keyword references the dynamic table being created.

    Requirements:

    - Only one DML statement is allowed per `REFRESH USING` clause.
    - Tables queried with `CHANGES()` must have change tracking enabled.
    - The `CHANGES()` clause can’t specify time bounds (`AT`/`BEFORE`/`END`).
    - Requires an explicit column list in the CREATE DYNAMIC TABLE statement.

    For syntax details and examples, see [Custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization).

`INITIALIZE`
:   Specifies the behavior of the [initial refresh](/user-guide/dynamic-tables/refresh-modes) of the dynamic table. This property can’t be
    altered after you create the dynamic table. To modify the property, replace the dynamic table with a CREATE OR REPLACE DYNAMIC TABLE command.

    > `ON_CREATE`
    > :   Refreshes the dynamic table synchronously at creation. If this refresh fails, dynamic table creation fails and displays an error message.
    >
    > `ON_SCHEDULE`
    > :   Refreshes the dynamic table at the next scheduled refresh.
    >
    >     The dynamic table is populated when the refresh schedule process runs. No data is populated when the dynamic table is created. If you try to
    >     query the table using `SELECT * FROM DYNAMIC TABLE`, you might see the following error because the first scheduled refresh has not yet
    >     occurred.
    >
    >     ```
    >     Dynamic Table is not initialized. Please run a manual refresh or wait for a scheduled refresh before querying.
    >     ```
    >
    > Default: `ON_CREATE`

`COMMENT 'string_literal'`
:   Specifies a comment for the column.

    (Note that comments can be specified at the column level or the table level. The syntax for each is slightly different.)

`MASKING POLICY = policy_name`
:   Specifies the [masking policy](/user-guide/security-column-intro) to set on a column.

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`PROJECTION POLICY policy_name`
:   Specifies the [projection policy](/user-guide/projection-policies) to set on a column.

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value for the column.

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`column_list`
:   If you want to change the name of a column or add a comment to a column in the dynamic table,
    include a column list that specifies the column names and, if needed, comments about
    the columns. You do not need to specify the data types of the columns.

    If any of the columns in the dynamic table are based on expressions - for example, not simple column names -
    then you must supply a column name for each column in the dynamic table. For instance, the column names are
    required in the following case:

    Copy code

    ```
    CREATE DYNAMIC TABLE my_dynamic_table (pre_tax_profit, taxes, after_tax_profit)
      TARGET_LAG = '20 minutes'
        WAREHOUSE = mywh
        AS
          SELECT revenue - cost, (revenue - cost) * tax_rate, (revenue - cost) * (1.0 - tax_rate)
          FROM staging_table;
    ```

    You can specify an optional comment for each column. For example:

    Copy code

    ```
    CREATE DYNAMIC TABLE my_dynamic_table (pre_tax_profit COMMENT 'revenue minus cost',
                    taxes COMMENT 'assumes taxes are a fixed percentage of profit',
                    after_tax_profit)
      TARGET_LAG = '20 minutes'
        WAREHOUSE = mywh
        AS
          SELECT revenue - cost, (revenue - cost) * tax_rate, (revenue - cost) * (1.0 - tax_rate)
          FROM staging_table;
    ```

`WITH CONTACT ( purpose = contact [ , purpose = contact ...] )`
:   Associate the new object with one or more [contacts](/user-guide/contacts-using).

    Specify the WITH CONTACT clause after all other clauses except the AS clause (if that clause is supported by this command).

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`ICEBERG_VERSION = integer`
:   Specifies the version of the Apache Iceberg™ specification that the table conforms to.

    Caution

    Before you use other engines to upgrade an Iceberg tables format-version in table properties to v3, ensure that the table isn’t used by
    engines or applications that don’t yet support v3. Downgrading format versions isn’t supported in the Apache Iceberg specification. Therefore, all
    readers and writers must support v3. The default version for Iceberg tables in Snowflake is v2, which can be configured to v3 if
    needed. Using Snowflake to perform in-place version upgrades isn’t supported at this time.

    If you don’t set this parameter, the Iceberg table defaults to the Iceberg version for the schema, database, or account. The schema
    takes precedence over the database, and the database takes precedence over the account.

    > - `2`: The table conforms with Iceberg version 2.
    > - `3`: The table conforms with Iceberg version 3.
    >
    > Default: `2`
    >
    > For more information about this parameter, see [ICEBERG\_VERSION](/sql-reference/parameters#label-iceberg-version).

`TARGET_FILE_SIZE = '{ AUTO | 16MB | 32MB | 64MB | 128MB }'`
:   Specifies a target Parquet file size for the table.

    - `'{ 16MB | 32MB | 64MB | 128MB }'` specifies a fixed target file size for the table.
    - `'AUTO'` works differently, depending on the table type:
      - Snowflake-managed tables: AUTO specifies that Snowflake should choose the file size for the table based on table characteristics
        such as size, DML patterns, ingestion workload, and clustering configuration. Snowflake automatically
        adjusts the file size, starting at 16 MB, for better read and write performance in Snowflake. Use this option to optimize table performance
        in Snowflake.
      - Externally managed tables: AUTO specifies that Snowflake should aggressively scale to the largest file size (128 MB).

    For more information, see [Set a target file size](/user-guide/tables-iceberg-manage#label-tables-iceberg-target-file-size).

    Default: AUTO

`PARTITION BY ( partitionExpression [ , partitionExpression , ... ] )`
:   Specifies one or more [partition expressions](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-snowflake-partitionexpressions)
    for the dynamic Iceberg table. For parameter details, see
    [Partition expression parameters (`partitionExpression`)](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-snowflake-partitionexpressions) in
    [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-snowflake).

`PATH_LAYOUT = { FLAT | HIERARCHICAL }`
:   Specifies the path layout that Snowflake uses when writing Parquet data files to the table:

    - `FLAT`: Snowflake writes all Parquet data files under the `data/` directory for the table.
    - `HIERARCHICAL`: Snowflake writes partitioned data under the `data/` directory for the table by using a hierarchical
      path layout. With this layout, each partition column is represented
      as a directory level in the path. To define these partition
      columns, use the PARTITION BY parameter. This layout is also called “Hive-style” partitioning.

      If you specify PATH\_LAYOUT = HIERARCHICAL without a PARTITION BY clause,
      Snowflake stores the Parquet data files by using a flat layout path. You can use the
      ALTER ICEBERG TABLE command to set PATH\_LAYOUT for an existing table.

    Note

    For externally managed tables that you create in a standard Snowflake database, Snowflake infers and honors the partitioning scheme
    that is specified by the remote catalog.

    Default: `FLAT`

`CLUSTER BY ( expr [ , expr , ... ] )`
:   Specifies one or more columns or column expressions in the dynamic table as the clustering key. Before you specify a clustering
    key for a dynamic table, you should understand micro-partitions. For more information, see [Understanding Snowflake Table Structures](/user-guide/tables-micro-partitions).

    Note the following when using clustering keys with dynamic tables:

    - Column definitions are required and must be explicitly specified in the statement.
    - By default, Automatic Clustering is not suspended for the new dynamic table, even if Automatic Clustering is suspended for the
      source table.
    - Clustering keys are not intended or recommended for all tables; they typically benefit very large (for example
      multi-terabyte) tables.
    - Specifying CLUSTER BY doesn’t cluster the data at creation time; instead, CLUSTER BY relies on
      Automatic Clustering to recluster the data over time.

    For more information, see [Clustering Keys & Clustered Tables](/user-guide/tables-clustering-keys).

    Default: No value (no clustering key is defined for the table)

`DATA_RETENTION_TIME_IN_DAYS = integer`
:   Specifies the retention period for the dynamic table so that Time Travel actions (SELECT, CLONE) can be performed on historical
    data in the dynamic table. Time Travel behaves the same way for dynamic tables as it behaves for traditional tables. For more
    information, see [Understanding & using Time Travel](/user-guide/data-time-travel).

    For a detailed description of this object-level parameter, as well as more information about object parameters, see
    [Parameters](/sql-reference/parameters).

    Values:

    - Standard Edition: `0` or `1`
    - Enterprise Edition:
      - `0` to `90` for permanent tables
      - `0` or `1` for temporary and transient tables

    Default:

    - Standard Edition: `1`
    - Enterprise Edition (or higher): `1` (unless a different default value was specified at the schema, database, or account level)

    Note

    A value of `0` effectively disables Time Travel for the table.

`MAX_DATA_EXTENSION_TIME_IN_DAYS = integer`
:   An object parameter that sets the maximum number of days Snowflake can extend the data retention period to prevent streams on the dynamic
    table from becoming stale.

    For a detailed description of this parameter, see [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-max-data-extension-time-in-days).

`COMMENT = 'string_literal'`
:   Specifies a comment for the dynamic table.

    (Note that comments can be specified at the column level or the table level. The syntax for each is slightly different.)

    Default: No value.

`COPY GRANTS`
:   Specifies to retain the access privileges from the original table when a new dynamic table is created using any of the following CREATE DYNAMIC TABLE variants:

    - CREATE OR REPLACE DYNAMIC TABLE
    - CREATE OR REPLACE DYNAMIC ICEBERG TABLE
    - CREATE OR REPLACE DYNAMIC TABLE … CLONE

    This parameter copies all privileges except OWNERSHIP from the existing dynamic table to the new dynamic table. The new dynamic
    table does not inherit any future grants defined for the object type in the schema. By default, the role that executes the
    CREATE DYNAMIC TABLE statement owns the new dynamic table.

    If this parameter is not included in the CREATE DYNAMIC TABLE statement, then the new table does not inherit any explicit access
    privileges granted on the original dynamic table, but does inherit any future grants defined for the object type in the schema.

    If the statement is replacing an existing table of the same name, then the grants are copied from the table being replaced. If there is
    no existing table of that name, then the grants are copied.

    For example, the following statement creates a dynamic table `dt1` cloned from `dt0` with all grants copied from `dt0`. The first
    time you run the command, `dt1` copies all grants from `dt0`. If you run the same command again, `dt1` will copy all grants from
    `dt1` and not `dt0`.

    Copy code

    ```
    CREATE OR REPLACE DYNAMIC TABLE dt1 CLONE dt0
      COPY GRANTS;
    ```

    Note the following:

    - With [data sharing](/guides-overview-sharing):

      - If the existing dynamic table was shared to another account, the replacement dynamic table is also shared.
      - If the existing dynamic table was shared with your account as a data consumer, and access was further granted to other roles in
        the account (using `GRANT IMPORTED PRIVILEGES` on the parent database), access is also granted to the replacement dynamic
        table.
    - The [SHOW GRANTS](/sql-reference/sql/show-grants) output for the replacement dynamic table lists the grantee for the copied privileges as the
      role that executed the CREATE TABLE statement, with the current timestamp when the statement was executed.
    - The operation to copy grants occurs atomically in the CREATE DYNAMIC TABLE command (that is, within the same transaction).

    This parameter is not supported by the CREATE OR ALTER variant syntax.

    Important

    The COPY GRANTS parameter can be placed anywhere in a CREATE [ OR REPLACE ] DYNAMIC TABLE command, except after the query
    definition.

    For example, the following dynamic table will fail to create:

    Copy code

    ```
    CREATE OR REPLACE DYNAMIC TABLE my_dynamic_table
      TARGET_LAG = DOWNSTREAM
      WAREHOUSE = mywh
      AS
        SELECT * FROM staging_table
        COPY GRANTS;
    ```

`COPY TAGS`
:   Applies [tags](/user-guide/object-tagging/introduction) when you use any of these CREATE DYNAMIC TABLE forms:

    > - CREATE OR REPLACE DYNAMIC TABLE
    > - CREATE OR REPLACE DYNAMIC TABLE … CLONE

    If the statement uses CREATE OR REPLACE DYNAMIC TABLE … COPY TAGS without CLONE or a WITH TAG clause, tags from the replaced dynamic table
    and its columns are retained on the new dynamic table.

    If the statement uses CLONE or WITH TAG together with COPY TAGS, Snowflake combines tags from the applicable sources. If both sources set
    the same tag, the value from the replaced dynamic table (carried over by COPY TAGS) takes precedence.

    For more information, including the effect when you alter columns in the CREATE OR REPLACE statement, see
    [the usage notes for COPY TAGS](/sql-reference/sql/create-dynamic-table#label-create-dynamic-table-usage-notes-copy-tags).

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`ROW ACCESS POLICY policy_name ON ( col_name [ , col_name ... ] )`
:   Specifies the [row access policy](/user-guide/security-row-intro) to set on a dynamic table.

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`AGGREGATION POLICY policy_name [ ENTITY KEY ( col_name [ , col_name ... ] ) ]`
:   Specifies an [aggregation policy](/user-guide/aggregation-policies) to set on a dynamic table. You can apply one or more aggregation
    policies on a table.

    Use the optional ENTITY KEY parameter to define which columns uniquely identify an entity within the dynamic table. For more information,
    see [Implementing entity-level privacy with aggregation policies](/user-guide/aggregation-policies-entity-privacy). You can specify one or more entity keys for an aggregation policy.

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`REQUIRE USER`
:   When specified, the dynamic table can’t run unless a user is specified. The dynamic table is not able to refresh unless a user is set
    in a manual refresh with the [COPY SESSION](/sql-reference/sql/alter-dynamic-table#label-alter-dynamic-table-refresh) parameter specified.

    If this option is enabled, the dynamic table must be created with the [ON\_SCHEDULE](/sql-reference/sql/create-dynamic-table#label-create-dt-initialize) parameter for
    `INITIALIZE`.

`FROZEN WHERE`
:   Specifies a condition that defines the frozen region of the dynamic table. For more information, see [Frozen regions and backfill](/user-guide/dynamic-tables/frozen-regions).

`STORAGE LIFECYCLE POLICY policy_name ON ( col_name [ , col_name ... ] )`
:   Specifies a [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies) to attach to the dynamic table.

    The columns specified in the ON clause must match the argument count and data types defined in the policy function signature.
    Snowflake uses these columns to evaluate the policy expression and determine which rows to delete or archive.

    For more information about using storage lifecycle policies with dynamic tables, see
    [Use storage lifecycle policies with dynamic tables](/user-guide/dynamic-tables/storage-lifecycle-policies).

    This parameter is not supported by the CREATE OR ALTER variant syntax.

`BACKFILL FROM <table_name>`
:   Specifies the table to backfill data from. The behavior depends on the type of dynamic table:

    - **SELECT-based dynamic tables with frozen regions:** Backfills data defined by the [frozen region](/user-guide/dynamic-tables/frozen-regions).
      The backfill data must remain unchanged, even if it differs from the upstream source.
      For more information, see [Seed a dynamic table with BACKFILL FROM](/user-guide/dynamic-tables/frozen-regions#label-create-dt-using-backfill).
    - **Custom incremental dynamic tables:** Provides initial population from an existing table, avoiding a full replay
      of source history on the initial refresh. This lets you seed the dynamic table with historical data so that subsequent
      incremental refreshes only need to process new changes.

`START AT (\{ STREAM => <stream_name> | TIMESTAMP => <timestamp> | STATEMENT => <query_id> | OFFSET => -<seconds> \})`
:   Specifies where subsequent incremental refreshes begin consuming changes. Requires `BACKFILL FROM` and a custom incremental dynamic table.

    - `STREAM => <stream_name>`: Begin incremental processing from the current offset of an existing stream.
    - `TIMESTAMP => <timestamp>`: Begin incremental processing from a specific point in time.
    - `STATEMENT => <query_id>`: Begin incremental processing from the point after a specific query completed.
    - `OFFSET => -<seconds>`: Begin incremental processing from a negative offset in seconds from the current time.

`EXECUTE AS USER user_name`
:   Refreshes the dynamic table as the specified user.

    To specify EXECUTE AS USER, you must use a role that has been granted the IMPERSONATE privilege on the `user_name` user. To grant this privilege,
    run the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command.

    `USE SECONDARY ROLES \{ ALL | NONE | <role> [ , ... ] \}`
    :   Specifies the secondary roles to use on the dynamic table. Can be used to override the default secondary roles that are otherwise used in execution.

        Can only be used with the EXECUTE AS USER option.

    For more information, see [Refresh with specific user privileges (EXECUTE AS USER)](/user-guide/dynamic-tables/privileges#label-dts-execute-as-user).

`ROW_TIMESTAMP = { TRUE | FALSE }`
:   Specifies whether to enable row timestamps on the table. You must use a role with the OWNERSHIP privilege.

    For more information, see [Use row timestamps to measure latency in your pipelines](/user-guide/data-engineering/row-timestamps).

`WITH DATA METRIC FUNCTION ( dmf_name ON ( col_name [ , col_name ... ] ) [ , dmf_binding ... ] )`
:   Associates one or more [data metric functions (DMFs)](/user-guide/data-quality-intro) with the dynamic table at creation time.
    The DMF begins running on the schedule configured for the table as soon as it is created.

    You can attach multiple DMF bindings by separating them with commas. Each binding accepts the same properties as
    [ALTER TABLE … ADD DATA METRIC FUNCTION](/sql-reference/sql/alter-table#label-alter-table-data-metric-function-action), including
    `EXECUTE AS ROLE`, `ANOMALY_DETECTION`, `SENSITIVITY`, `DATA_QUALITY_NOTIFICATION`, and `EXPECTATION`.

    For a description of each property, see
    [Data metric function actions](/sql-reference/sql/alter-table#label-alter-table-data-metric-function-action).

    Snowflake also accepts this clause without the parentheses around the binding list, but that
    form is deprecated and a future [behavior change release](/release-notes/behavior-changes)
    removes it.

    For usage guidance and examples, see [Attach DMFs at creation time](/user-guide/data-quality-working#label-dmf-create-with).

    Default: No value (no DMF is associated with the dynamic table)

    This parameter is not supported by the CREATE OR ALTER variant syntax.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE DYNAMIC TABLE | Schema in which you plan to create the dynamic table. |  |
| SELECT | Tables, views, and dynamic tables that you plan to query for the new dynamic table. |  |
| USAGE | Warehouse that you plan to use to refresh the table. |  |
| IMPERSONATE | User specified in EXECUTE AS USER | To refresh the dynamic table as a user, you must use a role that has been granted the IMPERSONATE privilege on that user. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When you execute the CREATE DYNAMIC TABLE command, the current role in use becomes
  the owner of the dynamic table. This role is used to perform refreshes of the dynamic
  table in the background.
- You can’t make changes to the schema after you create a dynamic table.
- Dynamic tables refresh as base objects change. Change tracking must
  be enabled on all base objects used by a dynamic table. See
  [Change tracking not enabled on base tables](/user-guide/dynamic-tables/troubleshoot-creation#label-dynamic-tables-and-change-tracking).
- If you want to replace an existing dynamic table and need to see its current definition,
  call the [GET\_DDL](/sql-reference/functions/get_ddl) function.
- Using [ORDER BY](/sql-reference/constructs/order-by) in the definition of a dynamic table
  might produce results sorted in an unexpected order. You can use ORDER BY when querying
  your dynamic table to ensure that rows selected return in a specific order.
- Snowflake doesn’t support using ORDER BY to create a view that selects from a dynamic
  table.
- To influence the order in which rows are stored in a dynamic table, consider enabling [clustering](/sql-reference/sql/create-dynamic-table#label-cluster-dts).
- To enable efficient updates, the initial refresh pre-clusters the data by the dynamic table’s clustering key if one is defined.
  Otherwise, the initial refresh pre-clusters by an internal metadata column, which can make the initial refresh of a dynamic table
  take longer than an equivalent [CREATE TABLE … AS SELECT](/sql-reference/sql/create-table#label-ctas-syntax) statement.
- Some expressions, clauses, and functions are not currently supported in dynamic tables.
  For a complete list, see [Don’t use dynamic tables when your pipeline has any of the following…](/user-guide/dynamic-tables/decision-guide#label-dynamic-tables-limitations).
- You can use `DYNAMIC_TABLE_REFRESH_BOUNDARY()` in the definition query to prevent an upstream dynamic table from being refreshed together
  with this dynamic table. The upstream dynamic table is treated as belonging to a separate pipeline, which means cascading refreshes and
  snapshot isolation do not apply across the boundary. For more information, see [Data consistency and pipeline boundaries](/user-guide/dynamic-tables/data-consistency).
- Using `OR REPLACE` is the equivalent to using DROP DYNAMIC TABLE on the existing dynamic table and then creating a new
  dynamic table with the same name. However, Snowflake doesn’t drop the old dynamic table until it has created the new dynamic table,
  including the initial refresh if `INITIALIZE = ON_CREATE` is specified. Instead, the new dynamic table is created as a
  hidden table, the refresh is run, then Snowflake atomically swaps it in for the existing dynamic table.
- Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- CREATE OR REPLACE … COPY TAGS
  - You don’t need privileges on the tags to use COPY TAGS.
  - You can use COPY TAGS with a CREATE OR REPLACE … CLONE statement or a WITH TAG clause. Tags from both sources are combined. If both
    sources set the same tag, the value from the replaced dynamic table (carried over by COPY TAGS) takes precedence.
  - If you rename a tagged column in the statement, the column in the new dynamic table will not retain the tag.
  - If you change the data type of a tagged column — for example, changing `NUMBER(8)` to `NUMBER(16)` — the column in the new dynamic
    table will not retain the tag.
  - If you swap column names in the statement, the tag stays with the column based on its name. For example, suppose only column `a` has a
    tag and you run the following command to swap the names of columns `a` and `b`:

    Copy code

    ```
    CREATE OR REPLACE DYNAMIC TABLE dst1 COPY TAGS AS SELECT b AS a, a AS b FROM src1
    ```

    Only column `a` is still tagged in the new dynamic table, although it contains the data from column `b` in the source table.

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## CREATE OR ALTER DYNAMIC TABLE usage notes

- All limitations of the [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table) command apply.

### Limitations

The following limitations apply specifically to the `CREATE OR ALTER DYNAMIC TABLE` variant. They don’t apply to [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table).

The following actions *aren’t* supported:

> - Swapping dynamic tables by using the SWAP WITH parameter.
> - Renaming a dynamic table by using the RENAME TO parameter.
> - Creating a clone of a dynamic table by using the CLONE parameter.
> - Suspending or resuming by using the SUSPEND and RESUME parameters. (Use [ALTER DYNAMIC TABLE … SUSPEND | RESUME](/sql-reference/sql/alter-dynamic-table) instead.)
> - Converting a TRANSIENT dynamic table into a non-TRANSIENT dynamic table, or vice versa.
> - Adding or changing tags, policies, and data metric functions. Any existing tags, policies, and data metric functions are preserved.
>   To add or modify these, use [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table).
> - For a dynamic Iceberg table, changing the Iceberg storage properties EXTERNAL\_VOLUME, CATALOG, or BASE\_LOCATION of an existing table isn’t supported. To change these, use CREATE OR REPLACE DYNAMIC ICEBERG TABLE, or ALTER ICEBERG TABLE.
> - Converting a regular dynamic table into a dynamic Iceberg table, or vice versa.
> - Changing BACKFILL FROM after the dynamic table is created.
> - Adding START AT after the dynamic table is created.
> - Changing START AT after the dynamic table is created.

The following rules apply to column changes:

- Dropping existing columns is supported.
- Adding new columns is supported, but they can only be added at the end of existing columns.
- Dropping columns that are used in a frozen region predicate or as clustering keys isn’t supported.
- Renaming existing trailing columns (the last column or last N columns in the column list) is supported, but the next refresh is a full reinitialization. Columns that aren’t at the end of the column list can’t be renamed. For example, `(id, name1, name2)` → `(id, name3, name4)` is supported, but `(id1, name3, name4)` isn’t.
- Adding COLLATE on a new column is supported. Adding, changing, or dropping COLLATE on an existing column isn’t supported.
- Specifying column-level masking policies, projection policies, tags, or contact properties isn’t supported.
  To add these to columns, use ALTER DYNAMIC TABLE after the column change takes effect.

INITIALIZE applies only at creation time and cannot be modified afterward. You can change REFRESH\_MODE with CREATE OR ALTER DYNAMIC TABLE, though some transitions trigger reinitialization (see [Refresh mode transitions](/user-guide/dynamic-tables/modify#label-dynamic-tables-refresh-mode-transitions)).

### No implicit refreshes

If you change an existing dynamic table by using the CREATE OR ALTER DYNAMIC TABLE
command, the command doesn’t trigger a refresh of the dynamic table. The dynamic table
refreshes according to its normal schedule.

However, if you create a new dynamic table by using the CREATE OR ALTER DYNAMIC TABLE
command and you specify `INITIALIZE = ON_CREATE`, the command triggers a refresh of the
dynamic table.

### Atomicity

The CREATE OR ALTER DYNAMIC TABLE command doesn’t guarantee *atomicity*. This means that if
a CREATE OR ALTER DYNAMIC TABLE statement fails during execution, it’s possible that a
subset of changes might have been applied to the table. If there’s a possibility of
partial changes, in most cases, the error message includes the following text:

```
CREATE OR ALTER execution failed. Partial updates may have been applied.
```

For example, suppose that you wanted to change the `TARGET_LAG` property and add a
clustering key for a dynamic table, but you change your mind and terminate the statement. In
this case, the `TARGET_LAG` property might still change while the clustering key isn’t
applied.

When changes are partially applied, the resulting table is in a valid state. In the
previous example, you can use additional ALTER DYNAMIC TABLE statements to complete the
original set of changes.

To recover from partial updates, try the following recovery methods:

- **Fix forward**: Re-execute the CREATE OR ALTER DYNAMIC TABLE statement. If the
  statement succeeds on the second attempt, the target state is achieved.

  If the statement doesn’t succeed, investigate the error message. If possible, fix the
  error and re-execute the CREATE OR ALTER DYNAMIC TABLE statement.
- **Roll back**: If it isn’t possible to fix forward, manually roll back the partial
  changes:

  - Investigate the state of the table by using the [DESCRIBE DYNAMIC TABLE](/sql-reference/sql/desc-dynamic-table)
    and [SHOW DYNAMIC TABLES](/sql-reference/sql/show-dynamic-tables) commands. Determine which partial
    changes were applied, if any.

    If partial changes were applied, execute the appropriate ALTER DYNAMIC TABLE
    statements to transform the dynamic table back to its original state.

For additional help, contact [Snowflake Support](/user-guide/contacting-support).

## Frozen region usage notes

- You can set only one frozen region predicate per dynamic table. Setting another predicate
  replaces the existing one.
- Frozen region predicates can’t contain the following items:

  - Subqueries
  - Nondeterministic functions (except timestamp functions like CURRENT\_TIMESTAMP or
    CURRENT\_DATE)
  - User-defined or external functions
  - Metadata columns (those starting with `METADATA$`)
  - Columns that result from aggregates, window functions, or nondeterministic functions
  - Columns that are passed through a window function operator and not a `PARTITION BY` column. Example: `col2` in `SUM(col1) OVER (PARTITION BY col1 ORDER BY col2)`
- When you use timestamp functions, the frozen region can’t shrink over time. For example,
  `TIMESTAMP_COL < CURRENT_TIMESTAMP()` is allowed, but
  `TIMESTAMP_COL > CURRENT_TIMESTAMP()` is not.
- Columns referenced in the frozen region predicate must be columns in the dynamic table,
  not columns from the base table.
- When the dynamic table has both a frozen region predicate and at least one primary key or unique constraint
  with the [RELY property](/user-guide/join-elimination#label-join-elimination-setting-rely), the columns referenced in the frozen region
  predicate must appear in every RELY PRIMARY KEY and RELY UNIQUE constraint (that is, the intersection of all
  RELY constraint column sets). Only RELY constraints are considered. For details, see
  [Interaction with RELY constraints](/user-guide/dynamic-tables/frozen-regions#label-dynamic-tables-frozen-rely-interaction).
- The following limitations apply when you work with [frozen regions and backfill](/user-guide/dynamic-tables/frozen-regions):

  - Currently, only regular and dynamic tables can be used for backfilling.
  - You can’t specify policies or tags in the new dynamic table because they are copied from the backfill table.
  - Clustering keys in the new dynamic table and backfill table must be the same.

## Examples

Create a dynamic table named `my_dynamic_table`:

Copy code

```
CREATE OR REPLACE DYNAMIC TABLE my_dynamic_table
  TARGET_LAG = '20 minutes'
  WAREHOUSE = mywh
  AS
    SELECT product_id, product_name FROM staging_table;
```

In the example above:

- The dynamic table materializes the results of a query of the `product_id` and `product_name` columns of the
  `staging_table` table.
- The target lag is 20 minutes, which means that the data in the dynamic table should ideally be no more than 20 minutes
  older than the data in `staging_table`.
- Snowflake uses the compute resources in warehouse `mywh` to refresh the data in the dynamic table.

Create a dynamic Iceberg table named `my_dynamic_table` that reads from `my_iceberg_table`:

Copy code

```
CREATE DYNAMIC ICEBERG TABLE my_dynamic_table (date TIMESTAMP_NTZ, id NUMBER, content STRING)
  TARGET_LAG = '20 minutes'
  WAREHOUSE = mywh
  EXTERNAL_VOLUME = 'my_external_volume'
  CATALOG = 'SNOWFLAKE'
  BASE_LOCATION = 'my_iceberg_table'
  AS
    SELECT product_id, product_name FROM staging_table;
```

Create a dynamic table with a multi-column clustering key:

Copy code

```
CREATE DYNAMIC TABLE my_dynamic_table (date TIMESTAMP_NTZ, id NUMBER, content VARIANT)
  TARGET_LAG = '20 minutes'
  WAREHOUSE = mywh
  CLUSTER BY (date, id)
  AS
    SELECT product_id, product_name FROM staging_table;
```

Clone a dynamic table as it existed exactly at the date and time of the specified timestamp:

Copy code

```
CREATE DYNAMIC TABLE my_cloned_dynamic_table CLONE my_dynamic_table AT (TIMESTAMP => TO_TIMESTAMP_TZ('04/05/2013 01:02:03', 'mm/dd/yyyy hh24:mi:ss'));
```

Configure a dynamic table to require a user for refreshes and then refresh the dynamic table:

Copy code

```
CREATE DYNAMIC TABLE my_dynamic_table
  TARGET_LAG = 'DOWNSTREAM'
  WAREHOUSE = mywh
  INITIALIZE = on_schedule
  REQUIRE USER
  AS
    SELECT product_id, product_name FROM staging_table;
```

Copy code

```
ALTER DYNAMIC TABLE my_dynamic_table REFRESH COPY SESSION;
```

Create a dynamic table with a frozen region:

Copy code

```
CREATE DYNAMIC TABLE my_dynamic_table
  TARGET_LAG = '1 hour'
  WAREHOUSE = my_warehouse
  FROZEN WHERE (ts < CURRENT_TIMESTAMP() - INTERVAL '1 day')
AS
  SELECT * FROM source_table;
```

Create a dynamic table by using the CREATE OR ALTER DYNAMIC TABLE command:

Copy code

```
CREATE OR ALTER DYNAMIC TABLE my_dynamic_table
  TARGET_LAG = DOWNSTREAM
  WAREHOUSE = mywh
  AS
    SELECT a, b FROM t;
```

Note

CREATE OR ALTER TABLE statements for existing tables can only be executed by a role with the OWNERSHIP privilege on `my_dynamic_table`.

Alter a dynamic table to set the DATA\_RETENTION\_TIME\_IN\_DAYS parameter and add a clustering key:

Copy code

```
CREATE OR ALTER DYNAMIC TABLE my_dynamic_table
 TARGET_LAG = DOWNSTREAM
 WAREHOUSE = mywh
 DATA_RETENTION_TIME_IN_DAYS = 2
 CLUSTER BY (a)
 AS
   SELECT a, b FROM t;
```

Modify the target lag and change the warehouse:

Copy code

```
CREATE OR ALTER DYNAMIC TABLE my_dynamic_table
 TARGET_LAG = '5 minutes'
 WAREHOUSE = my_other_wh
 DATA_RETENTION_TIME_IN_DAYS = 2
 CLUSTER BY (a)
 AS
   SELECT a, b FROM t;
```

Unset the DATA\_RETENTION\_TIME\_IN\_DAYS parameter. The absence of a parameter in the
modified CREATE OR ALTER DYNAMIC TABLE statement results in unsetting it. In this case,
unsetting the DATA\_RETENTION\_TIME\_IN\_DAYS parameter for the dynamic table resets it to
the default value of 1:

Copy code

```
CREATE OR ALTER DYNAMIC TABLE my_dynamic_table
 TARGET_LAG = '5 minutes'
 WAREHOUSE = my_other_wh
 CLUSTER BY (a)
 AS
   SELECT a, b FROM t;
```

**Write a v3 Snowflake-managed Iceberg table**

Note

For more information about other Iceberg v3 features that Snowflake supports, see [Apache Iceberg™ tables: Support for Apache Iceberg™ v3](/user-guide/tables-iceberg-v3-specification-support).

The following example writes a v3 Snowflake-managed Iceberg table as the output of a dynamic table:

Copy code

```
CREATE DYNAMIC ICEBERG TABLE my_dynamic_iceberg_v3_table (
    num_orders NUMBER(10,0),
    order_day
  )
  TARGET_LAG = '20 minutes'
  WAREHOUSE = my_warehouse
  EXTERNAL_VOLUME = 'my_external_volume'
  CATALOG = 'SNOWFLAKE'
  BASE_LOCATION = 'my_dynamic_iceberg_v3_table'
  ICEBERG_VERSION = 3
  AS
    SELECT
        COUNT(DISTINCT order_id)
        DATE_TRUNC('DAY', order_timestamp_ns) AS order_day
      FROM staging_v3_iceberg_table;
```

Note

Writing either a v2 or v3 externally managed Iceberg table as the target of a dynamic table isn’t supported. The output of a dynamic
Iceberg table can only be Snowflake-managed.

Create a dynamic table with a storage lifecycle policy that expires rows older than one week:

Copy code

```
CREATE DYNAMIC TABLE dt_orders
  TARGET_LAG = '1 minute'
  WAREHOUSE = transform_wh
  WITH STORAGE LIFECYCLE POLICY expire_after_1w ON (order_date)
  AS
    SELECT order_id, customer_id, order_date, product_name, quantity, unit_price, order_status
    FROM raw_orders;
```
