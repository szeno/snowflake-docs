Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$VERIFY\_EXTERNAL\_SECRET\_INTEGRATION

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Verifies that Snowflake can exchange a workload identity token for cloud credentials and list secrets through an
external secret provider integration.

## Syntax

Copy code

```
SYSTEM$VERIFY_EXTERNAL_SECRET_INTEGRATION( '<integration_name>' )
```

## Arguments

`integration_name`
:   Name of an external secret provider security integration with `TYPE = API_AUTHENTICATION` and
    `AUTH_TYPE = WORKLOAD_IDENTITY_FEDERATION`.

## Returns

Returns a string that describes the verification result.

A successful verification returns:

```
Verification successful.
```

When the cloud identity provider rejects the federated credential, the result identifies the issuer, subject, or
audience configuration as the likely cause. When the secret manager rejects the list request, the result identifies
cloud permissions as the likely cause. Connectivity failures produce an error.

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

- Verification performs a minimal list request. The cloud identity must have permission to list secrets even if you
  only intend to fetch a known secret.
- A successful verification doesn’t confirm access to every secret. Provider permissions can restrict individual
  secret values.

## Examples

Verify an AWS Secrets Manager integration:

Copy code

```
SELECT SYSTEM$VERIFY_EXTERNAL_SECRET_INTEGRATION('aws_sm_integration');
```
