# ALTER SCHEMA

Modifies the properties for an existing schema, including renaming the schema or swapping it with another schema, and changing the Time Travel
data retention period (if you are using Snowflake Enterprise Edition or higher).

See also:
:   [CREATE SCHEMA](/sql-reference/sql/create-schema) , [DESCRIBE SCHEMA](/sql-reference/sql/desc-schema) , [DROP SCHEMA](/sql-reference/sql/drop-schema) , [SHOW SCHEMAS](/sql-reference/sql/show-schemas) , [UNDROP SCHEMA](/sql-reference/sql/undrop-schema)

## Syntax

Copy code

```
ALTER SCHEMA [ IF EXISTS ] <name> RENAME TO <new_schema_name>

ALTER SCHEMA [ IF EXISTS ] <name> SWAP WITH <target_schema_name>

ALTER SCHEMA [ IF EXISTS ] <name> SET {
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
                                      [ DEFAULT_NOTEBOOK_COMPUTE_POOL_CPU = '<compute_pool_name>' ]
                                      [ DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU = '<compute_pool_name>' ]
                                      [ LOG_LEVEL = '<log_level>' ]
                                      [ TRACE_LEVEL = '<trace_level>' ]
                                      [ STORAGE_SERIALIZATION_POLICY = { COMPATIBLE | OPTIMIZED } ]
                                      [ CLASSIFICATION_PROFILE = '<profile_name>' ]
                                      [ COMMENT = '<string_literal>' ]
                                      [ CATALOG_SYNC = '<snowflake_open_catalog_integration_name>' ]
                                      [ REPLICABLE_WITH_FAILOVER_GROUPS = { 'YES' | 'NO' } ]
                                      [ BASE_LOCATION_PREFIX = '<string>']
                                      [ DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE = '<warehouse_name>']
                                      [ CONTACT <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ]
                                      [ OBJECT_VISIBILITY = PRIVILEGED } ]
                                      [ ENABLE_DATA_COMPACTION = { TRUE | FALSE } ]
                                      [ OAUTH_AUTHORIZATION_SERVER = <integration_name> ]
                                      [ OAUTH_SCOPES_SUPPORTED = '<comma_separated_scopes>' ]
                                      }

ALTER SCHEMA [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER SCHEMA [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER SCHEMA [ IF EXISTS ] <name> UNSET {
                                        DATA_RETENTION_TIME_IN_DAYS         |
                                        MAX_DATA_EXTENSION_TIME_IN_DAYS     |
                                        EXTERNAL_VOLUME                     |
                                        CATALOG                             |
                                        ICEBERG_DEFAULT_DDL_COLLATION       |
                                        ICEBERG_VERSION_DEFAULT             |
                                        ICEBERG_MERGE_ON_READ_BEHAVIOR      |
                                        ENABLE_ICEBERG_MERGE_ON_READ        |
                                        REPLACE_INVALID_CHARACTERS          |
                                        DEFAULT_DDL_COLLATION               |
                                        LOG_LEVEL                           |
                                        TRACE_LEVEL                         |
                                        STORAGE_SERIALIZATION_POLICY        |
                                        COMMENT                             |
                                        CATALOG_SYNC                        |
                                        REPLICABLE_WITH_FAILOVER_GROUPS     |
                                        BASE_LOCATION_PREFIX                |
                                        DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE|
                                        CONTACT <purpose>
                                        CLASSIFICATION_PROFILE
                                        OBJECT_VISIBILITY                   |
                                        CONTACT <purpose>                   |
                                        CLASSIFICATION_PROFILE              |
                                        ENABLE_DATA_COMPACTION              |
                                        OAUTH_AUTHORIZATION_SERVER          |
                                        OAUTH_SCOPES_SUPPORTED              |
                                        DCM PROJECT
                                        }
                                        [ , ... ]

ALTER SCHEMA [ IF EXISTS ] <name> { ENABLE | DISABLE } MANAGED ACCESS
```

