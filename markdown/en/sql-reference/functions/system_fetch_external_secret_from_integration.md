Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$FETCH\_EXTERNAL\_SECRET\_FROM\_INTEGRATION

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Fetches one secret value through an external secret provider security integration.

## Syntax

Copy code

```
SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION( '<integration_name>' , '<secret_identifier>' )
```

## Arguments

`integration_name`
:   Name of an external secret provider security integration with `TYPE = API_AUTHENTICATION` and
    `AUTH_TYPE = WORKLOAD_IDENTITY_FEDERATION`.

`secret_identifier`
:   Provider-specific identifier for exactly one secret:

    | Provider | Required identifier |
    | --- | --- |
    | AWS Secrets Manager | Full secret ARN, without a version or stage qualifier appended |
    | Azure Key Vault | Secret name returned by `SYSTEM$LIST_EXTERNAL_SECRETS` |
    | Google Cloud Secret Manager | Secret ID returned by `SYSTEM$LIST_EXTERNAL_SECRETS` |

    Expand

    Show lessSee more

## Returns

Returns a provider-specific JSON object that contains the secret value and metadata. Every provider response includes
`name`, `value`, and `version_id`. AWS responses include `arn`; Azure and Google Cloud responses include `id`.

Example response from AWS Secrets Manager:

Copy code

```
{
  "arn": "arn:aws:secretsmanager:us-west-2:123456789012:secret:my-secret-a1b2c3",
  "name": "my-secret-name",
  "value": "secret-value",
  "version_id": "version"
}
```

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Integration | Required on the specified integration. |

Expand

Show lessSee more

The `USAGE` privilege authorizes the current role to use the integration, including through role inheritance. The
cloud permissions granted to the integration’s federated identity determine which operations the integration can
perform and which secrets it can access.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Queries that call this function don’t appear in query history. Snowflake purges the persisted query result after
  approximately five minutes.
- The active query result contains the secret in plaintext. Don’t log, persist, or expose the result to unauthorized
  users.
- AWS binary secrets aren’t supported.
- For Google Cloud Secret Manager, the function returns the latest secret version. You can’t request an earlier
  version.

## Examples

Fetch an AWS Secrets Manager secret:

Copy code

```
SELECT SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION(
  'aws_sm_integration',
  'arn:aws:secretsmanager:us-west-2:123456789012:secret:my-secret-a1b2c3');
```

Extract the `value` field from an Azure Key Vault response:

Copy code

```
SELECT PARSE_JSON(
  SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION(
    'azure_kv_integration',
    'my-secret-name')):value::STRING;
```
