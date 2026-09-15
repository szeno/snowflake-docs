Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# BLOCK\_STORAGE\_HISTORY view

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Use the BLOCK\_STORAGE\_HISTORY view in the ACCOUNT\_USAGE schema to query the average daily block storage and snapshot usage for an account within the last 365 days.

## Columns

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

- Latency for the view can be up to 180 minutes (3 hours).
- The view provides daily block storage and snapshot usage within the last 365 days (1 year) for an account.
- Snapshots are not associated with compute pools; therefore, for snapshots the view has the NULL value in the COMPUTE\_POOL\_NAME and COMPUTE\_POOL\_ID columns.
- The BYTES column shows average usage of block storage volumes for a specific day, for a specific storage type, and for a specific compute pool (where appropriate) in the Snowflake account. For example, consider the following:

  - You use a 10 GiB block volume for 6 hours on 2025-02-01 for compute pool POOL\_1. Using 10 GiB for 6 hours is equivalent to 2.5 GiB per day
    (10 GiB \* 6/24 hours = 2.5 GiB per day = 2,684,354,560 bytes per day).
  - You use a 10 GiB block volume for 12 hours on 2025-02-01 for another compute pool POOL\_2. Using 10 GiB for 12 hours is equivalent to 5 GiB
    per day (10 GiB \* 12/24 hours = 5 GiB per day = 5,368,709,120 bytes per day).
  - You use a 20 GiB snapshot for 24 hours on 2025-02-01. Using 20 GiB for 24 hours is equivalent to 20 GiB per day = 21,474,836,480 bytes per day.

  Suppose that you query the BLOCK\_STORAGE\_HISTORY view:

  Copy code

  ```
  SELECT * FROM snowflake.account_usage.BLOCK_STORAGE_HISTORY
  ```

  The query returns the following results:

  ```
  +-------------------------------+--------------------+-------------------------+-----------------+----------------+-----------------------+-----------------------------+
  | USAGE_DATE                    | STORAGE_TYPE       | COMPUTE_POOL_NAME       | COMPUTE_POOL_ID |       BYTES    |       ADDITIONAL_IOPS |       ADDITIONAL_THROUGHPUT |
  |-------------------------------+--------------------+-------------------------+-----------------+----------------|-----------------------|-----------------------------|
  | 2025-02-01 00:00:00.000 -0700 | BLOCK_STORAGE      | POOL_1                  | 1               | 2,684,354,560  | 250.000000000         | 25.000000000                |
  | 2025-02-01 00:00:00.000 -0700 | BLOCK_STORAGE      | POOL_2                  | 2               | 5,368,709,120  | 0.50000000            | 0.500000000                 |
  | 2025-02-01 00:00:00.000 -0700 | SNAPSHOT           | NULL                    | NULL            | 21,474,836,480 | 0.000000000           | 0.000000000                 |
  +-------------------------------+--------------------+-------------------------+-----------------+----------------+-----------------------+-----------------------------+
  ```
- The additional IOPS (ADDITIONAL\_IOPS) and throughput (ADDITIONAL\_THROUGHPUT) values show the amount by which your [configured values](/developer-guide/snowpark-container-services/block-storage-volume#label-spcs-block-storage-volume-specifying) exceed their default values. For example, on AWS, the block configuration default IOPS is 3,000, and the default throughput is 125 MiB/second. If you configure an AWS block device with 4,000 IOPS and 225 MiB/second throughput, the additional IOPS would be 1,000 (4,000 - 3,000), and the additional throughput would be 100 MiB/second (225 - 125).

  The following three examples illustrate how you can get this information from the BLOCK\_STORAGE\_HISTORY view. Suppose that your account is set up with the following:

  - Your account provisioned a 10 GiB block volume (as part of a service) with 1000 additional IOPS and 100 MiB/second additional throughput for 6 hours on 2025-02-01 for compute pool `POOL_1`. If you query the view, you can get the following information from the `additional_iops` and `additional_throughput` columns:

    - Using 10 GiB for 6 hours equals 2.5 GiB per day (10 GiB x 6/24 hours = 2.5 GiB = 2,684,354,560 bytes per day).
    - Using 1000 additional IOPS for 6 hours equals 250 IOPS per day (1000 IOPS \* 6/24 hours = 250 IOPS per day).
    - Using 100 additional MiB/second for 6 hours equals an average of 25 MiB/second per day (100 MiB \* 6/24 hours = 25 MiB per day).
  - Your account provisioned a 10 GiB block volume (as part of a service) with 1 additional IOPS and 1 MiB/s additional throughput for 12 hours on 2025-02-01 for compute pool `POOL_2`.

    - Using 10 GiB for 12 hours equals 5 GiB per day (10 GiB \* 12/24 hours = 5 GiB per day = 5,368,709,120 bytes per day).
    - 1 additional IOPS used for 12 hours equals 0.5 IOPS per day (1 IOPS \* 12/24 hours = 0.5 IOPS per day).
    - 1 additional MiB/second used for 12 hours equals 0.5 MiB/second per day (1 MiB \* 12/24 hours = 0.5 MiB per day).
  - You use a 20 GiB snapshot for 24 hours on 2025-02-01. Using 20 GiB for 24 hours is equivalent to 20 GiB per day.

  When you query the view:

  Copy code

  ```
  SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.BLOCK_STORAGE_HISTORY;
  ```

  The `bytes`, `additional_iops`, and `additional_throughput` columns in the query output provide this information:

  ```
  +-------------------------------+--------------------+-------------------------+-----------------+----------------+-----------------------+-----------------------------+
  | USAGE_DATE                    | STORAGE_TYPE       | COMPUTE_POOL_NAME       | COMPUTE_POOL_ID |       BYTES    |       ADDITIONAL_IOPS |       ADDITIONAL_THROUGHPUT |
  |-------------------------------+--------------------+-------------------------+-----------------+----------------|-----------------------|-----------------------------|
  | 2025-02-01 00:00:00.000 -0700 | BLOCK_STORAGE      | POOL_1                  | 1               | 2,684,354,560  | 250.000000000         | 25.000000000                |
  | 2025-02-01 00:00:00.000 -0700 | BLOCK_STORAGE      | POOL_2                  | 2               | 5,368,709,120  | 0.50000000            | 0.500000000                 |
  | 2025-02-01 00:00:00.000 -0700 | SNAPSHOT           | NULL                    | NULL            | 21,474,836,480 | 0.000000000           | 0.000000000                 |
  +-------------------------------+--------------------+-------------------------+-----------------+----------------+-----------------------+-----------------------------+
  ```

  Note

  - If you attach multiple block volumes to a compute pool, the view aggregates the usage and returns one row.
  - If there are multiple snapshots present on a given day, the view aggregates the usage and returns one row.
  - If you attach a single block volume to a compute pool and use it for three days, then the view returns three rows because the view reports daily usage for each compute pool having block volumes attached.
