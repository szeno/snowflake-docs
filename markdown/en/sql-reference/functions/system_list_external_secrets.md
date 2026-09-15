Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$LIST\_EXTERNAL\_SECRETS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Lists the secrets visible to an external secret provider security integration.

## Syntax

Copy code

```
SYSTEM$LIST_EXTERNAL_SECRETS( '<integration_name>' [ , '<tag_or_label_key>' ] )
```

## Arguments

**Required:**

`integration_name`
:   Name of an external secret provider security integration with `TYPE = API_AUTHENTICATION` and
    `AUTH_TYPE = WORKLOAD_IDENTITY_FEDERATION`.

**Optional:**

`tag_or_label_key`
:   Returns only secrets that have the specified AWS or Azure tag key or Google Cloud label key.

## Returns

Returns a JSON array of strings. The identifier format depends on the provider:

| Provider | Returned identifier |
| --- | --- |
| AWS Secrets Manager | Full AWS Secrets Manager secret ARN |
| Azure Key Vault | Azure Key Vault secret name |
| Google Cloud Secret Manager | Google Cloud Secret Manager secret ID |

Expand

Show lessSee more

The function handles provider pagination and returns all matching secrets that the cloud identity can list.

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

- Filtering matches a key, not a key-value pair.
- Listing a secret doesn’t guarantee permission to read its value. The provider can grant list and read permissions
  separately.
- Pass one returned identifier to
  [SYSTEM$FETCH\_EXTERNAL\_SECRET\_FROM\_INTEGRATION](/sql-reference/functions/system_fetch_external_secret_from_integration).

## Examples

List all secrets visible through an integration:

Copy code

```
SELECT SYSTEM$LIST_EXTERNAL_SECRETS('aws_sm_integration');
```

List secrets with the `environment` tag or label key:

Copy code

```
SELECT SYSTEM$LIST_EXTERNAL_SECRETS('gcp_sm_integration', 'environment');
```
