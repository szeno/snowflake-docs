# Sep 10, 2026: External secret providers (*Preview*)

External secret providers are now in preview. If your organization already keeps API keys, database passwords, and
similar values in AWS Secrets Manager, Azure Key Vault, or Google Cloud Secret Manager, Snowflake can read those
values when a query needs them, so you don’t have to maintain a second copy in a Snowflake
[secret](/sql-reference/sql/create-secret).

Snowflake authenticates to your secret manager with workload identity federation, so you don’t store a cloud access
key, client secret, or service account key in Snowflake. Instead, you configure your cloud provider to trust the
identity of a security integration created with `TYPE = API_AUTHENTICATION` and
`AUTH_TYPE = WORKLOAD_IDENTITY_FEDERATION`.

A role that holds the `USAGE` privilege on the integration can read every secret that the integration’s cloud
identity can reach. Snowflake doesn’t provide per-secret privileges, so scope each integration’s cloud permissions
to the secrets that its Snowflake role should read.

For more information, see the following topics:

- [External secret providers](/user-guide/external-secret-providers)
- [Use external secret providers with Openflow](/user-guide/data-integration/openflow/security/external-secret-providers)
- [CREATE SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/create-security-integration-api-auth-external-secret-provider)
- [ALTER SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/alter-security-integration-api-auth-external-secret-provider)
- [SYSTEM$VERIFY\_EXTERNAL\_SECRET\_INTEGRATION](/sql-reference/functions/system_verify_external_secret_integration)
- [SYSTEM$LIST\_EXTERNAL\_SECRETS](/sql-reference/functions/system_list_external_secrets)
- [SYSTEM$FETCH\_EXTERNAL\_SECRET\_FROM\_INTEGRATION](/sql-reference/functions/system_fetch_external_secret_from_integration)
- [SYSTEM$GET\_SECURITY\_INTEGRATIONS\_FOR\_API\_PROVIDER](/sql-reference/functions/system_get_security_integrations_for_api_provider)
