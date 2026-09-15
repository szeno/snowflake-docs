# CREATE SECRET

Creates a new secret in the current or specified schema or replaces an existing secret.

See also:
:   [ALTER SECRET](/sql-reference/sql/alter-secret) , [DESCRIBE SECRET](/sql-reference/sql/desc-secret) , [DROP SECRET](/sql-reference/sql/drop-secret) ,
    [SHOW SECRETS](/sql-reference/sql/show-secrets)

## Syntax

**OAuth with client credentials flow:**

Copy code

```
CREATE [ OR REPLACE ] SECRET [ IF NOT EXISTS ] <name>
  TYPE = OAUTH2
  API_AUTHENTICATION = <security_integration_name>
  OAUTH_SCOPES = ( '<scope_1>' [ , '<scope_2>' ... ] )
  [ COMMENT = '<string_literal>' ]
```

**OAuth with authorization code grant flow:**

Copy code

```
CREATE [ OR REPLACE ] SECRET [ IF NOT EXISTS ] <name>
  TYPE = OAUTH2
  OAUTH_REFRESH_TOKEN = '<string_literal>'
  OAUTH_REFRESH_TOKEN_EXPIRY_TIME = '<string_literal>'
  API_AUTHENTICATION = <security_integration_name>
  [ COMMENT = '<string_literal>' ]
```

**Cloud provider:**

Copy code

```
CREATE [ OR REPLACE ] SECRET [ IF NOT EXISTS ] <name>
  TYPE = CLOUD_PROVIDER_TOKEN
  API_AUTHENTICATION = '<cloud_provider_security_integration>'
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
```

**Basic authentication:**

Copy code

```
CREATE [ OR REPLACE ] SECRET [ IF NOT EXISTS ] <name>
  TYPE = PASSWORD
  USERNAME = '<username>'
  PASSWORD = '<password>'
  [ COMMENT = '<string_literal>' ]
```

**Generic string:**

Copy code

```
CREATE [ OR REPLACE ] SECRET [ IF NOT EXISTS ] <name>
  TYPE = GENERIC_STRING
  SECRET_STRING = '<string_literal>'
  [ COMMENT = '<string_literal>' ]
```

**Symmetric key:**

Copy code

```
CREATE [ OR REPLACE ] SECRET [ IF NOT EXISTS ] <name>
  TYPE = SYMMETRIC_KEY
  ALGORITHM = GENERIC
```

**Workload identity federation:**

Copy code

```
CREATE [ OR REPLACE ] SECRET [ IF NOT EXISTS ] <name>
  TYPE = WORKLOAD_IDENTITY_FEDERATION
  [ COMMENT = '<string_literal>' ]
```

## OAuth with client credentials flow required parameters

`name`
:   String that specifies the identifier (that is, the name) for the secret. It must be unique in your schema.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TYPE = OAUTH2`
:   Specifies a secret to use with an OAuth grant flow.

`API_AUTHENTICATION = security_integration_name`
:   Specifies the `name` value of the Snowflake security integration that connects Snowflake to an external service.

`OAUTH_SCOPES = ( 'scope_1' [ , 'scope_2' ... ] )`
:   Specifies a comma-separated list of scopes to use when making a request from the OAuth server by a role with USAGE on the integration
    during the OAuth client credentials flow.

    This list must be a subset of the scopes defined in the `OAUTH_ALLOWED_SCOPES` property of the security integration. If the
    `OAUTH_SCOPES` property values are not specified, the secret inherits all of the scopes that are specified in the security
    integration.

    For the ServiceNow connector, the only possible scope value is `'useraccount'`.

## OAuth with authorization code grant flow required parameters

`name`
:   String that specifies the identifier (that is, the name) for the secret. It must be unique in your schema.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TYPE = OAUTH2`
:   Specifies a secret to use with the OAuth grant flow.

`OAUTH_REFRESH_TOKEN = 'string_literal'`
:   Specifies the token as a string that is used to obtain a new access token from the OAuth authorization server when the access token
    expires.

`OAUTH_REFRESH_TOKEN_EXPIRY_TIME = 'string_literal'`
:   Specifies the timestamp as a string when the OAuth refresh token expires.

`API_AUTHENTICATION = security_integration_name`
:   Specifies the `name` value of the Snowflake security integration that connects Snowflake to an external service.

