Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# AVAILABLE\_LISTING\_REFRESH\_HISTORY

Returns the past 14 days of refresh history for an available listing or a database mounted from a listing using cross-cloud
auto-fulfillment. The information returned contains replication details for data added to the listing database in each refresh event. This
function is available to consumers of listings who have any privilege on the available listing or mounted database.

## Syntax

Copy code

```
AVAILABLE_LISTING_REFRESH_HISTORY(
  OBJECT_TYPE => '<object_type>',
  OBJECT_NAME => '<object_name>' )
```

## Arguments

`OBJECT_TYPE => 'object_type'`
:   Type of the object, either `listing` or `database`.

`OBJECT_NAME => 'object_name'`
:   Name of the object, which can be either the listing’s global name or the mounted database name, depending on the object type.

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| OBJECT\_TYPE | TEXT | Lists the type of Snowflake object. For example, listing. |
| OBJECT\_NAME | TEXT | Name of the listing or the mounted database. |
| PHASE | TEXT | Current phase in the replication operation, represented as one phase out of a total of X phases. For example, 2/6. |
| PHASE\_NAME | TEXT | Name of the replication phases completed (or in progress) so far.  For the list of phases, see [usage notes](/sql-reference/functions/available_listing_refresh_history#label-listing-database-refresh-history-function-usage-notes). |
| PROGRESS | TEXT | PRIMARY\_UPLOADING\_DATA: Percentage of total bytes replicated.  SECONDARY\_DOWNLOADING\_METADATA: Percentage of the total number of objects replicated.  SECONDARY\_DOWNLOADING\_DATA: Percentage of total bytes replicated.  Empty for remaining phases. |
| START\_TIME | TIMESTAMP\_LTZ | Time when the replication phase began. |
| END\_TIME | TIMESTAMP\_LTZ | Time when the phase finished, if applicable.  NULL if the phase is in progress or is the terminating phase (`COMPLETED/FAILED/CANCELED`). |
| JOB\_UUID | TEXT | Query ID for the refresh job. |
| PRIMARY\_SNAPSHOT\_TIMESTAMP | TIMESTAMP\_LTZ | Timestamp when the primary snapshot was created. |
| ERROR | VARIANT | NULL if the refresh operation is successful. If the refresh operation fails, returns a JSON object that provides detailed information about the error:   - `errorCode`: Error code of the failure. - `errorMessage`: Error message of the failure. |

Expand

Show lessSee more

## Usage notes

- Only returns rows for a role with any privilege on the listing, if the listing is visible to the account.
- When `object_type` is set to `database` (as opposed to `listing`), only rows for roles with any privilege on that database are returned.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more information, see [Information Schema](/sql-reference/info-schema#label-info-schema-functions).

- Phase list in the order processed:
  1. SECONDARY\_SYNCHRONIZING\_MEMBERSHIP
  2. SECONDARY\_UPLOADING\_INVENTORY
  3. PRIMARY\_UPLOADING\_METADATA
  4. PRIMARY\_UPLOADING\_DATA
  5. SECONDARY\_DOWNLOADING\_METADATA
  6. SECONDARY\_DOWNLOADING\_DATA
  7. COMPLETED / FAILED / CANCELED

## Examples

Retrieve the history for the database `my_mounted_database`.

Copy code

```
SELECT * FROM TABLE(
  INFORMATION_SCHEMA.AVAILABLE_LISTING_REFRESH_HISTORY(
    OBJECT_TYPE=>'database',
    OBJECT_NAME=>'my_mounted_database'
  )
);
```
