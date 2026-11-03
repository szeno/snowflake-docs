# Workload identity federation for external consumers

An external consumer can authenticate to an [Open Data Sharing](/user-guide/open-data-sharing) catalog by using
[workload identity federation (WIF)](/user-guide/workload-identity-federation) instead of a programmatic access token (PAT). With WIF,
the consumer’s workload sends a token from its identity provider, and Snowflake matches it to a workload identity that you register on
the external consumer. You don’t need to create, distribute, or rotate a secret.

External consumers support the same identity providers and properties as user workload identities. For full details about each
property, see [ALTER USER … ADD WORKLOAD IDENTITY](/sql-reference/sql/alter-user-add-workload-identity).

This topic describes the SQL commands that manage workload identities for external consumers.

## Access control requirements

To add, modify, remove, or list workload identities for an external consumer, use a role that has the following privilege:

| Privilege | Object |
| --- | --- |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | External consumer |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

## Add a workload identity

Registers a named workload identity for an external consumer.

### Syntax

Copy code

```
ALTER EXTERNAL CONSUMER <consumer_name> ADD WORKLOAD IDENTITY <workload_identity_name>
  TYPE = { AWS | AZURE | GCP | OIDC }
  [ ARN = '<string_literal>' ]
  [ ISSUER = '<string_literal>' ]
  [ SUBJECT = '<string_literal>' ]
  [ OIDC_AUDIENCE_LIST = ( '<string_literal>' [ , '<string_literal>' ... ] ) ]
```

### Parameters

`consumer_name`
:   The identifier of the external consumer that the workload identity is associated with.

`ADD WORKLOAD IDENTITY workload_identity_name`
:   Registers a workload identity with the specified name. The name must be unique for the external consumer.

`TYPE = { AWS | AZURE | GCP | OIDC }`
:   The identity provider that issues the token that the consumer’s workload sends to Snowflake. These are the same `TYPE` values as for
    [ALTER USER … ADD WORKLOAD IDENTITY](/sql-reference/sql/alter-user-add-workload-identity). The consumer sends the same value in the
    `X-Snowflake-Workload-Identity-Provider` header when connecting. For more information, see [Connect to an open-sharing catalog](/user-guide/open-data-sharing-connect).

    You can specify the value with or without quotes; for example, `TYPE = AWS` and `TYPE = 'AWS'` are equivalent.

`ARN = 'string_literal'`
:   Required for `TYPE = AWS`. Not valid for other types.

    The Amazon Resource Name (ARN) of the AWS IAM role or user that the consumer’s workload runs as; for example,
    `arn:aws:iam::123456789012:role/example-consumer-role`. Accepted ARN forms are the same as for
    [ALTER USER … ADD WORKLOAD IDENTITY](/sql-reference/sql/alter-user-add-workload-identity).

