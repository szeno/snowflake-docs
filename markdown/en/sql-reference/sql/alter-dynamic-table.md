# ALTER DYNAMIC TABLE

Modifies the properties of a [dynamic table](/user-guide/dynamic-tables/overview).

See also:
:   [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table), [DESCRIBE DYNAMIC TABLE](/sql-reference/sql/desc-dynamic-table), [DROP DYNAMIC TABLE](/sql-reference/sql/drop-dynamic-table), [SHOW DYNAMIC TABLES](/sql-reference/sql/show-dynamic-tables)

Note

Frozen regions were previously named immutability constraints, and the `FROZEN WHERE` clause previously used the syntax `IMMUTABLE WHERE`. The legacy `IMMUTABLE WHERE` syntax continues to be supported, and `SHOW DYNAMIC TABLES` still uses the `immutable_where` column.

## Syntax

Copy code

```
ALTER DYNAMIC TABLE [ IF EXISTS ] <name> { SUSPEND | RESUME }

ALTER DYNAMIC TABLE [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER DYNAMIC TABLE [ IF EXISTS ] <name> SWAP WITH <target_dynamic_table_name>

ALTER DYNAMIC TABLE [ IF EXISTS ] <name> [ , <name> ... ] REFRESH [ COPY SESSION ]

ALTER DYNAMIC TABLE [ IF EXISTS ] <name> { clusteringAction }

ALTER DYNAMIC TABLE [ IF EXISTS ] <name> { tableColumnCommentAction }

ALTER DYNAMIC TABLE <name> { SET | UNSET } COMMENT = '<string_literal>'

ALTER DYNAMIC TABLE [ IF EXISTS ] <name> dataGovnPolicyTagAction

ALTER DYNAMIC TABLE [ IF EXISTS ] <name> searchOptimizationAction

ALTER DYNAMIC TABLE [ IF EXISTS ] <name> storageLifecyclePolicyAction

ALTER DYNAMIC TABLE [ IF EXISTS ] <name> SET
  [ TARGET_LAG = { '<num> { seconds | minutes | hours | days }'  | DOWNSTREAM } ],
  [ SCHEDULER = DISABLE | ENABLE ],
  [ WAREHOUSE = <warehouse_name> ],
  [ INITIALIZATION_WAREHOUSE = <warehouse_name> ],
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ],
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ DEFAULT_DDL_COLLATION = '<collation_specification>' ],
  [ LOG_LEVEL = '<log_level>' ],
  [ CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ],
  [ FROZEN WHERE ( <expr> ) ],
  [ EXECUTE AS USER <user_name>
    [ USE SECONDARY ROLES { ALL | NONE | <role> [ , ... ] } ]
  ]
  [ ROW_TIMESTAMP = { TRUE | FALSE } ]

ALTER DYNAMIC TABLE [ IF EXISTS ] <name> UNSET
  [ INITIALIZATION_WAREHOUSE ],
  [ DATA_RETENTION_TIME_IN_DAYS ],
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS ],
  [ DEFAULT_DDL_COLLATION ],
  [ LOG_LEVEL ],
  [ CONTACT <purpose> ],
  [ FROZEN WHERE ],
  [ EXECUTE AS USER ],
  [ ROW_TIMESTAMP ],
  [ DCM PROJECT ]
```

Where:

