# View results of a data metric function

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

You can access the results of a scheduled data metric function (DMF) in the following ways:

- Query the dedicated event table.
- Query the [DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/data_quality_monitoring_results) view, which is a
  flattened version of the event table.
- Call the [DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/functions/data_quality_monitoring_results) table function.

Each method of viewing results has its own access control requirements. For example, an application role that grants access to the table
function might not let you query the event table. For a description of these access control requirements, see
[Viewing data quality results](/user-guide/data-quality-access-control#label-data-quality-access-control-view).

Note

This topic describes how you can use SQL to view the results of a DMF. To interact with a user interface to see the results of a data quality check, see [Monitoring data quality checks in Snowsight](/user-guide/data-quality-ui-monitor). A DMF is a building block of a data quality check.

Note

If a DMF association uses a WITHIN GROUP clause, each evaluation produces one result row per
group, and the `GROUP_BY_INFO` column identifies the group for each row. For details, see
[Apply data quality checks by group](/user-guide/data-quality-group-by).

## Query the dedicated event table

This option gives you access to the raw data, and you have more freedom to post-process the data using derived objects, such as creating
views, table functions, or stored procedures based on how you want to analyze the results. Additionally, if you create these
derived objects, you can selectively grant access on these objects to different roles. For example, a data engineer can access the stored
procedures to maintain the approach to obtain the results, and a data analyst can access the view to analyze the results.

The event table is named `SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS_RAW`.

For information about the event table columns, see [Event table columns](/developer-guide/logging-tracing/event-table-columns).

For a representative example to query the event table, see the
[logging and tracing tutorial](/developer-guide/logging-tracing/tutorials/logging-tracing-getting-started).

## Query the DATA\_QUALITY\_MONITORING\_RESULTS view

This option enables you to query the [DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/data_quality_monitoring_results) view,
which flattens the raw data in the event table to enable easier access to the DMF results. Additionally, this option is best when data
post-processing is not needed and when you don’t want to grant access to the raw data.

The view exists in the LOCAL schema in the shared SNOWFLAKE database: `SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS`.

For information, see the [DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/local/data_quality_monitoring_results) view.

Note

The SNOWFLAKE.GOVERNANCE\_VIEWER database role does not have access to query the DATA\_QUALITY\_MONITORING\_RESULTS view.

## Call the DATA\_QUALITY\_MONITORING\_RESULTS table function

This option enables you to call the [DATA\_QUALITY\_MONITORING\_RESULTS](/sql-reference/functions/data_quality_monitoring_results) table function to view the DMF
results. The function returns the same columns as the DATA\_QUALITY\_MONITORING\_RESULTS view. However, you can only specify a single table
when calling the function. This option is best when you want to limit data metric function results to a single table and not provide
access to the measurements of other tables or the event table.
