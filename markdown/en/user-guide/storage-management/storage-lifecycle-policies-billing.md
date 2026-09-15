# Billing for storage lifecycle policies

When you use storage lifecycle policies, you incur costs for policy execution, data storage, and data operations.
This topic explains the cost components associated with storage lifecycle policies and provides
guidance on how to monitor each component.

## Policy execution costs

Each time Snowflake runs a storage lifecycle policy, you incur serverless compute charges to identify and process rows that
meet your defined conditions. Policies run automatically, approximately once every 24-hour period.
For billing details, see table 5 in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

### Monitoring

To view credits that are consumed by policy execution, use the following metering history views.
Filter for the STORAGE\_LIFECYCLE\_POLICY\_EXECUTION service type:

- [ACCOUNT\_USAGE.METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history)
- [ACCOUNT\_USAGE.METERING\_HISTORY](/sql-reference/account-usage/metering_history)
- [ORGANIZATION\_USAGE.METERING\_DAILY\_HISTORY](/sql-reference/organization-usage/metering_daily_history)

To view policy execution history and metadata, use the following views and function:

- [ACCOUNT\_USAGE.STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/account-usage/storage_lifecycle_policy_history)
- [ORGANIZATION\_USAGE.STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/organization-usage/storage_lifecycle_policy_history)
- [INFORMATION\_SCHEMA.STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/functions/storage_lifecycle_policy_history) (table function)

Note

Policy execution times can vary from execution to execution, even when processing similar amounts of data. To better understand
the cost of policy executions, monitor the credits charged for each execution along with the amount of data expired or archived.

## Archive storage costs

When you archive data, you incur charges for moving data to archive storage,
storing data in archive storage, and
retrieving archived data. If you drop a table with archived data,
you might also incur minimum storage duration charges.

### Moving data to archive storage

When a policy archives data, you incur a one-time serverless compute charge to move data from regular storage to the
cool or cold archive storage tier. For billing details, see table 5 in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

#### Monitoring

To view the credits consumed to move data to archive storage, use the following metering history views.
Filter for the STORAGE\_LIFECYCLE\_POLICY\_EXECUTION and ARCHIVE\_STORAGE\_WRITE service types:

- [ACCOUNT\_USAGE.METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history)
- [ACCOUNT\_USAGE.METERING\_HISTORY](/sql-reference/account-usage/metering_history)
- [ORGANIZATION\_USAGE.METERING\_DAILY\_HISTORY](/sql-reference/organization-usage/metering_daily_history)

### Data storage

After policy execution, you temporarily incur charges for *both* archive storage and [table storage](/user-guide/cost-exploring-data-storage).
Snowflake immediately copies data into the specified archive storage tier when the policy runs. However, the data remains in
table storage for seven or more days, which is the 7-day [Fail-safe](/user-guide/data-failsafe) period plus your
[Time Travel](/user-guide/data-time-travel) retention period set by DATA\_RETENTION\_TIME\_IN\_DAYS.

After this period, data in archive storage incurs ongoing storage charges.
For billing details, see table 3(e) in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

#### Monitoring

To view the volume of archived data in bytes for a table, database, or for your account, use the following views:

**Account Usage views:**

- [ACCOUNT\_USAGE.TABLE\_STORAGE\_METRICS](/sql-reference/account-usage/table_storage_metrics)
- [ACCOUNT\_USAGE.TABLES](/sql-reference/account-usage/tables)
- [ACCOUNT\_USAGE.DATABASE\_STORAGE\_USAGE\_HISTORY](/sql-reference/account-usage/database_storage_usage_history)
- [ACCOUNT\_USAGE.STORAGE\_USAGE](/sql-reference/account-usage/storage_usage)

**Organization Usage views:**

- [ORGANIZATION\_USAGE.TABLE\_STORAGE\_METRICS](/sql-reference/organization-usage/table_storage_metrics)
- [ORGANIZATION\_USAGE.TABLES](/sql-reference/organization-usage/tables)
- [ORGANIZATION\_USAGE.DATABASE\_STORAGE\_USAGE\_HISTORY](/sql-reference/organization-usage/database_storage_usage_history)

### Data retrieval

When you query [retrieve archived data](/user-guide/storage-management/storage-lifecycle-policies-retrieving-archived-data),
you incur the following charges:

- **Retrieval cost**: One-time charge to retrieve archived data from the archive storage tier.
- **File processing**: Serverless compute charge to process the retrieved data.
- **Temporary storage** (COLD tier only): When you retrieve data from the COLD tier, Snowflake temporarily stores the
  retrieved data in normal storage. This incurs additional storage charges.

For billing details, see tables 3(e) and 5 in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

Note

To estimate retrieval cost, use [EXPLAIN](/sql-reference/sql/explain) with
[CREATE TABLE … FROM ARCHIVE OF](/sql-reference/sql/create-table#label-create-table-from-archive-of-syntax). This shows the number of files that
will be retrieved from archive storage. For an example, see [Retrieve archived data](/user-guide/storage-management/storage-lifecycle-policies-retrieving-archived-data).

#### Monitoring

To view consumed credits and the cost related to retrieving archived data, use the following views:

- [ACCOUNT\_USAGE.ARCHIVE\_STORAGE\_DATA\_RETRIEVAL\_USAGE\_HISTORY](/sql-reference/account-usage/archive_storage_data_retrieval_usage_history)

To view the credits consumed for file processing in order to retrieve archived data, use the following metering history views.
Filter for the ARCHIVE\_STORAGE\_RETRIEVAL\_FILE\_PROCESSING service type:

- [ACCOUNT\_USAGE.METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history)
- [ACCOUNT\_USAGE.METERING\_HISTORY](/sql-reference/account-usage/metering_history)
- [ORGANIZATION\_USAGE.METERING\_DAILY\_HISTORY](/sql-reference/organization-usage/metering_daily_history)

To view temporary storage that you use when you retrieve data from the COLD storage tier,
use the ARCHIVE\_STORAGE\_RETRIEVAL\_TEMP\_BYTES column in the
[ACCOUNT\_USAGE.STORAGE\_USAGE](/sql-reference/account-usage/storage_usage).

### Minimum storage duration charges

Cloud providers impose a minimum storage duration for archive storage tiers. When you drop a table, Snowflake
deletes the table data from storage. If the table data is in archive storage and hasn’t been there for
the minimum duration set by the cloud provider, Snowflake charges you for the minimum duration.

For example, if you drop a table with data that Snowflake moved to the AWS cold storage tier 15 days ago, you still
incur storage cost for the remaining 165 days of the minimum cold storage period, which is the 180-day minimum minus 15 days already stored.

For archive storage billing details, see table 3(e) in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

The minimum storage duration varies by cloud provider and storage tier:

- **COOL tier**: 90-day minimum
- **COLD tier**: 180-day minimum

#### Monitoring

To view the amount of data that is subject to minimum storage duration charges for a table, use the following columns
in the TABLE\_STORAGE\_METRICS view:

- ARCHIVE\_STORAGE\_COOL\_EARLY\_DELETION\_PENALTY\_BYTES
- ARCHIVE\_STORAGE\_COLD\_EARLY\_DELETION\_PENALTY\_BYTES

These columns are available in the following topics:

- [ACCOUNT\_USAGE.TABLE\_STORAGE\_METRICS](/sql-reference/account-usage/table_storage_metrics)
- [ORGANIZATION\_USAGE.TABLE\_STORAGE\_METRICS](/sql-reference/organization-usage/table_storage_metrics)
