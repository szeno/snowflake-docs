# DESCRIBE ICEBERG TABLE

Describes either the columns in an [Apache Iceberg™ table](/user-guide/tables-iceberg) or the current values,
as well as the default values, for the properties of an Iceberg table.

DESCRIBE can be abbreviated to DESC.

Note that this topic refers to Iceberg tables as simply “tables” except where specifying *Iceberg tables* avoids confusion.

See also:
:   [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table), [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table), [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table), [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables)

## Syntax

Copy code

```
DESC[RIBE] [ ICEBERG ] TABLE <name> [ TYPE =  { COLUMNS | STAGE } ]
```

## Parameters

`name`
:   Specifies the identifier for the table to describe. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`TYPE = COLUMNS | STAGE`
:   Specifies whether to display the columns for the table or the stage properties (including their current and default values) for the
    table.

    Default: `TYPE = COLUMNS`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| SELECT | Iceberg table |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- This command does not show the object parameters for a table. Instead, use
  [SHOW PARAMETERS IN TABLE](/sql-reference/sql/show-parameters).
- DESC ICEBERG TABLE, [DESCRIBE TABLE](/sql-reference/sql/desc-table), and [DESCRIBE VIEW](/sql-reference/sql/desc-view) are interchangeable. Any of these
  commands retrieves the details for the table or view that matches the criteria in the statement; however, `TYPE = STAGE` does
  not apply for views because views don’t have stage properties.
- The output includes a `POLICY NAME` column to indicate the [masking policy](/user-guide/security-column-intro) set on the column.

  If a masking policy isn’t set on the column or if the Snowflake account isn’t Enterprise Edition or higher, Snowflake returns
  `NULL`.
- The command returns the `NAME_MAPPING` column only if you configure Iceberg Compatibility V2
  ([icebergCompatV2](https://github.com/delta-io/delta/blob/master/PROTOCOL.md#iceberg-compatibility-v2)) for the Delta table
  that your Iceberg table is based on.

  Note

  To view the `NAME_MAPPING` column, you must also enable the 2025\_01 behavior change bundle
  in your account.

  To [enable this bundle in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-enable-bundle),
  execute the following statement:

  Copy code

  ```
  SELECT SYSTEM$ENABLE_BEHAVIOR_CHANGE_BUNDLE('2025_01');
  ```

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

## Example

Create an example Iceberg table:

> Copy code
>
> ```
> CREATE OR REPLACE ICEBERG TABLE my_iceberg_table
>   CATALOG='my_catalog_integration'
>   EXTERNAL_VOLUME='my_ext_volume'
>   METADATA_FILE_PATH='path/to/metadata/v2.metadata.json';
> ```

Describe the columns in the table:

> Copy code
>
> ```
> DESC ICEBERG TABLE my_iceberg_table ;
> ```
