# ALTER EXTERNAL TABLE

Modifies the properties, columns, or constraints for an existing external table.

See also:
:   [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table) , [DROP EXTERNAL TABLE](/sql-reference/sql/drop-external-table) , [SHOW EXTERNAL TABLES](/sql-reference/sql/show-external-tables) , [DESCRIBE EXTERNAL TABLE](/sql-reference/sql/desc-external-table)

## Syntax

Copy code

```
ALTER EXTERNAL TABLE [ IF EXISTS ] <name> REFRESH [ '<relative-path>' ]

ALTER EXTERNAL TABLE [ IF EXISTS ] <name> ADD FILES ( '<path>/[<filename>]' [ , '<path>/[<filename>'] ] )

ALTER EXTERNAL TABLE [ IF EXISTS ] <name> REMOVE FILES ( '<path>/[<filename>]' [ , '<path>/[<filename>]' ] )

ALTER EXTERNAL TABLE [ IF EXISTS ] <name> SET
  [ AUTO_REFRESH = { TRUE | FALSE } ]
```

**Partitions added and removed manually**

> Copy code
>
> ```
> ALTER EXTERNAL TABLE <name> [ IF EXISTS ] ADD PARTITION ( <part_col_name> = '<string>' [ , <part_col_name> = '<string>' ] ) LOCATION '<path>'
>
> ALTER EXTERNAL TABLE <name> [ IF EXISTS ] DROP PARTITION LOCATION '<path>'
> ```

## Parameters

`name`
:   Identifier for the external table to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in double
    quotes. Identifiers enclosed in double quotes are also case sensitive.

`REFRESH [ 'relative-path' ]`
:   Accesses the staged data files referenced in the external table definition and updates the table metadata:

    - New files in the path are added to the table metadata.
    - Changes to files in the path are updated in the table metadata.
    - Files no longer in the path are removed from the table metadata.

    Optionally specify a relative path to refresh the metadata for a specific subset of the data files.

    Using this parameter only needs to be done once, when the external table is created. This step synchronizes the metadata with the latest set
    of associated files in the stage and path in the external table definition. Also, this step ensures the external table can read the data files
    in the specified stage and path, and that no files were missed in the external table definition.

    Note

    - This parameter isn’t supported by partitioned external tables when partitions are added manually by the object owner; that is,
      when `PARTITION_TYPE = USER_SPECIFIED`.
    - If `TABLE_FORMAT = DELTA` is set on the external table, `REFRESH` doesn’t support a relative path to refresh the
      metadata for a specific subset of the data files.

`ADD FILES`
:   Registers the specified comma-separated list of files with the external table metadata, and refreshes the table.
    For each file, list the path and filename relative to [ WITH ] LOCATION in the external table definition.
    For information, see [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table).

    This parameter is not supported by partitioned external tables when partitions are added manually by the object owner; that is,
    when `PARTITION_TYPE = USER_SPECIFIED`.

`REMOVE FILES`
:   Deregisters the specified comma-separated list of files from the external table metadata, and refreshes the table.
    For each file, list the path and filename relative to [ WITH ] LOCATION in the external table definition.
    For more information, see [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table).

    This parameter is not supported by partitioned external tables when partitions are added manually by the object owner; that is,
    when `PARTITION_TYPE = USER_SPECIFIED`.

`SET ...`
:   Specifies one or more properties/parameters to set for the external table that is separated by blank spaces, commas, or new lines:

    `AUTO_REFRESH = { TRUE | FALSE }`
    :   Specifies whether Snowflake should enable triggering automatic refreshes of the external table metadata when new or updated data files
        are available in the named external stage specified in the `[ WITH ] LOCATION =` setting.

        Note

        - ## You must configure an event notification for your storage location to notify Snowflake when new or updated data is availableto read into the external table metadata. For more information, see the instructions for your cloud storage service:

          Amazon S3:
          :   [Refresh external tables automatically for Amazon S3](/user-guide/tables-external-s3)

          - Google Cloud Storage:
            :   [Refresh external tables automatically for Google Cloud Storage](/user-guide/tables-external-gcs)
          - Microsoft Azure:
            :   [Refresh external tables automatically for Azure Blob Storage](/user-guide/tables-external-azure)
        - This parameter isn’t supported by partitioned external tables when partitions are added manually by the object owner;
          that is, when `PARTITION_TYPE = USER_SPECIFIED`.
        - Setting this parameter to TRUE isn’t supported for external tables that reference data files stored on an [S3-compatible external stage](/user-guide/data-load-s3-compatible-storage).

        `TRUE`
        :   Snowflake enables the triggering of automatic refreshes of the external table metadata.

        `FALSE`
        :   Snowflake doesn’t enable the triggering of automatic refreshes of the external table metadata. You must manually refresh the external table metadata
            periodically by using [ALTER EXTERNAL TABLE](/sql-reference/sql/alter-external-table) … REFRESH to synchronize the metadata with the current list of files in the stage path.

        Default: `TRUE`

