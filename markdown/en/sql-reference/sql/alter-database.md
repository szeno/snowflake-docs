# ALTER DATABASE

Modifies the properties for an existing database.

Database modifications include the following:

- Changing the name of the database or changing the Time Travel data retention period (if you are using Snowflake Enterprise Edition or higher).
- Enabling and managing database replication and failover.

See also:
:   [CREATE DATABASE](/sql-reference/sql/create-database), [DESCRIBE DATABASE](/sql-reference/sql/desc-database), [DROP DATABASE](/sql-reference/sql/drop-database), [SHOW DATABASES](/sql-reference/sql/show-databases), [UNDROP DATABASE](/sql-reference/sql/undrop-database)

## Syntax

Copy code

```
ALTER DATABASE [ IF EXISTS ] <name> RENAME TO <new_db_name>

ALTER DATABASE [ IF EXISTS ] <name> SWAP WITH <target_db_name>

ALTER DATABASE [ IF EXISTS ] <name> SET [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
                                        [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
                                        [ EXTERNAL_VOLUME = <external_volume_name> ]
                                        [ CATALOG = <catalog_integration_name> ]
                                        [ ICEBERG_DEFAULT_DDL_COLLATION = '<collation_specification>' ]
                                        [ ICEBERG_VERSION_DEFAULT = <integer> ]
                                        [ ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' } ]
                                        [ ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE } ]
                                        [ REPLACE_INVALID_CHARACTERS = { TRUE | FALSE } ]
                                        [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
                                        [ DEFAULT_NOTEBOOK_COMPUTE_POOL_CPU = '<compute_pool_name>' ]
                                        [ DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU = '<compute_pool_name>' ]
                                        [ OBJECT_VISIBILITY = { <object_visibility_spec> | PRIVILEGED } ]
                                        [ LOG_LEVEL = '<log_level>' ]
                                        [ METRIC_LEVEL = '<metric_level>' ]
                                        [ TRACE_LEVEL = '<trace_level>' ]
                                        [ STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED } ]
                                        [ EVENT_TABLE = <event_table_name> ]
                                        [ COMMENT = '<string_literal>' ]
                                        [ CATALOG_SYNC = '<snowflake_open_catalog_integration_name>' ]
                                        [ REPLICABLE_WITH_FAILOVER_GROUPS = { 'YES' | 'NO' } ]
                                        [ BASE_LOCATION_PREFIX = '<string>' ]
                                        [ DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE = <warehouse_name> ]
                                        [ CLASSIFICATION_PROFILE = '<profile_name>' ]
                                        [ CONTACT <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ]
                                        [ ENABLE_DATA_COMPACTION = { TRUE | FALSE } ]
                                        [ DATA_QUALITY_MONITORING_SETTINGS = <yaml_spec> ]
                                        [ OAUTH_AUTHORIZATION_SERVER = <integration_name> ]
                                        [ OAUTH_SCOPES_SUPPORTED = '<comma_separated_scopes>' ]

ALTER DATABASE <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER DATABASE <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER DATABASE [ IF EXISTS ] <name> SET FEATURE POLICY <policy_name> [ FORCE ]

ALTER DATABASE [ IF EXISTS ] <name> UNSET FEATURE POLICY

ALTER DATABASE [ IF EXISTS ] <name> UNSET { DATA_RETENTION_TIME_IN_DAYS         |
                                            MAX_DATA_EXTENSION_TIME_IN_DAYS     |
                                            EXTERNAL_VOLUME                     |
                                            CATALOG                             |
                                            ICEBERG_DEFAULT_DDL_COLLATION       |
                                            ICEBERG_VERSION_DEFAULT             |
                                            ICEBERG_MERGE_ON_READ_BEHAVIOR      |
                                            ENABLE_ICEBERG_MERGE_ON_READ        |
                                            DEFAULT_DDL_COLLATION               |
                                            DEFAULT_NOTEBOOK_COMPUTE_POOL_CPU   |
                                            DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU   |
                                            OBJECT_VISIBILITY                   |
                                            STORAGE_SERIALIZATION_POLICY        |
                                            EVENT_TABLE = <event_table_name>    |
                                            COMMENT                             |
                                            CATALOG_SYNC                        |
                                            REPLICABLE_WITH_FAILOVER_GROUPS     |
                                            BASE_LOCATION_PREFIX                |
                                            DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE|
                                            CLASSIFICATION_PROFILE              |
                                            CONTACT <purpose>                   |
                                            ENABLE_DATA_COMPACTION              |
                                            OAUTH_AUTHORIZATION_SERVER          |
                                            OAUTH_SCOPES_SUPPORTED              |
                                            DCM PROJECT
                                          }
                                          [ , ... ]
```

