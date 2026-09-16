# ALTER DATABASE (catalog-linked)

Modifies the properties for an existing [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database).

Database modifications include the following actions:

- Enabling or turning off automatic discovery.
- Changing the allowed and blocked namespaces.
- Changing the time interval that Snowflake should use for automatically discovering schemas and tables in your remote catalog.
- Changing whether your remote catalog is read only or writable.

## Syntax

Copy code

```
ALTER DATABASE [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER DATABASE [ IF EXISTS ] <name> SUSPEND DISCOVERY

ALTER DATABASE [ IF EXISTS ] <name> RESUME DISCOVERY

ALTER DATABASE [ IF EXISTS ] <name> UPDATE LINKED_CATALOG
  ADD ( '<namespace>' [ , ... ] ) TO ALLOWED_NAMESPACES

ALTER DATABASE [ IF EXISTS ] <name> UPDATE LINKED_CATALOG
  REMOVE ( '<namespace>' [ , ... ] ) FROM ALLOWED_NAMESPACES

ALTER DATABASE [ IF EXISTS ] <name> UPDATE LINKED_CATALOG
  UNSET ALLOWED_NAMESPACES

ALTER DATABASE [ IF EXISTS ] <name> UPDATE LINKED_CATALOG
  ADD ( '<namespace>' [ , ... ] ) TO BLOCKED_NAMESPACES

ALTER DATABASE [ IF EXISTS ] <name> UPDATE LINKED_CATALOG
  REMOVE ( '<namespace>' [ , ... ] ) FROM BLOCKED_NAMESPACES

ALTER DATABASE [ IF EXISTS ] <name> UPDATE LINKED_CATALOG
  UNSET BLOCKED_NAMESPACES

ALTER DATABASE [ IF EXISTS ] <name> UPDATE LINKED_CATALOG
  SET SYNC_INTERVAL_SECONDS = <value>

ALTER DATABASE [ IF EXISTS ] <name> UPDATE LINKED_CATALOG
  SET ALLOWED_WRITE_OPERATIONS = { NONE | ALL }

ALTER DATABASE [ IF EXISTS ] <name> SET [ BASE_LOCATION_PREFIX = '<string>' ]
                                        [ COMMENT = '<string_literal>' ]
                                        [ CONTACT <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ]
                                        [ ICEBERG_VERSION_DEFAULT = <integer> ]
                                        [ ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' } ]
                                        [ ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE } ]

ALTER DATABASE [ IF EXISTS ] <name> UNSET { BASE_LOCATION_PREFIX         |
                                            COMMENT                      |
                                            CONTACT                      |
                                            ICEBERG_VERSION_DEFAULT      |
                                            ICEBERG_MERGE_ON_READ_BEHAVIOR |
                                            ENABLE_ICEBERG_MERGE_ON_READ
                                          }
```

## Parameters

`name`
:   Specifies the identifier for the catalog-linked database to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Changes the name of the catalog-linked database to `new_name`. The new identifier must be unique for the account.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

    When an object is renamed, other objects that reference it must be updated with the new name.

