# CREATE DATABASE

Creates a new database in the system.

This command supports the following variants:

- [CREATE OR ALTER DATABASE](#label-create-or-alter-database-syntax): Creates a database if it doesn’t exist or alters an existing database.
- [CREATE DATABASE … CLONE](#label-create-database-clone-syntax): Creates a clone of an existing database, either in its current state or at a specific time or point in the past
  (using Time Travel). For more information about cloning a database, see [Cloning considerations](/user-guide/object-clone).
- [CREATE DATABASE … FROM BACKUP SET](#label-create-database-from-backup-set-syntax) (restores a database from a backup under a new name)

In addition, this command can be used to:

- Create a database from a specified listing. See [About sharing with listings](https://other-docs.snowflake.com/en/collaboration/collaboration-listings-about).
- Create a database from a share provided by another Snowflake account. For more information about shares, see
  [About Secure Data Sharing](/user-guide/data-sharing-intro).
- Create a replica of an existing primary database (for example, a secondary database). For more information about database replication, see
  [Introduction to database replication across multiple accounts](/user-guide/db-replication-intro).

See also:
:   [ALTER DATABASE](/sql-reference/sql/alter-database), [DESCRIBE DATABASE](/sql-reference/sql/desc-database), [DROP DATABASE](/sql-reference/sql/drop-database), [SHOW DATABASES](/sql-reference/sql/show-databases), [UNDROP DATABASE](/sql-reference/sql/undrop-database)

    [DESCRIBE SHARE](/sql-reference/sql/desc-share) , [SHOW SHARES](/sql-reference/sql/show-shares), [CREATE LISTING](/sql-reference/sql/create-listing)

## Syntax

**Standard Database**

Copy code

```
CREATE [ OR REPLACE ] [ TRANSIENT ] DATABASE [ IF NOT EXISTS ] <name>
    [ CLONE <source_schema>
        [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ]
        [ IGNORE TABLES WITH INSUFFICIENT DATA RETENTION ]
        [ IGNORE HYBRID TABLES ] ]
    [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
    [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
    [ EXTERNAL_VOLUME = <external_volume_name> ]
    [ CATALOG = <catalog_integration_name> ]
    [ ICEBERG_DEFAULT_DDL_COLLATION = '<collation_specification>' ]
    [ ICEBERG_VERSION_DEFAULT = <integer> ]
    [ ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' } ]
    [ ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE } ]
    [ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
    [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
    [ STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED } ]
    [ COMMENT = '<string_literal>' ]
    [ CATALOG_SYNC = '<snowflake_open_catalog_integration_name>' ]
    [ CATALOG_SYNC_NAMESPACE_MODE = { NEST | FLATTEN } ]
    [ CATALOG_SYNC_NAMESPACE_FLATTEN_DELIMITER = '<string_literal>' ]
    [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
    [ WITH CONTACT ( <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ) ]
    [ OBJECT_VISIBILITY = { <object_visibility_spec> | PRIVILEGED } ]
    [ ENABLE_DATA_COMPACTION = { TRUE | FALSE } ]
    [ OAUTH_AUTHORIZATION_SERVER = <integration_name> ]
    [ OAUTH_SCOPES_SUPPORTED = '<comma_separated_scopes>' ]
```

**Restored database (from a backup)**

Copy code

```
CREATE DATABASE <name> FROM BACKUP SET <backup_set> IDENTIFIER '<backup_id>'
```

**Standard Database (from a listing)**

Copy code

```
CREATE DATABASE <name> FROM LISTING '<listing_global_name>'
```

**Shared Database (from a Share)**

Copy code

```
CREATE DATABASE <name> FROM SHARE <provider_account>.<share_name>
```

**Secondary Database (Database Replication)**

Copy code

```
CREATE DATABASE <name>
    AS REPLICA OF <account_identifier>.<primary_db_name>
    [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
```

## Variant syntax

### CREATE OR ALTER DATABASE

Creates a new database if it doesn’t already exist, or transforms an existing database into the database defined in the statement.
A CREATE OR ALTER DATABASE statement follows the syntax rules of a CREATE DATABASE statement and has the same limitations as an
[ALTER DATABASE](/sql-reference/sql/alter-database) statement.

The following modifications are supported:

- Changing the following database properties and parameters:
  - [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days)
  - [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-max-data-extension-time-in-days)
  - [EXTERNAL\_VOLUME](/sql-reference/parameters#label-external-volume)
  - [CATALOG](/sql-reference/parameters#label-catalog)
  - [ICEBERG\_VERSION\_DEFAULT](/sql-reference/parameters#label-iceberg-version-default)
  - [ICEBERG\_MERGE\_ON\_READ\_BEHAVIOR parameter](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior)
  - [Deprecated: ENABLE\_ICEBERG\_MERGE\_ON\_READ](/user-guide/tables-iceberg-manage#label-enable-iceberg-merge-on-read)
  - [REPLACE\_INVALID\_CHARACTERS](/sql-reference/parameters#label-replace-invalid-characters)
  - [DEFAULT\_DDL\_COLLATION](/sql-reference/parameters#label-default-ddl-collation)
  - [STORAGE\_SERIALIZATION\_POLICY](/sql-reference/parameters#label-storage-serialization-policy)
  - [COMMENT](/sql-reference/sql/comment)

For more information, see [CREATE OR ALTER DATABASE usage notes](#label-create-or-alter-database-usage-notes) and [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

Copy code

```
CREATE OR ALTER [ TRANSIENT ] DATABASE <name>
    [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
    [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
    [ EXTERNAL_VOLUME = <external_volume_name> ]
    [ CATALOG = <catalog_integration_name> ]
    [ ICEBERG_DEFAULT_DDL_COLLATION = '<collation_specification>' ]
    [ ICEBERG_VERSION_DEFAULT = <integer> ]
    [ ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' } ]
    [ ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE } ]
    [ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
    [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
    [ LOG_LEVEL = '<log_level>' ]
    [ METRIC_LEVEL = '<metric_level>' ]
    [ TRACE_LEVEL = '<trace_level>' ]
    [ STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED } ]
    [ COMMENT = '<string_literal>' ]
    [ OBJECT_VISIBILITY = { <object_visibility_spec> | PRIVILEGED } ]
```

### CREATE DATABASE … CLONE

Creates a new database with the same parameter values:

> Copy code
>
> ```
> CREATE [ OR REPLACE ] DATABASE [ IF NOT EXISTS ] <name> CLONE <source_database>
>   [ ... ]
> ```

For more details, see [CREATE <object> … CLONE](/sql-reference/sql/create-clone).

## Required parameters

`name`
:   Specifies the identifier for the database; must be unique for your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Important

    As a best practice for [Database Replication and Failover](/user-guide/db-replication-intro), we recommend giving each
    secondary database the same name as its primary database. This practice supports referencing fully qualified objects
    (i.e. `'<db>.<schema>.<object>'`) by other objects in the same database, such as querying a fully qualified table name in a view.

    If a secondary database has a different name from the primary database, then these object references would break in the secondary database.

### Secure Data Sharing parameters

`provider_account.share_name`
:   Specifies the identifier of the [share](/user-guide/data-sharing-intro) from which to create the database. As documented, the name of the
    share must be fully qualified with the name of the account providing the share.

### Database replication parameters

Important

This section describes a limited database replication feature that is different from the
[account replication feature](/user-guide/account-replication-intro). Snowflake strongly
recommends using the account replication feature to replicate and failover databases.

`AS REPLICA OF account_identifier.primary_db_name`
:   Specifies the identifier for a primary database from which to create a replica (i.e. a secondary database). If the identifier contains spaces,
    special characters, or mixed-case characters, the entire string must be enclosed in double quotes.

    Requires the account identifier and name of the primary database.

    `account_identifier`
    :   Unique identifier of the account that stores the primary database. The preferred identifier is `organization_name.account_name`.
        To view the list of accounts enabled for replication in your organization, query SHOW REPLICATION ACCOUNTS.

        Though the legacy account locator can also be used as the account identifier, its use is discouraged as it may not work in the future.
        For more details about using the account locator as an account identifier, see [Database Replication Usage Notes](#database-replication-usage-notes).

    `primary_db_name`
    :   Name of the primary database. As a best practice, we recommend giving each secondary database the same name as its primary database.

    Note

    As a best practice for Database Replication and Failover, we recommend setting the optional parameter
    [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/sql/create-database#label-data-retention-time-in-days-parameter) to the same value on the secondary database as on the
    primary database.

### Backup parameters

The FROM BACKUP SET clause restores a database from a backup. You don’t specify other database
properties because they’re all the same as in the backed-up database.

Note

The FROM SNAPSHOT SET clause is deprecated. Use FROM BACKUP SET instead.

This form doesn’t have a CREATE OR REPLACE clause. You typically either restore the
database under a new name and recover any data or other objects from this new database,
or rename the original database and then restore the database under the original name.

Note

The restored database is independent of the original database from the backup.
There isn’t any cloning relationship between the restored and original databases.
Therefore, all the micro-partitions for tables in the restored database are owned
by that database.

If you want to make backups of the newly restored database, create a new backup set for it.

For more information about backups, see [Backups for disaster recovery and immutable storage](/user-guide/backups).

`backup_set`
:   Specifies the name of a backup set created for a specific database.
    You can use the SHOW BACKUP SETS command to locate the right backup set.

`backup_id`
:   Specifies the identifier of a specific backup within that backup set.
    You can use the SHOW BACKUPS IN BACKUP SET command to locate the right identifier within the backup
    set, based on the creation date and time for the backup.

### Listing parameters

`'listing_global_name'`
:   Specifies the global name of the listing from which to create the database, which must meet the following requirements:

    - Can’t be a paid listing.
    - Listing terms, if not of type `OFFLINE`, must have been accepted using Snowsight.
    - Listing data products must be available locally in the current region.

      Whether a listing is available in the local region can be determined by viewing the `is_ready_for_import` column
      of [DESCRIBE AVAILABLE LISTING](/sql-reference/sql/desc-available-listing).

You must have the IMPORT LISTING privilege to create a database from a listing.
You must have the IMPORT SHARE privilege to create a database from a share.

## Optional parameters

`TRANSIENT`
:   Specifies a database as transient. Transient databases do not have a Fail-safe period so they do not incur additional storage costs once
    they leave Time Travel; however, this means they are also not protected by Fail-safe in the event of a data loss. For more information, see
    [Understanding and viewing Fail-safe](/user-guide/data-failsafe).

    In addition, by definition, all schemas (and consequently all tables) created in a transient database are transient. For more information about
    transient tables, see [CREATE TABLE](/sql-reference/sql/create-table).

    Default: No value (i.e. database is permanent)

`CLONE source_db`
:   Specifies to create a clone of the specified source database. For more details about cloning a database, see [CREATE <object> … CLONE](/sql-reference/sql/create-clone).

`AT | BEFORE ( TIMESTAMP => timestamp | OFFSET => time_difference | STATEMENT => id )`
:   When cloning a database, the [AT | BEFORE](/sql-reference/constructs/at-before) clause specifies to use Time Travel to clone the database at or
    before a specific point in the past. If the specified Time Travel time is at or before the point in time when the database was created,
    the cloning operation fails with an error.

`IGNORE TABLES WITH INSUFFICIENT DATA RETENTION`

> Ignore tables that no longer have historical data available in Time Travel to clone. If the time in the past specified in the
> AT | BEFORE clause is beyond the data retention period for any child table in a database or schema, skip the cloning operation
> for the child table. For more information, see
> [Child Objects and Data Retention Time](/user-guide/object-clone#label-child-objects-and-data-retention-time).

`IGNORE HYBRID TABLES`
:   Ignore hybrid tables, which will not be cloned. Use this option to clone a database that contains hybrid tables.
    The cloned database includes other objects but skips hybrid tables.

    If you don’t use this option and your database contains one or more hybrid tables, the command ignores hybrid tables silently. However, the error handling for databases that contain hybrid tables will change in an upcoming release; therefore, you may want to add this parameter to your commands preemptively.

`DATA_RETENTION_TIME_IN_DAYS = integer`
:   Specifies the number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the database, as well as specifying the
    default Time Travel retention time for all schemas created in the database. For more details, see [Understanding & using Time Travel](/user-guide/data-time-travel).

    For a detailed description of this object-level parameter, as well as more information about object parameters, see
    [Parameters](/sql-reference/parameters).

    Values:

    > - Standard Edition: `0` or `1`
    > - Enterprise Edition:
    >   - `0` to `90` for permanent databases
    >   - `0` or `1` for transient databases

    Default:

    > - Standard Edition: `1`
    > - Enterprise Edition (or higher): `1` (unless a different default value was specified at the account level)

    Note

    A value of `0` effectively disables Time Travel for the database.

`MAX_DATA_EXTENSION_TIME_IN_DAYS = integer`
:   Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in the
    database to prevent streams on the tables from becoming stale.

    For a detailed description of this parameter, see [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-max-data-extension-time-in-days).

`EXTERNAL_VOLUME = external_volume_name`
:   Object parameter that specifies the default external volume to use for [Apache Iceberg™ tables](/user-guide/tables-iceberg).

    For more information about this parameter, see [EXTERNAL\_VOLUME](/sql-reference/parameters#label-external-volume).

`CATALOG = catalog_integration_name`
:   Object parameter that specifies the default catalog integration to use for [Apache Iceberg™ tables](/user-guide/tables-iceberg).

    For more information about this parameter, see [CATALOG](/sql-reference/parameters#label-catalog).

`ICEBERG_DEFAULT_DDL_COLLATION = 'collation_specification'`
:   Specifies a default [collation specification](/sql-reference/collation#label-collation-specification) for new string columns on
    Snowflake-managed Iceberg tables.

    For more information about the parameter, see [ICEBERG\_DEFAULT\_DDL\_COLLATION](/sql-reference/parameters#label-iceberg-default-ddl-collation).

`ICEBERG_VERSION_DEFAULT = integer`
:   Specifies the version of the Apache Iceberg™ table specification that Iceberg tables conform to.

    Values:
    :   `2`: New tables conform with Iceberg version 2.

        `3`: New tables conform with Iceberg version 3.

    Caution

    Before you use other engines to upgrade an Iceberg tables format-version in table properties to v3, ensure that the table isn’t used by
    engines or applications that don’t yet support v3. Downgrading format versions isn’t supported in the Apache Iceberg specification. Therefore, all
    readers and writers must support v3. The default version for Iceberg tables in Snowflake is v2, which can be configured to v3 if
    needed. Using Snowflake to perform in-place version upgrades isn’t supported at this time.

    Default:
    :   `2`

    For more information about this parameter, see [ICEBERG\_VERSION\_DEFAULT](/sql-reference/parameters#label-iceberg-version-default).

`DEFAULT_METADATA_WRITE_FORMAT = { SNOWFLAKE | ICEBERG }`
:   Specifies the default metadata write format for new tables created with `CREATE TABLE` and `ALTER TABLE` in this scope.

    Values:
    :   `SNOWFLAKE`: New tables use the standard Snowflake table format.

        `ICEBERG`: New tables are created as Apache Iceberg™ tables when `CATALOG = 'SNOWFLAKE'` is set at the database level.

    Default:
    :   `SNOWFLAKE`

    For a detailed description of this parameter, see [DEFAULT\_METADATA\_WRITE\_FORMAT](/sql-reference/parameters#label-default-metadata-write-format).

`ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' }`
:   Specifies how Snowflake performs row-level updates (UPDATE, DELETE, MERGE) on Apache Iceberg™ tables. Selects between merge-on-read
    (which writes Iceberg delete files alongside the data) and copy-on-write (which rewrites entire data files).

    The parameter values are case-insensitive.

    Values:
    :   `'AUTO'`: Snowflake selects merge-on-read or copy-on-write based on the table’s Iceberg format version and management mode. For details,
        see [ICEBERG\_MERGE\_ON\_READ\_BEHAVIOR parameter](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior).

        `'ENABLED'`: Merge-on-read is enabled for all Apache Iceberg™ tables to which this parameter applies, regardless of format version or management
        mode.

        `'DISABLED'`: Merge-on-read is disabled for all Apache Iceberg™ tables to which this parameter applies. All DML uses copy-on-write.

    Default:
    :   `'AUTO'`

    For a detailed description of this parameter, see [ICEBERG\_MERGE\_ON\_READ\_BEHAVIOR parameter](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior). For more information about merge-on-read
    and copy-on-write behavior in Snowflake, see [Use row-level deletes](/user-guide/tables-iceberg-manage#label-tables-iceberg-row-level-deletes).

`ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE }`
:   Warning

    This parameter is deprecated. Use [`ICEBERG_MERGE_ON_READ_BEHAVIOR`](/user-guide/tables-iceberg-manage#label-iceberg-merge-on-read-behavior) instead.
    The legacy parameter is still honored when `ICEBERG_MERGE_ON_READ_BEHAVIOR` is at its default (`'AUTO'`), but it will return an
    error in a future release.

    Specifies whether to enable merge-on-read behavior for Apache Iceberg™ tables.

    Values:
    :   `TRUE`: New tables use merge-on-read behavior. For **v2** tables, Snowflake uses positional delete files for row-level deletes. For **v3** tables, Snowflake uses deletion vectors when conditions are met.

        **Note:** Setting this parameter to `TRUE` does **not** enable merge-on-read for Snowflake-managed v2 Iceberg tables. When `ICEBERG_MERGE_ON_READ_BEHAVIOR` is at its default (`'AUTO'`), this setting routes through the auto matrix, which keeps Snowflake-managed v2 tables on copy-on-write. To enable merge-on-read for Snowflake-managed v2 tables, set `ICEBERG_MERGE_ON_READ_BEHAVIOR = 'ENABLED'` explicitly.

        `FALSE`: New tables use copy-on-write behavior.

    Default:
    :   `TRUE`

    For a detailed description of this parameter, see [Deprecated: ENABLE\_ICEBERG\_MERGE\_ON\_READ](/user-guide/tables-iceberg-manage#label-enable-iceberg-merge-on-read). For more information about merge-on-read
    and copy-on-write behavior in Snowflake, see [Use row-level deletes](/user-guide/tables-iceberg-manage#label-tables-iceberg-row-level-deletes).

`REPLACE_INVALID_CHARACTERS = { TRUE | FALSE }`
:   Specifies whether to replace invalid UTF-8 characters with the Unicode replacement character (�) in query results for an
    [Iceberg table](/sql-reference/sql/create-iceberg-table).
    You can only set this parameter for tables that use an external Iceberg catalog.

    - `TRUE` replaces invalid UTF-8 characters with the Unicode replacement character.
    - `FALSE` leaves invalid UTF-8 characters unchanged. Snowflake returns a user error message when it encounters invalid UTF-8
      characters in a Parquet data file.

    Default: `FALSE`

`DEFAULT_DDL_COLLATION = 'collation_specification'`
:   Specifies a default [collation specification](/sql-reference/collation#label-collation-specification) for all schemas and tables added to the database. The
    default can be overridden at the schema and individual table level.

    For more details about the parameter, see [DEFAULT\_DDL\_COLLATION](/sql-reference/parameters#label-default-ddl-collation).

`LOG_LEVEL = 'log_level'`
:   Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at
    the specified level (and at more severe levels) are ingested.

    For more information about levels, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level). For information about setting the log level, see
    [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

`METRIC_LEVEL = 'metric_level'`
:   Specifies whether metrics data should be ingested and made available in the active event table.

    For more information, see [METRIC\_LEVEL](/sql-reference/parameters#label-metric-level) and [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

`TRACE_LEVEL = 'trace_level'`
:   Controls how trace events are ingested into the event table.

    For information about levels, see [TRACE\_LEVEL](/sql-reference/parameters#label-trace-level). For information about setting trace level, see
    [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

`STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED }`
:   Specifies the storage serialization policy for [Apache Iceberg™ tables](/user-guide/tables-iceberg) that use Snowflake as the catalog.

    - `COMPATIBLE`: Snowflake performs encoding and compression of data files that ensures interoperability with third-party compute engines.
    - `OPTIMIZED`: Snowflake performs encoding and compression of data files that ensures the best table performance within Snowflake.

    Default: `OPTIMIZED`

`COMMENT = 'string_literal'`
:   Specifies a comment for the database.

    Default: No value

`CATALOG_SYNC = 'snowflake_open_catalog_integration_name'`
:   Specifies the name of a catalog integration configured for [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview).
    If specified, Snowflake syncs Snowflake-managed Apache Iceberg™ tables in the database with an external catalog in your Snowflake Open Catalog
    account. For more information about syncing Snowflake-managed Iceberg tables with Open Catalog, see [Sync a Snowflake-managed table with Snowflake Open Catalog](/user-guide/tables-iceberg-open-catalog-sync).

    For more information about this parameter, see [CATALOG\_SYNC](/sql-reference/parameters#label-catalog-sync).

    Default: No value

`CATALOG_SYNC_NAMESPACE_MODE = { NEST | FLATTEN }`
:   Specifies the catalog sync namespace mode for Snowflake-managed Iceberg tables in the database that you sync with
    Snowflake Open Catalog. This property specifies whether Snowflake syncs the table to Open Catalog with one or two parent namespaces. It
    only applies if you’re setting the `CATALOG_SYNC` parameter. After you create the database, you can’t alter this property.

    - `NEST`: Snowflake syncs two parent namespaces with the table.

      For example, suppose you have a `db2.public.table1` Iceberg table registered in Snowflake. You want to sync this table, along with its
      two parent namespaces, to the `catalog2` external catalog in Open Catalog. To sync the table with its two parent namespaces, use the
      default for `CATALOG_SYNC_NAMESPACE_MODE` (`NEST`). If you don’t specify the `CATALOG_SYNC_NAMESPACE_MODE` property, the default for
      this property is applied, which is `NEST`. Because you’re using the default for `CATALOG_SYNC_NAMESPACE_MODE`, you don’t need to specify
      `CATALOG_SYNC_NAMESPACE_FLATTEN_DELIMITER`. As a result, Snowflake syncs the table to Open Catalog with the following fully qualified
      name: `catalog2.db2.public.table1`.
    - `FLATTEN`: Snowflake syncs one parent namespace with the table, which contains the delimiter you set by using the
      `CATALOG_SYNC_NAMESPACE_FLATTEN_DELIMITER` property.

      Important

      If your third-party query engine can only query tables located up to the second namespace level in a catalog, you must set the
      `CATALOG_SYNC_NAMESPACE_MODE` property to `FLATTEN`. Otherwise, Snowflake will sync Snowflake-managed Iceberg tables to the
      third namespace level in Open Catalog and you can’t query the table.

      For example, suppose that you have a `db1.public.table1` Iceberg table registered in Snowflake. You want to sync this table and one parent
      namespace named `db1-public` with the `catalog1` external catalog in Open Catalog, so that the table is located at the second namespace level in Open Catalog.

      To sync the table with the `db1-public` parent namespace, set `CATALOG_SYNC_NAMESPACE_MODE` to `FLATTEN` and specify a hyphen (`-`) as the value
      for `CATALOG_SYNC_NAMESPACE_FLATTEN_DELIMITER`. As a result, Snowflake syncs this table to Open Catalog with the following
      fully qualified name: `catalog1.db1-public.table1`.

    Default: `NEST`

`CATALOG_SYNC_NAMESPACE_FLATTEN_DELIMITER = 'string_literal'`
:   Specifies a delimiter, which Snowflake inserts in the flattened namespace that results when Snowflake syncs a Snowflake-managed Iceberg
    table to Snowflake Open Catalog with one parent namespace. This delimiter property only applies when you set the [CATALOG\_SYNC\_NAMESPACE\_MODE](/sql-reference/sql/create-database#label-catalog-sync-namespace-mode)
    property to `FLATTEN`. Snowflake inserts this delimiter to avoid conflicts that could
    arise from flattening parent namespaces for different tables. After you create the database, you can’t alter this property.

    For example, suppose you want to sync the `customer.data.table1` and `custom.erdata.table1` Snowflake-managed Iceberg tables to the `catalog1`
    external catalog in Open Catalog. By setting the CATALOG\_SYNC\_NAMESPACE\_MODE property to `FLATTEN` and specifying a hyphen (`-`) for the
    delimiter, Snowflake syncs these tables with Open Catalog with the following fully qualified names:

    > - `catalog1.customer-data.table1`
    > - `catalog1.custom-erdata.table1`

    If you set the `CATALOG_SYNC_NAMESPACE_MODE` property to `FLATTEN`, a non-empty delimiter value is required. However, if you set the
    `CATALOG_SYNC_NAMESPACE_MODE` property to `NEST`, this delimiter property doesn’t apply and the configured value will be ignored.

    Valid characters: `0-9`, `A-Z`, `a-z`, `_`, `$`, `-`

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`WITH CONTACT ( purpose = contact [ , purpose = contact ...] )`
:   Associate the new object with one or more [contacts](/user-guide/contacts-using).

    Specify the WITH CONTACT clause after all other clauses except the AS clause (if that clause is supported by this command).

`OBJECT_VISIBILITY = { object_visibility_spec | PRIVILEGED }`
> - A YAML specification describing the visibility in one of the following formats:
>
>   Copy code
>
>   ```
>   $$
>   organization_targets:
>     - all_accounts_including_external
>   $$
>   ```
>
>   Or
>
>   Copy code
>
>   ```
>   $$
>   organization_targets:
>     - account: <account_name_1>
>     - account: <account_name_2>
>     - ...
>     - organization_user_group: <org_user_group_1>
>     - organization_user_group: <org_user_group_2>
>   $$
>   ```
>
>   In the syntax above:
>
>   - `all_accounts_including_external`: Specifies that all users in all accounts in the organization can see the object. This includes
>     all accounts within the organization, even those to which external parties may have been given access, such as
>     [reader accounts](/user-guide/data-sharing-reader-create).
>   - `account: account_name`: Specifies that all users in the specified account can see the object. You can specify multiple accounts.
>     Note that `account` is the account name, not the account locator. You must specify only the account name, excluding the organization name.09-22
>   - `organization_user_group: org_user_group`: Specifies that the specified [organization user group](/user-guide/organization-users#label-org-users-groups) can
>     see the object in all accounts in the organization where the [organization user group has been imported](/user-guide/organization-users#label-org-users-add).
> - `PRIVILEGED`: Specifies that only roles within the current account that are granted an explicit privilege on the object can see the object.
>   This is the default behavior in Snowflake.
>
> For examples, see [Make database objects discoverable in Universal Search](/user-guide/ui-snowsight/object-visibility-universal-search#label-object-visibility-examples).

`ENABLE_DATA_COMPACTION = { TRUE | FALSE }`
:   Specifies whether Snowflake should enable data compaction on Snowflake-managed [Apache Iceberg™ tables](/user-guide/tables-iceberg).

    - `TRUE`: Snowflake performs data compaction on the tables.
    - `FALSE`: Snowflake doesn’t perform data compaction on the tables.

    Default: `TRUE`

    For more information, see [ENABLE\_DATA\_COMPACTION](/sql-reference/parameters#label-enable-data-compaction) and [Set data compaction](/user-guide/tables-iceberg-manage#label-tables-iceberg-manage-set-data-compaction).

`OAUTH_AUTHORIZATION_SERVER = integration_name`
:   Object parameter that specifies an External OAuth security integration as the authorization server for MCP servers in this database.

    For a detailed description of this parameter, see [OAUTH\_AUTHORIZATION\_SERVER](/sql-reference/parameters#label-oauth-authorization-server).

`OAUTH_SCOPES_SUPPORTED = 'comma_separated_scopes'`
:   Object parameter that specifies the OAuth scopes to advertise for MCP servers in this database.

    For a detailed description of this parameter, see [OAUTH\_SCOPES\_SUPPORTED](/sql-reference/parameters#label-oauth-scopes-supported).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE DATABASE | Account | Required to create a new database.  Only the SYSADMIN role, or a higher role, has this privilege by default. The privilege can be granted to additional roles as needed. |
| USAGE | External volume, catalog integration | Required if setting the `EXTERNAL_VOLUME` or `CATALOG` object parameters, respectively. |
| IMPORT LISTING | Account | Required to create a database from a listing. |
| IMPORT SHARE | Account | Required to create a database from a share. |
| MANAGE VISIBILITY | Account | Required to set the OBJECT\_VISIBILITY property. Only the SECURITYADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |
| MODIFY LOG LEVEL | Account | Required to set the LOG\_LEVEL for a database. |
| MODIFY TRACE LEVEL | Account | Required to set the TRACE\_LEVEL for a database. |
| OWNERSHIP | Database | Required when executing an [ALTER DATABASE](/sql-reference/sql/alter-database) or [ALTER SCHEMA](/sql-reference/sql/alter-schema) statement to set object visibility, or when executing a [CREATE OR ALTER DATABASE](#label-create-or-alter-database-syntax) statement for an existing database.  OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## General usage notes

- Creating a database automatically sets it as the active/current database for the current session (equivalent to using the [USE DATABASE](/sql-reference/sql/use-database)
  command for the database).
- If a database with the same name already exists, an error is returned and the database is not created, unless the optional `OR REPLACE`
  keyword is specified in the command.

  Important

  Using `OR REPLACE` is the equivalent of using [DROP DATABASE](/sql-reference/sql/drop-database) on the existing database and then creating a new database with
  the same name; however, the dropped database is not permanently removed from the system. Instead, it is retained in Time Travel.
  This is important because dropped databases in Time Travel contribute to data storage for your account. For more information, see
  [Storage costs for Time Travel and Fail-safe](/user-guide/data-cdp-storage-costs).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- Creating a new database automatically creates two schemas in the database:

  - PUBLIC: Default schema for the database.
  - INFORMATION\_SCHEMA: Schema which contains views and table functions that can be used for querying metadata about the objects in the
    database, as well as across all objects in the account.
- Databases created from shares differ from standard databases in the following ways:

  - They do not have the PUBLIC schema unless it was explicitly granted to the share. They do include the
    INFORMATION\_SCHEMA schema automatically.
  - They cannot be cloned.
  - Properties, such as `TRANSIENT` and `DATA_RETENTION_TIME_IN_DAYS`, do not apply.
- When a database is active/current, the PUBLIC schema is also active/current by default unless a different schema is used or the PUBLIC
  schema has been dropped.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## CREATE OR ALTER DATABASE usage notes

- All limitations of the [ALTER DATABASE](/sql-reference/sql/alter-database) command apply.
- This command supports the properties and syntax that overlap between the CREATE DATABASE and ALTER DATABASE commands. For this
  reason, the following are *not* supported:
  - Swapping databases using the SWAP WITH parameter.
  - Renaming a database using the RENAME TO parameter.
  - Creating a clone of a database using the CLONE parameter.
  - Adding or changing tags and policies. Any existing tags and policies are preserved.
  - Converting a TRANSIENT database into a non-TRANSIENT database, or vice versa.
  - Creating a database from a share using CREATE OR ALTER DATABASE … FROM SHARE.
  - Creating a secondary (replica) database using CREATE OR ALTER DATABASE … AS REPLICA OF.

## Database replication usage notes

Important

This section describes a limited database replication feature that is different from the
[account replication feature](/user-guide/account-replication-intro). Snowflake strongly
recommends using the account replication feature to replicate and failover databases.

- Database replication uses Snowflake-provided compute resources instead of your own virtual warehouse to copy objects and data. However, the
  [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds) session/object parameter still controls how long a statement runs before it is canceled. The
  default value is `172800` (2 days). Because the initial replication of a primary database can take longer than 2 days to complete
  (depending on the amount of metadata in the database as well as the amount of data in database objects), we recommend increasing the
  STATEMENT\_TIMEOUT\_IN\_SECONDS value to `604800` (7 days, the maximum value) for the session in which you run the replication operation.

  Run the following [ALTER SESSION](/sql-reference/sql/alter-session) statement prior to executing the `ALTER DATABASE secondary_db_name REFRESH`
  statement in the same session:

  Copy code

  ```
  ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 604800;
  ```

  Note that the STATEMENT\_TIMEOUT\_IN\_SECONDS parameter also applies to the active warehouse in a session. The parameter honors the *lower*
  value set at the session or warehouse level. If you have an active warehouse in the current session, also set STATEMENT\_TIMEOUT\_IN\_SECONDS
  to `604800` for this warehouse (using [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse)).

  For example:

  Copy code

  ```
  -- determine the active warehouse in the current session (if any)
  SELECT CURRENT_WAREHOUSE();

  +---------------------+
  | CURRENT_WAREHOUSE() |
  |---------------------|
  | MY_WH               |
  +---------------------+

  -- change the STATEMENT_TIMEOUT_IN_SECONDS value for the active warehouse

  ALTER WAREHOUSE my_wh SET STATEMENT_TIMEOUT_IN_SECONDS = 604800;
  ```

  You can reset the parameter value to the default after the replication operation is completed:

  Copy code

  ```
  ALTER WAREHOUSE my_wh UNSET STATEMENT_TIMEOUT_IN_SECONDS;
  ```
- The preferred method of identifying the account that stores the primary database uses the organization name and account name as the
  account identifier. If you decide to use the legacy account locator instead, see [Account identifiers for replication and failover](/user-guide/admin-account-identifier#label-account-identifier-for-replication).
- The CREATE DATABASE … AS REPLICA command does not support the WITH TAG clause.

  This clause is not supported because the secondary database is read only. If your primary database specifies the WITH TAG clause, remove
  the clause prior to creating the secondary database. To verify whether your database has the WITH TAG clause, call the
  [GET\_DDL](/sql-reference/functions/get_ddl) function in your Snowflake account and specify the primary database in the function argument. If
  a tag is set on the database, the function output will include an ALTER DATABASE … SET TAG statement.

  For more information, see [Replication and tags](/user-guide/account-replication-considerations#label-replication-and-tags).

## Examples

Create two permanent databases, one with a data retention period of 10 days:

Copy code

```
CREATE DATABASE mytestdb;

CREATE DATABASE mytestdb2 DATA_RETENTION_TIME_IN_DAYS = 10;

SHOW DATABASES LIKE 'my%';

+---------------------------------+------------+------------+------------+--------+----------+---------+---------+----------------+
| created_on                      | name       | is_default | is_current | origin | owner    | comment | options | retention_time |
|---------------------------------+------------+------------+------------+--------+----------+---------+---------+----------------|
| Tue, 17 Mar 2016 16:57:04 -0700 | MYTESTDB   | N          | N          |        | PUBLIC   |         |         | 1              |
| Tue, 17 Mar 2016 17:06:32 -0700 | MYTESTDB2  | N          | N          |        | PUBLIC   |         |         | 10             |
+---------------------------------+------------+------------+------------+--------+----------+---------+---------+----------------+
```

Create a transient database:

Copy code

```
CREATE TRANSIENT DATABASE mytransientdb;

SHOW DATABASES LIKE 'my%';

+---------------------------------+---------------+------------+------------+--------+----------+---------+-----------+----------------+
| created_on                      | name          | is_default | is_current | origin | owner    | comment | options   | retention_time |
|---------------------------------+---------------+------------+------------+--------+----------+---------+-----------+----------------|
| Tue, 17 Mar 2016 16:57:04 -0700 | MYTESTDB      | N          | N          |        | PUBLIC   |         |           | 1              |
| Tue, 17 Mar 2016 17:06:32 -0700 | MYTESTDB2     | N          | N          |        | PUBLIC   |         |           | 10             |
| Tue, 17 Mar 2015 17:07:51 -0700 | MYTRANSIENTDB | N          | N          |        | PUBLIC   |         | TRANSIENT | 1              |
+---------------------------------+---------------+------------+------------+--------+----------+---------+-----------+----------------+
```

Create a database from a share provided by account `ab67890`:

Copy code

```
CREATE DATABASE snow_sales FROM SHARE ab67890.sales_s;
```

For more detailed examples of creating a database from a share, see [Consume imported data](/user-guide/data-share-consumers).

## Database replication examples

Important

This section describes a limited database replication feature that is different from the
[account replication feature](/user-guide/account-replication-intro). Snowflake strongly
recommends using the account replication feature to replicate and failover databases.

For an example of creating a replication group to replicate a single database to a target account, see
[Examples](/sql-reference/sql/create-replication-group#label-replication-group-single-database).

## CREATE OR ALTER DATABASE examples

### Create a simple database

Create a database named `db1`:

Copy code

```
CREATE OR ALTER DATABASE db1;
```

Alter database `db1` to set the DATA\_RETENTION\_TIME\_IN\_DAYS and DEFAULT\_DDL\_COLLATION parameters:

Copy code

```
CREATE OR ALTER DATABASE db1
  DATA_RETENTION_TIME_IN_DAYS = 5
  DEFAULT_DDL_COLLATION = 'de';
```

### Unset a parameter previously set on database

The [absence of a previously set parameter](#label-create-or-alter-database-usage-notes) in the modified database definition results
in unsetting it. In the following example, unset the DATA\_RETENTION\_TIME\_IN\_DAYS parameter for the database `db1` created
in the previous example:

Copy code

```
CREATE OR ALTER DATABASE db1
  DEFAULT_DDL_COLLATION = 'de';
```
