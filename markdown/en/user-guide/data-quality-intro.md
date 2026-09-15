# Introduction to data quality checks

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Data quality checks in Snowflake continuously validate the health of your data. These checks help you comply with regulatory standards, meet
service-level agreements through accurate metrics, and build credibility in data-driven decisions by providing automated, consistent data
validation. Cortex Data Quality lets you leverage AI to agentically suggest data quality checks based on characteristics of your metadata
and usage patterns, eliminating the need to manually define checks and accelerating your setup process while keeping your data securely
inside Snowflake. Once configured, quality checks run automatically on your chosen schedule, reporting violations so you can take corrective
action.

## Get started

Snowflake provides a web interface to set up data quality checks and monitor the results of these checks.

To get started, do one of the following:

- To set up data quality checks for your data, see [Use Snowsight to set up data quality checks](/user-guide/data-quality-ui-setup).
- To monitor the results of your existing data quality checks on a specific table or view, see [Monitoring data quality checks in Snowsight](/user-guide/data-quality-ui-monitor).
- To monitor data quality health across your entire account, see [Using the data quality monitoring dashboard](/user-guide/data-quality-centralized-dashboard).

## Core concepts of data quality checks

Data metric function (DMF)
:   A DMF measures an attribute of your data such as how many NULL values exist in a column or how often a table is being updated. The DMF
    returns a value based on the current state of your data, but doesn’t define whether that value constitutes a data quality issue; a DMF is
    a building block of a data quality check.

    Snowflake provides *system DMFs* to measure common metrics without requiring configuration. For a list of the system DMFs that are
    available for various dimensions, see [System data metric functions](/user-guide/data-quality-system-dmfs).

    If there isn’t a system DMF for the metric that you want to monitor, you can define a *custom DMF*. To learn how to create a custom DMF,
    see [Custom data metric functions](/user-guide/data-quality-custom-dmfs).

Expectations
:   An expectation is combined with a DMF to create a data quality check. When a DMF returns a value, it’s compared to the expectation’s
    definition to determine whether data passed or failed the check. Return values that fail the check are reported as expectation violations
    so you can take appropriate action.

    If you [use Snowsight to create a data quality check](/user-guide/data-quality-ui-setup), you choose the DMF and define the expectation at the
    same time. You can also [use SQL to work with expectations directly](/user-guide/data-quality-expectations).

Anomaly detection
:   Anomaly detection uses historical data to automatically detect when a DMF return value is above or below a predicted range. Currently,
    Snowflake can automatically detect anomalies in the volume and freshness of your data. For more information, see
    [Detecting anomalies in data quality](/user-guide/data-quality-anomaly).

DMF schedule
:   The DMF schedule for a table or view determines how often a DMF runs. Because a DMF powers a data quality check, the DMF schedule
    determines how often the quality check is performed. By default, the DMF schedule runs a DMF once every hour. To adjust the schedule for
    a table or view, see [Adjust how often quality checks run](/user-guide/data-quality-ui-setup#label-data-quality-ui-setup-schedule).

    The DMF schedule doesn’t affect how often Snowflake checks whether there is an anomaly.

## Supported table kinds

You can set a DMF on the following kinds of table objects:

- Dynamic table
- Event table
- External table
- Apache Iceberg™ table
- Materialized view
- Table (CREATE TABLE), including temporary and transient tables
- View

You cannot set a DMF on a hybrid table or a stream object.

## Cost considerations

The DMFs that power data quality checks use [serverless compute resources](/user-guide/cost-understanding-compute#label-serverless-credit-usage) that incur costs. For the
pricing of these costs, see [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

The credits consumed by the serverless compute resources are listed under the “Data Quality Monitoring” category on your monthly bill.
These credits include compute consumed by all system or user-defined data quality metrics that you use. You are not billed for creating a
DMF.

- Billing occurs only when a scheduled DMF is computed on an object. You are not billed for unscheduled data metric
  function usage, such as calling a DMF with a SELECT statement.
- The logging infrastructure consolidates metric outputs in the event table. Consumption incurred by the logging service shows up on
  your monthly bill as “Logging.”
- During this preview, Snowflake runs automatic checks in the background to identify popular
  schemas with preliminary data quality issues. These checks are provided by Snowflake and do not
  incur any charges to your account. See [Using the data quality monitoring dashboard](/user-guide/data-quality-centralized-dashboard).

Tip

To track consumption related to quality checks, you can query the following views:

> - [DATA\_QUALITY\_MONITORING\_USAGE\_HISTORY](/sql-reference/account-usage/data_quality_monitoring_usage_history) to
>   track your credit consumption related to using DMFs in your account.
> - [METERING\_DAILY\_HISTORY](/sql-reference/organization-usage/metering_daily_history) to track the daily credits consumed for an
>   account in your organization. The `service_type` column specifies `DATA_QUALITY_MONITORING`.

## Replication

For information about replication and DMFs, see [Replication of data metric functions (DMFs)](/user-guide/account-replication-considerations#label-replication-data-quality).

## Limitations

Note the following limitations when using DMFs:

- You can only have 50,000 total associations of DMFs on objects per account. Each instance of setting a DMF on a table or view counts as
  one association.
- [Data sharing](/user-guide/data-sharing-intro): You can’t grant privileges on a DMF to a share or set a DMF on a shared table or view.
- Setting a DMF on an object tag is not supported.
- You can’t set a DMF on objects in a [reader account](/user-guide/data-sharing-intro#label-about-reader-accounts).
- Trial accounts don’t support this feature.
