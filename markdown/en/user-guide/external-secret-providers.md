# External secret providers

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

An *external secret provider* is a cloud secret manager that you own and Snowflake reads from. If your organization
already keeps API keys, database passwords, and similar values in AWS Secrets Manager, Azure Key Vault, or Google
Cloud Secret Manager, Snowflake can retrieve those values when a query needs them. You don’t need to keep a second
copy in a Snowflake [secret](/sql-reference/sql/create-secret).

Snowflake authenticates to your secret manager with workload identity federation. You don’t store a cloud access
key, client secret, or service account key in Snowflake. Instead, you configure your cloud provider to trust the
identity of a Snowflake security integration.

## How external secret providers work

Each external secret provider is represented by a security integration with `TYPE = API_AUTHENTICATION` and
`AUTH_TYPE = WORKLOAD_IDENTITY_FEDERATION`. The integration stores the provider configuration and has its own
federated identity, described by an *issuer* (Snowflake’s OpenID Connect (OIDC) issuer URL, unique to your account)
and a *subject* (unique to one integration within that issuer). You configure your cloud provider to trust that
issuer and subject.

When a query reads a secret, Snowflake issues a short-lived token for the integration, exchanges the token with your
cloud provider for temporary credentials, and uses those credentials to call your secret manager. Nothing
long-lived is stored in Snowflake.

External secret providers authenticate through a security integration, not the `CREATE SECRET`-based outbound
workload identity federation mechanism described in [Workload identity federation for Snowflake workloads that access external services](/user-guide/workload-identity-federation-outbound), which is
a separate implementation for other external services.

## Access control

Two layers of permissions control access:

- **Snowflake permissions:** A role needs the `USAGE` privilege on the integration to verify the integration, list
  secrets, or read secret values. Snowflake doesn’t provide per-secret privileges for an external secret provider
  integration.
- **Cloud permissions:** The permissions granted to the federated cloud identity determine which secrets the
  integration can reach.

Warning

Granting `USAGE` on the integration lets the role read every secret that the integration’s cloud identity can reach.
Any user who can activate the role, including through role inheritance, can list those secrets and read their
plaintext values.

Before granting the integration, confirm which secrets the cloud identity can read and which users can activate the
role.

To give different Snowflake roles access to different secrets, create one integration for each group of secrets,
scope each integration’s cloud permissions to that group, and grant each integration to the appropriate role:

Copy code

```
GRANT USAGE ON INTEGRATION my_secret_provider_integration TO ROLE app_runtime_role;
```

## Set up an external secret provider

Setup takes a Snowflake role with the global `CREATE INTEGRATION` privilege, such as `ACCOUNTADMIN`, and permission
in your cloud account to configure a federated identity and grant it access to secrets. Follow the topic for your
secret manager:

- [Set up AWS Secrets Manager as an external secret provider](/user-guide/external-secret-providers-aws)
- [Set up Azure Key Vault as an external secret provider](/user-guide/external-secret-providers-azure)
- [Set up Google Cloud Secret Manager as an external secret provider](/user-guide/external-secret-providers-gcp)

Every topic creates the security integration before configuring cloud trust, because the two depend on each other:
the integration needs identifiers for your cloud resources, and the trust configuration needs the issuer and subject
that Snowflake generates for the integration. Snowflake doesn’t contact your cloud provider until you verify the
integration, so the identifiers you pass to `CREATE SECURITY INTEGRATION` can name resources that don’t exist yet.

## List available secrets

`SYSTEM$LIST_EXTERNAL_SECRETS` returns a JSON array of the secret identifiers that the integration can reach:

Copy code

```
SELECT SYSTEM$LIST_EXTERNAL_SECRETS('aws_sm_integration');
```

To return only secrets with a particular tag key (AWS or Azure) or label key (Google Cloud), pass the key as the
second argument:

Copy code

```
SELECT SYSTEM$LIST_EXTERNAL_SECRETS('aws_sm_integration', 'environment');
```

The returned identifier depends on the provider: a secret ARN for AWS Secrets Manager, a secret name for Azure Key
Vault, and a secret ID for Google Cloud Secret Manager.

For details, see [SYSTEM$LIST\_EXTERNAL\_SECRETS](/sql-reference/functions/system_list_external_secrets).

## Read a secret value

`SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION` accepts an integration name and one identifier returned by
`SYSTEM$LIST_EXTERNAL_SECRETS`. Don’t pass a resource URI or a list when the provider expects a name or ID:

Copy code

```
SELECT SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION(
  'aws_sm_integration',
  'arn:aws:secretsmanager:us-west-2:123456789012:secret:my-secret-a1b2c3');
```

The function returns a JSON object. The `value` field contains the secret string. Other fields identify the secret
and version and vary by provider. To use the value in a query, extract the `value` field:

Copy code

```
SELECT PARSE_JSON(
  SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION(
    'azure_kv_integration',
    'my-secret-name')):value::STRING;
```

Queries that call this function don’t appear in query history. Snowflake purges the persisted query result after
approximately five minutes. The returned value is still plaintext in the active query result. Don’t log, persist,
or expose that result to unauthorized users.

For details, see
[SYSTEM$FETCH\_EXTERNAL\_SECRET\_FROM\_INTEGRATION](/sql-reference/functions/system_fetch_external_secret_from_integration).

## Find integrations for a provider

`SYSTEM$GET_SECURITY_INTEGRATIONS_FOR_API_PROVIDER` returns a JSON array of integrations for a provider that are
visible to the current role:

Copy code

```
SELECT SYSTEM$GET_SECURITY_INTEGRATIONS_FOR_API_PROVIDER('AWS_SECRETS_MANAGER');
```

For details, see
[SYSTEM$GET\_SECURITY\_INTEGRATIONS\_FOR\_API\_PROVIDER](/sql-reference/functions/system_get_security_integrations_for_api_provider).

## Limitations and considerations

- **No per-secret privileges in Snowflake:** A role with `USAGE` on an integration can read every secret that the
  integration’s cloud identity can reach. Use separate integrations to separate access.
- **Provider type can’t be changed:** `API_PROVIDER` is immutable. Create another integration to use a different
  provider.
- **Replacing an integration changes its identity:** `CREATE OR REPLACE SECURITY INTEGRATION` generates a new
  subject. Use `ALTER SECURITY INTEGRATION` to change provider settings without invalidating cloud trust.
