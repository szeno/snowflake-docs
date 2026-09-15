Categories:
:   [Table functions](/sql-reference/functions-table)

# ICEBERG\_TABLE\_FILES

Returns information about the data files registered to an externally managed Apache Iceberg™ table at a specified
point in time.

See also:
:   [Apache Iceberg™ tables](/user-guide/tables-iceberg) , [Metadata and retention for Apache Iceberg™ tables](/user-guide/tables-iceberg-metadata) , [ALTER ICEBERG TABLE … REFRESH](/sql-reference/sql/alter-iceberg-table-refresh)

## Syntax

Copy code

```
ICEBERG_TABLE_FILES(
  TABLE_NAME => '<table_name>'
  [, AT => '<timestamp_ltz>']
)
```

## Arguments

**Required**

`TABLE_NAME => 'table_name'`
:   The name of the [externally managed Iceberg table](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration)
    for which you want to retrieve the data file information.

**Optional**

`AT => 'timestamp_ltz'`
:   Specifies an exact date and time to use for retrieving the file information. The value must be explicitly cast to a
    TIMESTAMP\_LTZ data type. For information, see [Date & time data types](/sql-reference/data-types-datetime).

    If not specified, the function returns information about the table files for the current
    [snapshot](/user-guide/tables-iceberg#label-tables-iceberg-snapshots).

## Output

The function returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| REGISTERED\_ON | TIMESTAMP\_LTZ | The timestamp of when the Parquet file was registered. |
| FILE\_NAME | TEXT | The full path to the registered file. |
| FILE\_SIZE | NUMBER | The size of the file (in bytes). |
| ROW\_COUNT | NUMBER | The number of rows in the file. |
| ROW\_COUNT\_GROUP | NUMBER | The number of row groups in the file. |
| MD5 | N/A | This field returns a placeholder value and should not be used. This field might be deprecated in a future release. |
| ETAG | N/A | This field returns a placeholder value and should not be used. This field might be deprecated in a future release. |
| LAST\_MODIFIED\_ON | N/A | This field returns a placeholder value and should not be used. This field might be deprecated in a future release. |

Expand

Show lessSee more

Note

The ETAG, MD5, and LAST\_MODIFIED\_ON fields return a placeholder value and should not be used. These fields might be deprecated in a future release.

## Examples

Retrieve information about the Parquet data files for the *current snapshot*
registered to an externally managed Iceberg table named `my_iceberg_table`:

Copy code

```
SELECT *
  FROM TABLE(
    INFORMATION_SCHEMA.ICEBERG_TABLE_FILES(
      TABLE_NAME => 'my_iceberg_table'
    )
  );
```

Output:

```
+-------------------------------------------------------+--------------------------------+------------+--------------------------------+------------+------------------+-----------------------------------+-----------------------------------+
| FILE_NAME                                             | REGISTERED_ON                  | FILE_SIZE  | LAST_MODIFIED_ON               | ROW_COUNT  | ROW_GROUP_COUNT  | ETAG                              | MD5                               |
| data/87/snow_D9zlAoeipII_AODxT1uXDxg_0_1_003.parquet  | 1969-12-31 16:00:00.000 -0800  | 27136      | 1969-12-31 16:00:00.000 -0800  | 30000      | 1                | NULL                              | NULL                              |
| data/08/snow_D9zlAoeipII_AODxT1uXDxg_0_1_006.parquet  | 1969-12-31 16:00:00.000 -0800  | 45568      | 1969-12-31 16:00:00.000 -0800  | 45000      | 1                | NULL                              | NULL                              |
| data/94/snow_D9zlAoeipII_AODxT1uXDxg_0_1_008.parquet  | 1969-12-31 16:00:00.000 -0800  | 45056      | 1969-12-31 16:00:00.000 -0800  | 45000      | 1                | NULL                              | NULL                              |
| data/24/snow_D9zlAoeipII_AODxT1uXDxg_0_1_004.parquet  | 1969-12-31 16:00:00.000 -0800  | 27136      | 1969-12-31 16:00:00.000 -0800  | 30000      | 1                | NULL                              | NULL                              |
+-------------------------------------------------------+--------------------------------+------------+--------------------------------+------------+------------------+-----------------------------------+-----------------------------------+
```

Retrieve information about the Parquet data files for a table named `my_iceberg_table`
at a specified time and day:

Copy code

```
SELECT file_name, file_size, row_count, row_group_count, etag, md5
  FROM TABLE(
    INFORMATION_SCHEMA.ICEBERG_TABLE_FILES(
      TABLE_NAME => 'my_iceberg_table',
      AT => CAST('2024-12-09 11:02:00' AS TIMESTAMP_LTZ)
    )
  );
```

Output:

```
+------------------------------------------------------+-----------+-----------+-----------------+----------------------------------+----------------------------------+
| FILE_NAME                                            | FILE_SIZE | ROW_COUNT | ROW_GROUP_COUNT | ETAG                             | MD5                              |
|------------------------------------------------------+-----------+-----------+-----------------+----------------------------------+----------------------------------|
| data/87/snow_D9zlAoeipII_AODxT1uXDxg_0_1_003.parquet | 27136     | 30000     | 1               | NULL                             | NULL                             |
| data/08/snow_D9zlAoeipII_AODxT1uXDxg_0_1_006.parquet | 45568     | 45000     | 1               | NULL                             | NULL                             |
| data/94/snow_D9zlAoeipII_AODxT1uXDxg_0_1_008.parquet | 45056     | 45000     | 1               | NULL                             | NULL                             |
| data/24/snow_D9zlAoeipII_AODxT1uXDxg_0_1_004.parquet | 27136     | 30000     | 1               | NULL                             | NULL                             |
+------------------------------------------------------+-----------+-----------+-----------------+----------------------------------+----------------------------------+
4 Row(s) produced. Time Elapsed: 1.502s
```
