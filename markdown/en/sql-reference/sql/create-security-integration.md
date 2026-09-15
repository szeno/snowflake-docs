# CREATE SECURITY INTEGRATION

Creates a new security integration in the account or replaces an existing integration. An integration is a Snowflake object that provides
an interface between Snowflake and a third-party service.

See also:
:   [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] SECURITY INTEGRATION [ IF NOT EXISTS ]
  <name>
  TYPE = { API_AUTHENTICATION | EXTERNAL_OAUTH | OAUTH | OIDC | SAML2 | SCIM }
  ...
```

The syntax varies considerably among security environments (i.e. types of security integrations). For specific syntax, usage notes, and
examples, see:

- [CREATE SECURITY INTEGRATION (AWS IAM Authentication)](/sql-reference/sql/create-security-integration-aws-iam)
- [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth)
- [CREATE SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/create-security-integration-api-auth-external-secret-provider)
- [CREATE SECURITY INTEGRATION (External OAuth)](/sql-reference/sql/create-security-integration-oauth-external)
- [CREATE SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/create-security-integration-oauth-snowflake)
- [CREATE SECURITY INTEGRATION (OIDC)](/sql-reference/sql/create-security-integration-oidc)
- [CREATE SECURITY INTEGRATION (SAML2)](/sql-reference/sql/create-security-integration-saml2)
- [CREATE SECURITY INTEGRATION (SCIM)](/sql-reference/sql/create-security-integration-scim)
