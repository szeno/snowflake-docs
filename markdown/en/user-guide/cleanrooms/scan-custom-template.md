# Security scans for custom templates

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

Snowflake runs a security scan on custom templates every 30 minutes to identify Jinja code that is susceptible to a SQL injection attack.

## Prerequisites

- To enable the custom template security scan, you must log into the clean rooms UI for that account at least once.
- The PRIVACY\_AND\_SECURITY\_SCANNER task must be running.

  To see if the task is running in the **Tasks** page in Snowsight:

  1. In the navigation menu, select **Transformation** » **Tasks**.

## View security scan results

Snowflake saves security scan results to the SAMOOHA\_BY\_SNOWFLAKE\_LOCAL\_DB.PUBLIC.TEMPLATE\_SCANNER\_RESULTS table in the provider’s
Snowflake account. This table is present only if the previously listed prerequisites are satisfied.

To view results of security scans:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Use the Horizon Catalog Explorer in Snowsight or a SQL query to view the security scan results:

   SnowsightSQL

   1. In the navigation menu, select **Catalog** » **Explorer**.
   2. Navigate to `SAMOOHA_BY_SNOWFLAKE_LOCAL_DB` » `PUBLIC` » `Tables` » `TEMPLATE_SCANNER_RESULTS`.
   3. Select **Data Preview**.

   1. In the navigation menu, select **Projects** » **Worksheets**.
   2. Select **+ SQL Worksheet**.
   3. To list the results of the security scans, paste and run the following
      statement:

      Copy code

      ```
      SELECT *
         FROM samooha_by_snowflake_local_db.public.template_scanner_results;
      ```
