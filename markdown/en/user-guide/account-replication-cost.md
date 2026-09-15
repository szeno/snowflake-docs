# Understanding replication cost

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Charges based on replication are divided into two categories: data transfer and compute resources. Both categories are billed on the
target account (i.e. the account that stores the secondary database or secondary replication/failover group that is refreshed).

Data transfer:
:   The initial replication and subsequent synchronization operations transfer data between regions. Cloud providers charge for
    data transferred from one region to another within their own network.

    The data transfer rate is determined by the location of the source account (i.e. the account that stores the primary replication
    or failover group). For data transfer pricing, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

    For more information, see [Understanding data transfer cost](/user-guide/cost-understanding-data-transfer).

Compute resources:
:   Replication operations use Snowflake-provided compute resources for the following:

    - To determine the delta of both metadata and data to be copied during the refresh operation.
    - To copy the data between accounts across regions.

    The service type for compute costs for replication in the [account usage](/sql-reference/account-usage) and
    [organization usage](/sql-reference/organization-usage) views is REPLICATION.

    For more information, see [Understanding compute cost](/user-guide/cost-understanding-compute).

Note

- The target account also incurs standard storage costs for the data in each secondary database in the account.
- The target account also incurs costs for the automatic background processes that service
  [materialized views](/user-guide/account-replication-considerations#label-replication-and-materialized-views)
  and [search optimization](/user-guide/search-optimization/working-with-tables#label-search-optimization-replication-support). For details, see the “Serverless
  Feature Credit Table” in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) for the costs per compute hour.
- Replication charges are applied even if the initial replication or a refresh operation doesn’t succeed. Any data that is copied
  before the initial replication or refresh operation fails can be reused by a subsequent refresh operation (if performed within 14 days)
  and doesn’t need to be copied again.

## Estimating and controlling costs

In general, monthly billing for replication is proportional to:

- Amount of table data in the primary database, or databases in a replication/failover group, that changes as a result of data loading
  or DML operations.
- Frequency of secondary database, or replication/failover group, refreshes from the primary database or replication/failover group.

You can control the cost of replication by carefully choosing which databases or objects to replicate and their refresh frequency. You
can stop incurring replication costs by ceasing refresh operations.

## Viewing actual costs

Users with the ACCOUNTADMIN role can use SQL to view the amount of data transferred (in bytes) and the credit usage for
replication using replication or failover groups for your Snowflake account within a specified date range.

Users with the ACCOUNTADMIN role can use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) or SQL to view the amount of replication data transferred
(in bytes) for your Snowflake account within a specified date range.

> Snowsight:
> :   In the navigation menu, select **Admin** » **Cost management**.

To view the data transfer amounts and credit usage for replication for your account:

> SQL:
> :   Query either of the following:
>
>     - [REPLICATION\_GROUP\_USAGE\_HISTORY](/sql-reference/functions/replication_group_usage_history) table function (in the [Snowflake Information Schema](/sql-reference/info-schema)). This
>       function returns replication usage activity within the last 14 days.
>     - [REPLICATION\_GROUP\_USAGE\_HISTORY view](/sql-reference/account-usage/replication_group_usage_history) (in [Account Usage](/sql-reference/account-usage)). This view returns
>       replication usage activity within the last 365 days (1 year).
>
>     For examples, see [Monitor replication costs](/user-guide/account-replication-monitor#label-replication-group-cost).

To view the cost of replication for individual databases replicated with Database Replication, see
[Monitoring database replication cost](/user-guide/db-replication-config#label-monitoring-database-replication-cost).

## Pricing for optimized refresh

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all Business Critical Edition (or higher) accounts.

When a failover group has [optimized refresh](/user-guide/account-replication-config#label-optimized-refresh) enabled
(`OPTIMIZED_REFRESH = TRUE`), account replication for that failover group is billed under the following model. Failover groups where
`OPTIMIZED_REFRESH = FALSE` continue to be billed under the existing replication pricing described in the previous sections.

| Dimension | Rate | Notes |
| --- | --- | --- |
| Replicated data volume | 5 credits per TB | Charged on the data replicated to the target account on each refresh. |
| Changed objects | 0.2 credits per 10,000 changed objects | Applies only after the first 25,000,000 changed objects per account per month. The free allowance is summed across all failover groups in the account on a calendar-month basis. |

Expand

Show lessSee more

A *changed object* count reflects the metadata changes that Snowflake replicates since the previous refresh, including changes to
internal, nested, and hidden metadata elements that aren’t directly visible in SQL. The count is *weighted*, not absolute: a single
user-visible action (such as altering a table or granting a privilege) can register as multiple changed objects, depending on how many
internal metadata records the action affects.

Object data (the rows in a table) is billed under the replicated data volume dimension, not the changed object dimension.

Note

- The setting is per failover group. You can mix optimized refresh and Replication Classic in the same account; each failover group is
  billed under the pricing model that matches its current `OPTIMIZED_REFRESH` setting.
- Optimized refresh doesn’t change replica storage costs in the target account or cross-region or cross-cloud egress charges. Those
  charges are unchanged.