## Database replication and failover syntax

Important

This section describes a limited database replication feature that is different from the
[account replication feature](/user-guide/account-replication-intro). Snowflake strongly
recommends using the account replication feature to replicate and failover databases.

**Database Replication**

Copy code

```
ALTER DATABASE <name> ENABLE REPLICATION TO ACCOUNTS <account_identifier> [ , <account_identifier> ... ] [ IGNORE EDITION CHECK ]

ALTER DATABASE <name> DISABLE REPLICATION [ TO ACCOUNTS <account_identifier> [ , <account_identifier> ... ] ]

ALTER DATABASE <name> REFRESH
```

**Database Failover**

Copy code

```
ALTER DATABASE <name> ENABLE FAILOVER TO ACCOUNTS <account_identifier> [ , <account_identifier> ... ]

ALTER DATABASE <name> DISABLE FAILOVER [ TO ACCOUNTS <account_identifier> [ , <account_identifier> ... ] ]

ALTER DATABASE <name> PRIMARY
```

## Parameters

`name`
:   Specifies the identifier for the database to alter. If the identifier contains spaces, special characters, or mixed-case characters, the entire
    string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`RENAME TO new_db_name`
:   Specifies the new identifier for the database; must be unique for your account.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

    When an object is renamed, other objects that reference it must be updated with the new name.

`SWAP WITH target_db_name`
:   Swaps all objects (schemas, tables, views, and so on) and metadata, including identifiers, between the two specified databases. Also swaps all access
    control privileges granted on the databases and objects they contain. `SWAP WITH` essentially performs a rename of both databases as a
    single operation.

