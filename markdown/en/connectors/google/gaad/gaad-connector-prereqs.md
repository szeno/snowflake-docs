# Preparing your Google Analytics and Google Cloud accounts

Before installing :

- Ensure that your Google Analytics properties are migrated to Google Analytics 4 (GA4). The does not support Universal Analytics.
- Ensure that the **Google Analytics Admin API** and **Google Analytics Data API** are enabled for your Google Cloud project.
- Do one of the following:
  - Create a service account key for your Google Cloud project. The uses the service account to authenticate against the GA4 API. For more information, see [Configure service account authentication for Google Cloud](/connectors/google/gaad/gaad-connector-create-service-account-key).
  - Alternatively, configure the OAuth consent screen and client ID in your Google Cloud project. The uses the OAuth consent screen and the client ID to authenticate against the GA4 API. For more information, see [Configure OAuth authentication for Google Cloud](/connectors/google/gaad/gaad-connector-create-client-id).
