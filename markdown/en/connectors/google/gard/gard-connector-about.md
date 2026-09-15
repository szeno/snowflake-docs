# About the Snowflake Connector for Google Analytics Raw Data

Google Analytics is a cloud-based tool that provides insight into how users interact with your website. You can use it to analyze user actions, track the number of visitors and page views, and analyze bounce rates for a page.

The Snowflake Connector for Google Analytics Raw Data enables you to automatically ingest event-level Google Analytics 4 (GA4) data into your Snowflake account. If you want to extract aggregated report data, see [About the](/connectors/google/gaad/gaad-connector-about)  and the [GA4 Reporting API](https://developers.google.com/analytics/devguides/reporting/data/v1).

To extract Snowflake Connector for Google Analytics Raw Data – the granular, event-level details – you must set up a manual link between a GA4 property and a Google Cloud Platform (GCP) project. This enables the export of raw data into BigQuery. The Snowflake Connector for Google Analytics Raw Data then connects to the [BigQuery Storage API](https://cloud.google.com/bigquery/docs/reference/storage/), and downloads the data into your Snowflake account.

[![The high-level architecture diagram of the Snowflake Connector for Google Analytics Raw Data](/static/images/gard_diagram.png)](/static/images/gard_diagram.png)

The Snowflake Connector for Google Analytics Raw Data ingests data to the selected destination database and schema. Tables and views containing your Google Analytics 4 data within that schema are temporarily owned by the connector, for as long as the connector is installed.
If you want to uninstall, but do not want to lose your data, please see the [Uninstalling and reinstalling the Snowflake Connector for Google Analytics Raw Data](/connectors/google/gard/gard-connector-uninstalling-and-reinstalling) section and read about the data ownership transfer during uninstallation.

For release note information, see [Snowflake Connector for Google Analytics Raw Data release notes](/release-notes/connectors/gard).

## Known limitations

The Snowflake Connector for Google Analytics Raw Data has the following limitations:

- Accounts in government regions are currently not supported.
- The Snowflake Connector for Google Analytics Raw Data does not work on Snowflake trial accounts due to external access security concerns. This is not expected to change in the future.
- The connector can retrieve data for Google Analytics 4 (GA4) properties only. Universal Analytics (UA) is not, and will not be supported.
- The Snowflake Connector for Google Analytics Raw Data assumes that the application is the owner (has OWNERSHIP privilege) of all tables and views in [destination schema](/connectors/google/gard/gard-connector-setting-up-data#label-gard-connector-preparing-destination-database). Granting the FUTURE OWNERSHIP privilege on tables or views in this SCHEMA/DATABASE, or using a managed schema, will result in connector not working correctly.
- The AUTOCOMMIT parameter has to be enabled in the session interacting with the connector.
- The connector will not work correctly if custom date formats are set in the account.
- Emojis are not supported as parts of the application name set during connector installation.
- Switching Google analytics export to a different project is not supported.
