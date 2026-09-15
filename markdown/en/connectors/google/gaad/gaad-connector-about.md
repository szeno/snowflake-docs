# About the

Google Analytics is a cloud-based tool that provides insight into how users interact with your website. You can use it to analyze user actions, track the number of visitors and page views, and analyze bounce rates for a page.

The enables you to automatically ingest aggregated data from Google Analytics 4 (GA4) reports into your Snowflake account. The connector extracts aggregated data using the [GA4 Reporting API](https://developers.google.com/analytics/devguides/reporting/data/v1).

Data ingestion relies on v1 of the [Google Analytics Data API](https://developers.google.com/analytics/devguides/reporting/data/v1). For more information about ingestion model, see  [ingestion model](/connectors/google/gaad/gaad-ingestion-model).

Note

- The connector can only ingest Google Analytics 4 (GA4) report data.
- The connector requires the `date` dimension to be present in a report definition.

For release note information, see  [release notes](/release-notes/connectors/gaad).

## Limitations

The has the following limitations:

- Accounts in government regions are not supported.
- The connector can only retrieve data for Google Analytics 4 (GA4) properties. Universal Analytics (UA) are not supported.
- The data in Google Analytics might change up to 72 hours after it is recorded. Currently, the connector cannot reflect the changes in real time.
- The is not supported with Snowflake trial accounts due to external access security concerns.
- The creates tables and views for the ingested data in a database and schema chosen by the user. Currently, the connector must have ownership of those tables and views. There must be no future ownership grants on the database or schema, and the schema must not have managed access enabled.
- Users can configure at most 40 reports. Currently, this limit cannot be increased.
- [AUTOCOMMIT](/sql-reference/parameters#label-autocommit) must be enabled to configure and use the connector.
- Currently, the connector requires the [TIMESTAMP\_INPUT\_FORMAT](/sql-reference/parameters#label-timestamp-input-format) to be set to AUTO.
- If the warehouse used by the connector has [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds) set, it must be set to a minimum of 4 hours.
