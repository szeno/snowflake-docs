# Set up Azure Key Vault as an external secret provider

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

This topic configures Snowflake to read secrets from Azure Key Vault. Snowflake authenticates as a Microsoft Entra
application that has a federated credential for Snowflake’s OpenID Connect (OIDC) issuer, so you don’t store a client
secret or certificate in Snowflake.

For background on the feature and for the functions that read secrets after setup, see
[External secret providers](/user-guide/external-secret-providers).

## Prerequisites

- A Snowflake role with the global `CREATE INTEGRATION` privilege, such as `ACCOUNTADMIN`.
- An Azure key vault that contains the secrets you intend to read.
- Permission in the Microsoft Entra tenant to register an application and add a federated credential, and permission
  on the vault to grant access to secrets.

These instructions use the Azure portal. If you use the Azure CLI or an infrastructure-as-code tool instead, apply the
same Snowflake values to the Microsoft Entra and Azure resources described in these steps. Follow the linked Microsoft
documentation for tool-specific procedures.

## Step 1: Create the Entra application and grant vault access

The Entra application doesn’t depend on the Snowflake issuer, so you can create it now. You add its federated
credential in [Step 4](#label-external-secret-providers-azure-configure-trust).

1. In the Azure portal, go to **Microsoft Entra ID** > **Add** > **App registration**.
2. Enter a name, keep the default single-tenant option, leave the redirect URI empty, and register the application.
3. On the application’s **Overview** page, record the **Application (client) ID** and the **Directory (tenant) ID**.
4. Open the key vault. On its **Overview** page, record the **Vault URI**, such as
   `https://my-vault.vault.azure.net`.
5. Give the application permission to list secrets and read secret values:

   - If the vault uses Azure role-based access control, go to **Access control (IAM)** > **Add** >
     **Add role assignment**, select the **Key Vault Secrets User** role, and assign it to the application.
   - If the vault uses vault access policies, go to **Access policies** > **Create**, select the **Get** and
     **List** secret permissions, and select the application as the principal.

For other ways to create the application, see
[Register an application with the Microsoft identity platform](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)
in the Microsoft identity platform documentation. For more information about granting access to a key vault, see the
[Azure role-based access control guide for Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide)
or [Assign a Key Vault access policy](https://learn.microsoft.com/en-us/azure/key-vault/general/assign-access-policy)
in the Azure Key Vault documentation.

## Step 2: Create the security integration

Create the integration with the tenant ID, client ID, and vault URI that you recorded:

Copy code

```
CREATE SECURITY INTEGRATION azure_kv_integration
  TYPE = API_AUTHENTICATION
  AUTH_TYPE = WORKLOAD_IDENTITY_FEDERATION
  API_PROVIDER = AZURE_KEY_VAULT
  AZURE_TENANT_ID = '00000000-0000-0000-0000-000000000000'
  AZURE_AD_APPLICATION_ID = '11111111-1111-1111-1111-111111111111'
  AZURE_KEY_VAULT_URI = 'https://my-vault.vault.azure.net'
  ENABLED = TRUE;
```

For the complete syntax and parameter descriptions, see
[CREATE SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/create-security-integration-api-auth-external-secret-provider).

Important

Don’t use `CREATE OR REPLACE SECURITY INTEGRATION` to change this integration later. Replacing it generates a new
subject, which invalidates the federated credential that you configure in
[Step 4](#label-external-secret-providers-azure-configure-trust). To change provider settings without changing the
subject, use
[ALTER SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/alter-security-integration-api-auth-external-secret-provider).

## Step 3: Get the issuer and subject

Describe the integration to retrieve its federated identity values:

Copy code

```
DESCRIBE SECURITY INTEGRATION azure_kv_integration;
```

Record these rows from the output:

| Property | Property value |
| --- | --- |
| WORKLOAD\_IDENTITY\_FEDERATION\_ISSUER | An auto-generated HTTPS URL |
| WORKLOAD\_IDENTITY\_FEDERATION\_SUBJECT | An auto-generated unique identifier |

Expand

Show lessSee more

The issuer identifies the Snowflake identity provider that Microsoft Entra ID trusts. The subject restricts that
trust to this integration.

## Step 4: Configure Azure trust

Add a federated credential to the application so it accepts Snowflake tokens:

1. In the Azure portal, open the Entra application whose client ID you set as `AZURE_AD_APPLICATION_ID`.
2. Go to **Certificates & secrets** > **Federated credentials** > **Add credential**.
3. For **Federated credential scenario**, select **Other issuer**.
4. For **Issuer**, enter the `WORKLOAD_IDENTITY_FEDERATION_ISSUER` value.
5. For **Subject identifier**, enter the `WORKLOAD_IDENTITY_FEDERATION_SUBJECT` value.
6. Enter a name for the credential, confirm that **Audience** is `api://AzureADTokenExchange`, and then add the
   credential.

For other ways to create the federated credential, see
[Configure an application to trust an external identity provider](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-create-trust)
in the Microsoft Entra Workload ID documentation.

## Step 5: Verify the integration

Verify that Snowflake can exchange a token and list secrets from the vault:

Copy code

```
SELECT SYSTEM$VERIFY_EXTERNAL_SECRET_INTEGRATION('azure_kv_integration');
```

Verification confirms that Snowflake can exchange a token with Microsoft Entra ID and list secrets. It doesn’t read a
secret value, so it doesn’t confirm that the application can get one.

For return values and error behavior, see
[SYSTEM$VERIFY\_EXTERNAL\_SECRET\_INTEGRATION](/sql-reference/functions/system_verify_external_secret_integration).

If verification fails, check the following:

- The issuer and subject on the federated credential match the current `DESCRIBE SECURITY INTEGRATION` output, and
  the audience is `api://AzureADTokenExchange`.
- `AZURE_TENANT_ID`, `AZURE_AD_APPLICATION_ID`, and `AZURE_KEY_VAULT_URI` match the application and the vault.
- The application can list secrets, through either a role assignment or a vault access policy.

Tip

New federated credentials can take up to a minute to propagate. If verification fails immediately after you
configure trust, wait, and then try again before changing the configuration.

## Step 6: Grant access to the integration

Grant `USAGE` on the integration to the roles that need to read secrets:

Copy code

```
GRANT USAGE ON INTEGRATION azure_kv_integration TO ROLE app_runtime_role;
```

Warning

`USAGE` on the integration lets a Snowflake role read every secret that the Entra application can reach. Snowflake
doesn’t provide per-secret privileges, so the application’s access to the vault is the only place to limit which
secrets are readable. Grant `USAGE` only to roles that should have access to all of them.

To give different Snowflake roles access to different secrets, create one integration for each group of secrets. For
more information, see
[Access control](/user-guide/external-secret-providers#label-external-secret-providers-access-control).

## Step 7: Test reading a secret

Using a role that has `USAGE` on the integration, list the secrets that the integration can reach:

Copy code

```
SELECT SYSTEM$LIST_EXTERNAL_SECRETS('azure_kv_integration');
```

Copy a secret name from the result, and use it to fetch the secret. The following query fetches the secret value but
returns only the secret name:

Copy code

```
SELECT PARSE_JSON(
  SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION(
    'azure_kv_integration',
    '<secret_name>')):name::STRING;
```

A successful query confirms that the Entra application can read the secret value. If verification in Step 5 succeeded
but this query fails, check the application’s **Get** permission through its role assignment or vault access policy.
For more examples, see
[Read a secret value](/user-guide/external-secret-providers#label-external-secret-providers-read-secret).

## Limitations

- `SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION` returns the latest version of a secret. You can’t request a specific
  version.
- Both `SYSTEM$LIST_EXTERNAL_SECRETS` and `SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION` identify a secret by its
  name. Passing a full secret URI instead fails.

For limitations that apply to every provider, see
[Limitations and considerations](/user-guide/external-secret-providers#label-external-secret-providers-limitations).
