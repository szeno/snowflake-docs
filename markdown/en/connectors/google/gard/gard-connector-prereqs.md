# Preparing your Google Analytics and Google Cloud accounts

Before installing the Snowflake connector for Snowflake Connector for Google Analytics Raw Data:

- Ensure that your Google account has access to both Google Analytics and Google Cloud.
- Ensure that your Google Analytics properties are migrated to Google Analytics 4 (GA4). The Snowflake connector for Snowflake Connector for Google Analytics Raw Data does not support Universal Analytics.
- Configure the BigQuery link for each GA4 property you want to load to Snowflake. The link enables the GA4 raw data extraction to the Google Cloud project. For details, see [Configuring BigQuery Link for Google Analytics 4 property](/connectors/google/gard/gard-connector-create-link).
- Configure authentication for your Google Cloud project. Choose one of the two authentication methods supported by Snowflake Connector for Google Analytics Raw Data:

  - **Service account authentication**: Create a service account key for your Google Cloud project. The connector uses the service account to authenticate to the Google Cloud project and to read the GA4 data from the BigQuery storage. For details, see [Configuring service account authentication for Google Cloud Platform (GCP)](/connectors/google/gard/gard-connector-create-service-account-key).
  - **OAuth authentication**: Configure the OAuth consent screen and client ID for your Google Cloud project. The connector uses the OAuth consent screen and the client ID to authenticate to the Google Cloud project and to read the GA4 data from the BigQuery storage. For details, see [Configuring OAuth authentication for Google Cloud Platform (GCP)](/connectors/google/gard/gard-connector-create-client-id).
- Ensure that the Cloud Resource Manager API is enabled for your Google Cloud project. This allows the connector to list the GA4 properties available in your project.
