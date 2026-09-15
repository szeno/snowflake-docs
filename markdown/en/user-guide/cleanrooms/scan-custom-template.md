# Security scans for custom templates

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

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
2. Use the database object explorer in Snowsight or a SQL query to view the security scan results:

   SnowsightSQL

   1. In the navigation menu, select **Catalog** » **Database Explorer**.
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