## Parameters

`name`
:   Specifies the identifier for the schema to alter. If the identifier contains spaces, special characters, or mixed-case characters, the entire
    string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`RENAME TO new_schema_name`
:   Specifies the new identifier for the schema; must be unique for the database.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database while optionally renaming the schema. To do so, specify a qualified
    `new_schema_name` value that includes the new database name in the form `db_name.new_schema_name`.

    Note

    The destination database must already exist. In addition, a schema with the same name cannot already exist in the new location;
    otherwise, the statement returns an error.

    When an object is renamed, other objects that reference it must be updated with the new name.

`SWAP WITH target_schema_name`
:   Swaps all objects (tables, views, etc.) and metadata, including identifiers, between the two specified schemas. Also swaps all access control
    privileges granted on the schemas and objects they contain. `SWAP WITH` essentially performs a rename of both schemas as a single operation.

`SET ...`
:   Specifies one (or more) properties to set for the schema (separated by blank spaces, commas, or new lines):

    `DATA_RETENTION_TIME_IN_DAYS = integer`
    :   Specifies the number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the schema, as well as specifying the
        default Time Travel retention time for all tables created in the schema.

        The value you can specify depends on the Snowflake Edition you are using:

        - Standard Edition: `0` or `1`
        - Enterprise Edition (or higher): `0` to `90`

    `MAX_DATA_EXTENSION_TIME_IN_DAYS = integer`
    :   Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in the schema
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

        - Any new columns added to existing tables in the schema.
        - All columns in new tables added to the schema.

        Setting the parameter does not change the collation specification for any existing columns.

        For more details about the parameter, see [DEFAULT\_DDL\_COLLATION](/sql-reference/parameters#label-default-ddl-collation).

    `DEFAULT_NOTEBOOK_COMPUTE_POOL_CPU = compute_pool_name`
    :   CPU compute pool name that overrides the default CPU compute pool Snowflake provisioned in your account for running Notebooks. For more information, see [System compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pools-default-compute-pools-for-notebooks).

    `DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU = compute_pool_name`
    :   GPU compute pool name that overrides the default GPU compute pool Snowflake provisioned in your account for running Notebooks. For more information, see [System compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pools-default-compute-pools-for-notebooks).

    `LOG_LEVEL = 'log_level'`
    :   Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at
        the specified level (and at more severe levels) are ingested.

        For more information about levels, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level). For information about setting log level, see
        [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

    `TRACE_LEVEL = 'trace_level'`
    :   Controls how trace events are ingested into the event table.

        For information about levels, see [TRACE\_LEVEL](/sql-reference/parameters#label-trace-level). For information about setting trace level, see
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

    `CLASSIFICATION_PROFILE = 'profile_name'`
    :   Associates the schema with a classification profile so that sensitive data in the schema is
        [automatically classified](/user-guide/classify-auto).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the schema.

    `CATALOG_SYNC = 'snowflake_open_catalog_integration_name'`
    :   Specifies the name of a catalog integration configured for [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview).
        If specified, Snowflake syncs Snowflake-managed Apache Iceberg™ tables in the schema with an external catalog in your Snowflake Open Catalog account.
        For more information about syncing Snowflake-managed Iceberg tables with Open Catalog, see [Sync a Snowflake-managed table with Snowflake Open Catalog](/user-guide/tables-iceberg-open-catalog-sync).

        For more information about this parameter, see [CATALOG\_SYNC](/sql-reference/parameters#label-catalog-sync).

        Default: No value

    `REPLICABLE_WITH_FAILOVER_GROUPS = { 'YES' | 'NO' }`
    :   Specifies if this schema is eligible for replication.
        You can set this property to `NO` to prevent individual schemas
        within a database from being replicated.

        For more information about this parameter, see [Schema-level replication for failover groups](/user-guide/account-replication-config#label-schema-level-replication).

        Default: `'YES'`

    `DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE = 'warehouse_name'`
    :   Specifies the default warehouse to use when you create a notebook using SQL.

    `BASE_LOCATION_PREFIX = 'string'`
    :   Specifies a prefix for Snowflake to use in the write path for Snowflake-managed Apache Iceberg™ tables.
        For more information,
        see [data and metadata directories for Iceberg tables](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-base-location) and
        [BASE\_LOCATION\_PREFIX](/sql-reference/parameters#label-base-location-prefix) in the Snowflake Parameters topic.

        Default: No value

`OBJECT_VISIBILITY = PRIVILEGED`

> [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
>
> Available to all accounts.
>
> Specifies that only roles within the current account that are granted an explicit privilege on the object can see the object. This is the default behavior in Snowflake.
>
> For examples, see [Make database objects discoverable in Universal Search](/user-guide/ui-snowsight/object-visibility-universal-search#label-object-visibility-examples).

`ENABLE_DATA_COMPACTION = { TRUE | FALSE }`
:   Specifies whether Snowflake should enable data compaction on Snowflake-managed [Apache Iceberg™ tables](/user-guide/tables-iceberg).

    - `TRUE`: Snowflake performs data compaction on the tables.
    - `FALSE`: Snowflake doesn’t perform data compaction on the tables.

    Default: `TRUE`

    For more information, see [ENABLE\_DATA\_COMPACTION](/sql-reference/parameters#label-enable-data-compaction) and [Set data compaction](/user-guide/tables-iceberg-manage#label-tables-iceberg-manage-set-data-compaction).

`OAUTH_AUTHORIZATION_SERVER = integration_name`
:   Specifies the name of an [External OAuth security integration](/sql-reference/sql/create-security-integration-oauth-external) to use as the authorization server for MCP servers in this schema. When set, Snowflake advertises the external issuer in the Protected Resource Metadata endpoint for MCP servers in this schema, and rejects OAuth tokens that weren’t issued by the specified authorization server. This enforcement applies only to OAuth calls against MCP server endpoints.

    Must be a valid `EXTERNAL_OAUTH` security integration. The integration must exist at SET time; if the integration is later dropped or disabled, the Protected Resource Metadata endpoint publishes an empty `authorization_servers` list and doesn’t fall back to Snowflake OAuth.

    This parameter follows Snowflake’s standard account/database/schema lineage inheritance. A schema-level value overrides any database-level or account-level value.

    Default: No value (inherits from database or account, or uses Snowflake OAuth if unset at all levels)

    For more information, see [Configure External OAuth authentication for MCP servers](/user-guide/snowflake-cortex/cortex-agents-mcp#label-cortex-mcp-external-oauth) and [OAUTH\_AUTHORIZATION\_SERVER](/sql-reference/parameters#label-oauth-authorization-server).

`OAUTH_SCOPES_SUPPORTED = 'comma_separated_scopes'`
:   Specifies a comma-separated list of OAuth scopes to advertise in the Protected Resource Metadata endpoint for MCP servers in this schema.

    For accepted scope values and SET-time validation rules, see [OAUTH\_SCOPES\_SUPPORTED](/sql-reference/parameters#label-oauth-scopes-supported).

    If `OAUTH_AUTHORIZATION_SERVER` is also set, the advertised scopes are those in this parameter. If only `OAUTH_SCOPES_SUPPORTED` is set without `OAUTH_AUTHORIZATION_SERVER`, Snowflake uses the specified scopes with Snowflake OAuth.

    This parameter follows Snowflake’s standard account/database/schema lineage inheritance. A schema-level value overrides any database-level or account-level value.

    Default: No value (inherits from database or account). If unset at all levels with Snowflake OAuth, advertises `session:role:all`. If unset while `OAUTH_AUTHORIZATION_SERVER` is set, advertises `session:role-any` when the integration has `EXTERNAL_OAUTH_ANY_ROLE_MODE = ENABLE` or `ENABLE_FOR_PRIVILEGE`; otherwise advertises an empty list.

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
    - `REPLACE_INVALID_CHARACTERS`
    - `DEFAULT_DDL_COLLATION`
    - `TAG tag_name [ , tag_name ... ]`
    - `LOG_LEVEL`
    - `TRACE_LEVEL`
    - `STORAGE_SERIALIZATION_POLICY`
    - `COMMENT`
    - `CATALOG_SYNC`
    - `REPLICABLE_WITH_FAILOVER_GROUPS`
    - `BASE_LOCATION_PREFIX`
    - `DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE`
    - `CONTACT purpose`
    - `CLASSIFICATION_PROFILE`
    - `OBJECT_VISIBILITY`
    - `ENABLE_DATA_COMPACTION`
    - `OAUTH_AUTHORIZATION_SERVER`
    - `OAUTH_SCOPES_SUPPORTED`

    You can reset multiple properties/parameters with a single ALTER statement; however, each property/parameter must be separated by a
    comma. When resetting a property/parameter, specify only the name; specifying a value for the property will return an error.

`UNSET DCM PROJECT`

> Detaches the schema from the [DCM project](/user-guide/dcm-projects/dcm-projects-overview) that currently manages it.
> The command removes the association between the schema and the DCM project without dropping the schema. See [Detach objects from a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-detach-object) for more information.

`{ ENABLE | DISABLE } MANAGED ACCESS`
:   Enable managed access for a schema, or disable to convert a managed access schema to a regular schema. Managed access schemas centralize
    privilege management with the schema owner.

    In regular schemas, the owner of an object (i.e. the role that has the OWNERSHIP privilege on the object) can grant further privileges on
    their objects to other roles. In managed access schemas, the schema owner manages all privilege grants, including
    [future grants](/user-guide/security-access-control-configure#label-granting-future-privs-on-schema-objects), on objects in the schema. Object owners retain the OWNERSHIP privileges
    on the objects; however, only the schema owner can manage privilege grants on the objects.

## Usage notes

- To rename a schema, the role used to perform the operation must have the CREATE SCHEMA privilege on the database for the schema and OWNERSHIP
  privileges on the schema.
- To swap two schemas, the role used to perform the operation must have OWNERSHIP privileges on both schemas.
- To convert a regular schema to a managed access schema:

  - The schema owner (i.e. the role that has the OWNERSHIP privileges on the schema) must also have the global MANAGE GRANTS privilege. The
    MANAGE GRANTS privilege is required because another role with this privilege could have defined future grants on objects of a specified
    type in the schema. After a regular schema becomes a managed access schema, the schema owner could revoke the future grants without
    understanding why a role with the MANAGE GRANTS privilege granted them.
  - All open future grants must be revoked using [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege) with the FUTURE keyword.

  After a regular schema is converted to a managed access schema, all privileges previously granted on individual objects are retained; however,
  the object owners cannot grant further privileges on those objects.
- To convert a managed access schema to a regular schema, the schema owner must also have the global MANAGE GRANTS privilege only if the
  current schema has future privilege grants defined.
- For schemas in a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database), this command only supports
  the following parameters:

  - SET/UNSET with the following options:

    - CLASSIFICATION\_PROFILE
    - COMMENT
    - CONTACT
    - STORAGE\_SERIALIZATION\_POLICY
    - TAG
  - ENABLE MANAGED ACCESS and DISABLE MANAGED ACCESS.
- To specify the default version of the Apache Iceberg™ specification that Iceberg tables conform to, the role used to perform the operation
  must have the OWNERSHIP privilege on the schema.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Rename schema `schema1` to `schema2`:

> Copy code
>
> ```
> ALTER SCHEMA IF EXISTS schema1 RENAME TO schema2;
> ```

Convert a regular schema to a managed access schema:

> Copy code
>
> ```
> ALTER SCHEMA schema2 ENABLE MANAGED ACCESS;
> ```
