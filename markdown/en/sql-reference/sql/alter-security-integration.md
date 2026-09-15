# ALTER SECURITY INTEGRATION

Modifies the properties for an existing security integration.

See also:
:   [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations) , [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

## Syntax

Copy code

```
ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name> SET <parameters>

ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name>  UNSET <parameter>

ALTER [ SECURITY ] INTEGRATION <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER [ SECURITY ] INTEGRATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

The syntax varies considerably among security environments (i.e. types of security integrations). For specific syntax, usage notes, and
examples, see:

- [ALTER SECURITY INTEGRATION (AWS IAM Authentication)](/sql-reference/sql/alter-security-integration-aws-iam)
- [ALTER SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/alter-security-integration-api-auth)
- [ALTER SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/alter-security-integration-api-auth-external-secret-provider)
- [ALTER SECURITY INTEGRATION (External OAuth)](/sql-reference/sql/alter-security-integration-oauth-external)
- [ALTER SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/alter-security-integration-oauth-snowflake)
- [ALTER SECURITY INTEGRATION (OIDC)](/sql-reference/sql/alter-security-integration-oidc)
- [ALTER SECURITY INTEGRATION (SAML2)](/sql-reference/sql/alter-security-integration-saml2)
- [ALTER SECURITY INTEGRATION (SCIM)](/sql-reference/sql/alter-security-integration-scim)
