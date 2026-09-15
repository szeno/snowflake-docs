# About Openflow Connector for Google Sheets

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of Openflow Connector for Google Sheets, its workflow, and limitations.

The Openflow Connector for Google Sheets enables the ingestion of Google Sheets data into Snowflake. It uses the Google Sheets API
to fetch data and persist that data in a table dedicated to a given range from a sheet.
The connector creates the destination table in the database and the schema provided in the configuration.

Use this connector if you’re looking to do the following:

- Load data from Google sheets into Snowflake tables for reporting, analytics and insights

## Workflow

1. A **Google Cloud administrator** creates a service account and a key as described in
   [Service account credentials](https://developers.google.com/workspace/guides/create-credentials#service-account).
2. A **Google Sheets user** creates a Google Sheets spreadsheet and shares it with the service account.
   The first row of data represents the column names in the destination table that the connector will create.
   It cannot contain actual data. If a column contains multiple data types, the connector selects the least restrictive type.
3. A **Snowflake account administrator** configures the connector as follows:
   1. Installs the connector.
   2. Creates Snowflake warehouse, destination database, destination schema, and key.
   3. Specifies the required parameters for the connector, such as Snowflake Warehouse, Destination Database, Snowflake Key, and Spreadsheet ID.
   4. Runs the connector flow. The connector performs the following tasks when run in Openflow:
      1. Retrieves the data from a specified spreadsheet.
      2. Creates and updates the destination table to reflect the schema of data from Google Sheets.
         If the destination table is not created, then it is truncated.
      3. Inserts the data into the destination table.

## Limitations

- The connector saves numeric values from a sheet only as INT or DOUBLE types.
  Because of this, small rounding errors may occur in the least significant digits if sheets contain floating point numbers.
  The connector currently doesn’t support higher precision.
- Incremental load is not supported. The connector uses the truncate and load ingestion strategy.

## Next steps

[Set up the Openflow Connector for Google Sheets](/user-guide/data-integration/openflow/connectors/google-sheets/setup)