## AWS IAM required parameters

`TYPE = CLOUD_PROVIDER_TOKEN`
:   Specifies that this is a secret for use with a cloud provider, such as Amazon Web Services (AWS).

`API_AUTHENTICATION = 'cloud_provider_security_integration'`
:   Specifies the `name` value of the Snowflake [security integration](/sql-reference/sql/create-security-integration-aws-iam)
    that connects Snowflake to a cloud provider.

## Basic authentication required parameters

`name`
:   String that specifies the identifier (that is, the name) for the secret. It must be unique in your schema.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TYPE = PASSWORD`
:   Specifies a secret to use with basic authentication.

    When specifying this type you must specify values for the username and password properties.

`USERNAME = 'username'`
:   Specifies the username value to store in the secret.

    Specify this value when setting the `TYPE` value to `PASSWORD` for use with basic authentication.

`PASSWORD = 'password'`
:   Specifies the password value to store in the secret.

    Specify this value when setting the `TYPE` value to `PASSWORD` for use with basic authentication.

## Generic string parameters

`name`
:   String that specifies the identifier (that is, the name) for the secret. It must be unique in your schema.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TYPE = GENERIC_STRING`
:   Specifies a secret to store a sensitive string value.

`SECRET_STRING = 'string_literal'`
:   Specifies the string to store in the secret.

    The string can be an API token or a sensitive string value that can be used in the handler code of a UDF or stored procedure. For
    details, see [Creating and using an external access integration](/developer-guide/external-network-access/creating-using-external-network-access).

    You should not use this property to store any kind of OAuth token; use one of the other secret types for your OAuth use cases.

## Symmetric key parameters

Symmetric key secrets generate a cryptographic key that can be used for cryptographic operations. It’s currently used only to generate
[synthetic data](/user-guide/synthetic-data).

`ALGORITHM`
:   Specifies which algorithm to use to generate the symmetric key. The only value supported is `GENERIC`, which generates a 256-bit key.

## Workload identity federation parameters

`name`
:   String that specifies the identifier (that is, the name) for the secret. It must be unique in your schema.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TYPE = WORKLOAD_IDENTITY_FEDERATION`
:   Specifies a secret that lets a Snowflake workload authenticate to an external service using workload identity federation, with Snowflake
    acting as the OpenID Connect (OIDC) provider. When you create the secret, Snowflake stores the issuer URL and the subject identifier of the
    workload as properties of the secret.

    For more information, see [Workload identity federation for Snowflake workloads that access external services](/user-guide/workload-identity-federation-outbound).

## Optional parameters

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the secret.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE SECRET | Schema |  |
| USAGE | Database or schema |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

### OAuth with client credentials

Create a secret for use with the OAuth client credentials flow:

Copy code

```
CREATE OR REPLACE SECRET mysecret
  TYPE = OAUTH2
  API_AUTHENTICATION = mysecurityintegration
  OAUTH_SCOPES = ('useraccount')
  COMMENT = 'secret for the ServiceNow connector'
```

### OAuth with authorization code grant

Create a secret for use with the OAuth code grant flow:

Copy code

```
CREATE SECRET service_now_creds_oauth_code
  TYPE = OAUTH2
  OAUTH_REFRESH_TOKEN = '34n;vods4nQsdg09wee4qnfvadH'
  OAUTH_REFRESH_TOKEN_EXPIRY_TIME = '2022-01-06 20:00:00'
  API_AUTHENTICATION = sn_oauth;
```

### AWS IAM

Create a secret for use with Amazon Web Services (AWS) by including the AWS IAM ARN for authentication:

Copy code

```
CREATE SECRET aws_secret
  TYPE = CLOUD_PROVIDER_TOKEN
  API_AUTHENTICATION = myawsiamintegration
  ENABLED = TRUE;
```

### Basic authentication

Create a secret that specifies a username and password to access ServiceNow:

Copy code

```
CREATE SECRET service_now_creds_pw
  TYPE = PASSWORD
  USERNAME = 'jsmith1'
  PASSWORD = 'W3dr@fg*7B1c4j';
```

### Workload identity federation

Create a secret that lets a Snowflake workload authenticate to external services using workload identity federation:

Copy code

```
CREATE SECRET my_db.auth.my_workload
  TYPE = WORKLOAD_IDENTITY_FEDERATION;
```