`ISSUER = 'string_literal'`
:   - For `TYPE = AZURE`, required. The Entra ID tenant’s Authority URL, in the form
      `https://login.microsoftonline.com/<tenant_id>/v2.0`.
    - For `TYPE = OIDC`, required. The OpenID Connect (OIDC) issuer URL.
    - For `TYPE = AWS`, optional. The account-specific issuer URL from AWS, which enables JWT-based authentication. For more information,
      see [Upgrade to JWT-based authentication (recommended)](/user-guide/workload-identity-federation#label-wif-aws-upgrade-jwt).

`SUBJECT = 'string_literal'`
:   Required for `TYPE = AZURE`, `TYPE = GCP`, and `TYPE = OIDC`.

    - For `TYPE = AZURE`, the Object ID (Principal ID) of the managed identity assigned to the consumer’s Azure workload.
    - For `TYPE = GCP`, the `uniqueId` property of the Google Cloud service account that the consumer’s workload runs as. The value must be
      10 to 30 digits.
    - For `TYPE = OIDC`, the identifier of the consumer’s workload. The format is specific to the OIDC provider.

`OIDC_AUDIENCE_LIST = ( 'string_literal' [ , 'string_literal' ... ] )`
:   Optional for `TYPE = OIDC`. The audiences an ID token is allowed to use. If you omit this property, the token’s `aud` claim must be
    `snowflakecomputing.com`.

### Examples

Register an AWS workload identity for the external consumer `acme_consumer`:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer ADD WORKLOAD IDENTITY acme_aws
  TYPE = AWS
  ARN = 'arn:aws:iam::123456789012:role/acme-iceberg-reader';
```

Register an AWS workload identity that uses JWT-based authentication:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer ADD WORKLOAD IDENTITY acme_aws_jwt
  TYPE = AWS
  ARN = 'arn:aws:iam::123456789012:role/acme-iceberg-reader'
  ISSUER = '<aws_issuer_url>';
```

Register a Microsoft Azure workload identity:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer ADD WORKLOAD IDENTITY acme_azure
  TYPE = AZURE
  ISSUER = 'https://login.microsoftonline.com/<tenant_id>/v2.0'
  SUBJECT = '<managed_identity_object_id>';
```

Register a Google Cloud workload identity:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer ADD WORKLOAD IDENTITY acme_gcp
  TYPE = GCP
  SUBJECT = '123456789012345678901';
```

Register an OIDC workload identity, for example for a GitHub Actions workflow:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer ADD WORKLOAD IDENTITY acme_oidc
  TYPE = OIDC
  ISSUER = 'https://token.actions.githubusercontent.com'
  SUBJECT = 'repo:acme/iceberg-reader:ref:refs/heads/main';
```

## Modify a workload identity

Disables or enables a workload identity, sets or unsets its comment, or renames it. You can disable a workload identity to block it
from authenticating without removing it.

You can’t change `TYPE`, `ARN`, `ISSUER`, `SUBJECT`, or `OIDC_AUDIENCE_LIST` after you create a workload identity. To change them,
remove the workload identity and add a new one.

### Syntax

Copy code

```
ALTER EXTERNAL CONSUMER <consumer_name> MODIFY WORKLOAD IDENTITY <workload_identity_name>
  SET [ DISABLED = { TRUE | FALSE } ] [ COMMENT = '<string_literal>' ]

ALTER EXTERNAL CONSUMER <consumer_name> MODIFY WORKLOAD IDENTITY <workload_identity_name>
  UNSET { DISABLED | COMMENT } [ , ... ]

ALTER EXTERNAL CONSUMER <consumer_name> MODIFY WORKLOAD IDENTITY <workload_identity_name>
  RENAME TO <new_workload_identity_name>
```

### Examples

Disable a workload identity:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer MODIFY WORKLOAD IDENTITY acme_aws
  SET DISABLED = TRUE;
```

Set a comment on a workload identity:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer MODIFY WORKLOAD IDENTITY acme_aws
  SET COMMENT = 'Reader workload';
```

Re-enable a workload identity and remove its comment:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer MODIFY WORKLOAD IDENTITY acme_aws
  UNSET DISABLED, COMMENT;
```

Rename a workload identity:

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer MODIFY WORKLOAD IDENTITY acme_aws
  RENAME TO acme_reader;
```

## Remove a workload identity

Removes a workload identity from an external consumer. After you remove it, the consumer’s workload can no longer use that identity to
authenticate.

### Syntax

Copy code

```
ALTER EXTERNAL CONSUMER <consumer_name> REMOVE WORKLOAD IDENTITY <workload_identity_name>
```

### Example

Copy code

```
ALTER EXTERNAL CONSUMER acme_consumer REMOVE WORKLOAD IDENTITY acme_aws;
```

## List workload identities

Lists the workload identities registered for an external consumer.

### Syntax

Copy code

```
SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS FOR EXTERNAL CONSUMER <consumer_name>
```

### Output

The command returns the following columns:

| Column | Description |
| --- | --- |
| `name` | Name of the workload identity. |
| `type` | Identity provider for the workload identity: `AWS`, `AZURE`, `GCP`, or `OIDC`. |
| `comment` | Comment for the workload identity. Empty when no comment is set. |
| `last_used` | Date and time when the workload identity was last used to authenticate. |
| `created_on` | Date and time when the workload identity was created. |
| `additional_info` | Details of the registered identity, which depend on `type`. For example, for `AWS`, the AWS partition, account, principal type, IAM role or user name, and issuer when set. For `OIDC`, the issuer, subject, and audience list. |
| `status` | Status of the workload identity: `ACTIVE` or `DISABLED`. |

Expand

Show lessSee more

### Example

Copy code

```
SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS FOR EXTERNAL CONSUMER acme_consumer;
```

## Workload identities and the external consumer lifecycle

- If you replace an external consumer with `CREATE OR REPLACE EXTERNAL CONSUMER`, the new consumer doesn’t inherit any workload
  identities or PATs from the consumer that it replaces. Add them again.
- If you drop an external consumer, its workload identities and PATs are dropped with it.
