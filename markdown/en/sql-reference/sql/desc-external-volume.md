# DESCRIBE EXTERNAL VOLUME

Describes the properties of an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def).

DESCRIBE can be abbreviated to DESC.

See also:
:   [ALTER EXTERNAL VOLUME](/sql-reference/sql/alter-external-volume) , [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume) , [DROP EXTERNAL VOLUME](/sql-reference/sql/drop-external-volume) , [SHOW EXTERNAL VOLUMES](/sql-reference/sql/show-external-volumes)

## Syntax

Copy code

```
DESC[RIBE] EXTERNAL VOLUME <name>
```

## Parameters

`name`
:   Specifies the identifier for the external volume to describe. If the identifier contains spaces or special characters, the entire string
    must be enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `parent_property` | The parent property. This column includes the `STORAGE_LOCATIONS` property, which holds a set of named cloud storage locations. |
| `property` | The name of the property. This column can include the properties listed in the following table. |
| `property_type` | The property type. |
| `property_value` | The value assigned to the property. |
| `property_default` | The default property value. |

Expand

Show lessSee more

The `property` column can include the following properties of an external volume object:

| Property | Description |
| --- | --- |
| `comment` | The comment set for the external volume, if any. |
| `allow_writes` | Specifies whether write operations are allowed for the external volume. |
| `storage_location_n` | Details for a cloud storage location associated with the external volume, where `n` is a unique number that distinguishes the location from others in the `STORAGE_LOCATIONS` list; for example, `storage_location_1`.  For more information about storage location properties, see [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume#label-create-external-volume-cloudproviderparams). |
| `active` | The name of the [active storage location](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-ext-vol-active-storage-location) for the external volume. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | External volume |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

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

## Examples

Describe an external volume:

Copy code

```
DESC EXTERNAL VOLUME my_external_volume;
```

The following shows the output of DESCRIBE EXTERNAL VOLUME for an external volume with one storage location.
The property value for `STORAGE_LOCATION_1` is abbreviated for display purposes.

```
+-------------------+--------------------+---------------+-------------------------------------------------------------------------------------------+------------------+
| parent_property   | property           | property_type | property_value                                                                            | property_default |
|-------------------+--------------------+---------------+-------------------------------------------------------------------------------------------+------------------|
|                   | ALLOW_WRITES       | Boolean       | true                                                                                      | true             |
| STORAGE_LOCATIONS | STORAGE_LOCATION_1 | String        | {"NAME":"my_storage_us_west","STORAGE_PROVIDER":"S3","STORAGE_BASE_URL":"s3://...", ...}  |                  |
| STORAGE_LOCATIONS | ACTIVE             | String        | my_storage_us_west                                                                        |                  |
+-------------------+--------------------+---------------+-------------------------------------------------------------------------------------------+------------------+
```
