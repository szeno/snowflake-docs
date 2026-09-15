# CREATE SECURITY INTEGRATION (External secret provider)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates an API authentication security integration that uses workload identity federation to access AWS Secrets
Manager, Azure Key Vault, or Google Cloud Secret Manager.

For other external API authentication methods, see
[CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth).

See also:
:   [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration) , [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) , [ALTER SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/alter-security-integration-api-auth-external-secret-provider) , [SYSTEM$VERIFY\_EXTERNAL\_SECRET\_INTEGRATION](/sql-reference/functions/system_verify_external_secret_integration) , [SYSTEM$LIST\_EXTERNAL\_SECRETS](/sql-reference/functions/system_list_external_secrets) , [SYSTEM$FETCH\_EXTERNAL\_SECRET\_FROM\_INTEGRATION](/sql-reference/functions/system_fetch_external_secret_from_integration) , [SYSTEM$GET\_SECURITY\_INTEGRATIONS\_FOR\_API\_PROVIDER](/sql-reference/functions/system_get_security_integrations_for_api_provider) , [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] SECURITY INTEGRATION [ IF NOT EXISTS ] <name>
  TYPE = API_AUTHENTICATION
  AUTH_TYPE = WORKLOAD_IDENTITY_FEDERATION
  API_PROVIDER = { AWS_SECRETS_MANAGER | AZURE_KEY_VAULT | GCP_SECRET_MANAGER }
  ENABLED = { TRUE | FALSE }
  [ AWS_ROLE_ARN = '<aws_role_arn>' ]
  [ AWS_REGION = '<aws_region>' ]
  [ AZURE_TENANT_ID = '<azure_tenant_id>' ]
  [ AZURE_AD_APPLICATION_ID = '<azure_application_id>' ]
  [ AZURE_KEY_VAULT_URI = '<azure_key_vault_uri>' ]
  [ GCP_SECRET_MANAGER_PROJECT = '<gcp_project>' ]
  [ GCP_WIF_PROVIDER = '<gcp_workload_identity_provider>' ]
  [ GCP_SERVICE_ACCOUNT_EMAIL = '<gcp_service_account_email>' ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Specifies the identifier for the integration. The identifier must be unique in your account.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TYPE = API_AUTHENTICATION`
:   Specifies that the integration authenticates Snowflake to an external API.

`AUTH_TYPE = WORKLOAD_IDENTITY_FEDERATION`
:   Specifies that Snowflake authenticates with workload identity federation. Snowflake issues a short-lived token for
    the integration and exchanges it with the cloud provider.

`API_PROVIDER = { AWS_SECRETS_MANAGER | AZURE_KEY_VAULT | GCP_SECRET_MANAGER }`
:   Specifies the external secret provider. The selected provider determines which additional parameters are required:

    | Provider | Required parameters |
    | --- | --- |
    | `AWS_SECRETS_MANAGER` | `AWS_ROLE_ARN`, `AWS_REGION` |
    | `AZURE_KEY_VAULT` | `AZURE_TENANT_ID`, `AZURE_AD_APPLICATION_ID`, `AZURE_KEY_VAULT_URI` |
    | `GCP_SECRET_MANAGER` | `GCP_SECRET_MANAGER_PROJECT`, `GCP_WIF_PROVIDER`, `GCP_SERVICE_ACCOUNT_EMAIL` |

    Expand

    Show lessSee more

    You can’t change `API_PROVIDER` after creating the integration.

`ENABLED = { TRUE | FALSE }`
:   Specifies whether the integration can be used:

    - `TRUE` allows roles with `USAGE` on the integration to call the external secret provider functions.
    - `FALSE` prevents the integration from being used.

## Optional parameters

`COMMENT = 'string_literal'`
:   Specifies a comment for the integration.

    Default: No value

## Provider parameters

Specify only the parameters for the selected `API_PROVIDER`.

### AWS Secrets Manager

`AWS_ROLE_ARN = 'aws_role_arn'`
:   Specifies the ARN of the AWS IAM role that Snowflake assumes with workload identity federation.

`AWS_REGION = 'aws_region'`
:   Specifies the AWS region used for AWS Security Token Service (STS) and Secrets Manager calls. Snowflake derives the
    token audience from this region’s AWS partition.

### Azure Key Vault

`AZURE_TENANT_ID = 'azure_tenant_id'`
:   Specifies the Microsoft Entra tenant ID.

`AZURE_AD_APPLICATION_ID = 'azure_application_id'`
:   Specifies the application (client) ID of the Entra application configured with the federated identity credential.

`AZURE_KEY_VAULT_URI = 'azure_key_vault_uri'`
:   Specifies the HTTPS URI of the key vault, such as `https://my-vault.vault.azure.net`.

### Google Cloud Secret Manager

`GCP_SECRET_MANAGER_PROJECT = 'gcp_project'`
:   Specifies the Google Cloud project ID that contains the secrets.

`GCP_WIF_PROVIDER = 'gcp_workload_identity_provider'`
:   Specifies the workload identity provider resource path without the `//iam.googleapis.com/` prefix. Use this form:

    ```
    projects/<project_number>/locations/global/workloadIdentityPools/<pool_id>/providers/<provider_id>
    ```

    Snowflake adds the prefix when deriving the token audience.

`GCP_SERVICE_ACCOUNT_EMAIL = 'gcp_service_account_email'`
:   Specifies the Google service account that Snowflake impersonates before calling Secret Manager.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |
| CREATE SECURITY INTEGRATION | Account | Available to Native Apps. Grants the ability to create external security integrations of type `API_AUTHENTICATION`. This privilege doesn’t grant the ability to create other security integration types. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can’t specify `OR REPLACE` and `IF NOT EXISTS` in the same statement.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.
- Before creating the integration, prepare the cloud resource identifiers required for the selected provider. For
  the complete setup sequence, see [External secret providers](/user-guide/external-secret-providers).
- After creating the integration, run `DESCRIBE SECURITY INTEGRATION` to get
  `WORKLOAD_IDENTITY_FEDERATION_ISSUER` and `WORKLOAD_IDENTITY_FEDERATION_SUBJECT`. Use those values to configure
  cloud trust.
- Replacing an integration generates a new subject. If the cloud trust configuration uses the old subject, provider
  authentication fails. Use
  [ALTER SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/alter-security-integration-api-auth-external-secret-provider) to change provider
  settings without changing the subject.

## Examples

Create an integration for AWS Secrets Manager:

Copy code

```
CREATE SECURITY INTEGRATION aws_sm_integration
  TYPE = API_AUTHENTICATION
  AUTH_TYPE = WORKLOAD_IDENTITY_FEDERATION
  API_PROVIDER = AWS_SECRETS_MANAGER
  AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake-secrets-role'
  AWS_REGION = 'us-west-2'
  ENABLED = TRUE;
```

Create an integration for Azure Key Vault:

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

Create an integration for Google Cloud Secret Manager:

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
