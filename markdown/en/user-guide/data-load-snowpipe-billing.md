# Snowpipe costs

With Snowpipe’s serverless compute model, users can initiate any size load without managing a virtual warehouse. Instead, Snowflake provides and manages the compute resources, automatically growing or shrinking capacity based on the current Snowpipe load.

Important

Snowpipe ingestion is billed based on a fixed credit amount per GB. This simplified model provides you with more predictable data-loading expenses and simplifies cost estimation. The former cost model had two components: the actual compute resources used to load data, measured per-second/per-core, and a per-1,000-files charge.

This credit-per-GB billing model applies to all Snowflake editions: Standard, Enterprise, Business Critical, and Virtual Private Snowflake (VPS).

For text files — such as CSV, JSON, XML — you are charged based on their uncompressed size. For binary files — such as Parquet, Avro, ORC — you are charged based on their observed size regardless of compression.

For more information, see [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Resource consumption and management overhead

With the credit-per-GB pricing model, Snowpipe billing is calculated based on a fixed credit amount per GB of data that you loaded. This simplified approach means that you don’t need to track or manage compute utilization, which was formerly measured with per-second/per-core granularity.

File sizes and staging frequency might impact the performance of Snowpipe. For recommended best practices, see [Continuous data loads — that is, Snowpipe — and file sizing](/user-guide/data-load-considerations-prepare#label-snowpipe-file-size).

## Estimation of Snowpipe charges

Estimating Snowpipe charges is straightforward. You can calculate your expected costs by using your anticipated data volume and the fixed credit amount per GB. Because text files — such as CSV, JSON, XML — are charged based on their uncompressed size, you must know the compression ratio of your text files.

You can verify these calculations against your actual usage by examining the BILLED\_BYTES column in the relevant Account Usage views. The BILLED\_BYTES column was introduced in the [2025\_05 BCR bundle](/release-notes/bcr-bundles/2025_05/bcr-2045).

To understand the actual credit consumption for your specific workloads, we suggest that you experiment by performing a typical set of loads.

## View data-load history and cost

Account administrators (users with the ACCOUNTADMIN role) or users with a role granted the MONITOR USAGE global privilege can use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) or SQL to view the credits billed to your Snowflake account within a specified date range.

Occasionally, the data compaction and maintenance process can consume Snowflake credits. For example, the returned results might show that you consumed credits with 0 BYTES\_INSERTED and 0 FILES\_INSERTED. This means that your data is not being loaded, but the data compaction and maintenance process has consumed some credits.

To view the credits billed for Snowpipe data loading for your account:

> Snowsight:
> :   In the navigation menu, select **Admin** » **Cost management**.
>
> SQL:
> :   Query either of the following:
>
>     - [PIPE\_USAGE\_HISTORY](/sql-reference/functions/pipe_usage_history) table function (in the [Snowflake Information Schema](/sql-reference/info-schema)).
>     - [PIPE\_USAGE\_HISTORY view](/sql-reference/account-usage/pipe_usage_history) (in [Account Usage](/sql-reference/account-usage)).
>
>       You can run the following queries against the PIPE\_USAGE\_HISTORY view. You can verify costs based on volume by using the `BYTES_BILLED` column.
>
>       **Query: Snowpipe cost history (by day, by object)**
>
>       The following query provides a full list of pipes and the volume of credits that you consumed through the service over the last 30 days, broken out by day.
>
>       Copy code
>
>       ```
>       SELECT TO_DATE(start_time) AS date,
>         pipe_name,
>         SUM(credits_used) AS credits_used,
>         SUM(bytes_billed) AS bytes_billed_total
>       FROM snowflake.account_usage.pipe_usage_history
>       WHERE start_time >= DATEADD(month,-1,CURRENT_TIMESTAMP())
>       GROUP BY 1,2
>       ORDER BY bytes_billed_total DESC;
>       ```
>
>       **Query: Snowpipe History & m-day average**
>
>       The following query shows the average daily credits consumed by Snowpipe that are grouped by week over the last year. This query can help you identify anomalies in daily consumption averages over the year so that you can investigate sudden increases or unexpected changes in consumption.
>
>       Copy code
>
>       ```
>       WITH credits_by_day AS (
>         SELECT TO_DATE(start_time) AS date,
>        SUM(credits_used) AS credits_used,
>        SUM(bytes_billed) AS bytes_billed_total
>         FROM snowflake.account_usage.pipe_usage_history
>         WHERE start_time >= DATEADD(year,-1,CURRENT_TIMESTAMP())
>         GROUP BY 1
>       )
>       SELECT DATE_TRUNC('week',date),
>         AVG(credits_used) AS avg_daily_credits,
>         AVG(bytes_billed_total) AS avg_daily_bytes_billed
>       FROM credits_by_day
>       GROUP BY 1
>       ORDER BY 1;
>       ```

Note

[Resource monitors](/user-guide/resource-monitors) provide control over virtual warehouse credit usage; however, you cannot use them to control
credit usage for the Snowflake-provided warehouses, including the [![Snowflake logo in blue (no text)](/static/images/logo-snowflake-sans-text.png)](/static/images/logo-snowflake-sans-text.png) **SNOWPIPE** warehouse.
