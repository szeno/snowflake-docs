# Set up Google Cloud Secret Manager as an external secret provider

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

This topic configures Snowflake to read secrets from Google Cloud Secret Manager. Snowflake exchanges its OpenID
Connect (OIDC) token through a workload identity pool and then impersonates a service account, so you don’t store a
service account key in Snowflake.

For background on the feature and for the functions that read secrets after setup, see
[External secret providers](/user-guide/external-secret-providers).

## Prerequisites

- A Snowflake role with the global `CREATE INTEGRATION` privilege, such as `ACCOUNTADMIN`.
- A Google Cloud project with secrets in Secret Manager.
- The IAM, Resource Manager, Service Account Credentials, and Security Token Service APIs enabled in the project.
- Permission in the project to create a service account, create a workload identity pool and provider, and grant
  access to secrets.

These instructions use the Google Cloud console. If you use the gcloud CLI or an infrastructure-as-code tool instead,
apply the same Snowflake values to the Google Cloud resources described in these steps. Follow the linked Google Cloud
documentation for tool-specific procedures.

## Step 1: Create the service account and plan the pool

The service account doesn’t depend on the Snowflake issuer, so you can create it now. Choose the IDs for the workload
identity pool and provider that you create in
[Step 4](#label-external-secret-providers-gcp-configure-trust), and construct the provider resource path that the
integration requires.

1. In the Google Cloud console, select the project that contains the secrets. Record its **project ID** and its
   **project number**, both shown on the project dashboard.
2. Go to **IAM & Admin** > **Service accounts** > **Create service account**. Record the service account email
   address.
3. Grant the service account access to the secrets:

   - For each secret, open **Secret Manager**, select the secret, and on the **Permissions** tab, grant the service
     account the **Secret Manager Secret Accessor** role.
   - To let the integration list secrets, grant the service account the **Secret Manager Viewer** role on the
     project.

   For other ways to grant these roles, see
   [Access control with IAM](https://cloud.google.com/secret-manager/docs/access-control) in the Google Cloud Secret
   Manager documentation.
4. Choose an ID for a workload identity pool, and an ID for a provider within that pool. Construct the provider
   resource path from the project number and those IDs:

   ```
   projects/<project_number>/locations/global/workloadIdentityPools/<pool_id>/providers/<provider_id>
   ```

   The path uses the project number, not the project ID. The pool and the provider don’t need to exist yet.
   Snowflake doesn’t contact Google Cloud until you verify the integration.

## Step 2: Create the security integration

Set `GCP_WIF_PROVIDER` to the resource path that you constructed, even though the pool and provider don’t exist yet:

Copy code

```
CREATE SECURITY INTEGRATION gcp_sm_integration
  TYPE = API_AUTHENTICATION
  AUTH_TYPE = WORKLOAD_IDENTITY_FEDERATION
  API_PROVIDER = GCP_SECRET_MANAGER
  GCP_SECRET_MANAGER_PROJECT = 'my-gcp-project'
  GCP_WIF_PROVIDER = 'projects/123456789012/locations/global/workloadIdentityPools/my-pool/providers/snowflake-provider'
  GCP_SERVICE_ACCOUNT_EMAIL = 'snowflake-secrets@my-gcp-project.iam.gserviceaccount.com'
  ENABLED = TRUE;
```

`GCP_SECRET_MANAGER_PROJECT` takes the project ID. `GCP_WIF_PROVIDER` takes the path that contains the project
number.

For the complete syntax and parameter descriptions, see
[CREATE SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/create-security-integration-api-auth-external-secret-provider).

Important

Don’t use `CREATE OR REPLACE SECURITY INTEGRATION` to change this integration later. Replacing it generates a new
subject, which invalidates the service account grant that you configure in
[Step 4](#label-external-secret-providers-gcp-configure-trust). To change provider settings without changing the
subject, use
[ALTER SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/alter-security-integration-api-auth-external-secret-provider).

## Step 3: Get the issuer and subject

Describe the integration to retrieve its federated identity values:

Copy code

```
DESCRIBE SECURITY INTEGRATION gcp_sm_integration;
```

Record these rows from the output:

| Property | Property value |
| --- | --- |
| WORKLOAD\_IDENTITY\_FEDERATION\_ISSUER | An auto-generated HTTPS URL |
| WORKLOAD\_IDENTITY\_FEDERATION\_SUBJECT | An auto-generated unique identifier |

Expand

Show lessSee more

The issuer identifies the Snowflake identity provider that the workload identity pool trusts. The subject restricts
that trust to this integration.

## Step 4: Configure Google Cloud trust

Create the workload identity pool and provider, and then let the pool identity impersonate the service account:

1. In the Google Cloud console, go to **IAM & Admin** > **Workload Identity Federation** > **Create pool**.
2. Enter the pool ID that you chose in [Step 1](#label-external-secret-providers-gcp-service-account), and continue.
3. For the provider, select **OpenID Connect (OIDC)**, and enter these values:

   - **Provider ID:** The provider ID that you chose in Step 1.
   - **Issuer (URL):** The `WORKLOAD_IDENTITY_FEDERATION_ISSUER` value.
   - **Audiences:** Select **Default audience**.
4. For **Configure provider attributes**, map `google.subject` to `assertion.sub`, and then save the provider.

   For more information, see
   [Configure workload identity federation with other identity providers](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-providers)
   in the Google Cloud documentation.
5. Go to **IAM & Admin** > **Service accounts**, select the service account from Step 1, and on the
   **Principals with access** tab, select **Grant access**.
6. For the principal, enter the following value, replacing `<snowflake_subject>` with the
   `WORKLOAD_IDENTITY_FEDERATION_SUBJECT` value:

   ```
   principal://iam.googleapis.com/projects/<project_number>/locations/global/workloadIdentityPools/<pool_id>/subject/<snowflake_subject>
   ```
7. Assign the **Workload Identity User** role (`roles/iam.workloadIdentityUser`), and then save.

## Step 5: Verify the integration

Verify that Snowflake can exchange a token and list secrets from Secret Manager:

Copy code

```
SELECT SYSTEM$VERIFY_EXTERNAL_SECRET_INTEGRATION('gcp_sm_integration');
```

Verification confirms that Snowflake can impersonate the service account and list secrets. It doesn’t read a secret
value, so it doesn’t confirm that the service account can access a secret version.

For return values and error behavior, see
[SYSTEM$VERIFY\_EXTERNAL\_SECRET\_INTEGRATION](/sql-reference/functions/system_verify_external_secret_integration).

If verification fails, check the following:

- The issuer on the provider matches the current `DESCRIBE SECURITY INTEGRATION` output, and the provider uses the
  default audience.
- The pool and provider IDs that you used to construct `GCP_WIF_PROVIDER` in
  [Step 1](#label-external-secret-providers-gcp-service-account) match the resources that you created in
  [Step 4](#label-external-secret-providers-gcp-configure-trust), and the path uses the project number.
- The principal that you granted **Workload Identity User** uses the current subject.
- The service account has the **Secret Manager Viewer** role on the project, which is what lets it list secrets.

Tip

New identity providers can take up to a minute to propagate. If verification fails immediately after you configure
trust, wait, and then try again before changing the configuration.

## Step 6: Grant access to the integration

Grant `USAGE` on the integration to the roles that need to read secrets:

Copy code

```
GRANT USAGE ON INTEGRATION gcp_sm_integration TO ROLE app_runtime_role;
```

Warning

`USAGE` on the integration lets a Snowflake role read every secret that the service account can reach. Snowflake
doesn’t provide per-secret privileges, so the service account’s access to secrets is the only place to limit which
secrets are readable. Grant `USAGE` only to roles that should have access to all of them.

To give different Snowflake roles access to different secrets, create one integration for each group of secrets. For
more information, see
[Access control](/user-guide/external-secret-providers#label-external-secret-providers-access-control).

## Step 7: Test reading a secret

Using a role that has `USAGE` on the integration, list the secrets that the integration can reach:

Copy code

```
SELECT SYSTEM$LIST_EXTERNAL_SECRETS('gcp_sm_integration');
```

Copy a secret ID from the result, and use it to fetch the secret. The following query fetches the secret value but
returns only the secret name:

Copy code

```
SELECT PARSE_JSON(
  SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION(
    'gcp_sm_integration',
    '<secret_id>')):name::STRING;
```

A successful query confirms that the service account can access the secret value. If verification in Step 5 succeeded
but this query fails, check that the service account has the **Secret Manager Secret Accessor** role for the secret.
For more examples, see
[Read a secret value](/user-guide/external-secret-providers#label-external-secret-providers-read-secret).

## Limitations

- `SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION` returns the latest version of a secret. You can’t request an
  earlier version.
- Both `SYSTEM$LIST_EXTERNAL_SECRETS` and `SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION` identify a secret by its
  secret ID, not by its full resource name.

For limitations that apply to every provider, see
[Limitations and considerations](/user-guide/external-secret-providers#label-external-secret-providers-limitations).
