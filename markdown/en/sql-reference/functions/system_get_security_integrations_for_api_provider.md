Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_SECURITY\_INTEGRATIONS\_FOR\_API\_PROVIDER

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

For a specified API provider, lists the external secret provider security integrations visible to the current role.

## Syntax

Copy code

```
SYSTEM$GET_SECURITY_INTEGRATIONS_FOR_API_PROVIDER( '<api_provider>' )
```

## Arguments

`api_provider`
:   Provider value. Specify one of these case-insensitive values:

    - `AWS_SECRETS_MANAGER`
    - `AZURE_KEY_VAULT`
    - `GCP_SECRET_MANAGER`

## Returns

Returns a JSON array of matching integration names. The result includes the integrations with
`TYPE = API_AUTHENTICATION` and `AUTH_TYPE = WORKLOAD_IDENTITY_FEDERATION` that use the specified provider and are
visible to the current role.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Integration | The result includes integrations on which the current role has this privilege, including through role inheritance. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The provider value is case-insensitive.
- An empty or unsupported provider value produces an error.
- An empty JSON array means that no matching integration is visible to the current role.

## Examples

List visible AWS Secrets Manager integrations:

Copy code

```
SELECT SYSTEM$GET_SECURITY_INTEGRATIONS_FOR_API_PROVIDER('AWS_SECRETS_MANAGER');
```
