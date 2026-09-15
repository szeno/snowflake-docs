Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# LISTING\_REFRESH\_HISTORY

Returns the past 14 days of refresh history for a cross-cloud auto-fulfillment listing.
The information returned contains replication details for refresh events where the listing is
synchronized to a specified target region.

This function is available to providers of listings who have any privilege on the specified listing.

## Syntax

Copy code

```
LISTING_REFRESH_HISTORY(
  LISTING_NAME => '<listing_name>'
  [ , SNOWFLAKE_REGION => '<snowflake_region>' ]
  [ , REGION_GROUP => '<region_group>' ] )
```

## Arguments

**Required**

`LISTING_NAME => 'listing_name'`
:   SQL identifier of a cross-cloud auto-fulfillment listing in this account. The SQL identifier for
    listings can be found in the name column returned by show listings in data exchange <exchange\_name>.
    Similarly, the SQL identifier for data exchanges can be found in the name column returned by
    `show data exchanges`.

**Optional**

`SNOWFLAKE_REGION => 'snowflake_region'`
:   The Snowflake region group to which the listing is replicated, where you can view the refresh history for that replication. This follows
    the same formatting as the column `snowflake_region` returned by [SHOW REGIONS](/sql-reference/sql/show-regions). If no region is specified, the
    history for all target regions is displayed.

`REGION_GROUP => 'region_group'`
:   The Snowflake region group to which the listing is replicated, for which you can view the refresh history.

    `PUBLIC` by default. This argument only needs to be specified if the target region being monitored
    is in a US government or Virtual Private Snowflake region.

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| LISTING\_NAME | TEXT | Name of the cross-cloud auto-fulfillment listing in this account. |
| SNOWFLAKE\_REGION | TEXT | Name of the Snowflake region the listing is replicated to. For example, `aws_us_east_1`. |
| REGION\_GROUP | TEXT | Name of the Snowflake region group the listing is replicated to. For example, PUBLIC. |
| PHASE | TEXT | Current phase in the replication operation, represented as one phase out of a total of X phases. For example, 2/6. |
| PHASE\_NAME | TEXT | Name of the replication phases completed (or in progress) so far.  For the list of phases, see [usage notes](/sql-reference/functions/listing_refresh_history#label-listing-refresh-history-function-usage-notes). |
| PROGRESS | TEXT | The current replication progress as a percentage. |
| START\_TIME | TIMESTAMP\_LTZ | Time when the replication phase began. |
| END\_TIME | TIMESTAMP\_LTZ | Time when the phase finished, if applicable.  NULL if the phase is in progress or is the terminating phase (`COMPLETED/FAILED/CANCELED`). |
| JOB\_UUID | TEXT | Query ID for the refresh job. |
| TOTAL\_BYTES | VARIANT | A JSON object that provides detailed information about refreshed databases:   - `totalBytesToReplicate`: Total number of bytes expected to be replicated. - `bytesUploaded`: Actual number of bytes uploaded. - `bytesDownloaded`: Actual number of bytes downloaded. - `bytesSkipped`: Number of bytes skipped during a refresh when Egress Cost Optimizer is enabled. - `databases`: List of JSON objects containing the following fields for each member database:   - `name`: Name of the database.   - `totalBytesToReplicate`: Total bytes expected to be replicated for the database. |
| OBJECT\_COUNT | VARIANT | A JSON object that provides detailed information about refreshed objects:   - `totalObjects`: Total number of objects in the replication or failover group. - `completedObjects`: Total number of objects completed. - `objectTypes`: List of JSON objects containing the following fields for each type:   - `objectType`: Type of object (for example users, roles, grants, warehouses, schemas, tables, columns, etc).   - `totalObjects`: Total number of objects of this type in the replication or failover group.   - `completedObjects`: Total number of objects of this type that were completed. |
| PRIMARY\_SNAPSHOT\_TIMESTAMP | TIMESTAMP\_LTZ | Timestamp when the primary snapshot was created. |
| ERROR | VARIANT | NULL if the refresh operation is successful. If the refresh operation fails, returns a JSON object that provides detailed information about the error:   - `errorCode`: Error code of the failure. - `errorMessage`: Error message of the failure. |

Expand

Show lessSee more

## Usage notes

- Only returns rows for a role with any privilege on the listing.
- Only returns rows for a listing in the current account.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be
  fully-qualified.

  For more information, see [Information Schema](/sql-reference/info-schema#label-info-schema-functions).

- Phase list in the order processed:
  1. SECONDARY\_SYNCHRONIZING\_MEMBERSHIP
  2. SECONDARY\_UPLOADING\_INVENTORY
  3. PRIMARY\_UPLOADING\_METADATA
  4. PRIMARY\_UPLOADING\_DATA
  5. SECONDARY\_DOWNLOADING\_METADATA
  6. SECONDARY\_DOWNLOADING\_DATA
  7. COMPLETED / FAILED / CANCELED

- The output will also include the history of other listings that reference the same database, as they are refreshed together. If the input
  is an application listing, it contains the history of all application listings in the given region.
- In the PRIMARY\_UPLOADING\_DATA and SECONDARY\_DOWNLOADING\_DATA phases, the `totalBytesToReplicate` value is estimated prior to the
  replication operation. This value may differ from the `totalBytesToUpload` or `totalBytesToDownload` value in the respective
  phase.

  For example, if during the PRIMARY\_UPLOADING\_DATA phase, a previous replication operation uploaded some bytes but was canceled before the
  operation completed, those bytes would not be uploaded again. In that case, `totalBytesToUpload` would be lower
  than `totalBytesToReplicate`.

## Examples

Retrieve the history for the listing `my_listing` refreshing to AWS US East-1, a public cloud region.

> Copy code
>
> ```
> select * from table(information_schema.listing_refresh_history(listing_name=>'my_listing',snowflake_region=>'AWS_US_EAST_1'))
> ```