### Partitions added and removed manually

Use the following parameters to add or remove partitions when the partition type for the external table is user-specified; that is,
`PARTITION_TYPE = USER_SPECIFIED`:

`ADD PARTITION ( <part_col_name> = '<string>' [ , <part_col_name> = '<string>' , ... ] ) LOCATION '<path>'`
:   Manually add a partition for one or more partition columns defined for the external table in a specified location; that is, path.

    Note

    The maximum length of user-specified partition column names is 32 characters.

    Adding a partition also adds any new or updated files in the location to the external table metadata.

`DROP PARTITION LOCATION '<path>'`
:   Manually drop all partitions in a specified location; that is, path.

    Dropping a partition also removes any files in the location from the external table metadata.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | External table | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| USAGE | Stage | Required to manually refresh the external table metadata. |
| USAGE | File format | Required to manually refresh the external table metadata. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Only the external table owner — the role with the OWNERSHIP privilege on the external table — or higher can run this command.
- The following commands can be used in explicit transactions (using [BEGIN](/sql-reference/sql/begin) … [COMMIT](/sql-reference/sql/commit)):

  - `ALTER EXTERNAL TABLE ... REFRESH`
  - `ALTER EXTERNAL TABLE ... ADD FILES`
  - `ALTER EXTERNAL TABLE ... REMOVE FILES`

  Explicit transactions could be used to ensure a consistent state when manually replacing updated files in external table metadata.
- Add or remove columns in an external table by using the following syntax:

  Add column:
  :   Copy code

      ```
      ALTER TABLE <name> ADD COLUMN ( <col_name> <col_type> AS <expr> ) [, ...]
      ```

  Rename column:
  :   Copy code

      ```
      ALTER TABLE <name> RENAME COLUMN <col_name> to <new_col_name>
      ```

  Drop column:
  :   Copy code

      ```
      ALTER TABLE <name> DROP COLUMN <col_name>
      ```

      Note

      The default VALUE and METADATA$FILENAME columns cannot be dropped.

  For examples, see the [ALTER TABLE](/sql-reference/sql/alter-table) topic.
- To add and drop a row access policy on an external table, or to set or unset a tag, use the [ALTER TABLE](/sql-reference/sql/alter-table) command.

  However, you can create an external table with a row access policy and a tag on the table. For more information, see [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table).
- You can use data metric functions with external tables by running an [ALTER TABLE](/sql-reference/sql/alter-table) command. For more information, see
  [Use SQL to set up data metric functions](/user-guide/data-quality-working).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

### Refresh metadata manually

Manually refresh the entire set of external table metadata that is based on changes in the referenced data files:

Copy code

```
ALTER EXTERNAL TABLE exttable_json REFRESH;
```

Similar to the first example, but manually refresh only a path of the metadata for an external table:

Copy code

```
CREATE OR REPLACE STAGE mystage
  URL='<cloud_platform>://twitter_feed/logs/'
  .. ;

-- Create the external table
-- 'daily' path includes paths in </YYYY/MM/DD/> format
CREATE OR REPLACE EXTERNAL TABLE daily_tweets
  WITH LOCATION = @twitter_feed/daily/;

-- Refresh the metadata for a single day of data files by date
ALTER EXTERNAL TABLE exttable_part REFRESH '2018/08/05/';
```

### Add or remove files manually

Add an explicit list of files to the external table metadata:

Copy code

```
ALTER EXTERNAL TABLE exttable1 ADD FILES ('path1/sales4.json.gz', 'path1/sales5.json.gz');
```

Remove an explicit list of files from the external table metadata:

Copy code

```
ALTER EXTERNAL TABLE exttable1 REMOVE FILES ('path1/sales4.json.gz', 'path1/sales5.json.gz');
```

Replace an updated log file for December 2019 in the external table metadata in an explicit transaction:

Copy code

```
BEGIN;

ALTER EXTERNAL TABLE extable1 REMOVE FILES ('2019/12/log1.json.gz');

ALTER EXTERNAL TABLE extable1 ADD FILES ('2019/12/log1.json.gz');

COMMIT;
```

### Add or remove partitions manually

Manually add partitions in a specified location for the partition columns:

Copy code

```
ALTER EXTERNAL TABLE et2 ADD PARTITION(col1='2022-01-24', col2='a', col3='12') LOCATION '2022/01';
```

Snowflake adds the partitions to the metadata for the external table. The operation also adds any new data files in the specified
location to the metadata.

Manually remove partitions from a specified location:

Copy code

```
ALTER EXTERNAL TABLE et2 DROP PARTITION LOCATION '2022/01';
```

Snowflake removes the partitions from the metadata for the external table. The operation also removes any data files in the specified
location from the metadata.
