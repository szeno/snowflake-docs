Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$SHOW\_DYNAMIC\_TABLES\_CREATED\_FOR\_RESHARING

When a consumer of a listing reshares the listing’s data into another region, Snowflake creates hidden dynamic tables to enable listing auto-fulfillment in the target region. This system function returns information about the hidden dynamic tables that Snowflake creates under the *outgoing* view to materialize imported data for cross-region resharing.

Use this function to:

- Identify which imported objects have backing dynamic tables for a given outgoing view.
- Inspect the most recent refresh times for those dynamic tables (for debugging or cost/health analysis).

See also:
:   [Resharing listings](/collaboration/reshare-listings)

## Syntax

Copy code

```
SYSTEM$SHOW_DYNAMIC_TABLES_CREATED_FOR_RESHARING( '<view_name>' )
```

## Arguments

`'view_name'`
:   The name of the outgoing view attached to a listing or share whose imported data is being auto-materialized into hidden dynamic tables for
    resharing.

    You can pass a fully qualified view name, for example:

    Copy code

    ```
    SYSTEM$SHOW_DYNAMIC_TABLES_CREATED_FOR_RESHARING(
      'RESHARER_DB.PUBLIC.SHARED_VIEW'
    );
    ```

## Returns

Returns a JSON string containing an array of objects. Each object represents a hidden dynamic table created under the specified view for
resharing:

| Field | Type | Description |
| --- | --- | --- |
| dtName | STRING | The fully qualified name of the hidden dynamic table nested under the outgoing view (for example, `_<id>_IMPORTED_DB.SCHEMA.TABLE_DT_FOR_RESHARING`). |
| dtSourceObject | STRING | The fully qualified name of the imported object (for example, `IMPORTED_DB.SCHEMA.TABLE`) that is being materialized into this dynamic table for resharing. This corresponds to the original imported entity referenced in the view definition. |
| dtRefreshStartTimeMillis | NUMBER | The epoch timestamp in milliseconds when the most recent refresh of this dynamic table started. Null if no refresh has occurred. Convert with `TO_TIMESTAMP_LTZ(value:dtRefreshStartTimeMillis::number, 3)`. |
| dtRefreshEndTimeMillis | NUMBER | The epoch timestamp in milliseconds when the most recent refresh of this dynamic table completed. Null if no refresh has occurred. Convert with `TO_TIMESTAMP_LTZ(value:dtRefreshEndTimeMillis::number, 3)`. |
| status | STRING | The status of the most recent refresh. Null if no refresh has occurred. Possible values: `SCHEDULED`, `EXECUTING`, `SUCCEEDED`, `FAILED`, `CANCELLED`, `UPSTREAM_FAILED`. For descriptions of each status, see the [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) output. |

Expand

Show lessSee more

## Usage notes

- In the following scenarios, dynamic tables aren’t created and the function returns no rows:

  - The view doesn’t reference any imported databases.
  - The view uses imported data that is not eligible for resharing.
  - The view hasn’t yet been processed by the listing auto-fulfillment.
- This function is intended for observability and debugging.

## Examples

The following example retrieves the dynamic tables created for a reshared view:

Copy code

```
SELECT * FROM TABLE(FLATTEN(input =>
  PARSE_JSON(
    SYSTEM$SHOW_DYNAMIC_TABLES_CREATED_FOR_RESHARING(
      'RESHARER_DB.PUBLIC.SHARED_VIEW'
    )
  )
));
```

To get a readable table with proper timestamps:

Copy code

```
SELECT
  value:dtName::STRING AS dt_name,
  value:dtSourceObject::STRING AS dt_source_object,
  TO_TIMESTAMP_LTZ(value:dtRefreshStartTimeMillis::NUMBER, 3) AS dt_refresh_start_time,
  TO_TIMESTAMP_LTZ(value:dtRefreshEndTimeMillis::NUMBER, 3) AS dt_refresh_end_time,
  value:status::STRING AS status
FROM TABLE(FLATTEN(input =>
  PARSE_JSON(
    SYSTEM$SHOW_DYNAMIC_TABLES_CREATED_FOR_RESHARING(
      'RESHARER_DB.PUBLIC.SHARED_VIEW'
    )
  )
));
```

Sample output:

```
+----------------------------------------------------------+----------------------------+-------------------------------+-------------------------------+-------------------+
| DT_NAME                                                  | DT_SOURCE_OBJECT           | DT_REFRESH_START_TIME         | DT_REFRESH_END_TIME           | STATUS            |
+----------------------------------------------------------+----------------------------+-------------------------------+-------------------------------+-------------------+
| _12345_IMPORTED_DB.PUBLIC.TABLE_A_DT_FOR_RESHARING       | IMPORTED_DB.PUBLIC.TABLE_A | 2026-03-19 10:00:00.000 -0700 | 2026-03-19 10:00:05.000 -0700 | SUCCEEDED |
| _12345_IMPORTED_DB.PUBLIC.VIEW_B_DT_FOR_RESHARING        | IMPORTED_DB.PUBLIC.VIEW_B  | 2026-03-19 10:00:01.000 -0700 | 2026-03-19 10:00:04.000 -0700 | SUCCEEDED |
+----------------------------------------------------------+----------------------------+-------------------------------+-------------------------------+-------------------+
```
