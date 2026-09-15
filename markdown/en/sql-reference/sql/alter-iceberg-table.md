# ALTER ICEBERG TABLE

Modifies properties such as clustering options and tags for an existing [Apache Iceberg™ table](/user-guide/tables-iceberg).

Note

To replace the catalog integration for an externally managed Iceberg table in a standard Snowflake database with a different
catalog integration, see [SYSTEM$SET\_CATALOG\_INTEGRATION](/sql-reference/functions/system_set_catalog_integration).

You can also use an ALTER ICEBERG TABLE statement to refresh a table, convert a table, or alter a structured type column. The syntax for those operations varies
considerably. To view the syntax, parameter descriptions, usage notes, and examples for refreshing or converting an Iceberg table,
see the following pages:

- [ALTER ICEBERG TABLE … REFRESH](/sql-reference/sql/alter-iceberg-table-refresh)
- [ALTER ICEBERG TABLE … CONVERT TO MANAGED](/sql-reference/sql/alter-iceberg-table-convert-to-managed)
- [ALTER ICEBERG TABLE … ALTER COLUMN … SET DATA TYPE (structured types)](/sql-reference/sql/alter-iceberg-table-alter-column-set-data-type)

This topic refers to Iceberg tables as simply “tables” except where specifying *Iceberg tables* avoids confusion.

See also:
:   [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) , [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) , [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) , [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table)

## Syntax

Copy code

```
ALTER ICEBERG TABLE [ IF EXISTS ] <table_name> { clusteringAction | tableColumnAction }

ALTER ICEBERG TABLE [ IF EXISTS ] <table_name> SET
  [ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
  [ CATALOG_SYNC = '<snowflake_open_catalog_integration_name>']
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ AUTO_REFRESH = { TRUE | FALSE } ]
  [ TARGET_FILE_SIZE = { AUTO | 16MB | 32MB | 64MB | 128MB } ]
  [ PATH_LAYOUT = { FLAT | HIERARCHICAL } ]
  [ CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
  [ LOG_EVENT_LEVEL = { ERROR | WARN | DEBUG } ]
  [ ERROR_LOGGING = { TRUE | FALSE } ]
  [ ENABLE_DATA_COMPACTION = { TRUE | FALSE } ]
  [ ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' } ]
  [ ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE } ]

ALTER ICEBERG TABLE [ IF EXISTS ] <table_name> UNSET
  [ REPLACE_INVALID_CHARACTERS ]
  [ LOG_EVENT_LEVEL ]
  [ ERROR_LOGGING ]
  [ ENABLE_DATA_COMPACTION ]
  [ ICEBERG_MERGE_ON_READ_BEHAVIOR ]
  [ ENABLE_ICEBERG_MERGE_ON_READ ]

ALTER ICEBERG TABLE [ IF EXISTS ] dataGovnPolicyTagAction

ALTER ICEBERG TABLE [ IF EXISTS ] <table_name> searchOptimizationAction
```

Where:

