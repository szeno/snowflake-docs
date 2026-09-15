# November 11, 2024 — Snowflake Notebooks Warehouse Runtime — *General Availability*

With this release, we are pleased to announce the general availability of Snowflake Notebooks on Amazon Web Services (AWS), Microsoft
Azure, and Google Cloud Platform (GCP) commercial regions.

Snowflake Notebooks is a development interface in Snowsight that offers an interactive, cell-based programming environment for Python
and SQL. In Snowflake Notebooks, you can perform exploratory data analysis, develop machine learning models, and perform other data science and
data engineering tasks all in one place. For more information, see [About Legacy Snowflake Notebooks](/user-guide/ui-snowsight/notebooks).

## Updates

- **Cell output limits** - When viewing cell results for each DataFrame output, only 10,000 rows or 8 MB is displayed, whichever is lower.
  For each cell, only 20 MB of output is allowed.
- **Reconnection/idle time setting** - Users can configure an idle timeout setting to automatically shut down the notebook session once the
  setting is met. The default setting is 30 minutes. Notebooks will automatically reconnect if you return to the session before the timeout
  setting has elapsed. You can change the idle time for each notebook in Snowsight or using the IDLE\_AUTO\_SHUTDOWN\_TIME\_SECONDS
  property using SQL. For more information, see [Develop and run code in Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-develop-run).
