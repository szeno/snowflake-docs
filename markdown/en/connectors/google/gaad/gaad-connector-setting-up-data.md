# Set up data ingestion for your instance

This topic describes how to access the in your Snowflake account.

## Add reports in the connector

To set up data ingestion using Snowsight, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the Snowflake Connector for , and then select the tile for the connector.
4. In the **Data sync** section, select **Add report**.
5. In the new dialog, complete the following fields:

   | Field | Description |
   | --- | --- |
   | **Report name** | Identifier for the new report  Specify a name that is unique for your destination schema. The name of the report must follow the naming rules for [unquoted object identifiers](/sql-reference/identifiers-syntax#label-unquoted-identifier). |
   | **Property** | A Google Analytics property that holds the data you want to ingest  Choose one of the available Google Analytics properties.  Note  If a Google Analytics property that you want to use is not available, check whether the credentials used by the connector have access to it. For more information, see [Preparing your Google Analytics and Google Cloud accounts](/connectors/google/gaad/gaad-connector-prereqs). |
   | **Dimensions** | Google Analytics 4 dimensions to be included in your report  Dimensions are attributes of your data. For example, the dimension `city` indicates the city from which an event originates. The connector includes the `date` dimension in all reports.  Note  The dimensions field appears after you select the Google Analytics property. At most nine dimensions can be configured.  For more details about the available dimensions, see [API Dimensions & Metrics](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema). |
   | **Metrics** | Google Analytics 4 metrics to be included in your report  Metrics are quantitative measurements of a report. For example, the metric `active1DayUsers` is the number of distinct active users on your site or app within a one-day period. You must select at least one metric.  Note  The metrics field appears after you select the Google Analytics property. At most 10 metrics can be configured.  For more details about the available metrics, see [API Dimensions & Metrics](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema). |
   | **Keep empty rows** | If this is selected, the ingested data should contain records with dimension combinations for which all the metrics are zero (indicating that there were no events correlated with those dimensions).  Note  Some dimension combinations might not be present in the ingested data. |
   | **Avoid sampling** | If selected, the connector may cancel some ongoing ingestion runs and retry with a shorter interval length to download unsampled data, see  [ingestion model](/connectors/google/gaad/gaad-ingestion-model). |
   | **Sync data from** | Start date for the initial load of data |
   | **Sync schedule** | Sync frequency for the ongoing load of data |

   Expand

   Show lessSee more
6. Select **Start Sync**.

It can take a few minutes for the ingestion process to be complete. The table and view with your report data will not be visible in the destination
database until the data from GA is fully fetched.

## Delete reports from the connector

Note

Deleting the report does not delete the ingested data for that report.

1. In the **Data sync** section, next to the report that you want to delete, select the trash bin button .

   A confirmation dialog asks you to confirm that you want to delete the selected report.
2. Select **Delete Report**.

The delete report process may take several minutes.
