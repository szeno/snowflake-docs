# Configure a catalog integration for Google Cloud BigLake Metastore

Use the [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest) command to create an Iceberg REST catalog integration that connects Snowflake to Google Cloud BigLake Metastore. For Google Cloud concepts and console tasks, see the [BigQuery documentation](https://cloud.google.com/bigquery/docs).

This integration uses [Google Cloud workload identity federation](https://cloud.google.com/iam/docs/workload-identity-federation) so Snowflake can authenticate to Google Cloud without long-lived service account keys.

## Prerequisites

Before you configure the integration, obtain the workload identity issuer URL for your Snowflake account.

1. In Snowflake, run:

   Copy code

   ```
   SELECT SYSTEM$GET_WORKLOAD_IDENTITY_ISSUER_URL();
   ```
2. Save the returned issuer URL. You need it when you create the OIDC provider in Google Cloud.

## Step 1: Create an OIDC provider in Google Cloud

To establish trust between Snowflake and your Google Cloud environment, create a workload identity pool and an OIDC provider.

1. In the Google Cloud console, open **IAM & Admin** and go to the [workload identity pools page](https://console.cloud.google.com/iam-admin/workload-identity-pools).
2. Create a workload identity pool.
3. Add an OIDC provider to the pool:

   - **Issuer (URL)**: The Snowflake issuer URL from the prerequisites.
   - **Audience**: Select **Default audience**.
4. Record the provider’s audience resource name. It typically uses this pattern:

   ```
   //iam.googleapis.com/projects/<project_number>/locations/global/workloadIdentityPools/<pool_id>/providers/<provider_id>
   ```

For more information, see [Configure workload identity federation](https://cloud.google.com/iam/docs/configuring-workload-identity-federation) in the Google Cloud documentation.

## Step 2: Create a catalog integration

Use [CREATE CATALOG INTEGRATION (Apache Iceberg™ REST)](/sql-reference/sql/create-catalog-integration-rest) with OAuth and the `TOKEN_EXCHANGE` grant type so Snowflake can exchange its identity token for a Google Cloud access token.

The following example creates a catalog integration for BigLake:

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION biglake_catalog_int
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = 'https://biglake.googleapis.com/iceberg/v1/restcatalog'
    CATALOG_NAME = '<gcs_base_location>'
    ADDITIONAL_HEADERS = (
      "x-goog-user-project" = '<gcp_project_id>'
    )
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_GRANT_TYPE = TOKEN_EXCHANGE
    OAUTH_TOKEN_URI = 'https://sts.googleapis.com/v1/token'
    OAUTH_AUDIENCE = '<gcp_oidc_audience_url>'
    OAUTH_ALLOWED_SCOPES = ('https://www.googleapis.com/auth/bigquery')
  )
  ENABLED = TRUE;
```

### Parameters

`CATALOG_URI`
:   BigLake Iceberg REST catalog endpoint: `https://biglake.googleapis.com/iceberg/v1/restcatalog`.

`CATALOG_NAME`
:   Typically the Google Cloud Storage base path for your BigLake tables (for example, `gs://my-bucket/iceberg-data`).

`ADDITIONAL_HEADERS`
:   Required. Headers Snowflake sends with REST catalog requests. BigLake requires the `x-goog-user-project` header so Google Cloud can attribute usage to the correct billing project. Set the value to your Google Cloud project ID.

`OAUTH_GRANT_TYPE = TOKEN_EXCHANGE`
:   Enables workload identity federation so Snowflake can obtain Google Cloud access tokens through token exchange.

`OAUTH_TOKEN_URI`
:   Google Security Token Service token endpoint: `https://sts.googleapis.com/v1/token`.

`OAUTH_AUDIENCE`
:   The full audience resource name of the Google Cloud OIDC provider you recorded in step 1.

`OAUTH_ALLOWED_SCOPES`
:   OAuth scopes for BigLake and related APIs. The example uses the BigQuery scope `https://www.googleapis.com/auth/bigquery`. Use the scopes your organization requires.

## Step 3: Grant Google Cloud IAM permissions

After you create the integration, map the Snowflake workload identity to a Google Cloud principal and grant IAM roles.

1. In Snowflake, describe the catalog integration:

   Copy code

   ```
   DESC CATALOG INTEGRATION biglake_catalog_int;
   ```
2. Note the value of the `WORKLOAD_IDENTITY_FEDERATION_SUBJECT` property.
3. In Google Cloud, grant the roles your use case needs to a principal in this form:

   ```
   principal://iam.googleapis.com/projects/<project_number>/locations/global/workloadIdentityPools/<pool_id>/subject/<subject_id>
   ```

   Replace `subject_id` with the `WORKLOAD_IDENTITY_FEDERATION_SUBJECT` value from the previous step.

   Your organization might use roles such as `roles/bigquery.admin` or `roles/storage.objectViewer`. Apply the [principle of least privilege](https://cloud.google.com/iam/docs/using-iam-securely) and choose roles that match your catalog and storage access requirements.

## Step 4: Verify the catalog integration

To confirm authentication and headers, call [SYSTEM$VERIFY\_CATALOG\_INTEGRATION](/sql-reference/functions/system_verify_catalog_integration):

Copy code

```
SELECT SYSTEM$VERIFY_CATALOG_INTEGRATION('biglake_catalog_int');
```

For more context, see [Use SYSTEM$VERIFY\_CATALOG\_INTEGRATION to check your catalog integration configuration](/user-guide/tables-iceberg-configure-catalog-integration-rest-check-config#label-tables-iceberg-rest-catalog-integration-verify-system-function).

## Adjust the BigLake API rate limit

Google Cloud enforces a default per-minute rate limit on BigLake Iceberg REST catalog read requests. If your Snowflake workload exceeds this limit, increase the quota in the Google Cloud console.

1. In the Google Cloud console, open **IAM & Admin** and go to **Quotas & System Limits**.
2. Filter the list by the **BigLake API** service.
3. Locate the **Iceberg REST Catalog read requests per minute** quota.
4. Click the three dots (more actions) for that quota, and then select **Edit Quota**.
5. Enter a new limit and submit the change.

If the maximum allowed value is still too small for your workload, open a support ticket with Google Cloud to request an increase to the maximum quota.

## Next steps

After verification succeeds, create a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database) so Snowflake can discover and query your BigLake Iceberg tables:

Copy code

```
CREATE OR REPLACE DATABASE biglake_db
  LINKED_CATALOG = (
    CATALOG = 'biglake_catalog_int'
  );
```

For syntax and options, see [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked).
