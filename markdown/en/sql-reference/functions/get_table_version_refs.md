Categories:
:   [Table functions](/sql-reference/functions-table)

# GET\_TABLE\_VERSION\_REFS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns one row for each tag or branch in the Iceberg table metadata that Snowflake has indexed, when the snapshot that the
reference points to is present in that metadata. Each row includes the target snapshot and the reference’s retention settings.

To query the snapshot that a reference points to, pass the reference name to the AT clause. For more information, see
[Time Travel for Apache Iceberg™ tables](/user-guide/tables-iceberg-time-travel).

## Syntax

Copy code

```
GET_TABLE_VERSION_REFS(
  '<table_name>'
)
```

## Arguments

`'table_name'`
:   The name of the Iceberg table whose references you want to retrieve. The table name is a string, so it must be enclosed in single
    quotes. If the table name is fully qualified, such as `'<db>.<schema>.<table_name>'`, enclose the entire name in single quotes.

## Output

The function returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| REFERENCE\_NAME | TEXT | The name of the tag or branch. |
| REFERENCE\_TYPE | TEXT | `TAG` or `BRANCH`. |
| VERSION\_ID | NUMBER | The Iceberg snapshot ID that the reference points to. |
| VERSION\_CREATED\_AT | TEXT | The time when that snapshot was committed. |
| MAX\_REFERENCE\_AGE\_IN\_MS | NUMBER | How long the reference is retained, in milliseconds. For a tag, this value comes from the `RETAIN` clause. NULL if the reference has no retention period. |
| MIN\_SNAPSHOTS\_TO\_KEEP | NUMBER | The minimum number of snapshots retained on a branch. Always NULL for tags. |
| MAX\_SNAPSHOT\_AGE\_IN\_MS | NUMBER | How long snapshots are retained on a branch, in milliseconds. Always NULL for tags. |

Expand

Show lessSee more

## Usage notes

- The argument must be a literal string. You can’t pass a column or an expression.
- The function reads the Iceberg table metadata that Snowflake has indexed, so its output can lag the catalog. A reference whose
  snapshot is missing from the loaded metadata is omitted. For an externally managed table, refresh the table to see references
  that another engine created. For a Snowflake-managed table, a tag that you just created appears after Snowflake next updates
  the table metadata.
- To confirm that a tag you just created is queryable, run `SELECT ... AT(VERSION_TAG => '<tag_name>')`. Don’t rely on this
  function as the immediate post-condition.
- For a Delta-based table, the function returns no rows.

## Examples

List the tags and branches on an Iceberg table named `my_iceberg_table`:

Copy code

```
SELECT * FROM TABLE(INFORMATION_SCHEMA.GET_TABLE_VERSION_REFS('my_db.my_schema.my_iceberg_table'));
```

Output:

```
+----------------+----------------+---------------------+---------------------------------+-------------------------+-----------------------+------------------------+
| REFERENCE_NAME | REFERENCE_TYPE | VERSION_ID          | VERSION_CREATED_AT              | MAX_REFERENCE_AGE_IN_MS | MIN_SNAPSHOTS_TO_KEEP | MAX_SNAPSHOT_AGE_IN_MS |
|----------------+----------------+---------------------+---------------------------------+-------------------------+-----------------------+------------------------|
| main           | BRANCH         | 7742318844925117331 | Mon, 09 Dec 2024 14:22:07 -0800 |                    NULL |                  NULL |                   NULL |
| month_end      | TAG            | 6201065399847600377 | Mon, 09 Dec 2024 11:00:50 -0800 |               604800000 |                  NULL |                   NULL |
+----------------+----------------+---------------------+---------------------------------+-------------------------+-----------------------+------------------------+
```

List only the tags, with their retention periods expressed in days:

Copy code

```
SELECT reference_name, version_id, max_reference_age_in_ms / 86400000 AS retain_days
  FROM TABLE(INFORMATION_SCHEMA.GET_TABLE_VERSION_REFS('my_db.my_schema.my_iceberg_table'))
  WHERE reference_type = 'TAG';
```
