# SHOW ICEBERG TABLES

Lists the [Apache Iceberg™ tables](/user-guide/tables-iceberg) for which you have access privileges.

The command can be used to list Iceberg tables for the current/specified database or schema, or across your entire account.

This command returns different output columns than [SHOW TABLES](/sql-reference/sql/show-tables).
The output returns Iceberg table metadata and properties, ordered lexicographically by database, schema, and Iceberg table name (see
[Output](#output) in this topic for descriptions of the output columns). This is important to note if you want to filter the results using the
provided filters.

Note that this topic refers to Iceberg tables as simply “tables” except where specifying *Iceberg tables* avoids confusion.

See also:
:   [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) , [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) , [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table) , [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) , [SHOW TABLES](/sql-reference/sql/show-tables)

## Syntax

Copy code

```
SHOW [ TERSE ] [ ICEBERG ] TABLES [ LIKE '<pattern>' ]
                                  [ IN
                                        {
                                          ACCOUNT                  |

                                          DATABASE                 |
                                          DATABASE <database_name> |

                                          SCHEMA                   |
                                          SCHEMA <schema_name>     |
                                          <schema_name>
                                        }
                                  ]
                                  [ STARTS WITH '<name_string>' ]
                                  [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`TERSE`
:   Optionally returns only a subset of the output columns:

    - `created_on`
    - `name`
    - `kind`

      The `kind` column value is always ICEBERG TABLE.
    - `database_name`
    - `schema_name`

    Default: No value (all columns are included in the output)

`ICEBERG`
:   Returns Iceberg tables only.

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`[ IN ... ]`
:   Optionally specifies the scope of the command. Specify one of the following:

    `ACCOUNT`
    :   Returns records for the entire account.

    `DATABASE`, `DATABASE db_name`
    :   Returns records for the current database in use or for a specified database (`db_name`).

        If you specify `DATABASE` without `db_name` and no database is in use, the keyword has no effect on the output.

        Note

        Using SHOW commands without an `IN` clause in a database context can result in fewer than expected results.

        Objects with the same name are only displayed once if no `IN` clause is used. For example, if you have table `t1` in
        `schema1` and table `t1` in `schema2`, and they are both in scope of the database context you’ve specified (that is, the database
        you’ve selected is the parent of `schema1` and `schema2`), then SHOW TABLES only displays one of the `t1` tables.

    `SCHEMA`, `SCHEMA schema_name`
    :   Returns records for the current schema in use or a specified schema (`schema_name`).

        `SCHEMA` is optional if a database is in use or if you specify the fully qualified `schema_name` (for example, `db.schema`).

        If no database is in use, specifying `SCHEMA` has no effect on the output.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows [ FROM 'name_string' ]`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

    The optional `FROM 'name_string'` subclause effectively serves as a “cursor” for the results. This enables fetching the
    specified number of rows following the first row whose object name matches the specified string:

    - The string must be enclosed in single quotes and is case sensitive.
    - The string does not have to include the full object name; partial names are supported.

    Default: No value (no limit is applied to the output)

    Note

    For SHOW commands that support both the `FROM 'name_string'` and `STARTS WITH 'name_string'` clauses, you can combine
    both of these clauses in the same statement. However, both conditions must be met or they cancel out each other and no results are
    returned.

    In addition, objects are returned in lexicographic order by name, so `FROM 'name_string'` only returns rows with a higher
    lexicographic value than the rows returned by `STARTS WITH 'name_string'`.

    For example:

    - `... STARTS WITH 'A' LIMIT ... FROM 'B'` would return no results.
    - `... STARTS WITH 'B' LIMIT ... FROM 'A'` would return no results.
    - `... STARTS WITH 'A' LIMIT ... FROM 'AB'` would return results (if any rows match the input strings).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| SELECT | Iceberg table | To see a particular Iceberg table in the output for SHOW ICEBERG TABLES, a role must have the SELECT privilege on that table. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- If an account (or database or schema) has a large number of Iceberg tables, then searching the entire account (or database or schema)
  can consume a significant amount of compute resources.

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

## Output

Note

The following output schema is for the SHOW ICEBERG TABLES command. For information about the output of SHOW TABLES,
see [Identifying Iceberg Tables with SHOW TABLES](#identifying-iceberg-tables-with-show-tables) (in this topic).

The command output provides table properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the table was created. |
| `name` | Name of the table. |
| `database_name` | Database in which the table is stored. |
| `schema_name` | Schema in which the table is stored. |
| `owner` | Role that owns the table. |
| `external_volume_name` | Name of the external volume where the Iceberg table data and metadata are stored. |
| `catalog_name` | Name of the catalog integration object associated with the Iceberg table when the table is not managed by Snowflake. `SNOWFLAKE` when the table is managed by Snowflake. |
| `iceberg_table_type` | Type of Iceberg table. `UNMANAGED` if the table is not managed by Snowflake. `NOT ICEBERG` otherwise. |
| `catalog_table_name` | Name of the table as recognized by the catalog. |
| `catalog_namespace` | For externally managed tables, the namespace that was defined when the table was created. If not defined at the table level, the default namespace associated with the catalog integration used by the table. For Snowflake-managed tables that you sync with Snowflake Open Catalog, this field isn’t required, so the value is `null`. |
| `base_location` | Relative path from the `EXTERNAL_VOLUME` location to the table metadata and data files. |
| `can_write_metadata` | Signifies whether Snowflake can write metadata to the location specified by the `base_location`. |
| `comment` | Comment for the table. |
| `name_mapping` | List of objects with information about table columns that use [column projection](https://iceberg.apache.org/spec/#column-projection). For more information, see [name\_mapping](#label-tables-iceberg-show-tables-name-mapping). |
| `owner_role_type` | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| `catalog_sync_name` | Denotes the name of the catalog integration for Snowflake Open Catalog that the Snowflake-managed Apache Iceberg™ table syncs to. If the table doesn’t sync with Snowflake Open Catalog or isn’t managed by Snowflake, the value is `NULL`. |
| `auto_refresh_status` | The automated refresh status for an externally managed Iceberg table. This column displays the same results for the table as the [SYSTEM$AUTO\_REFRESH\_STATUS](/sql-reference/functions/system_auto_refresh_status) function. |
| `partition_specs` | List of objects describing the Apache Iceberg™ partition specifications for the table, as found in the Iceberg metadata file. Includes specification for both Snowflake-managed and externally managed Iceberg tables. For more information, see [partition\_specs](#label-tables-iceberg-show-tables-partition-specs). |
| `current_partition_spec_id` | ID for the partition spec that is currently active for the Iceberg table. This ID corresponds to a value for `spec-id` in `partition_specs`. |

Expand

Show lessSee more

### name\_mapping

The `name_mapping` output column provides information about table columns that use [column projection](https://iceberg.apache.org/spec/#column-projection).

If a table doesn’t contain any columns with an associated name mapping, the output column has a value of `[NULL]`. Otherwise, the value is
a list of objects, where each object corresponds to a column that has an associated name mapping (sometimes referred to as a mapped field).
Each object can contain the following three properties:

- `field-id`: The Iceberg field ID.
- `names`: A list of name strings for the field.
- `fields`: A list of field mappings for the child fields of struct, map, or list columns.

For example:

Copy code

```
[
  {
    "field-id": 1,
    "names": [
      "id",
      "record_id"
    ]
  },
  {
    "field-id": 2,
    "names": [
      "data"
    ]
  },
  {
    "field-id": 3,
    "names": [
      "location"
    ],
    "fields": [
      {
        "field-id": 4,
        "names": [
          "latitude",
          "lat"
        ]
      },
      {
        "field-id": 5,
        "names": [
          "longitude",
          "long"
        ]
      }
    ]
  }
]
```

Note

Field IDs can be non-consecutive if a column, or a field in a [structured type](/sql-reference/data-types-structured)
column doesn’t have an associated name mapping.

### partition\_specs

Each object in the `partition_specs` column includes a `spec-id`,
followed by the fields for the partition specification. Each field is an OBJECT value with the
following key-value pairs:

- `name`: The name of the partition.
- `transform`: The transformation applied to the source column to generate a partition value. This value determines how data is grouped
  into partitions.
- `source-id`: The identifier of the original table column or field that is used for partitioning.
- `field-id`: The partition field ID. This field identifies a partition field and is unique in a partition specification. However, for
  Iceberg v2 table metadata, the field ID is unique across all partition specifications.

For example:

Copy code

```
[ {
    "spec-id" : 0,
    "fields" : [ {
      "name" : "COL1",
      "transform" : "identity",
      "source-id" : 1,
      "field-id" : 1000
      }, {
      "name" : "COL1_trunc_100",
      "transform" : "truncate[100]",
      "source-id" : 1,
      "field-id" : 1001
      }
    ]
} ]
```

The example shows one partition specification; however, a table can have multiple partition specifications.

## Examples

Show all the Iceberg tables whose name starts with `glue` that you have privileges to view in the `tpch.public` schema:

> Copy code
>
> ```
> SHOW ICEBERG TABLES LIKE 'glue%' IN tpch.public;
> ```

## Identifying Iceberg tables with SHOW TABLES

The [SHOW TABLES](/sql-reference/sql/show-tables) command output has a column that indicates whether a table is an Iceberg table.
This column appears in addition to the regular SHOW TABLES [output columns](/sql-reference/sql/show-tables#label-show-tables-output).

The column has the following name and possible values:

| Column name | Values |
| --- | --- |
| is\_iceberg | `Y` if the table is an Iceberg table; `N` otherwise. |

Expand

Show lessSee more
