Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# BLOCK\_STORAGE\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view can be used to query the average daily block storage and snapshot usage for Snowpark Container Services across
all the accounts in your organization.

See also:
:   [BLOCK\_STORAGE\_HISTORY view](/sql-reference/account-usage/block_storage_history) (Account Usage)

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| USAGE\_DATE | TIMESTAMP\_LTZ | Date of this storage usage record. The date is based on the local time zone. |
| STORAGE\_TYPE | VARCHAR | `BLOCK_STORAGE` or `SNAPSHOT`. |
| COMPUTE\_POOL\_NAME | VARCHAR | Name of the compute pool associated with this storage usage. For the `SNAPSHOT` storage type, this field is NULL. |
| COMPUTE\_POOL\_ID | NUMBER | Internal, Snowflake-generated identifier of the compute pool associated with this storage usage. For the `SNAPSHOT` storage type, this field is NULL. |
| BYTES | NUMBER | Average number of bytes used on the given date. |
| ADDITIONAL\_IOPS | NUMBER | Average number of additional IOPS used on the given date. |
| ADDITIONAL\_THROUGHPUT | NUMBER | Average amount of additional throughput (MiB per second) used on the given date. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- The view provides daily block storage and snapshot usage within the last 365 days (1 year).
- Snapshots are not associated with compute pools; therefore, for snapshots the view has the NULL value in the COMPUTE\_POOL\_NAME and
  COMPUTE\_POOL\_ID columns.
- The BYTES column shows average usage of block storage volumes for a specific day, for a specific storage type, and for a specific compute
  pool (where appropriate). For example, using a 10 GiB block volume for 6 hours on a given date is equivalent to 2.5 GiB for that date
  (10 GiB \* 6/24 hours = 2.5 GiB per day = 2,684,354,560 bytes per day).
- The additional IOPS (ADDITIONAL\_IOPS) and throughput (ADDITIONAL\_THROUGHPUT) values show the amount that
  [configured values](/developer-guide/snowpark-container-services/block-storage-volume#label-spcs-block-storage-volume-specifying) exceed their default values. For example, on AWS, the block configuration
  default IOPS is 3,000, and the default throughput is 125 MiB/second. If an AWS block device is configured with 4,000 IOPS and
  225 MiB/second throughput, the additional IOPS would be 1,000 (4,000 - 3,000), and the additional throughput would be 100 MiB/second
  (225 - 125).

Note

- If multiple block volumes are attached to a compute pool, the view aggregates the usage and returns one row.
- If there are multiple snapshots present on a given day, the view aggregates the usage and returns one row.
- If a single block volume is attached to a compute pool and used for three days, then the view returns three rows because the view reports
  daily usage for each compute pool having block volumes attached.
