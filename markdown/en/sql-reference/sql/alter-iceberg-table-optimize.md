# ALTER ICEBERG TABLE … OPTIMIZE

Rewrites affected partitions in a supported [Apache Iceberg™ table](/user-guide/tables-iceberg) to apply position deletes to the data
files. Use this command to clear active position-delete files from the table metadata before upgrading or converting a table.

## Syntax

Copy code

```
ALTER ICEBERG TABLE [ IF EXISTS ] <table_name> OPTIMIZE (REMOVE_POSITION_DELETES)
```

## Parameters

`table_name`
:   Identifier for the table to optimize.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`REMOVE_POSITION_DELETES`
:   Rewrites all affected partitions that contain v2-style position-delete files using copy-on-write. After the
    operation succeeds, active position-delete files for live data files are cleared from the table metadata.
    This includes v2-style position-delete files written by external engines.

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

- This operation is supported for Snowflake-managed Iceberg v2 tables and externally managed Iceberg v2 and v3 tables. It isn’t
  supported for Snowflake-managed Iceberg v3 tables, which record row-level deletes as deletion vectors instead of position-delete files.
- If the table has no partitions with position-delete files, the operation doesn’t rewrite any files or create a new table version.
- For externally managed Iceberg v3 tables, partitions that use deletion vectors aren’t rewritten. This operation doesn’t remove
  deletion vectors.
- For a partitioned table, the operation writes every rewritten data file under the table’s current default partition spec,
  including files that were originally written under an earlier partition spec.
- The operation doesn’t preserve the table’s existing output clustering. You might need to recluster the table afterward.

## Examples

The following example clears active position-delete files for live data files from the table metadata before upgrading a v2 table to Iceberg v3:

Copy code

```
ALTER ICEBERG TABLE my_v2_iceberg_table OPTIMIZE (REMOVE_POSITION_DELETES);
ALTER ICEBERG TABLE my_v2_iceberg_table UPGRADE TO ICEBERG VERSION 3;
```
