Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_TABLE\_ARCHIVE\_METADATA

Returns metadata about the archived data for a table,
without requiring data retrieval from the archive tier.

See also:
:   [Storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies),
    [Retrieve archived data](/user-guide/storage-management/storage-lifecycle-policies-retrieving-archived-data)

## Syntax

Copy code

```
SYSTEM$GET_TABLE_ARCHIVE_METADATA( '<table_name>' )
```

## Arguments

`'table_name'`
:   The name of the table with archived data. The table must have had data archived to the COOL or COLD tier,
    usually by a storage lifecycle policy.

## Returns

Returns a TEXT value containing JSON with metadata about the archived data. The JSON structure includes:

- `rowCount`: The number of rows in the archive.
- `columns`: An object containing metadata for each column:
  - `column_id`: The column ID (as shown in the COLUMNS view).
  - `data_type`: Column data type
  - `min`: The minimum value for the column, or `null` if not applicable.
  - `max`: The maximum value for the column, or `null` if not applicable.

Note

The `min` and `max` values are `null` for TEXT, OBJECT, ARRAY, and VARIANT data types.

The output also includes the archived timestamp column (`METADATA$STORAGE_LIFECYCLE_POLICY_ARCHIVED_TIMESTAMP`),
which indicates when each row was archived.

**Example output:**

Copy code

```
{
  "rowCount": 2304,
  "columns": {
    "CUSTOMER_ID": {
      "column_id": 10283,
      "data_type": "fixed",
      "min": -23,
      "max": 54032
    },
    "CUSTOMER_NAME": {
      "column_id": 10284,
      "data_type": "text",
      "min": null,
      "max": null
    },
    "METADATA$STORAGE_LIFECYCLE_POLICY_ARCHIVED_TIMESTAMP": {
      "data_type": "timestampltz",
      "min": "2025-01-02T03:04:05.6789Z",
      "max": "2025-11-12T13:14:15.1617Z"
    }
  }
}
```

## Usage notes

- The table owner or an account administrator (a user with the ACCOUNTADMIN role) who has access
  to the table can execute this function.
- Use this function to inspect archived data metadata without incurring the cost of retrieving data
  from the archive tier.
- The `column_id` field helps distinguish columns when a column has been dropped and a new column
  with the same name has been added later.
- To retrieve the actual archived data, use the
  [CREATE TABLE … FROM ARCHIVE OF](/sql-reference/sql/create-table#label-create-table-from-archive-of-syntax) command.

## Examples

Retrieve metadata about archived data for a table:

Copy code

```
SELECT SYSTEM$GET_TABLE_ARCHIVE_METADATA('my_database.my_schema.my_table');
```

Parse the JSON output to extract specific information:

Copy code

```
SELECT PARSE_JSON(SYSTEM$GET_TABLE_ARCHIVE_METADATA('my_database.my_schema.my_table')):rowCount AS archived_row_count;
```