> Copy code
>
> ```
> clusteringAction ::=
>   {
>      CLUSTER BY ( <expr> [ , <expr> , ... ] )
>      /* { SUSPEND | RESUME } RECLUSTER is valid action */
>    | { SUSPEND | RESUME } RECLUSTER
>    | DROP CLUSTERING KEY
>   }
> ```
>
> Copy code
>
> ```
> tableColumnAction ::=
>   {
>      ADD [ COLUMN ] [ IF NOT EXISTS ] <col_name> <col_type> [ DEFAULT <col_default> ]
>         [ inlineConstraint ]
>         [ COLLATE '<collation_specification>' ]
>
>    | RENAME COLUMN <col_name> TO <new_col_name>
>
>    | ALTER | MODIFY [ ( ]
>                           , [ COLUMN ] <col1_name> { [ SET ] NOT NULL | DROP NOT NULL }
>                           , [ COLUMN ] <col1_name> [ [ SET DATA ] TYPE ] <type>
>                           , [ COLUMN ] <col1_name> COMMENT '<string>'
>                           , [ COLUMN ] <col1_name> UNSET COMMENT
>                           , [ COLUMN ] <col1_name> SET WRITE DEFAULT <col_write_default>
>                           , [ COLUMN ] <col1_name> DROP WRITE DEFAULT
>                         [ , [ COLUMN ] <col2_name> ... ]
>                         [ , ... ]
>                     [ ) ]
>
>    | DROP [ COLUMN ] [ IF EXISTS ] <col1_name> [, <col2_name> ... ]
>   }
>
>   inlineConstraint ::=
>     [ NOT NULL ]
>     [ CONSTRAINT <constraint_name> ]
>     {
>         UNIQUE
>       | PRIMARY KEY
>       | [ FOREIGN KEY ] REFERENCES <ref_table_name> [ ( <ref_col_name> ) ]
>       | CHECK ( <expr> )
>     }
>     [ <constraint_properties> ]
> ```
>
> Copy code
>
> ```
> dataGovnPolicyTagAction ::=
>   {
>       SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
>     | UNSET TAG <tag_name> [ , <tag_name> ... ]
>   }
>   |
>   {
>       ADD ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] )
>     | DROP ROW ACCESS POLICY <policy_name>
>     | DROP ROW ACCESS POLICY <policy_name> ,
>         ADD ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] )
>     | DROP ALL ROW ACCESS POLICIES
>   }
>   |
>   {
>       SET AGGREGATION POLICY <policy_name>
>         [ ENTITY KEY ( <col_name> [, ... ] ) ]
>         [ FORCE ]
>     | UNSET AGGREGATION POLICY
>   }
>   |
>   {
>       SET JOIN POLICY <policy_name>
>         [ FORCE ]
>     | UNSET JOIN POLICY
>   }
>   |
>   ADD [ COLUMN ] [ IF NOT EXISTS ] <col_name> <col_type>
>     [ [ WITH ] MASKING POLICY <policy_name>
>           [ USING ( <col1_name> , <cond_col_1> , ... ) ] ]
>     [ [ WITH ] PROJECTION POLICY <policy_name> ]
>     [ [ WITH ] TAG ( <tag_name> = '<tag_value>'
>           [ , <tag_name> = '<tag_value>' , ... ] ) ]
>   |
>   {
>     { ALTER | MODIFY } [ COLUMN ] <col1_name>
>         SET MASKING POLICY <policy_name>
>           [ USING ( <col1_name> , <cond_col_1> , ... ) ] [ FORCE ]
>       | UNSET MASKING POLICY
>   }
>   |
>   {
>     { ALTER | MODIFY } [ COLUMN ] <col1_name>
>         SET PROJECTION POLICY <policy_name>
>           [ FORCE ]
>       | UNSET PROJECTION POLICY
>   }
>   |
>   { ALTER | MODIFY } [ COLUMN ] <col1_name> SET TAG
>       <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
>       , [ COLUMN ] <col2_name> SET TAG
>           <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
>   |
>   { ALTER | MODIFY } [ COLUMN ] <col1_name> UNSET TAG <tag_name> [ , <tag_name> ... ]
>                    , [ COLUMN ] <col2_name> UNSET TAG <tag_name> [ , <tag_name> ... ]
> ```
>
> Copy code
>
> ```
> searchOptimizationAction ::=
>   {
>      ADD SEARCH OPTIMIZATION [
>        ON <search_method_with_target> [ , <search_method_with_target> ... ]
>      ]
>
>    | DROP SEARCH OPTIMIZATION [
>        ON { <search_method_with_target> | <column_name> | <expression_id> }
>           [ , ... ]
>      ]
>   }
> ```
>
> For details, see [Search optimization actions ()](#label-alter-iceberg-table-searchoptimizationaction).

## Parameters

`table_name`
:   Identifier for the table to modify.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Specifies one or more properties/parameters to set for the external table (separated by blank spaces, commas, or new lines):

    `REPLACE_INVALID_CHARACTERS = { TRUE | FALSE }`
    :   Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results.
        You can only set this parameter for tables that use an external Iceberg catalog.

        - `TRUE` replaces invalid UTF-8 characters with the Unicode replacement character.
        - `FALSE` leaves invalid UTF-8 characters unchanged. Snowflake returns a user error message when it encounters invalid UTF-8
          characters in a Parquet data file.

        If not specified, the Iceberg table defaults to the parameter value for the schema, database, or account.
        The schema takes precedence over the database, and the database takes precedence over the account.

        Default: `FALSE`

    `CATALOG_SYNC = 'snowflake_open_catalog_integration_name'`
    :   Specifies the name of a catalog integration configured for [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview). Snowflake syncs
        the table with an external catalog in your Snowflake Open Catalog account. For more information about syncing Snowflake-managed Iceberg tables with Open Catalog, see [Sync a Snowflake-managed table with Snowflake Open Catalog](/user-guide/tables-iceberg-open-catalog-sync).

        For more information about this parameter, see [CATALOG\_SYNC](/sql-reference/parameters#label-catalog-sync).

    `DATA_RETENTION_TIME_IN_DAYS = integer`
    :   Specifies the retention period for a Snowflake-managed table so that Time Travel actions (SELECT, CLONE, UNDROP) can be performed on historical
        data in the table. For more information, see [Understanding & using Time Travel](/user-guide/data-time-travel).

        For a detailed description of this object-level parameter, as well as more information about object parameters, see
        [Parameters](/sql-reference/parameters).

        Values:

        > - Standard Edition: `0` or `1`
        > - Enterprise Edition: `0` to `90` for permanent tables

        Default:

        > - Standard Edition: `1`
        > - Enterprise Edition (or higher): `1` (unless a different default value was specified at the schema, database, or account level)

        Note

        A value of `0` effectively disables Time Travel for the table.

    `AUTO_REFRESH = { TRUE | FALSE }`
    :   Specifies whether Snowflake should automatically poll the external Iceberg catalog that is associated with the table for metadata updates.

        If no value is specified for the `REFRESH_INTERVAL_SECONDS` parameter on the catalog integration, Snowflake uses a default
        refresh interval of 30 seconds.

        For more information, see [automated refresh](/user-guide/tables-iceberg-auto-refresh).

        Default: FALSE

        > Note
        >
        > Using AUTO\_REFRESH with INFER\_SCHEMA isn’t supported.

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

    `PATH_LAYOUT = { FLAT | HIERARCHICAL }`
    :   Specifies the path layout that Snowflake uses when writing Parquet data files to the table. You can set this parameter for an existing table.

        For more information about this parameter, see [PATH\_LAYOUT](/sql-reference/parameters#label-path-layout).

    `CONTACT purpose = contact [ , purpose = contact ... ]`
    :   Associate the existing object with one or more [contacts](/user-guide/contacts-using). For a list of valid purposes, see [Associate a contact with an object](/user-guide/contacts-using#label-contacts-associate).

        You cannot set the CONTACT property with other properties in the same statement.

    `LOG_EVENT_LEVEL = { ERROR | WARN | DEBUG }`
    :   Specifies the severity level of automated refresh log events that should be ingested and made available in the active event table.
        The [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) parameter determines which events to capture based on the following values:

        - `ERROR`: Events that signal a change requiring human intervention to resolve.
        - `WARN`: Events that signal an issue that can be resolved without human intervention.
        - `DEBUG`: High-volume events.

        Note

        There is no default severity level. To capture events, you must set the severity level at either the
        Iceberg table level or account level.

        For more information, see [Monitor automated refresh events](/user-guide/tables-iceberg-auto-refresh#label-tables-iceberg-auto-refresh-events).

`ERROR_LOGGING = { TRUE | FALSE }`
:   Specifies whether to turn on DML error logging for the table.

    - `TRUE` turns on DML error logging for the table.
    - `FALSE` turns off DML error logging for the table.

    For more information, see [DML error logging](/user-guide/data-load-overview#label-data-load-overview-dml-error-logging).

    Note

    If the [OPT\_OUT\_ERROR\_LOGGING](/sql-reference/parameters#label-opt-out-error-logging) parameter is set to `TRUE` for a session,
    DML error logging isn’t turned on, regardless of whether it is turned on for specific tables.

`ENABLE_DATA_COMPACTION = { TRUE | FALSE }`
:   Specifies whether Snowflake should enable data compaction on the table. You can only set this parameter for Snowflake-managed tables.

    > - `TRUE`: Snowflake performs data compaction on the table.
    > - `FALSE`: Snowflake doesn’t perform data compaction on the table.
    >
    > Default: `TRUE`
    >
    > For more information, see [ENABLE\_DATA\_COMPACTION](/sql-reference/parameters#label-enable-data-compaction) and [Set data compaction](/user-guide/tables-iceberg-manage#label-tables-iceberg-manage-set-data-compaction).

    `ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' }`
    :   Specifies how Snowflake performs row-level updates (UPDATE, DELETE, MERGE) on this Apache Iceberg™ table. Selects between merge-on-read
        (which writes Iceberg delete files alongside the data) and copy-on-write (which rewrites entire data files).

        If you don’t set this parameter, the Iceberg table inherits the setting from the schema, database, or account. The schema takes
        precedence over the database, and the database takes precedence over the account.

        The parameter values are case-insensitive.

        Values:
        :   `'AUTO'`: Snowflake selects merge-on-read or copy-on-write based on the table’s Iceberg format version and management mode. For details,
            see [ICEBERG\_MERGE\_ON\_READ\_BEHAVIOR parameter](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior).

            `'ENABLED'`: The table uses merge-on-read. For tables that conform to v2 of the Apache Iceberg™ table specification, Snowflake writes positional
            delete files for row-level deletes. For tables that conform to v3, Snowflake writes deletion vectors when conditions are met.

            `'DISABLED'`: The table uses copy-on-write for all DML operations.

        Default:
        :   `'AUTO'`

        For a detailed description of this parameter, see [ICEBERG\_MERGE\_ON\_READ\_BEHAVIOR parameter](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior).

    `ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE }`
    :   Warning

        This parameter is deprecated. Use [`ICEBERG_MERGE_ON_READ_BEHAVIOR`](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior) instead.
        The legacy parameter is still honored when `ICEBERG_MERGE_ON_READ_BEHAVIOR` is at its default (`'AUTO'`), but it will return an
        error in a future release.

        Specifies whether the table uses merge-on-read behavior.

        If you don’t set this parameter, the Iceberg table defaults to the merge-on-read behavior that is specified for the schema, database,
        or account. The schema takes precedence over the database, and the database takes precedence over the account.

        Values:

        `TRUE`: The table uses merge-on-read behavior. Depending on whether the table conforms to v2 or v3 of the
        Apache Iceberg™ table specification, the behavior is as described in the following list:

        - If the table conforms with v2, Snowflake uses positional delete files for row-level deletes.
        - If the table conforms with v3, Snowflake uses deletion vectors for row-level deletes when conditions are met.

        **Note:** Setting this parameter to `TRUE` does **not** enable merge-on-read for Snowflake-managed v2 Iceberg tables. When `ICEBERG_MERGE_ON_READ_BEHAVIOR` is at its default (`'AUTO'`), this setting routes through the auto matrix, which keeps Snowflake-managed v2 tables on copy-on-write. To enable merge-on-read for a Snowflake-managed v2 table, set `ICEBERG_MERGE_ON_READ_BEHAVIOR = 'ENABLED'` on the table, schema, database, or account.

        `FALSE`: The table uses copy-on-write behavior.

        Default: `TRUE`

        For a detailed description of this parameter, see [Deprecated: ENABLE\_ICEBERG\_MERGE\_ON\_READ](/user-guide/tables-iceberg-manage#label-enable-iceberg-merge-on-read).

`UNSET`
:   Currently, you can only unset the following parameters with this command:

    > - `REPLACE_INVALID_CHARACTERS`
    > - `CATALOG_SYNC`
    > - `LOG_EVENT_LEVEL`
    > - `ENABLE_DATA_COMPACTION`
    > - `ICEBERG_MERGE_ON_READ_BEHAVIOR`
    > - `ENABLE_ICEBERG_MERGE_ON_READ`

## Clustering actions (`clusteringAction`)

Note

Clustering is only supported for tables that use Snowflake as the Iceberg catalog.

`CLUSTER BY ( expr [ , expr , ... ] )`
:   Specifies (or modifies) one or more table columns or column expressions as the clustering key for the table. These are the
    columns/expressions for which clustering is maintained by [Automatic Clustering](/user-guide/tables-auto-reclustering).

    To learn more about clustering, see [Clustering Keys & Clustered Tables](/user-guide/tables-clustering-keys).

`SUSPEND | RESUME RECLUSTER`
:   Enables or disables [Automatic Clustering](/user-guide/tables-auto-reclustering) for the table.

`DROP CLUSTERING KEY`
:   Drops the clustering key for the table.

For more information about clustering keys and reclustering, see [Understanding Snowflake Table Structures](/user-guide/tables-micro-partitions).

## Table column actions (`tableColumnAction`)

`ADD [ COLUMN ] [ IF NOT EXISTS ] col_name col_data_type [ DEFAULT col_default ]` `[ inlineConstraint ]` `[ COLLATE 'collation_specification' ] [ , ... ]`
:   > Adds a new column. You can specify a default value, an inline constraint, and a [collation specification](/sql-reference/collation#label-collate-clause).
    >
    > For additional details about table column actions, see:
    >
    > - [CREATE | ALTER TABLE … CONSTRAINT](/sql-reference/sql/create-table-constraint)
    > - [CREATE MASKING POLICY](/sql-reference/sql/create-masking-policy)
    > - [CREATE TAG](/sql-reference/sql/create-tag)
    >
    > You can perform ADD COLUMN operations on multiple columns in the same command.
    >
    > If you aren’t sure whether the column already exists, you can specify IF NOT EXISTS when adding the column. If the column already
    > exists, ADD COLUMN has no effect on the existing column and doesn’t result in an error.
    >
    > Note
    >
    > You can’t specify IF NOT EXISTS if you are also specifying any of the following for the new column:
    >
    > - AUTOINCREMENT, or IDENTITY
    > - UNIQUE, PRIMARY KEY, or FOREIGN KEY

    `DEFAULT col_default`
    :   For Iceberg version 3 (v3) tables only, specifies the default value for the column. If the data type for the
        column is string, you must surround the default value with single quotes.

        The value you specify is used as both the initial default and write default for the column. To change the write default for the column,
        use ALTER ICEBERG TABLE … ALTER COLUMN … SET WRITE DEFAULT.

        Important

        When you specify a default value for a column, you must specify a static value; you can’t specify an expression or
        function for the value. This requirement is in accordance with the Iceberg v3 specification and applies to both the initial default
        and write default.

        For more information about using default values with Iceberg tables, see [Use default values with Iceberg tables](/user-guide/tables-iceberg-manage#label-tables-iceberg-default-values).

`RENAME COLUMN col_name to new_col_name`
:   Renames the specified column to a new name that’s not currently used for any other columns in the table.

    You can’t rename a column that’s part of a clustering key.

    When you rename an object, such as a table or column, you must update other objects that reference it with the new name.

`{ ALTER | MODIFY } COLUMN col_name ...`
:   > Modifies the properties for a column.

    `SET WRITE DEFAULT col_default`
    :   For Iceberg version 3 (v3) tables only, specifies the write default value for the column. If the data type for the
        column is string, you must surround the default value with single quotes.

        If the column already has a write default, you can use this setting to change the write default.

        Important

        When you specify a default value for a column, you must specify a static value; you can’t specify an expression or
        function for the value. This requirement is in accordance with the Iceberg v3 specification and applies to both the initial default
        and write default.

        For more information about using default values with Iceberg tables, see [Use default values with Iceberg tables](/user-guide/tables-iceberg-manage#label-tables-iceberg-default-values).

    `DROP WRITE DEFAULT`
    :   For Iceberg version 3 (v3) tables only, drops the write default value for the column.

        For more information about using default values with Iceberg tables, see [Use default values with Iceberg tables](/user-guide/tables-iceberg-manage#label-tables-iceberg-default-values).

`DROP COLUMN [ IF EXISTS ] col_name [ CASCADE | RESTRICT ]`
:   Removes the specified column from the table.

    If you aren’t sure whether the column already exists, you can specify IF EXISTS when dropping the column. If the column doesn’t
    exist, DROP COLUMN has no effect and doesn’t result in an error.

    Dropping a column is a metadata-only operation. It doesn’t immediately re-write the micro-partitions and
    therefore doesn’t immediately free up the space used by the column. Typically, the space within an individual
    micro-partition is freed the next time that the micro-partition is re-written, which is typically when a write is
    done either due to DML (INSERT, UPDATE, DELETE) or re-clustering.

## Data Governance policy and tag actions (`dataGovnPolicyTagAction`)

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`policy_name`
:   Identifier for the policy; must be unique for your schema.

The following clauses apply to all table kinds that support row access policies, such as but not limited to tables, views, and event tables.
To simplify, the clauses just refer to “table.”

> `ADD ROW ACCESS POLICY policy_name ON (col_name [ , ... ])`
> :   Adds a row access policy to the table.
>
>     At least one column name must be specified. Additional columns can be specified with a comma separating each column name. Use this
>     expression to add a row access policy to both an event table and an external table.
>
> `DROP ROW ACCESS POLICY policy_name`
> :   Drops a row access policy from the table.
>
>     Use this clause to drop the policy from the table.
>
> `DROP ROW ACCESS POLICY policy_name, ADD ROW ACCESS POLICY policy_name ON ( col_name [ , ... ] )`
> :   Drops the row access policy that is set on the table and adds a row access policy to the same table in a single SQL statement.
>
> `DROP ALL ROW ACCESS POLICIES`
> :   Drops all [row access policy](/user-guide/security-row-using) associations from the table.
>
>     This expression is helpful when a row access policy is dropped from a schema before dropping the policy from an event table. Use this expression to drop row access policy associations from the table.
>
>     Suppose that a row access policy applied to the table when the backup was created, and the policy was later dropped. After you
>     restore the table from a [backup](/user-guide/backups), you can’t query it until you run an ALTER TABLE command with the
>     DROP ALL ROW ACCESS POLICIES clause.
>
> `SET AGGREGATION POLICY policy_name`
> :   `[ ENTITY KEY (col_name [ , ... ]) ] [ FORCE ]`
>     :   Assigns an [aggregation policy](/user-guide/aggregation-policies) to the table.
>
>         Use the optional ENTITY KEY parameter to define which columns uniquely identity an entity within the table. For more information, see
>         [Implementing entity-level privacy with aggregation policies](/user-guide/aggregation-policies-entity-privacy).
>
>         Use the optional FORCE parameter to atomically replace an existing aggregation policy with the new aggregation policy.
>
> `UNSET AGGREGATION POLICY`
> :   Detaches an aggregation policy from the table.
>
> `SET JOIN POLICY policy_name`
> :   `[ FORCE ]`
>     :   Assigns a [join policy](/user-guide/join-policies) to the table.
>
>         Use the optional FORCE parameter to atomically replace an existing join policy with the new join policy.
>
> `UNSET JOIN POLICY`
> :   Detaches a join policy from the table.

`{ ALTER | MODIFY } [ COLUMN ] ...`
:   `USING ( col_name , cond_col_1 ... )`
    :   Specifies the arguments to pass into the conditional masking policy SQL expression.

        The first column in the list specifies the column for the policy conditions to mask or tokenize the data and must match the
        column to which the masking policy is set.

        The additional columns specify the columns to evaluate to determine whether to mask or tokenize the data in each row of the query
        result when a query is made on the first column.

        If the USING clause is omitted, Snowflake treats the conditional masking policy as a normal
        [masking policy](/user-guide/security-column-intro).

    `FORCE`
    :   Replaces a masking or projection policy that is currently set on a column with a different policy in a single statement.

        Note that using the `FORCE` keyword with a masking policy requires the [data type](/sql-reference-data-types) of the policy
        in the ALTER TABLE statement (i.e. STRING) to match the data type of the masking policy currently set on the column (i.e. STRING).

        If a masking policy is not currently set on the column, specifying this keyword has no effect.

        For details, see: [Replace a masking policy on a column](/user-guide/security-column-intro#label-security-column-intro-replace-policy) or [Replace a projection policy](/user-guide/projection-policies#label-projection-policy-replace).

## Search optimization actions (`searchOptimizationAction`)

`ADD SEARCH OPTIMIZATION`
:   Adds [search optimization](/user-guide/search-optimization-service) for the entire table or, if you specify the optional
    ON clause, for specific columns.

    Note

    Search optimization can be expensive to maintain, especially if the data in the table changes frequently.
    For more information, see [Search optimization cost estimation and management](/user-guide/search-optimization/cost-estimation#label-search-optimization-maintenance-billing).

`ON search_method_with_target [, search_method_with_target ... ]`
:   Specifies that you want to configure search optimization for specific columns (instead of the entire table).

    For `search_method_with_target`, use an expression with the following syntax:

    Copy code

    ```
    <search_method>( <target> [ , <target> , ... ] [ , ANALYZER => '<analyzer_name>' ] )
    ```

    Where:

    - `search_method` specifies one of the following methods that optimizes queries for a particular type of predicate:

      | Search method | Description |
      | --- | --- |
      | `FULL_TEXT` | Predicates that use VARCHAR (text) types. |
      | `EQUALITY` | Equality and IN predicates. |
      | `SUBSTRING` | Predicates that match substrings and regular expressions (for example, [[ NOT ] LIKE](/sql-reference/functions/like), [[ NOT ] ILIKE](/sql-reference/functions/ilike), [[ NOT ] RLIKE](/sql-reference/functions/rlike), and [REGEXP\_LIKE](/sql-reference/functions/regexp_like)). |

      Expand

      Show lessSee more
    - `target` specifies the column or an asterisk (\*).

      Depending on the value of `search_method`, you can specify a column of one of the following types:

      | Search method | Supported targets |
      | --- | --- |
      | `FULL_TEXT` | Columns of VARCHAR (text) data types. |
      | `EQUALITY` | Columns of numerical, string, and binary data types. |
      | `SUBSTRING` | Columns of VARCHAR (text) data types. |

      Expand

      Show lessSee more

      To specify all applicable columns in the table as targets, use an asterisk (`*`).

      Note that you can’t specify both an asterisk and specific column names for a given search method. However, you can
      specify an asterisk in different search methods.

      For example, you can specify the following expressions:

      Copy code

      ```
      -- Allowed
      ON SUBSTRING(*)
      ON EQUALITY(*), SUBSTRING(*)
      ```

      You can’t specify the following expressions:

      Copy code

      ```
      -- Not allowed
      ON EQUALITY(*, c1)
      ON EQUALITY(c1, *)
      ON EQUALITY(v1:path, *)
      ON EQUALITY(c1), EQUALITY(*)
      ```

    - `ANALYZER => 'analyzer_name'` specifies the name of the text analyzer, if `search_method`
      is `FULL_TEXT`.

      For more information about search optimization analyzers, see [ALTER TABLE](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-analyzer).

    To specify more than one search method on a target, use a comma to separate each subsequent method and target:

    Copy code

    ```
    ALTER ICEBERG TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1), EQUALITY(c2, c3);
    ```

    If you run the ALTER ICEBERG TABLE … ADD SEARCH OPTIMIZATION ON … command multiple times on the same table, each subsequent command
    adds to the existing configuration for the table. For example, suppose that you run the following commands:

    Copy code

    ```
    ALTER ICEBERG TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1, c2);
    ALTER ICEBERG TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c3, c4);
    ```

    This adds equality predicates for the columns c1, c2, c3, and c4 to the configuration for the table. This is equivalent to
    running the command:

    Copy code

    ```
    ALTER ICEBERG TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1, c2, c3, c4);
    ```

    For examples, see [Enabling search optimization for specific columns](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-adding).

`DROP SEARCH OPTIMIZATION`
:   Removes [search optimization](/user-guide/search-optimization-service) for the entire table or, if you specify the
    optional ON clause, from specific columns.

    Note

    - If a table has the search optimization property, then dropping the table and undropping it preserves the
      search optimization property.
    - Removing the search optimization property from a table and then adding it back incurs the same cost as adding it the first
      time.

`ON search_method_with_target | column_name | expression_id [ , ... ]`
:   Specifies that you want to drop the search optimization configuration for specific columns (instead of
    dropping search optimization for the entire table).

    To identify the column configuration to drop, specify one of the following:

    - For `search_method_with_target`, specify a method for optimizing queries for one or more specific columns. Use the
      [syntax described earlier](/sql-reference/sql/alter-iceberg-table#label-alter-iceberg-table-searchoptimizationaction-search-method-target).
    - For `column_name`, specify the name of the column configured for search optimization. Specifying the column name drops
      all expressions for that column.
    - For `expression_id`, specify the ID for an expression listed in the output of the
      [DESCRIBE SEARCH OPTIMIZATION](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-displaying) command.

    To specify more than one of these, use a comma between items.

    You can specify any combination of search methods with targets, column names, and expression IDs.

    For examples, see [Dropping search optimization for specific columns](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-dropping).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Iceberg table | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| USAGE | External volume |  |
| USAGE | Catalog integration | Required if the table uses a catalog integration. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Only the table owner (that is, the role with the OWNERSHIP privilege on the table) or higher can execute this command.
- Clustering is only supported for tables that use Snowflake as the Iceberg catalog. To add clustering to an Iceberg table,
  you must also have the USAGE or OWNERSHIP privileges on the schema and database that contain the table.
- For tables in a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database), the following features aren’t supported:

  - Setting the NOT NULL, COMMENT, and DATA TYPE properties for an existing column.
  - Setting column constraints.
  - Clustering.
- You can use data metric functions with Iceberg tables by executing an [ALTER TABLE](/sql-reference/sql/alter-table) command. For more information, see
  [Use SQL to set up data metric functions](/user-guide/data-quality-working).
- For more information about using search optimization with Iceberg tables, including limitations, see
  [Support for Apache Iceberg™ tables](/user-guide/search-optimization/queries-that-benefit#label-search-optimization-service-iceberg) in the search optimization documentation.
- Regarding metadata:

  Attention
- To troubleshooting issues with altering the CATALOG\_SYNC parameter, see [You can’t alter an Iceberg table when specifying the CATALOG\_SYNC parameter](/user-guide/tables-iceberg-open-catalog-troubleshooting#label-alter-iceberg-table-catalog-sync-parameter-troubleshooting)

## Examples

The following example sets a tag (`my_tag`) with a value of `customer` on an Iceberg table.

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table SET TAG my_tag = 'customer';
```

The following example enables [automated refresh](/user-guide/tables-iceberg-auto-refresh) for an existing externally managed table:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table SET AUTO_REFRESH = TRUE;
```

The following examples add and drop search optimization for an Iceberg table:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table ADD SEARCH OPTIMIZATION ON SUBSTRING(C6);

ALTER ICEBERG TABLE my_iceberg_table DROP SEARCH OPTIMIZATION ON EQUALITY(C7, C8);
```
