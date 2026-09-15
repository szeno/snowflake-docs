# ALTER SECURITY INTEGRATION (External secret provider)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Modifies an API authentication security integration used to access AWS Secrets Manager, Azure Key Vault, or Google
Cloud Secret Manager.

For other external API authentication methods, see
[ALTER SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/alter-security-integration-api-auth).

See also:
:   [ALTER SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/alter-security-integration-api-auth) , [CREATE SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/create-security-integration-api-auth-external-secret-provider) , [SYSTEM$VERIFY\_EXTERNAL\_SECRET\_INTEGRATION](/sql-reference/functions/system_verify_external_secret_integration) , [SYSTEM$LIST\_EXTERNAL\_SECRETS](/sql-reference/functions/system_list_external_secrets) , [SYSTEM$FETCH\_EXTERNAL\_SECRET\_FROM\_INTEGRATION](/sql-reference/functions/system_fetch_external_secret_from_integration) , [SYSTEM$GET\_SECURITY\_INTEGRATIONS\_FOR\_API\_PROVIDER](/sql-reference/functions/system_get_security_integrations_for_api_provider) , [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

## Syntax

### AWS Secrets Manager

Copy code

```
ALTER SECURITY INTEGRATION <name> SET
  [ ENABLED = { TRUE | FALSE } ]
  [ AWS_ROLE_ARN = '<aws_role_arn>' ]
  [ AWS_REGION = '<aws_region>' ]
  [ COMMENT = '<string_literal>' ]
```

### Azure Key Vault

Copy code

```
ALTER SECURITY INTEGRATION <name> SET
  [ ENABLED = { TRUE | FALSE } ]
  [ AZURE_TENANT_ID = '<azure_tenant_id>' ]
  [ AZURE_AD_APPLICATION_ID = '<azure_application_id>' ]
  [ AZURE_KEY_VAULT_URI = '<azure_key_vault_uri>' ]
  [ COMMENT = '<string_literal>' ]
```

### Google Cloud Secret Manager

Copy code

```
ALTER SECURITY INTEGRATION <name> SET
  [ ENABLED = { TRUE | FALSE } ]
  [ GCP_SECRET_MANAGER_PROJECT = '<gcp_project>' ]
  [ GCP_WIF_PROVIDER = '<gcp_workload_identity_provider>' ]
  [ GCP_SERVICE_ACCOUNT_EMAIL = '<gcp_service_account_email>' ]
  [ COMMENT = '<string_literal>' ]
```

## Parameters

`name`
:   Specifies the identifier of the integration to modify.

`SET ...`
:   Sets one or more properties for the existing provider type. For parameter descriptions, see
    [CREATE SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/create-security-integration-api-auth-external-secret-provider).

    You can’t set `API_PROVIDER`. Create another integration to use a different provider.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Integration | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- Altering provider settings preserves `WORKLOAD_IDENTITY_FEDERATION_ISSUER` and
  `WORKLOAD_IDENTITY_FEDERATION_SUBJECT`.
- If you change an identity resource or an audience-determining setting, update the cloud trust configuration to
  match. For AWS, changing `AWS_REGION` can change the audience.
- Use `ENABLED = FALSE` to prevent the integration from being used while you update its cloud configuration.

## Examples

Change the AWS role without changing the integration’s Snowflake identity:

Copy code

```
ALTER SECURITY INTEGRATION aws_sm_integration SET
  AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/new-snowflake-secrets-role';
```

Disable an integration while updating its cloud trust configuration:

Copy code

```
ALTER SECURITY INTEGRATION azure_kv_integration SET ENABLED = FALSE;
```
