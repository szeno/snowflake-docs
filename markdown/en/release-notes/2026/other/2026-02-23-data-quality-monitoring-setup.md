# Feb 23, 2026: Simplified setup for Data Quality Monitoring

Data quality checks in Snowflake continuously validate the health of your data, helping you comply with regulatory standards, meet
service-level agreements, and build credibility in data-driven decisions through automated, consistent data validation.

This preview simplifies the setup of data quality checks.

## Cortex Data Quality (*Preview*)

Cortex Data Quality uses AI to intelligently suggest data quality checks based on characteristics of your metadata and usage patterns.
Leveraging the [Snowflake Cortex AI\_COMPLETE function](/sql-reference/functions/ai_complete), it eliminates the need to manually define quality checks, which accelerates the
setup process and allows someone without deep domain expertise to implement checks.

For more information, see [Set up quality checks using Cortex Data Quality](/user-guide/data-quality-ui-setup#label-data-quality-ui-setup-cortex).

## User interface for creating data quality checks (*Preview*)

You can now set up and manage data quality checks directly in [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in). The user interface lets you create quality checks
using two strategies: accept AI-suggested checks from Cortex Data Quality, or manually define checks based on your knowledge of your data.
You can define rules, monitor results, and investigate quality issues without writing SQL.

For more information, see [Use Snowsight to set up data quality checks](/user-guide/data-quality-ui-setup).