> Copy code
>
> ```
> clusteringAction ::=
>   {
>     CLUSTER BY ( <expr> [ , <expr> , ... ] )
>     | { SUSPEND | RESUME } RECLUSTER
>     | DROP CLUSTERING KEY
>   }
> ```
>
> For more information, see [Clustering Keys & Clustered Tables](/user-guide/tables-clustering-keys).
>
> Copy code
>
> ```
> tableCommentAction ::=
>   {
>     ALTER | MODIFY [ ( ]
>                            [ COLUMN ] <col1_name> COMMENT '<string>'
>                          , [ COLUMN ] <col1_name> UNSET COMMENT
>                        [ , ... ]
>                    [ ) ]
>   }
> ```
>
> Copy code
>
> ```
> dataGovnPolicyTagAction ::=
>   {
>       ADD ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] )
>     | DROP ROW ACCESS POLICY <policy_name>
>     | DROP ROW ACCESS POLICY <policy_name> ,
>         ADD ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] )
>     | DROP ALL ROW ACCESS POLICIES
>   }
>   |
>   {
>     SET AGGREGATION POLICY <policy_name>
>       [ ENTITY KEY ( <col_name> [, ... ] ) ]
>       [ FORCE ]
>   | UNSET AGGREGATION POLICY
>   }
>   |
>   {
>     { ALTER | MODIFY } [ COLUMN ] <col1_name>
>         SET MASKING POLICY <policy_name>
>           [ USING ( <col1_name> , <cond_col_1> , ... ) ] [ FORCE ]
>       | UNSET MASKING POLICY
>   }
>   |
>   { ALTER | MODIFY } [ COLUMN ] <col1_name> SET TAG
>       <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
>       , [ COLUMN ] <col2_name> SET TAG
>           <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
>   |
>   {
>     { ALTER | MODIFY } [ COLUMN ] <col1_name>
>         SET PROJECTION POLICY <policy_name>
>           [ FORCE ]
>       | UNSET PROJECTION POLICY
> }
> |
>   { ALTER | MODIFY } [ COLUMN ] <col1_name> UNSET TAG <tag_name> [ , <tag_name> ... ]
>                   , [ COLUMN ] <col2_name> UNSET TAG <tag_name> [ , <tag_name> ... ]
>   }
>   |
>   {
>       SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
>     | UNSET TAG <tag_name> [ , <tag_name> ... ]
>   }
> ```
>
> Copy code
>
> ```
> searchOptimizationAction ::=
>   {
>     ADD SEARCH OPTIMIZATION [
>       ON <search_method_with_target> [ , <search_method_with_target> ... ]
>         [ EQUALITY ]
>       ]
>
>     | DROP SEARCH OPTIMIZATION [
>       ON { <search_method_with_target> | <column_name> | <expression_id> }
>         [ EQUALITY ]
>         [ , ... ]
>       ]
>
>     | SUSPEND SEARCH OPTIMIZATION [
>        ON { <search_method_with_target> | <column_name> | <expression_id> }
>           [ , ... ]
>      ]
>
>     | RESUME SEARCH OPTIMIZATION [
>        ON { <search_method_with_target> | <column_name> | <expression_id> }
>           [ , ... ]
>      ]
>   }
> ```
>
> For details, see [Search optimization actions (`searchOptimizationAction`)](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction).
>
> Copy code
>
> ```
> storageLifecyclePolicyAction ::=
>   {
>       ADD STORAGE LIFECYCLE POLICY <policy_name> ON ( <col_name> [ , <col_name> ... ] )
>     | DROP STORAGE LIFECYCLE POLICY
>   }
> ```
>
> For more information, see [Use storage lifecycle policies with dynamic tables](/user-guide/dynamic-tables/storage-lifecycle-policies).

## Parameters