`SET ...`
:   Specifies one (or more) properties to set for the database (separated by blank spaces, commas, or new lines):

    `DATA_RETENTION_TIME_IN_DAYS = num`
    :   Specifies the number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the database, as well as specifying the
        default Time Travel retention time for all schemas created in the database.

        The value you can specify depends on the Snowflake Edition you are using:

        - Standard Edition: `0` or `1`
        - Enterprise Edition (or higher): `0` to `90`

    `MAX_DATA_EXTENSION_TIME_IN_DAYS = integer`
    :   Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in the database
        to prevent streams on the tables from becoming stale.

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
    :   Specifies a default [collation specification](/sql-reference/collation#label-collation-specification) for:

        - Any new columns added to existing tables in the database.
        - All columns in new tables added to the database.

        Setting the parameter does not change the collation specification for any existing columns.

        For more information about the parameter, see [DEFAULT\_DDL\_COLLATION](/sql-reference/parameters#label-default-ddl-collation).

    `DEFAULT_NOTEBOOK_COMPUTE_POOL_CPU = compute_pool_name`
    :   CPU compute pool name that overrides the default CPU compute pool Snowflake provisioned in your account for running Notebooks. For more information, see [System compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pools-default-compute-pools-for-notebooks).

    `DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU = compute_pool_name`
    :   GPU compute pool name that overrides the default GPU compute pool Snowflake provisioned in your account for running Notebooks. For more information, see [System compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pools-default-compute-pools-for-notebooks).

    `OBJECT_VISIBILITY = { object_visibility_spec | PRIVILEGED }`
    > [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
    >
    > Available to all accounts.
    >
    > Specifies the visibility of objects in the database, which controls the [discoverability of the objects](/user-guide/ui-snowsight/object-visibility-universal-search)
    > and enables users without explicit access privileges to find objects and request access.
    >
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
    >
    > Default: `'PRIVILEGED'`

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

        For information about levels, see [TRACE\_LEVEL](/sql-reference/parameters#label-trace-level). For information about setting the trace level, see
        [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

    `STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED }`
    :   Specifies the storage serialization policy for [Apache Iceberg™ tables](/user-guide/tables-iceberg) that use Snowflake as the catalog.

        - `COMPATIBLE`: Snowflake performs encoding and compression of data files that ensures interoperability with third-party compute engines.
        - `OPTIMIZED`: Snowflake performs encoding and compression of data files that ensures the best table performance within Snowflake.

        Default: `OPTIMIZED`

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `CONTACT purpose = contact [ , purpose = contact ... ]`
    :   Associate the existing object with one or more [contacts](/user-guide/contacts-using). For a list of valid purposes, see [Associate a contact with an object](/user-guide/contacts-using#label-contacts-associate).

        You cannot set the CONTACT property with other properties in the same statement.

    `EVENT_TABLE = event_table_name`
    :   Specifies the fully-qualified name of the event table that should collect telemetry data from objects in the database, such as
        procedures and UDFs.

        For more information, see [Associate an event table with an object](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-object).

        Associating an event table with a database is available in [Enterprise Edition or higher](/user-guide/intro-editions).

    `CLASSIFICATION_PROFILE = 'profile_name'`
    :   Sets a classification profile on the database to implement [sensitive data classification](/user-guide/classify-auto)
        for all of the tables and views in the database.

        Specify `profile_name` as a fully qualified name of a classification profile (that is, an instance of the
        CLASSIFICATION\_PROFILE class).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the database.

    `CATALOG_SYNC = 'snowflake_open_catalog_integration_name'`
    :   Specifies the name of a catalog integration configured for [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview).
        If specified, Snowflake syncs Snowflake-managed Apache Iceberg™ tables in the database with an external catalog in your Snowflake Open Catalog account. For more
        information about syncing Snowflake-managed Iceberg tables with Open Catalog, see [Sync a Snowflake-managed table with Snowflake Open Catalog](/user-guide/tables-iceberg-open-catalog-sync).

        For more information about this parameter, see [CATALOG\_SYNC](/sql-reference/parameters#label-catalog-sync).

        Default: No value

    `REPLICABLE_WITH_FAILOVER_GROUPS = { 'YES' | 'NO' }`
    :   Specifies if all the schemas in the database are eligible for replication.
        You can set this property to `NO` for a database, and then allow some schemas
        to be replicated by setting the equivalent property to `YES` for those schemas.

        For more information about this parameter, see [Schema-level replication for failover groups](/user-guide/account-replication-config#label-schema-level-replication).

        Default: `'YES'`

    `DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE`
    :   Specifies the default warehouse to be used when creating a notebook using SQL.

    `BASE_LOCATION_PREFIX = 'string'`
    :   Specifies a prefix for Snowflake to use in the write path for Snowflake-managed Apache Iceberg™ tables.
        For more information,
        see [data and metadata directories for Iceberg tables](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-base-location) and
        [BASE\_LOCATION\_PREFIX](/sql-reference/parameters#label-base-location-prefix) in the Snowflake Parameters topic.

        Default: No value

    `ENABLE_DATA_COMPACTION = { TRUE | FALSE }`
    :   Specifies whether Snowflake should enable data compaction on Snowflake-managed [Apache Iceberg™ tables](/user-guide/tables-iceberg).

        - `TRUE`: Snowflake performs data compaction on the tables.
        - `FALSE`: Snowflake doesn’t perform data compaction on the tables.

        Default: `TRUE`

        For more information, see [ENABLE\_DATA\_COMPACTION](/sql-reference/parameters#label-enable-data-compaction) and [Set data compaction](/user-guide/tables-iceberg-manage#label-tables-iceberg-manage-set-data-compaction).

    `DATA_QUALITY_MONITORING_SETTINGS = yaml_spec`
    > [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
    >
    > Available to all accounts that are Enterprise Edition (or higher).
    >
    > To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
    >
    > Specifies settings that control whether notifications are sent when data quality issues are detected in the database. Set the property
    > to a [dollar-quoted](/sql-reference/data-types-text#label-dollar-quoted-string-constants) YAML specification in the following format:
    >
    > Copy code
    >
    > ```
    > $$
    > notification:
    >   enabled: <boolean>
    >   email_recipients: [ <list_of_emails> ]
    >   integrations:
    >     - <notification_integration>
    >   cooldown_hours: <integer>
    >   metadata_included: <boolean>
    > $$
    > ```
    >
    > In the syntax above:
    >
    > - `enabled`: If `true`, notifications are sent when there is a data quality issue.
    > - `email_recipients`: An array of email addresses, where each address is enclosed in single quotes.
    > - `integrations`: Specifies a list of [notification integrations](/sql-reference/sql/create-notification-integration) that
    >   provide an interface between Snowflake and a third-party messaging service that sends the notifications.
    > - `cooldown_hours`: Number of hours that Snowflake waits before sending another notification. Valid values are between `1` (one hour) and `720` (30 days), inclusive.
    > - `metadata_included`: If `true`, the notification includes metadata that identifies which object within the database had
    >   the data quality issue. If `false`, the notification is sent, but it doesn’t identify which object had the issue.
    >
    > For more information about setting this parameter, including an example, see [Configure database settings for data quality notifications](/user-guide/data-quality-notifications#label-data-quality-notifications-database).

    `OAUTH_AUTHORIZATION_SERVER = integration_name`
    :   Specifies the name of an [External OAuth security integration](/sql-reference/sql/create-security-integration-oauth-external) to use as the authorization server for MCP servers in this database. When set, Snowflake advertises the external issuer in the Protected Resource Metadata endpoint for MCP servers in this database, and rejects OAuth tokens that weren’t issued by the specified authorization server. This enforcement applies only to OAuth calls against MCP server endpoints.

        Must be a valid `EXTERNAL_OAUTH` security integration. The integration must exist at SET time; if the integration is later dropped or disabled, the Protected Resource Metadata endpoint publishes an empty `authorization_servers` list and doesn’t fall back to Snowflake OAuth.

        This parameter follows Snowflake’s standard account/database/schema lineage inheritance. A database-level value overrides any account-level value; a schema-level value within this database overrides the database-level value.

        Default: No value (inherits from account, or uses Snowflake OAuth if unset at all levels)

        For more information, see [Configure External OAuth authentication for MCP servers](/user-guide/snowflake-cortex/cortex-agents-mcp#label-cortex-mcp-external-oauth) and [OAUTH\_AUTHORIZATION\_SERVER](/sql-reference/parameters#label-oauth-authorization-server).

    `OAUTH_SCOPES_SUPPORTED = 'comma_separated_scopes'`
    :   Specifies a comma-separated list of OAuth scopes to advertise in the Protected Resource Metadata endpoint for MCP servers in this database.

        For accepted scope values and SET-time validation rules, see [OAUTH\_SCOPES\_SUPPORTED](/sql-reference/parameters#label-oauth-scopes-supported).

        If `OAUTH_AUTHORIZATION_SERVER` is also set, the advertised scopes are those in this parameter. If only `OAUTH_SCOPES_SUPPORTED` is set without `OAUTH_AUTHORIZATION_SERVER`, Snowflake uses the specified scopes with Snowflake OAuth.

        This parameter follows Snowflake’s standard account/database/schema lineage inheritance. A database-level value overrides any account-level value; a schema-level value within this database overrides the database-level value.

        Default: No value (inherits from account). If unset at all levels with Snowflake OAuth, advertises `session:role:all`. If unset while `OAUTH_AUTHORIZATION_SERVER` is set, advertises `session:role-any` when the integration has `EXTERNAL_OAUTH_ANY_ROLE_MODE = ENABLE` or `ENABLE_FOR_PRIVILEGE`; otherwise advertises an empty list.

        For more information, see [Configure External OAuth authentication for MCP servers](/user-guide/snowflake-cortex/cortex-agents-mcp#label-cortex-mcp-external-oauth) and [OAUTH\_SCOPES\_SUPPORTED](/sql-reference/parameters#label-oauth-scopes-supported).

`UNSET ...`
:   Specifies one (or more) properties and/or parameters to unset for the database, which resets them to the defaults:

    - `DATA_RETENTION_TIME_IN_DAYS`
    - `MAX_DATA_EXTENSION_TIME_IN_DAYS`
    - `EXTERNAL_VOLUME`
    - `CATALOG`
    - `ICEBERG_DEFAULT_DDL_COLLATION`
    - `ICEBERG_VERSION_DEFAULT`
    - `ICEBERG_MERGE_ON_READ_BEHAVIOR`
    - `ENABLE_ICEBERG_MERGE_ON_READ`
    - `DEFAULT_DDL_COLLATION`
    - `TAG tag_name [ , tag_name ... ]`
    - `DEFAULT_NOTEBOOK_COMPUTE_POOL_CPU`
    - `DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU`
    - `STORAGE_SERIALIZATION_POLICY`
    - `EVENT_TABLE = event_table_name`
    - `COMMENT`
    - `CATALOG_SYNC`
    - `REPLICABLE_WITH_FAILOVER_GROUPS`
    - `BASE_LOCATION_PREFIX`
    - `DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE`
    - `CLASSIFICATION_PROFILE`
    - `CONTACT purpose`
    - `ENABLE_DATA_COMPACTION`
    - `OAUTH_AUTHORIZATION_SERVER`
    - `OAUTH_SCOPES_SUPPORTED`

    You can reset multiple properties/parameters with a single ALTER statement; however, each property/parameter must be separated by a
    comma. When resetting a property/parameter, specify only the name; specifying a value for the property will return an error.

    You cannot unset the CONTACT property with other properties in the same statement.

`SET FEATURE POLICY policy_name [ FORCE ]`

> Applies a [feature policy](/user-guide/feature-policies) to the database. A feature policy
> controls which object types can be created within the database.
>
> Use `FORCE` to replace an existing policy without unsetting it first.
>
> Requires the `APPLY FEATURE POLICY` privilege on the account.

`UNSET FEATURE POLICY`

> Removes the feature policy from the database. When unset, the account-level
> `FOR ALL DATABASES` or `FOR ALL PERSONAL DATABASES` policy takes effect for this database,
> if one is set. See
> [Feature policy precedence](/user-guide/feature-policies#label-feature-policy-precedence) for
> details.

`UNSET DCM PROJECT`

> Detaches the database from the [DCM project](/user-guide/dcm-projects/dcm-projects-overview) that currently manages it.
> The command removes the association between the database and the DCM project without dropping the database. See [Detach objects from a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-detach-object) for more information.

## Database replication and failover parameters

Important

This section describes a limited database replication feature that is different from the
[account replication feature](/user-guide/account-replication-intro). Snowflake strongly
recommends using the account replication feature to replicate and failover databases.

`ENABLE REPLICATION TO ACCOUNTS account_identifier [ , account_identifier ... ]`
:   Promotes a local database to serve as a primary database for replication. A primary database can be replicated in one or more accounts,
    allowing users in those accounts to query objects in each *secondary* (that is, replica) database.

    Alternatively, modify an existing primary database to add to or remove from the list of accounts that can store a replica of the database.

    Provide a comma-separated list of accounts in your organization that can store a replica of this database.

    `account_identifier`
    :   Unique identifier of the account. The preferred identifier is `organization_name.account_name`. To view the list of accounts
        enabled for replication in your organization, query [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts).

        Though the legacy account locator can also be used as the account identifier, its use is discouraged as it may not work in the future.
        For more information about using the account locator as an account identifier, see [Database Replication and Failover Usage Notes](#database-replication-and-failover-usage-notes).

    `IGNORE EDITION CHECK`
    :   Allows replicating data to accounts on lower editions in either of the following scenarios:

        - The primary database is in a Business Critical (or higher) account but one or more of the accounts approved for replication are on lower
          editions. Business Critical Edition is intended for Snowflake accounts with extremely sensitive data.
        - The primary database is in a Business Critical (or higher) account and a signed business associate agreement is in place to store PHI data
          in the account per HIPAA and [HITRUST](/user-guide/intro-cloud-platforms#label-hitrust-csf-cert) regulations, but no such agreement is in place for one or more of the
          accounts approved for replication, regardless if they are Business Critical (or higher) accounts.

        Both scenarios are prohibited by default in an effort to help prevent account administrators for Business Critical (or higher) accounts from
        inadvertently replicating sensitive data to accounts on lower editions.

`DISABLE REPLICATION [ TO ACCOUNTS account_identifier [ , account_identifier ... ] ]`
:   Disables replication for this primary database, meaning no replica of this database (that is, secondary database) in another account can be refreshed.
    Any secondary databases remain linked to the primary database, but requests to refresh a secondary database are denied.

    Note that disabling replication for a primary database does not prevent it from being replicated to the same account; therefore, the database
    continues to be listed in the [SHOW REPLICATION DATABASES](/sql-reference/sql/show-replication-databases) output.

    Optionally provide a comma-separated list of accounts in your organization to disable replication for this database only in the specified
    accounts.

    `account_identifier`
    :   Unique identifier of the account. The preferred identifier is `organization_name.account_name`. To view the list of accounts
        enabled for replication in your organization, query [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts).

        Though the legacy account locator can also be used as the account identifier, its use is discouraged as it may not work in the future.
        For more information about using the account locator as an account identifier, see [Database Replication and Failover Usage Notes](#database-replication-and-failover-usage-notes).

`REFRESH`
:   Refreshes a secondary database from a snapshot of its primary database. A snapshot includes changes to the objects and data.

`ENABLE FAILOVER TO ACCOUNTS account_identifier [ , account_identifier ... ]`
:   Specifies a comma-separated list of accounts in your organization where a replica of this primary database can be promoted to serve as the
    primary database.

    `account_identifier`
    :   Unique identifier of the account. The preferred identifier is `organization_name.account_name`. To view the list of accounts
        enabled for replication in your organization, query [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts).

        Though the legacy account locator can also be used as the account identifier, its use is discouraged as it may not work in the future.
        For more information about using the account locator as an account identifier, see [Database Replication and Failover Usage Notes](#database-replication-and-failover-usage-notes).

`DISABLE FAILOVER [ TO ACCOUNTS account_identifier [ , account_identifier ... ] ]`
:   Disables failover for this primary database, meaning no replica of this database (that is, secondary database) can be promoted to serve as the
    primary database.

    Optionally provide a comma-separated list of accounts in your organization to disable failover for this database only in the specified
    accounts.

    `account_identifier`
    :   Unique identifier of the account. The preferred identifier is `organization_name.account_name`. To view the list of accounts
        enabled for replication in your organization, query [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts).

        Though the legacy account locator can also be used as the account identifier, its use is discouraged as it may not work in the future.
        For more information about using the account locator as an account identifier, see [Database Replication and Failover Usage Notes](#database-replication-and-failover-usage-notes).

`PRIMARY`
:   Promotes the specified secondary (replica) database to serve as the primary database. When promoted, the database becomes writeable. At the same
    time, the previous primary database becomes a read-only secondary database.

## Usage notes

- To rename a database, the role used to perform the operation must have the CREATE DATABASE global privilege and OWNERSHIP privilege on
  the database.
- To swap two databases, the role used to perform the operation must have OWNERSHIP privileges on both databases.
- To update a comment, the role used to perform the operation must be granted or inherit the MODIFY privilege on the database.
- To specify the default version of the Apache Iceberg™ specification that Iceberg tables conform to, you must use a role that has been granted the OWNERSHIP privilege on the database.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Database replication and failover usage notes

Important

This section describes a limited database replication feature that is different from the
[account replication feature](/user-guide/account-replication-intro). Snowflake strongly
recommends using the account replication feature to replicate and failover databases.

- Only account administrators (users with the ACCOUNTADMIN role) can enable and manage database replication and failover.
- A default 10 TB size limit is applied when a primary database is initially replicated to a secondary database. To change or remove the size limit,
  set the [INITIAL\_REPLICATION\_SIZE\_LIMIT\_IN\_TB](/sql-reference/parameters#label-initial-replication-size-in-tb) parameter at the account level.

  Note that there is currently no default size limit applied to subsequent refreshes of a secondary database.
- The preferred method of identifying an account uses the organization name and account name as the account
  identifier. If you decide to use the legacy account locator instead, see [Account identifiers for replication and failover](/user-guide/admin-account-identifier#label-account-identifier-for-replication).

## General examples

Rename database `db1` to `db2`:

> Copy code
>
> ```
> ALTER DATABASE IF EXISTS db1 RENAME TO db2;
> ```

## Database replication examples

Important

This section describes a limited database replication feature that is different from the
[account replication feature](/user-guide/account-replication-intro). Snowflake strongly
recommends using the account replication feature to replicate and failover databases.

Use a replication or failover group to replicate and failover a single database. For examples, see one of the following:

- [Examples](/sql-reference/sql/create-failover-group#label-failover-group-single-database).
- [Examples](/sql-reference/sql/create-replication-group#label-replication-group-single-database).
