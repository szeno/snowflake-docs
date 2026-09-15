Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# BLOCK\_STORAGE\_SNAPSHOTS view

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

This Account Usage view displays a row for each [block storage snapshot](/developer-guide/snowpark-container-services/block-storage-volume#label-snowpark-containers-block-storage-manage-snapshots) in the account.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| SNAPSHOT\_ID | NUMBER | ID of the snapshot. |
| SNAPSHOT\_NAME | VARCHAR | Name of the snapshot. |
| DATABASE\_ID | VARCHAR | Internal, Snowflake-generated identifier of the database that the snapshot belongs to. |
| DATABASE\_NAME | VARCHAR | Name of the database that the snapshot belongs to. |
| SCHEMA\_ID | NUMBER | Internal, Snowflake-generated identifier of the schema that the snapshot belongs to. |
| SCHEMA\_NAME | VARCHAR | Name of the schema that the snapshot belongs to. |
| SERVICE\_ID | NUMBER | ID of the service for which the snapshot is created. |
| SERVICE\_NAME | VARCHAR | Name of the service for which the snapshot is created. |
| VOLUME \_NAME | VARCHAR | Volume from the specified service for which the snapshot is created. |
| INSTANCE | NUMBER | ID of the service instance for which the snapshot is created. |
| SIZE | NUMBER | Size in GB of the snapshot. |
| ENCRYPTION | VARCHAR | [Encryption type of the volume](/developer-guide/snowpark-container-services/block-storage-volume#label-spcs-block-storage-volume-specifying) from which the snapshot was created. |
| COMMENT | VARCHAR | General comment about the snapshot. |
| OWNER | VARCHAR | Role that owns the snapshot. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the snapshot. |
| CREATED\_ON | TIMESTAMP\_LTZ | Creation time of the snapshot. |
| LAST\_ALTERED\_ON | TIMESTAMP\_LTZ | Last altered time of the snapshot. |
| DELETED\_ON | TIMESTAMP\_LTZ | Deletion time of the snapshot. |

Expand

Show lessSee more

## Usage notes

- Latency for the view might be up to 180 minutes (3 hours).

## Example

Copy code

```
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.BLOCK_STORAGE_SNAPSHOTS;
```