`name`
:   Identifier for the dynamic table to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SUSPEND | RESUME`
:   Specifies the action to perform on the dynamic table:

    - `SUSPEND` suspends refreshes on the dynamic table. If the dynamic table is used
      by other dynamic tables, they are also suspended.
    - `RESUME` resumes refreshes on the dynamic table. Resume operations cascade
      downstream to all downstream dynamic tables not manually suspended.

    When `SCHEDULER = DISABLE`, the command isolates the dynamic table from pipeline scheduling. `TARGET_LAG`-based refresh is
    suspended, and a manual refresh on this dynamic table doesn’t cascade to upstream dynamic tables.

`RENAME TO new_name`
:   Renames the specified dynamic table with a new identifier that is not currently used by
    any other dynamic tables in the schema.

    Renaming a dynamic table requires the CREATE DYNAMIC TABLE privilege on the schema for
    the dynamic table.

    You can also move the dynamic table to a different database and/or schema while
    optionally renaming the dynamic table. To do so, specify a qualified `new_name`
    value that includes the new database and/or schema name in the form
    `db_name.schema_name.new_name` or `schema_name.new_name`,
    respectively.

    The following restrictions apply:

    - The destination database and/or schema must already exist. In addition, an object
      with the same name cannot already exist in the new location; otherwise, the
      statement returns an error.
    - You can’t move an object to a managed access schema unless the object owner
      (that is, the role that has the OWNERSHIP privilege on the object) also owns the
      target schema.
    - When an object (table, column, etc.) is renamed, other objects that reference it
      must be updated with the new name.

`SWAP WITH target_dynamic_table_name`
:   Swaps two dynamic tables in a single transaction. The role used to perform this
    operation must have OWNERSHIP privileges on both dynamic tables.

    The following restrictions apply:

    - You can only swap a dynamic table with another dynamic table.

`REFRESH [ COPY SESSION ]`
:   Manually refreshes one or more dynamic tables. You can list multiple dynamic tables to refresh
    in a single statement by separating their names with commas.

    Both user-suspended and auto-suspended dynamic tables can be manually refreshed.
    Manually refreshed dynamic tables return MANUAL as the output for `refresh_trigger`
    in the DYNAMIC\_TABLE\_REFRESH\_HISTORY function.

    When `SCHEDULER = DISABLE`, refreshing a single dynamic table only refreshes that table and doesn’t cascade to any other
    dynamic tables.

    When `SCHEDULER = ENABLE`, refreshing a dynamic table also refreshes all upstream dynamic tables, but the cascade
    stops at any upstream dynamic table that has `SCHEDULER = DISABLE`.

    Listing multiple dynamic tables in a single statement refreshes each listed dynamic table regardless of
    its `SCHEDULER` setting; `SCHEDULER = DISABLE` doesn’t remove a listed dynamic table from the refresh set.

    **Semantics for a multi-table list**

    Snowflake merges the upstream dependencies of every listed dynamic table into one pipeline and refreshes
    that pipeline at a single data timestamp. If two listed dynamic tables share an upstream, that upstream
    refreshes exactly once. Each listed dynamic table refreshes on its own configured warehouse. With
    `IF EXISTS`, Snowflake silently skips names in the list that don’t resolve to an existing dynamic
    table; the statement succeeds for the remaining dynamic tables.

    **Restrictions**

    - Every listed dynamic table must be a unique object. Duplicate names, including short names, quoted names, and fully qualified names that resolve to the same table, produce an error.
    - The statement can’t run inside a multi-statement transaction.
    - For a multi-table list, the role’s OPERATE (or OWNERSHIP) privilege must extend to every listed dynamic table and every upstream dynamic table that refreshes as part of the pipeline. See [Grant OPERATE to manage a dynamic table](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges-alter) for the general privilege model.
    - If any listed dynamic table ends in a `FAILED`, `UPSTREAM_FAILED`, or `CANCELLED` refresh status, the statement returns an error. Dynamic tables that already refreshed successfully remain refreshed; their refresh history rows aren’t rolled back.

    For error codes with causes and resolutions, see [Error code reference for dynamic tables](/user-guide/dynamic-tables/error-codes).

    For information on dynamic table refresh status, see [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history).

    `COPY SESSION`

    > Runs the refresh operation in a copy of the current session using the current user and
    > warehouse.
    >
    > This only applies to a single manual refresh; it does not permanently update the credentials for the dynamic table.
    > Use the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to transfer the ownership for scheduled
    > refreshes. For more information, see [Grant OWNERSHIP to transfer full control](/user-guide/dynamic-tables/privileges#label-dynamic-tables-manage-ownership).
    >
    > The primary role is the role that owns the dynamic table and secondary roles will match
    > the DEFAULT\_SECONDARY\_ROLES property of the user.

`SET ...`
:   Specifies one or more properties/parameters to set for the table (separated by blank
    spaces, commas, or new lines):

    `TARGET_LAG = { num { seconds | minutes | hours | days } | DOWNSTREAM }`
    :   > Specifies the target lag for the dynamic table:

        `'num seconds | minutes | hours | days'`
        :   Specifies the maximum amount of time that the dynamic table’s content should lag
            behind changes to the base tables.

            For example:

            - If the data in the dynamic table should lag by no more than 5 minutes, specify `5 minutes`.
            - If the data in the dynamic table should lag by no more than 5 hours, specify `5 hours`.

            The minimum value is 1 minute. If a dynamic table A depends on another dynamic
            table B, the minimum lag for A must be greater than or equal to the lag for B.

        `DOWNSTREAM`
        :   Specifies that the dynamic table should be refreshed if any dynamic table
            downstream of it is refreshed.

    `SCHEDULER = { DISABLE | ENABLE }`
    :   Specifies whether the dynamic table is to be refreshed automatically by Snowflake.

        `DISABLE`
        :   Excludes the dynamic table from automatic background refresh. The table isn’t refreshed on a schedule, either directly or
            through downstream dependencies.

        - Manual control: Refreshing must be triggered manually by using `ALTER DYNAMIC TABLE ... REFRESH`.
        - Isolation: A manual refresh of a disabled table doesn’t automatically refresh its upstream dependencies. This creates a “isolation
          boundary,” allowing external orchestrators, like dbt, to manage specific table refreshes in isolation without triggering the entire
          pipeline.
        - `TARGET_LAG` can’t be defined when `SCHEDULER = DISABLE`.

        `ENABLE`
        :   Enables automatic scheduling for the dynamic table. Snowflake refreshes the table alongside its dependencies to maintain snapshot consistency, scheduling refreshes to meet the defined `TARGET_LAG`.

    `WAREHOUSE = warehouse_name`
    :   Specifies the name of the warehouse that provides the compute resources for
        refreshing the dynamic table.

        You must use a role that has the USAGE privilege on this warehouse. For more information, see [Privilege quick reference](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges).

        For guidance on choosing a warehouse for optimal refresh performance, see [WAREHOUSE vs INITIALIZATION\_WAREHOUSE](/user-guide/dynamic-tables/warehouse-selection#label-dt-optimize-warehouse).

    `INITIALIZATION_WAREHOUSE = warehouse_name`
    :   Specifies a warehouse to use for all dynamic table [initializations and reinitializations](/user-guide/dynamic-tables/overview#label-dynamic-tables-initialization).

        When this parameter is set, the specified warehouse is used for all initializations and reinitializations; otherwise, the dynamic
        table uses the warehouse that is specified by the required WAREHOUSE parameter for all refreshes.

        You must use a role that has the USAGE privilege on this warehouse. For more information, see [Privilege quick reference](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges).

    `DATA_RETENTION_TIME_IN_DAYS = integer`
    :   Object-level parameter that modifies the retention period for the dynamic table for
        Time Travel. For more details, see [Understanding & using Time Travel](/user-guide/data-time-travel) and
        [Working with Temporary and Transient Tables](/user-guide/tables-temp-transient).

        For a detailed description of this parameter and more information about object
        parameters, see [Parameters](/sql-reference/parameters).

        Values:

        > - Standard Edition: `0` or `1`
        > - Enterprise Edition:
        >   - `0` to `90` for permanent dynamic tables
        >   - `0` or `1` for transient dynamic tables

        Note

        A value of `0` effectively disables Time Travel for the dynamic table.

    `MAX_DATA_EXTENSION_TIME_IN_DAYS = integer`
    :   Object parameter that specifies the maximum number of days Snowflake can extend the
        data retention period to prevent streams on the dynamic table from becoming stale.

        For a detailed description of this parameter, see
        [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-max-data-extension-time-in-days).

    `DEFAULT_DDL_COLLATION = 'collation_specification'`
    :   Specifies a default [collation specification](/sql-reference/collation#label-collation-specification)
        for any new columns added to the dynamic table.

        Setting this parameter does not change the collation specification for any
        existing columns.

        For more information, see [DEFAULT\_DDL\_COLLATION](/sql-reference/parameters#label-default-ddl-collation).

    `LOG_LEVEL = 'log_level'`
    :   Specifies the severity level of [events for this dynamic table](/user-guide/dynamic-tables/monitoring#label-dynamic-tables-monitoring-sql-events) that are
        ingested and made available in the active event table. Events at the specified level (and at more severe levels) are
        ingested.

        For more information about levels, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level). For information about setting the log level, see
        [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

    `CONTACT purpose = contact [ , purpose = contact ... ]`
    :   Associate the existing object with one or more [contacts](/user-guide/contacts-using). For a list of valid purposes, see [Associate a contact with an object](/user-guide/contacts-using#label-contacts-associate).

        You cannot set the CONTACT property with other properties in the same statement.

    `FROZEN WHERE`
    :   Specifies a condition that defines the frozen region of the dynamic table. For more
        information, see [Frozen regions and backfill](/user-guide/dynamic-tables/frozen-regions). If the dynamic table has
        primary key or unique constraints with the RELY property, the columns in the predicate must
        appear in every RELY PRIMARY KEY and RELY UNIQUE constraint (that is, the intersection of all
        RELY constraint column sets). For details, see
        [Interaction with RELY constraints](/user-guide/dynamic-tables/frozen-regions#label-dynamic-tables-frozen-rely-interaction).

    `EXECUTE AS USER user_name`
    :   Refreshes the dynamic table as the specified user, rather than as the SYSTEM user.

        To specify EXECUTE AS USER, you must use a role that has been granted the IMPERSONATE privilege on the `user_name` user. To grant this privilege,
        run the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) command.

        `USE SECONDARY ROLES { ALL | NONE | role [ , ... ] }`
        :   Specifies the secondary roles to use on the dynamic table. Can be used to override the default secondary roles that are otherwise used in execution.

            Can only be used with the EXECUTE AS USER option.

        For more information, see [Refresh with specific user privileges (EXECUTE AS USER)](/user-guide/dynamic-tables/privileges#label-dts-execute-as-user).

    `ROW_TIMESTAMP = { TRUE | FALSE }`
    :   Adds or removes row timestamps on the table.

        - `TRUE` adds row timestamps on the table.
        - `FALSE` removes row timestamps on the table. This parameter setting permanently deletes all stored METADATA$ROW\_LAST\_COMMIT\_TIME values.
          Reenabling it will not restore these values and Time Travel queries will return nothing.

`UNSET ...`
:   Specifies one or more properties/parameters to unset for the dynamic table, which
    resets them back to their defaults:

    - `INITIALIZATION_WAREHOUSE`
    - `DATA_RETENTION_TIME_IN_DAYS`
    - `MAX_DATA_EXTENSION_TIME_IN_DAYS`
    - `DEFAULT_DDL_COLLATION`
    - `LOG_LEVEL`
    - `CONTACT purposes`
    - `FROZEN WHERE`
    - `EXECUTE AS USER`
    - `ROW_TIMESTAMP`
    - `DCM PROJECT`

`UNSET DCM PROJECT`

> Detaches the dynamic table from the [DCM project](/user-guide/dcm-projects/dcm-projects-overview) that currently manages it.
> The command removes the association between the dynamic table and the DCM project without dropping the dynamic table. See [Detach objects from a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-detach-object) for more information.

## Clustering actions (`clusteringAction`)

`CLUSTER BY ( expr [ , expr , ... ] )`
:   Specifies (or modifies) one or more table columns or column expressions as the
    clustering key for the dynamic table. These are the columns/expressions for which
    clustering is maintained by Automatic Clustering. Before you specify a clustering key
    for a dynamic table, you should understand micro-partitions. For more information, see
    [Understanding Snowflake Table Structures](/user-guide/tables-micro-partitions).

    Note the following when using clustering keys with dynamic tables:

    - Column definitions are required and must be explicitly specified in the statement.
    - Clustering keys are not intended or recommended for all tables; they
      typically benefit very large (for example, multi-terabyte) tables.

`SUSPEND | RESUME RECLUSTER`
:   Enables or disables [Automatic Clustering](/user-guide/tables-auto-reclustering) for the dynamic table.

`DROP CLUSTERING KEY`
:   Drops the clustering key for the dynamic table.

For more information about clustering keys and reclustering, see [Understanding Snowflake Table Structures](/user-guide/tables-micro-partitions).

## Table comment actions (`tableCommentAction`)

`ALTER | MODIFY [ ( ]` `[ COLUMN ] <col1_name> COMMENT '<string>'` `, [ COLUMN ] <col1_name> UNSET COMMENT` `[ , ... ]` `[ ) ]`
:   Alters a comment or overwrites the existing comment for a column in the dynamic table.

`SET | UNSET COMMENT = '<string_literal>'`
:   Adds a comment or overwrites the existing comment for the dynamic table.

## Data Governance policy and tag actions (`dataGovnPolicyTagAction`)

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`policy_name`
:   Identifier for the policy; must be unique for your schema.

    `ADD ROW ACCESS POLICY policy_name ON (col_name [ , ... ])`
    :   Adds a row access policy to the dynamic table.

        At least one column name must be specified. Additional columns can be specified
        with a comma separating each column name.

    `DROP ROW ACCESS POLICY policy_name`
    :   Drops a row access policy from the dynamic table.

    `DROP ROW ACCESS POLICY policy_name, ADD ROW ACCESS POLICY policy_name ON ( col_name [ , ... ] )`
    :   Drops the row access policy that is set on the dynamic table and adds a row access
        policy to the same dynamic table in a single SQL statement.

    `DROP ALL ROW ACCESS POLICIES`
    :   Drops all [row access policy](/user-guide/security-row-using) associations from the dynamic table.

        You must also use this clause to access a dynamic table that you restore from a [backup](/user-guide/backups), if a
        row access policy applied to the table when the backup was created and the policy was later dropped. After the dynamic table
        is restored, you can’t query it until you run an ALTER TABLE command with the DROP ALL ROW ACCESS POLICIES clause.

    `{ ALTER | MODIFY } [ COLUMN ] ...`
    :   `USING ( col_name , cond_col_1 ... )`
        :   Specifies the arguments to pass into the conditional masking policy.

            The first column in the list specifies the data to be masked or tokenized based on
            policy conditions and must match the column to which the masking policy
            is applied.

            The additional columns specify which data to evaluate for masking or tokenization
            in each row of the query result when selecting from the first column.

            If the USING clause is omitted, Snowflake treats the conditional masking policy as a
            normal [masking policy](/user-guide/security-column-intro).

    `SET AGGREGATION POLICY {policy_name}`
    :   `[ ENTITY KEY ({col_name} [ , ... ]) ] [ FORCE ]`
        :   Assigns an [aggregation policy](/user-guide/aggregation-policies) to the dynamic table.

            Use the optional ENTITY KEY parameter to define which columns uniquely identity an entity within the dynamic table. For
            more information, see [Implementing entity-level privacy with aggregation policies](/user-guide/aggregation-policies-entity-privacy).

            Use the optional FORCE parameter to atomically replace an existing aggregation policy with the new aggregation policy.

    `UNSET AGGREGATION POLICY`
    :   Detaches an aggregation policy from the dynamic table.

    `FORCE`
    :   Replaces a masking or projection policy that is currently set on a column with a
        different policy in a single statement.

        Note that using the `FORCE` keyword with a masking policy requires the
        [data type](/sql-reference-data-types) of the policy in the ALTER DYNAMIC
        TABLE statement (i.e. STRING) to match the data type of the masking policy currently
        set on the column (i.e. STRING).

        If a masking policy is not currently set on the column, specifying this keyword has
        no effect.

        For details, see: [Replace a masking policy on a column](/user-guide/security-column-intro#label-security-column-intro-replace-policy) or
        [Replace a projection policy](/user-guide/projection-policies#label-projection-policy-replace).

## Search optimization actions (`searchOptimizationAction`)

`ADD SEARCH OPTIMIZATION`
:   Adds [search optimization](/user-guide/search-optimization-service) for the
    entire dynamic table or, if you specify the optional `ON` clause, for specific
    columns.

    Search optimization can be expensive to maintain, especially if the data in the table
    changes frequently. For more information, see
    [Search optimization cost estimation and management](/user-guide/search-optimization/cost-estimation#label-search-optimization-maintenance-billing).

`ON search_method_with_target [, search_method_with_target ... ]`
:   Specifies that you want to configure search optimization for specific columns or
    VARIANT fields (rather than the entire dynamic table).

    For `search_method_with_target`, use an expression with the following syntax:

    Copy code

    ```
    <search_method>(<target> [, ...])
    ```

    Where:

    - `search_method` specifies one of the following methods that optimizes
      queries for a particular type of predicate:

      - `GEO`: Predicates that use GEOGRAPHY types.
      - `SUBSTRING`: Predicates that match substrings and regular expressions (for
        example, [[ NOT ] LIKE](/sql-reference/functions/like), [[ NOT ] ILIKE](/sql-reference/functions/ilike),
        [[ NOT ] RLIKE](/sql-reference/functions/rlike), [REGEXP\_LIKE](/sql-reference/functions/regexp_like),
        etc.)
      - `EQUALITY`: Equality and IN predicates.
    - `target` specifies the column, VARIANT field, or an asterisk (\*).

      Depending on the value of `search_method`, you can specify a column or
      VARIANT field of one of the following types:

      - `GEO`: Columns of the GEOGRAPHY data type.
      - `SUBSTRING`: Columns of string or VARIANT data types, including paths to
        fields in VARIANTs. Specify paths to fields as described under `EQUALITY`;
        searches on nested fields are improved in the same way.
      - `EQUALITY`: Columns of numeric, string, binary, and VARIANT data types,
        including paths to fields in VARIANT columns.

        To specify a VARIANT field, use
        [dot or bracket notation](/user-guide/querying-semistructured#label-traversing-semistructured-data). For
        example:

        - `my_column:my_field_name.my_nested_field_name`
        - `my_column['my_field_name']['my_nested_field_name']`

        You may also use a colon-delimited path to the field. For example:

        - `my_column:my_field_name:my_nested_field_name`

        When you specify a VARIANT field, the configuration applies to all nested fields
        under that field.

        For example, if you specify `ON EQUALITY(src:a.b)`:

        - This configuration can improve queries `on src:a.b` and on any nested fields
          (for example, `src:a.b.c`, `src:a.b.c.d`, etc.).
        - This configuration only affects queries that use the `src:a.b` prefix (for
          example, `src:a`, `src:z`, etc.).

    To specify all applicable columns in the table as targets, use an asterisk (`*`).

    Note that you can’t specify both an asterisk and specific column names for a
    given search method. However, you can specify an asterisk in different search methods.

    For example, you can specify the following expressions:

    Copy code

    ```
    ON SUBSTRING(*)
    ON EQUALITY(*), SUBSTRING(*), GEO(*)
    ```

    You can’t specify the following expressions:

    Copy code

    ```
    ON EQUALITY(*, c1)
    ON EQUALITY(c1, *)
    ON EQUALITY(v1:path, *)
    ON EQUALITY(c1), EQUALITY(*)
    ```

    To specify more than one search method on a target, use a comma to separate each
    subsequent method and target:

    Copy code

    ```
    ALTER DYNAMIC TABLE my_dynamic_table ADD SEARCH OPTIMIZATION ON EQUALITY(c1), EQUALITY(c2, c3);
    ```

    If you run the ALTER DYNAMIC TABLE … ADD SEARCH OPTIMIZATION ON … command multiple
    times on the same table, each subsequent command adds to the existing configuration
    for the table. For instance, suppose that you run the following commands:

    Copy code

    ```
    ALTER DYNAMIC TABLE my_dynamic_table ADD SEARCH OPTIMIZATION ON EQUALITY(c1, c2);
    ALTER DYNAMIC TABLE my_dynamic_table ADD SEARCH OPTIMIZATION ON EQUALITY(c3, c4);
    ```

    This adds equality predicates for the columns `c1`, `c2`, `c3`, and `c4` to
    the configuration for the table. This is equivalent to running the command:

    Copy code

    ```
    ALTER DYNAMIC TABLE my_dynamic_table ADD SEARCH OPTIMIZATION ON EQUALITY(c1, c2, c3, c4);
    ```

    For examples, see [Enabling search optimization for specific columns](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-adding).

`DROP SEARCH OPTIMIZATION`
:   Removes [search optimization](/user-guide/search-optimization-service) for the
    entire dynamic table or, if you specify the optional `ON` clause, from specific
    columns.

    The following restrictions apply:

    - If a dynamic table has the search optimization property, then dropping the dynamic
      table and undropping it preserves the search optimization property.
    - Removing the search optimization property from a dynamic table and then adding it
      back incurs the same cost as adding it the first time.

`ON search_method_with_target | column_name | expression_id [, ... ]`
:   Specifies that you want to drop the search optimization configuration for specific
    columns or VARIANT fields (rather than dropping search optimization for the entire
    dynamic table).

    To identify the column configuration to drop, specify one of the following:

    - For `search_method_with_target`, specify a method for optimizing queries for
      one or more specific targets, which can be columns or VARIANT fields. Use the
      [syntax described earlier](/sql-reference/sql/alter-dynamic-table#label-alter-dynamic-table-searchoptimizationaction-search-method-target).
    - For `column_name`, specify the name of the column configured for search
      optimization. Specifying the column name drops all expressions for that column,
      including expressions that use VARIANT fields in the column.
    - For `expression_id`, specify the ID for an expression listed in the output
      of the [DESCRIBE SEARCH OPTIMIZATION](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-displaying)
      command.

    You can specify any combination of search methods with targets, column names, and
    expression IDs using a comma between items.

    For examples, see [Dropping search optimization for specific columns](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-dropping).

## Storage lifecycle policy actions (`storageLifecyclePolicyAction`)

`ADD STORAGE LIFECYCLE POLICY policy_name ON ( col_name [ , col_name ... ] )`
:   Attaches a [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies) to
    the dynamic table.

    The columns specified in the ON clause must match the argument count and data types defined in the policy function signature.
    Snowflake uses these columns to evaluate the policy expression and determine which rows to delete or archive.

    For more information about using storage lifecycle policies with dynamic tables, see
    [Use storage lifecycle policies with dynamic tables](/user-guide/dynamic-tables/storage-lifecycle-policies).

`DROP STORAGE LIFECYCLE POLICY`
:   Removes the storage lifecycle policy from the dynamic table.

    Caution

    Dropping the storage lifecycle policy triggers a full reinitialization on the next refresh. Snowflake refreshes all rows, including those that were previously in the expired region. For the full set of changes that trigger reinitialization, see [Reinitialization triggers](/user-guide/dynamic-tables/storage-lifecycle-policies#label-dynamic-tables-slp-reinit).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or OPERATE | The dynamic table you want to alter. | Some actions are only supported with the OWNERSHIP privilege. For more information, see [Grant OPERATE to manage a dynamic table](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges-alter). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To alter a dynamic table, you must be using a role that has OPERATE privilege on that
  dynamic table. For general information, see [Grant MONITOR to view metadata](/user-guide/dynamic-tables/privileges#label-dynamic-tables-privileges-view-metadata).
- Making changes to masking policies on a base table causes a [reinitialization](/user-guide/dynamic-tables/overview#label-dynamic-tables-initialization).
- If you want to update an existing dynamic table and need to see its current definition,
  call the [GET\_DDL](/sql-reference/functions/get_ddl) function.
- You can use data metric functions with dynamic tables by executing an [ALTER TABLE](/sql-reference/sql/alter-table)
  command. For more information, see [Use SQL to set up data metric functions](/user-guide/data-quality-working).
- You cannot use [IDENTIFIER()](/sql-reference/identifier-literal) to specify the
  name of the dynamic table to alter. For example, the following statement isn’t supported:

  Copy code

  ```
  ALTER DYNAMIC TABLE IDENTIFIER(my_dynamic_table) SUSPEND;
  ```
- After a reinitialization or full refresh, search indexes on dynamic tables are rebuilt.
  This process involves dropping the existing indexes and rebuilding them from scratch,
  which might incur higher costs. For more information, see [Search optimization cost estimation and management](/user-guide/search-optimization/cost-estimation).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Change the target lag of a dynamic table named `my_dynamic_table` to 1 hour:

Copy code

```
ALTER DYNAMIC TABLE my_dynamic_table SET
  TARGET_LAG = '1 hour';