`SUSPEND DISCOVERY`
:   Suspends automatic discovery. You might want to suspend automatic discovery to prevent consuming unnecessary credits or
    resources if an underlying issue is preventing Snowflake from discovering the tables in your remote catalog. For example,
    you might want to suspend automatic discovery because there is an underlying issue with missing permissions or a misconfiguration.
    After you resolve the issue, run ALTER DATABASE … RESUME DISCOVERY to resume discovery.

    To confirm that automatic discovery is suspended, call the [SYSTEM$CATALOG\_LINK\_STATUS](/sql-reference/functions/system_catalog_link_status) function and
    verify that the `executionState` field is set to `SUSPENDED`. If you suspend automatic discovery but an automatic discovery task is
    currently running, the execution state won’t change to suspended until the task is complete.

    Note

    Suspending automatic discovery doesn’t turn off automated refresh. To turn off automated refresh for an existing
    Iceberg table, see [Enable or turn off automated refresh](/user-guide/tables-iceberg-auto-refresh#label-tables-iceberg-auto-refresh-update).

`RESUME DISCOVERY`
:   Resumes automatic discovery. You might want to resume discovery for the following reasons:

    - You suspended discovery to resolve an issue and now you’re ready to resume discovery.
    - You want to force an immediate discovery run to ensure that recent changes, such as fixed permissions, are picked up.

    To confirm that automatic discovery is resumed, call the [SYSTEM$CATALOG\_LINK\_STATUS](/sql-reference/functions/system_catalog_link_status) function, and then
    verify that the `executionState` field is set to `RUNNING`.

`UPDATE LINKED_CATALOG`
:   Updates the properties that apply to catalog-linked databases. You can set the following properties:

    `ADD ( 'namespace1' [ , 'namespace2' , ... ] ) TO ALLOWED_NAMESPACES`
    :   Specifies one or more namespaces in your remote catalog to limit the scope of automatic discovery. Snowflake syncs the specified
        namespaces and all namespaces and tables that are nested under them.

        - If you created a catalog-linked database with an empty ALLOWED\_NAMESPACES list, Snowflake syncs *all* of the namespaces and tables from the
          remote catalog.

          If you later alter the database by specifying the ALLOWED\_NAMESPACES parameter to only allow a specific list of namespaces,
          Snowflake updates the catalog-linked database to only retain those namespaces you allow. All the other namespaces and tables are
          dropped from the catalog-linked database.
        - If you created a catalog-linked database with a list of ALLOWED\_NAMESPACES, Snowflake only creates those allowed namespaces in
          the catalog-linked database.

          If you later alter the database to add namespaces to the ALLOWED\_NAMESPACES list, Snowflake only creates the
          newly added namespaces and retains the existing allowed namespaces. If you remove namespaces from the ALLOWED\_NAMESPACES list,
          Snowflake only drops the newly removed namespaces from the catalog-linked database and retains all of the remaining allowed namespaces.

        If a nested namespace is in the ALLOWED\_NAMESPACES list but you set the
        NAMESPACE\_MODE parameter to IGNORE\_NESTED\_NAMESPACE, Snowflake doesn’t sync the nested namespace or any schemas and tables under it.

    `REMOVE ( 'namespace1' [ , 'namespace2' , ... ] ) FROM ALLOWED_NAMESPACES`
    :   Specifies one or more namespaces in your remote catalog to remove from your list of allowed namespaces.

    `UNSET ALLOWED_NAMESPACES`
    :   Unsets your list of allowed namespaces to the default, which is all namespaces are allowed.

    `ADD ( 'namespace1' [ , 'namespace2' , ... ] ) TO BLOCKED_NAMESPACES`
    :   Specifies one or more namespaces in your remote catalog to block for automatic discovery.

        Snowflake blocks the specified namespaces and all namespaces and tables that are nested under them.

        If you specify both ALLOWED\_NAMESPACES and BLOCKED\_NAMESPACES, the BLOCKED\_NAMESPACES list takes precedence.
        For example, if `ns1.ns2` is allowed, but `ns1` is blocked, then Snowflake won’t sync `ns1.ns2`.

    `REMOVE ( 'namespace1' [ , 'namespace2' , ... ] ) FROM BLOCKED_NAMESPACES`
    :   Specifies one or more namespaces in your remote catalog to remove from your list of blocked namespaces.

    `UNSET BLOCKED_NAMESPACES`
    :   Unsets your list of blocked namespaces to the default, which is zero namespaces are blocked.

    `SET SYNC_INTERVAL_SECONDS = value`
    :   Specifies the time interval in seconds that Snowflake should use for automatically discovering schemas and tables in your remote catalog.
        You can reduce your credit consumption by setting a longer time interval.

        Values: 30 to 86400 (1 day), inclusive

        Default: 30 seconds

    `SET ALLOWED_WRITE_OPERATIONS = { NONE | ALL }`
    :   Specifies whether your catalog-linked database is read-only or writable.

        - `NONE`: Your catalog-linked database is read-only.

          When your catalog-linked database is read only, any operation that you run that requires committing to the catalog fails. For
          example, DROP ICEBERG TABLE.
        - `ALL`: Your catalog-linked database is writable.

          Warning

          When your catalog-linked database has write permissions enabled, Snowflake propagates table drops to the remote catalog, which removes
          the table and data from both systems.

          Creating and writing to tables in nested namespaces is supported only when the catalog-linked database uses a catalog
          integration for a catalog that supports nested namespaces. For more information, see
          [Use CREATE SCHEMA to create namespaces in your external catalog](/user-guide/tables-iceberg-externally-managed-writes#label-tables-iceberg-externally-managed-writes-create-schema).

        Default: `ALL`

`SET ...`
:   Specifies one or more properties or parameters to set for the catalog-linked database, separated by blank spaces, commas, or new lines:

    `BASE_LOCATION_PREFIX = 'string'`
    :   Specifies a prefix for Snowflake to use in the write path for externally managed Apache Iceberg™ tables.
        For more information,
        see [Data and metadata directories for Iceberg tables](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-base-location) and
        [BASE\_LOCATION\_PREFIX](/sql-reference/parameters#label-base-location-prefix).

        Default: No value

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the catalog-linked database.

    `CONTACT purpose = contact [ , purpose = contact ... ]`
    :   Associate the existing object with one or more [contacts](/user-guide/contacts-using). For a list of valid purposes, see [Associate a contact with an object](/user-guide/contacts-using#label-contacts-associate).

        You cannot set the CONTACT property with other properties in the same statement.

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

`UNSET ...`
:   Specifies one or more properties or parameters to unset for the database, which resets them to the defaults:

    - `BASE_LOCATION_PREFIX`
    - `COMMENT`
    - `CONTACT`
    - `ICEBERG_VERSION_DEFAULT`
    - `ICEBERG_MERGE_ON_READ_BEHAVIOR`
    - `ENABLE_ICEBERG_MERGE_ON_READ`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | The catalog-linked database being modified. | Required to suspend or resume automatic table discovery. |
| OWNERSHIP or MODIFY | The catalog-linked database being modified. | Required for all other operations. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Reset the list of allowed namespaces for a catalog-linked database named `my_linked_db` to the default.

Copy code

```
ALTER DATABASE IF EXISTS my_linked_db UPDATE LINKED_CATALOG
  UNSET ALLOWED_NAMESPACES;
```

Add `my_namespace` to the list of allowed namespaces for a catalog-linked database named `my_linked_db`.

Copy code

```
ALTER DATABASE IF EXISTS my_linked_db UPDATE LINKED_CATALOG
 ADD ('my_namespace') TO ALLOWED_NAMESPACES;
```
