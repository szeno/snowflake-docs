# DROP ICEBERG TABLE

Removes an [Apache Iceberg™ table](/user-guide/tables-iceberg) from the current/specified schema, but retains a version of the
Iceberg table so that it can be recovered using [UNDROP ICEBERG TABLE](/sql-reference/sql/undrop-iceberg-table). For more information, see [Usage Notes](#usage-notes) (in this topic).

Note that this topic refers to Iceberg tables as simply “tables” except where specifying *Iceberg tables* avoids confusion.

See also:
:   [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) , [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) , [UNDROP ICEBERG TABLE](/sql-reference/sql/undrop-iceberg-table)

## Syntax

Copy code

```
DROP [ ICEBERG ] TABLE [ IF EXISTS ] <name> [ CASCADE | RESTRICT ] [ PURGE ]
```

## Parameters

`name`
:   Specifies the identifier for the table to drop. If the identifier contains spaces, special characters, or mixed-case characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive
    (for example, `"My Object"`).

    If the table identifier is not fully qualified (in the form of `db_name.schema_name.table_name` or
    `schema_name.table_name`), the command looks for the table in the current schema for the session.

`CASCADE | RESTRICT`
:   Specifies whether the table can be dropped if foreign keys exist that reference the table:

    - `CASCADE` drops the table even if the table has primary/unique keys that are referenced by foreign keys in other tables.
    - `RESTRICT` returns a warning about existing foreign key references and does not drop the table.

    Default: `CASCADE`

`PURGE`
:   When specified for an externally managed Iceberg table in a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database),
    forwards the purge intent in the drop-table request to the external Iceberg catalog.
    Snowflake does not delete data files directly — the external catalog is responsible for removing the table’s
    underlying data and metadata files from storage.

    `PURGE` can only be used with externally managed Iceberg tables in a catalog-linked database. Using it on a
    non-externally-managed table, a non-Iceberg table, or a table outside a catalog-linked database results in a
    compilation error.

    As an alternative to specifying `PURGE` on each statement, you can set the `PURGE_ON_DROP_TABLE` parameter
    on the table, schema, or catalog-linked database so that every `DROP TABLE` automatically forwards the purge
    intent to the catalog. For more information, see [PURGE\_ON\_DROP\_TABLE](/sql-reference/sql/drop-iceberg-table#label-purge-on-drop-table-param).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Iceberg table | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| USAGE | External volume |  |
| USAGE | Integration (catalog) | Required if the Iceberg table uses an external catalog. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- For [externally managed Iceberg tables with writes enabled](/user-guide/tables-iceberg-externally-managed-writes) that
  are in a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database), Snowflake also instructs your
  external Iceberg REST catalog to drop the table. Snowflake makes a call to your remote Iceberg catalog instructing it
  to drop the table entry. By default, Snowflake does not signal the catalog to delete the table’s underlying data and
  metadata files from storage.

  To also remove the underlying files, specify the `PURGE` keyword or set the `PURGE_ON_DROP_TABLE` parameter
  on the table, schema, or catalog-linked database. When purge is requested, Snowflake forwards purge intent
  in the drop-table request to the catalog. Snowflake never deletes external data files directly — the catalog
  is responsible for the actual file deletion.

  Snowflake only drops the table after confirming that the table has successfully been dropped from the remote catalog.

  Note

  For a writable externally managed Iceberg table in a standard Snowflake database (not a catalog-linked database),
  `DROP ICEBERG TABLE` removes only the table entry in Snowflake. It doesn’t drop or deregister the table in your
  remote catalog. To remove the table from the remote catalog, use the catalog’s own API or tooling.

  If you use the AWS Glue Data Catalog as your external catalog, the catalog does not honor the purge flag, so
  the underlying table files are retained regardless of whether `PURGE` is specified. This behavior is specific
  to the AWS Glue Data Catalog implementation.

- The `PURGE_ON_DROP_TABLE` parameter, when set to `TRUE` on a table, schema, or catalog-linked database,
  automatically forwards the purge intent to the external catalog on every `DROP TABLE` — without requiring
  the explicit `PURGE` keyword. The same purge intent is also forwarded on the implicit drop performed by
  `CREATE OR REPLACE TABLE`. For more information and examples, see
  [Dropping an Iceberg table](/user-guide/tables-iceberg-externally-managed-writes#label-tables-iceberg-external-writes-drop-table).
- Dropping a table does not permanently remove it from the system. Snowflake retains a version of the dropped table in
  [Time Travel](/user-guide/data-time-travel) for the number of days specified by the `DATA_RETENTION_TIME_IN_DAYS` parameter for
  the table. For more information, see [Metadata and snapshots for Iceberg tables](/user-guide/tables-iceberg#label-tables-iceberg-snapshots).
- Within the Time Travel retention period, you can restore a dropped table by using the [UNDROP ICEBERG TABLE](/sql-reference/sql/undrop-iceberg-table) command.
- After a dropped table has been purged, it cannot be recovered; it must be recreated.
- After dropping a table, creating a table with the same name creates a new version of the table. You can restore
  the dropped version of the previous table with the following steps:

  1. Rename the current version of the table to a different name.
  2. Use the [UNDROP ICEBERG TABLE](/sql-reference/sql/undrop-iceberg-table) command to restore the previous version.
- Before you drop a table, verify that no views reference the table. Dropping a table that is referenced by a view
  invalidates the view (querying the view returns an “object does not exist” error).

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Drop a table:

> Copy code
>
> ```
> DROP ICEBERG TABLE t2;
>
> +--------------------------+
> | status                   |
> |--------------------------|
> | T2 successfully dropped. |
> +--------------------------+
> ```

Drop the table again, but don’t raise an error if the table doesn’t exist:

> Copy code
>
> ```
> DROP ICEBERG TABLE IF EXISTS t2;
>
> +------------------------------------------------------------+
> | status                                                     |
> |------------------------------------------------------------|
> | Drop statement executed successfully (T2 already dropped). |
> +------------------------------------------------------------+
> ```

Drop a table in a catalog-linked database and forward the purge intent to the external catalog:

> Copy code
>
> ```
> DROP ICEBERG TABLE my_catalog_linked_db.public.my_iceberg_table PURGE;
>
> +-----------------------------------------+
> | status                                  |
> |-----------------------------------------|
> | MY_ICEBERG_TABLE successfully dropped.  |
> +-----------------------------------------+
> ```
