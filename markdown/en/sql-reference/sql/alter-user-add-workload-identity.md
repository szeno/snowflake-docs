# ALTER USER … ADD WORKLOAD IDENTITY

Registers a named [workload identity](/user-guide/workload-identity-federation) for a user.

See also:
:   [ALTER USER … MODIFY WORKLOAD IDENTITY](/sql-reference/sql/alter-user-modify-workload-identity) ,
    [ALTER USER … REMOVE WORKLOAD IDENTITY](/sql-reference/sql/alter-user-remove-workload-identity) ,
    [SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS](/sql-reference/sql/show-user-workload-identity-authentication-methods)

## Syntax

Copy code

```
ALTER USER [ IF EXISTS ] [ <username> ] ADD WORKLOAD IDENTITY <workload_identity_name>
  TYPE = { AWS | AZURE | GCP | OIDC }
  [ ARN = '<string_literal>' ]
  [ ISSUER = '<string_literal>' ]
  [ SUBJECT = '<string_literal>' ]
  [ OIDC_AUDIENCE_LIST = ( '<string_literal>' [ , '<string_literal>' ... ] ) ]
```

## Required parameters

`ADD WORKLOAD IDENTITY workload_identity_name`
:   Registers a workload identity with the specified name.

    The name `DEFAULT` is reserved for the workload identity assigned with the `WORKLOAD_IDENTITY` user property. Use [ALTER USER](/sql-reference/sql/alter-user) to set or unset that property. You can’t use `DEFAULT` as a name in this command.

`TYPE = { AWS | AZURE | GCP | OIDC }`
:   The provider that issues the attestation the workload sends to Snowflake.

    You can’t change `TYPE` after you create the workload identity. To use a different provider, remove the workload identity and add a new one.

## Optional parameters

`username`
:   The name of the user that the workload identity is associated with. A workload identity belongs to one user.

    To register a workload identity for another user, specify that user’s name.

    If you omit `username`, the command registers the workload identity for the user who is currently logged in (the active user of this session).

`ARN = 'string_literal'`
:   Required for `TYPE = AWS`. Not valid for other types.

    The Amazon Resource Name (ARN) that identifies the AWS user or role associated with the workload. Snowflake accepts the following forms of [IAM identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html):

    - `arn:aws:iam::account:user/user_name_with_path`
    - `arn:aws:iam::account:role/role_name_with_path`
    - `arn:aws:sts::account:assumed-role/role_name/role_session_name`

    For help obtaining the ARN, see [Configure Snowflake](/user-guide/workload-identity-federation#label-wif-aws-authentication-snowflake).

    You can’t change `ARN` after you create the workload identity.

`ISSUER = 'string_literal'`
:   Required for `TYPE = AZURE` and `TYPE = OIDC`. Not valid for other types.

    - For `TYPE = AZURE`, the Entra ID tenant’s Authority URL, in the form `https://login.microsoftonline.com/tenant/v2.0`. For help obtaining this URL, see [Configure Microsoft Azure](/user-guide/workload-identity-federation#label-wif-azure-configure-azure).
    - For `TYPE = OIDC`, the OpenID Connect (OIDC) issuer URL. For examples, see [Use cases](/user-guide/workload-identity-federation#label-wif-getting-started).

    The value can’t exceed 2048 characters.

    You can’t change `ISSUER` after you create the workload identity.

`SUBJECT = 'string_literal'`
:   Required for `TYPE = AZURE`, `TYPE = GCP`, and `TYPE = OIDC`. Not valid for other types.

    - For `TYPE = AZURE`, the case-sensitive Object ID (Principal ID) of the managed identity assigned to the Azure workload.
    - For `TYPE = GCP`, the `uniqueId` property of the service account associated with the workload. The value must be 10 to 30 digits. For help obtaining this identifier, see [Configure Snowflake](/user-guide/workload-identity-federation#label-wif-gcp-authentication-snowflake).
    - For `TYPE = OIDC`, the identifier of the workload. The format is specific to the OIDC provider. For examples, see [Use cases](/user-guide/workload-identity-federation#label-wif-getting-started).

    For `TYPE = AZURE` and `TYPE = OIDC`, the value can’t exceed 255 characters.

    You can’t change `SUBJECT` after you create the workload identity.

`OIDC_AUDIENCE_LIST = ( 'string_literal' [ , 'string_literal' ... ] )`
:   Optional for `TYPE = OIDC`. Not valid for other types.

    The audiences an ID token is allowed to use. Snowflake accepts the attestation only when every value in the token’s `aud` claim is in this list. The `aud` claim must contain at least one value, and it must not contain a value that is absent from this list.

    The list can contain up to 10 values. Each value must be 1 to 2048 characters with no spaces. If a value contains `:`, it must be a valid URI.

    If you omit this property, or set it to an empty list, every value in the token’s `aud` claim must be `snowflakecomputing.com`.

    You can’t change `OIDC_AUDIENCE_LIST` after you create the workload identity.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MODIFY PROGRAMMATIC AUTHENTICATION METHODS | User | Required to register a workload identity. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can register a workload identity only for a user whose `TYPE` property is `SERVICE` or `SERVICE_AGENT`.
- Each user can have a maximum of 10 workload identities by default. Disabled workload identities count toward this limit. The workload identity assigned with the `WORKLOAD_IDENTITY` user property also counts toward this limit.
- The workload identity name must be unique for that user. A different user can have a workload identity with the same name.
- You can’t add a workload identity from a fixed-role session. That includes a session confined to one role and a session where a restricted session scope locks role switching. Workload identities don’t support a role restriction. The command fails with `Cannot add a workload identity from a fixed-role session.`
- You can’t add a workload identity for a user in a read-only secondary account. Make the change in the primary account.
- Snowflake rejects a workload identity that duplicates an existing workload identity in the account:
  - For `TYPE = AWS`, the AWS partition, account, principal type, and principal name must be unique, including across users. For an assumed-role ARN, the principal name is the role name. The role session name isn’t part of this check. The error is `099704`.
  - For `TYPE = AZURE`, the combination of `ISSUER` and `SUBJECT` must be unique, including across users. The error is `099708`.
  - For `TYPE = GCP`, `SUBJECT` must be unique in the account, including across users. The error is `099707`.
  - For `TYPE = OIDC`, the combination of `ISSUER` and `SUBJECT` must be unique, including across users. The error is `099706`.
- To set a comment or disable the workload identity, use [ALTER USER … MODIFY WORKLOAD IDENTITY](/sql-reference/sql/alter-user-modify-workload-identity) after you create it.

## Examples

Register an AWS workload identity named `aws_prod` for the user `example_service_user`:

Copy code

```
ALTER USER IF EXISTS example_service_user ADD WORKLOAD IDENTITY aws_prod
  TYPE = AWS
  ARN = 'arn:aws:iam::123456789012:role/snowflake-workload';
```

Register an OIDC workload identity that accepts either of two audiences:

Copy code

```
ALTER USER IF EXISTS example_service_user ADD WORKLOAD IDENTITY oidc_prod
  TYPE = OIDC
  ISSUER = 'https://oidc.example.com'
  SUBJECT = 'repo:example/workload:ref:refs/heads/main'
  OIDC_AUDIENCE_LIST = ('snowflakecomputing.com', 'https://example.com');
```
