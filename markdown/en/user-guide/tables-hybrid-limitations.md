# Limitations and unsupported features for hybrid tables

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

The following guidance on [limitations](#label-hybrid-tables-limitations) and
[unsupported features](#label-hybrid-tables-unsupported) applies to hybrid tables, and is subject
to change.

Be sure to read both sections.

Note

Reach out to your account team if you have questions.

## Limitations

- [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions)
- [Collations](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-collations)
- [Consistency](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-consistency)
- [Constraints](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-constraints)
- [COPY](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-copy)
- [Data size](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-data-size)
- [Data types not supported in indexes](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-data-types)
- [DML commands](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-dml-commands)
- [Higher-order functions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-functions)
- [Native applications](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-native-apps)
- [Persisted query results](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-query-results)
- [Quotas and throttling](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-ht-quotas-throttling)
- [Secondary indexes](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-secondary-indexes)
- [Throughput](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-throughput)
- [Time Travel and cloning](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-time-travel)
- [Transactions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-transactions)
- [Transient schemas and databases](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-transient-schemas)
- [%tri-secret-secure%](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-tss)

Clouds and regions
:   Hybrid tables are generally available in all commercial Amazon Web Services (AWS) and
    Microsoft Azure [regions](/user-guide/intro-regions).

    Note the following restrictions:

    - Hybrid tables are not available in Google Cloud.
    - Hybrid tables are not available in [U.S. SnowGov Regions](/user-guide/intro-regions#label-intro-regions-snowgov-regions).
    - Hybrid tables are not supported in trial accounts.
    - If you are a Virtual Private Snowflake (VPS) customer, contact
      [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to inquire about enabling hybrid tables for your account.

Collations
:   Hybrid tables support collations only on character columns that are not indexed. PRIMARY KEY columns and other
    indexed columns don’t accept the COLLATE clause. If the [DEFAULT\_DDL\_COLLATION](/sql-reference/parameters#label-default-ddl-collation) parameter is set for
    hybrid tables in an account, database, or schema, the parameter is ignored for indexed columns.

    For more information, see [Collations on hybrid table columns](/sql-reference/sql/create-hybrid-table#label-hybrid-table-collations-disable) and [Collation control](/sql-reference/collation#label-collation-control).

Consistency
:   By default, hybrid tables use a session-based consistency model where read operations in the session return
    the latest data from write operations in the same session. There might be some staleness (less than 100 ms) for
    changes made outside of the session. To avoid staleness,
    set `READ_LATEST_WRITES = true` at the statement or session level. Note that this
    might incur some latency overhead of a few milliseconds.

Constraints
:   PRIMARY KEY, UNIQUE, and FOREIGN KEY constraints are enforced for hybrid tables, but some limitations apply.
    For information, see [Constraints for hybrid tables](/sql-reference/sql/create-hybrid-table#label-hybrid-table-notes-on-constraints).

COPY
:   When you load a hybrid table with the COPY INTO command, `ABORT_STATEMENT` is the only option that is
    supported for `ON_ERROR`. Setting `ON_ERROR=SKIP_FILE` returns an error. For
    more information, see [Loading data](/user-guide/tables-hybrid-create#label-create-loading-data).

Data size
:   You are limited to storing 2 TB of data in hybrid tables per Snowflake database.
    See [Quotas and throttling](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-ht-quotas-throttling) for more information.

Data types not supported in indexes
:   Columns with [geospatial data types](/sql-reference/data-types-geospatial)
    (GEOGRAPHY and GEOMETRY), [semi-structured data types](/sql-reference/data-types-semistructured)
    (ARRAY, OBJECT, VARIANT), and [vector data types](/sql-reference/data-types-vector) (VECTOR) are not supported as either
    PRIMARY KEY columns (which are automatically indexed) or explicitly indexed columns. (Hybrid table columns support these
    data types as long as the columns are not indexed.)

    The [UUID](/sql-reference/data-types-uuid) data type isn’t supported for any column in a hybrid table.

    The [TIMESTAMP\_TZ](/sql-reference/data-types-datetime#label-datatypes-timestamp-variations) data type (or a [TIMESTAMP](/sql-reference/data-types-datetime#label-datatypes-timestamp) data
    type that resolves to TIMESTAMP\_TZ) is not supported for columns that are indexed using UNIQUE, PRIMARY KEY, and FOREIGN KEY
    constraints. However, TIMESTAMP\_TZ is supported for secondary indexes.

    See also [Secondary indexes](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-secondary-indexes).

DML commands
:   When using DML commands to change a small number of rows, optimize performance
    by using INSERT, UPDATE, or DELETE statements instead of MERGE.

Higher-order functions
:   The [FILTER](/sql-reference/functions/filter), [REDUCE](/sql-reference/functions/reduce), and
    [TRANSFORM](/sql-reference/functions/transform) higher-order functions are not supported in queries
    against hybrid tables.

Native applications
:   You can include hybrid tables in a Snowflake Native App. However, hybrid tables
    cannot be shared from the provider to the consumer. Native Apps can create
    hybrid tables in the consumer account, and they can read from and write to
    those hybrid tables. You can also expose hybrid tables to application roles
    so that they can be queried directly by consumer users.

    You cannot create a hybrid table in a provider account, nor can you include
    that hybrid table in a view that is shared through the Native App.

Persisted query results
:   Queries against hybrid tables do not use the results cache, as defined with the
    [USE\_CACHED\_RESULT parameter](/sql-reference/parameters#label-use-cached-result). See [Using Persisted Query Results](/user-guide/querying-persisted-results).

Quotas and throttling
:   Your usage of hybrid tables is restricted by quotas in order to ensure equitable availability of
    shared resources, ensure consistent quality of service, and reduce spikes in usage.

    | Quota | Default | Notes |
    | --- | --- | --- |
    | Hybrid storage | 2 TB per Snowflake database | This quota controls how much data you can store in hybrid tables. This limit applies only to active hybrid table data in the row store; it does not apply to object storage. If you exceed the storage quota, write operations that add data to any hybrid tables are temporarily blocked until you bring your hybrid storage consumption back under quota by removing tables or data.  You can reclaim space in a matter of seconds by [dropping](/sql-reference/sql/drop-table) or [truncating](/sql-reference/sql/truncate-table) unneeded hybrid tables. However, when you [delete](/sql-reference/sql/delete) data from tables, it takes some number of hours to recover space (because background compaction is required). |
    | Hybrid table requests | Approximately 16,000 operations per second, per Snowflake database | This quota controls the rate at which you can read from and write to hybrid tables. You should be able to achieve up to 16,000 operations per second against hybrid tables for a balanced workload consisting of 80% point reads and 20% point writes. To monitor throttling, see the example in [AGGREGATE\_QUERY\_HISTORY view](/sql-reference/account-usage/aggregate_query_history). |
    | Databases that contain hybrid tables | 200 total per Snowflake account, and no more than 100 databases added within a one-hour window | This quota controls how many databases within your Snowflake account may contain hybrid tables. If you exceed this quota, you will be unable to create a hybrid table in a new database without dropping all hybrid tables from an existing database. If necessary, you can request help from [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to increase the quota. |

    Expand

    Show lessSee more

    Throttling can be caused by a combination of factors that result in too many read and write requests being sent to the hybrid
    table storage provider:

    - Too many read requests can occur because of poorly optimized queries or because of a large, aggressive workload with very
      high query concurrency.
    - Too many write requests can occur because the bulk-load path wasn’t chosen when a table was loaded or because the workload
      consists of too many concurrent write operations.

    If you receive an error or throttling occurs because of a quota limit, contact your system administrator or DBA to look into the
    overall Unistore workload; possibly it can be modified to avoid exceeding the quota. DBAs can contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to
    evaluate query performance and quota usage. For some workloads, you might need to initiate a quota increase by requesting help from
    the support team.

Secondary indexes
:   The following secondary index features are *not* supported:

    > - Adding a column to an existing index.
    > - Altering an index on an existing hybrid table.

    Changes can be applied by dropping and re-creating the index.

    To use a secondary index on a hybrid table, you must use a role that is granted the SELECT privilege on the table.
    If you only have access to objects other than the hybrid table itself, you will not be able to use secondary indexes.

    TIMESTAMP\_NTZ is a supported column type for secondary indexes; however, TIMESTAMP\_TZ is *not* supported.
    [DATETIME](/sql-reference/data-types-datetime#label-datatypes-datetime) is an alias for TIMESTAMP\_NTZ and is therefore supported.
    [TIMESTAMP](/sql-reference/data-types-datetime#label-datatypes-timestamp) is supported when configured as an alias for TIMESTAMP\_NTZ.

    For more information about secondary indexes, see [Add secondary indexes](/user-guide/tables-hybrid-index#label-add-secondary-indexes).

Throughput
:   You can execute up to approximately 16,000 operations per second against
    hybrid tables in each database in your account for a balanced 80%/20% read/write workload. If
    you exceed this limit, Snowflake might reduce your throughput.
    See [Quotas and throttling](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-ht-quotas-throttling) for more information.

Time Travel and cloning
:   [Time Travel](/user-guide/data-time-travel) queries that select from hybrid tables are supported
    with the following limitations:

    - Only the TIMESTAMP parameter is supported in the AT clause.

      - The value of the TIMESTAMP parameter must be the same for all tables that belong to the same database.
      - If the tables belong to different databases, you can use different TIMESTAMP values.
    - The OFFSET, STATEMENT, and STREAM parameters are not supported.
    - The BEFORE clause is not supported.
    - The UNDROP TABLE command, which depends on Time Travel, is not supported.

    For information about cloning support for hybrid tables, see [Clone databases that contain hybrid tables](/user-guide/tables-hybrid-clone).

Transactions
:   For hybrid tables, the transaction scope is the database in which the hybrid table resides. All the hybrid tables
    referenced in a transaction must reside in the same database; standard Snowflake tables referenced in the same
    transaction may reside in different databases.

Transient schemas and databases
:   You cannot create hybrid tables that are [temporary or transient](/user-guide/tables-temp-transient).
    In turn, you cannot create hybrid tables within transient schemas or databases.

Tri-Secret Secure
:   You can use hybrid tables in a TSS-enabled account by enabling Dedicated Storage Mode. For information,
    see [Hybrid Tables Dedicated Storage Mode for TSS](/user-guide/tables-hybrid-dedicated-storage-mode).

## Unsupported features

At this time, hybrid tables do not support:

- [Clustering keys](/user-guide/tables-clustering-keys)

  Data in hybrid tables is ordered by the primary key.
- [Data sharing](/guides-overview-sharing)
- [Dynamic tables](/user-guide/dynamic-tables/overview)
- [Fail-safe](/user-guide/data-failsafe)
- [Materialized views](/user-guide/views-materialized)
- [Query Acceleration Service](/user-guide/query-acceleration-service)
- [Replication](/user-guide/account-replication-intro)
- [Search Optimization Service](/user-guide/search-optimization-service)
- [Snowpipe](/user-guide/data-load-snowpipe-intro)
- [Snowpipe Streaming API](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview)
- [Streams](/user-guide/streams-intro)
- [UNDROP](/sql-reference/sql/undrop-table)

  - [UNDROP SCHEMA](/sql-reference/sql/undrop-schema) and
    [UNDROP DATABASE](/sql-reference/sql/undrop-database) commands succeed for entities that
    contain hybrid tables, but those hybrid tables and their associated
    constraints and indexes cannot be restored.
  - The DELETED column in [TABLES view](/sql-reference/account-usage/tables) displays
    the time of deletion as the UNDROP time of the parent entity.
  - The [ACCESS\_HISTORY view](/sql-reference/account-usage/access_history) contains an entry for DROP/UNDROP of the parent
    entity, but no entries for hybrid tables.