```

Specify downstream target lag for `my_dynamic_table`:

Copy code

```
ALTER DYNAMIC TABLE my_dynamic_table SET TARGET_LAG = DOWNSTREAM;
```

Suspend a dynamic table:

Copy code

```
ALTER DYNAMIC TABLE my_dynamic_table SUSPEND;
```

Resume a dynamic table:

Copy code

```
ALTER DYNAMIC TABLE my_dynamic_table RESUME;
```

Rename `my_dynamic_table`:

Copy code

```
ALTER DYNAMIC TABLE my_dynamic_table RENAME TO my_updated_dynamic_table;
```

Swap `my_dynamic_table` with `my_new_dynamic_table`:

Copy code

```
ALTER DYNAMIC TABLE my_dynamic_table SWAP WITH my_new_dynamic_table;
```

Change the clustering key for a dynamic table:

Copy code

```
ALTER DYNAMIC TABLE my_dynamic_table CLUSTER BY (date);
```

Remove clustering from a dynamic table:

Copy code

```
ALTER DYNAMIC TABLE my_dynamic_table DROP CLUSTERING KEY;
```

Perform a manual refresh of `my_dynamic_table` using the user, secondary roles, and warehouse settings
from the current session. This ensures that the refresh operation runs with the exact context
of the user session.

Copy code

```
ALTER DYNAMIC TABLE my_dynamic_table REFRESH COPY SESSION
```

To modify or remove an existing frozen region predicate, you can replace it:

Copy code

```
ALTER DYNAMIC TABLE my_dynamic_table SET FROZEN WHERE ( <new_expr> );
```

Alternatively, remove a frozen region predicate:

Copy code

```
ALTER DYNAMIC TABLE my_dynamic_table UNSET FROZEN WHERE;
```

Add a storage lifecycle policy to a dynamic table:

Copy code

```
ALTER DYNAMIC TABLE dt_orders ADD STORAGE LIFECYCLE POLICY expire_after_1w ON (order_date);
```

Remove a storage lifecycle policy from a dynamic table:

Copy code

```
ALTER DYNAMIC TABLE dt_orders DROP STORAGE LIFECYCLE POLICY;
```
