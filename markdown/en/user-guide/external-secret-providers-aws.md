# Set up AWS Secrets Manager as an external secret provider

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

This topic configures Snowflake to read secrets from AWS Secrets Manager. Snowflake authenticates with an AWS
Identity and Access Management (IAM) role that trusts Snowflake’s OpenID Connect (OIDC) identity provider, so you
don’t store an AWS access key in Snowflake.

For background on the feature and for the functions that read secrets after setup, see
[External secret providers](/user-guide/external-secret-providers).

## Prerequisites

- A Snowflake role with the global `CREATE INTEGRATION` privilege, such as `ACCOUNTADMIN`.
- An AWS account with secrets in AWS Secrets Manager that you intend to read.
- Permission in the AWS account to create an IAM identity provider and an IAM role, and to grant the role access to
  the secrets and, when applicable, their customer-managed KMS keys.

These instructions use the AWS console. If you use the AWS CLI or an infrastructure-as-code tool instead, apply the
same Snowflake values to the AWS resources described in these steps. Follow the linked AWS documentation for
tool-specific procedures.

## Step 1: Plan the IAM role

Don’t create the IAM role yet. AWS doesn’t let you create a web identity role until the OIDC identity provider
exists, and that provider needs the Snowflake issuer URL from
[Step 3](#label-external-secret-providers-aws-get-identity). Instead, decide on the role’s name now, and construct
the Amazon Resource Name (ARN) that the integration requires.

Record the following values:

- **AWS region:** The region that contains the secrets, such as `us-west-2`.
- **AWS account ID:** The 12-digit ID of the account that owns the secrets. The AWS console shows it in the account
  menu.
- **Role name:** A name you choose for the IAM role that you create in
  [Step 4](#label-external-secret-providers-aws-configure-trust), such as `snowflake-secrets-role`.

Construct the role ARN from the account ID and the role name:

```
arn:aws:iam::<aws_account_id>:role/<role_name>
```

Use the ARN prefix for your partition: `arn:aws-us-gov:` for AWS GovCloud (US), and `arn:aws-cn:` for AWS China. If
you plan to create the role under an IAM path, include the path before the role name.

The role doesn’t need to exist when you create the integration. Snowflake doesn’t contact AWS until you verify the
integration. If the ARN doesn’t match the role that you create in Step 4, verification in
[Step 5](#label-external-secret-providers-aws-verify) fails.

## Step 2: Create the security integration

Set `AWS_ROLE_ARN` to the ARN that you constructed, even though the role doesn’t exist yet:

Copy code

```
CREATE SECURITY INTEGRATION aws_sm_integration
  TYPE = API_AUTHENTICATION
  AUTH_TYPE = WORKLOAD_IDENTITY_FEDERATION
  API_PROVIDER = AWS_SECRETS_MANAGER
  AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake-secrets-role'
  AWS_REGION = 'us-west-2'
  ENABLED = TRUE;
```

For the complete syntax and parameter descriptions, see
[CREATE SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/create-security-integration-api-auth-external-secret-provider).

Important

Don’t use `CREATE OR REPLACE SECURITY INTEGRATION` to change this integration later. Replacing it generates a new
subject, which invalidates the trust policy that you configure in
[Step 4](#label-external-secret-providers-aws-configure-trust). To change provider settings without changing the
subject, use
[ALTER SECURITY INTEGRATION (External secret provider)](/sql-reference/sql/alter-security-integration-api-auth-external-secret-provider).

## Step 3: Get the issuer and subject

Describe the integration to retrieve its federated identity values:

Copy code

```
DESCRIBE SECURITY INTEGRATION aws_sm_integration;
```

Record these rows from the output:

| Property | Property value |
| --- | --- |
| WORKLOAD\_IDENTITY\_FEDERATION\_ISSUER | An auto-generated HTTPS URL |
| WORKLOAD\_IDENTITY\_FEDERATION\_SUBJECT | An auto-generated unique identifier |

Expand

Show lessSee more

The issuer identifies the Snowflake identity provider that AWS trusts. The subject restricts that trust to this
integration.

## Step 4: Configure AWS trust and permissions

AWS validates the token’s audience along with its issuer and subject. Snowflake derives the audience from the DNS
suffix of `AWS_REGION`. Use the following values for commonly used AWS partitions:

| Regions | Audience |
| --- | --- |
| Commercial and AWS GovCloud (US) | `sts.amazonaws.com` |
| AWS China | `sts.amazonaws.com.cn` |

Expand

Show lessSee more

First, add Snowflake as an OIDC identity provider:

1. In the AWS console, go to **IAM** > **Identity providers** > **Add provider**.
2. Select **OpenID Connect**.
3. For **Provider URL**, enter the `WORKLOAD_IDENTITY_FEDERATION_ISSUER` value, and then select **Get thumbprint**.
4. For **Audience**, enter the audience for the integration’s AWS region.
5. Select **Add provider**.

For other ways to create the provider, see
[Creating OpenID Connect (OIDC) identity providers in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)
in the AWS Identity and Access Management User Guide.

Then create the IAM role that you named in [Step 1](#label-external-secret-providers-aws-plan):

1. Go to **IAM** > **Roles** > **Create role**.
2. For **Trusted entity type**, select **Web identity**.
3. For **Identity provider**, select the provider that you just added, and for **Audience**, select the audience for
   the integration’s AWS region.
4. Add a condition where the key ends with `:sub`, the condition is `StringEquals`, and the value is the
   `WORKLOAD_IDENTITY_FEDERATION_SUBJECT` value. This restricts the role to this one integration.
5. Attach a permissions policy that grants the role:

   - `secretsmanager:GetSecretValue` for the secrets that Snowflake can read.
   - `secretsmanager:ListSecrets` for all resources. This action doesn’t support resource-level permissions.
6. For the role name, enter the name that you used to construct `AWS_ROLE_ARN`, and then create the role.

For other ways to create the role, see
[Creating a role for OpenID Connect federation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html)
in the AWS Identity and Access Management User Guide.

Scope access to secret values as narrowly as possible. For more information, see
[Identity-based policies](https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_iam-policies.html)
in the AWS Secrets Manager User Guide.

### Equivalent trust policy for the AWS CLI or infrastructure as code

The console builds the role’s trust policy from the identity provider, audience, and condition that you select. If you
manage IAM with the AWS CLI or an infrastructure-as-code tool instead, use the following equivalent trust policy:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:<partition>:iam::<aws_account_id>:oidc-provider/<issuer_host_and_path>"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "<issuer_host_and_path>:aud": "<audience>",
          "<issuer_host_and_path>:sub": "<snowflake_subject>"
        }
      }
    }
  ]
}
```

Replace the placeholders with your values:

- `<partition>`: The AWS partition: `aws`, `aws-us-gov`, or `aws-cn`.
- `<aws_account_id>`: The account that owns the role.
- `<issuer_host_and_path>`: The `WORKLOAD_IDENTITY_FEDERATION_ISSUER` value without the `https://` prefix.
- `<audience>`: The audience from the preceding table.
- `<snowflake_subject>`: The `WORKLOAD_IDENTITY_FEDERATION_SUBJECT` value.

### Permissions for customer-managed KMS keys

Secrets Manager encrypts every secret with an AWS Key Management Service (KMS) key, and it decrypts on behalf of the
identity that reads the secret. If a secret uses a customer-managed key instead of the AWS-managed key for Secrets
Manager (`aws/secretsmanager`), the role also needs permission to decrypt with that key. Without that permission,
the role can list the secret, but reading its value fails.

For the permissions to grant and where to grant them, see
[Permissions for the KMS key](https://docs.aws.amazon.com/secretsmanager/latest/userguide/security-encryption.html#security-encryption-authz)
in the AWS Secrets Manager User Guide.

## Step 5: Verify the integration

Verify that Snowflake can exchange a token and list secrets from AWS Secrets Manager:

Copy code

```
SELECT SYSTEM$VERIFY_EXTERNAL_SECRET_INTEGRATION('aws_sm_integration');
```

Verification confirms that Snowflake can assume the role and list secrets. It doesn’t read a secret value, so it
doesn’t confirm that the role can decrypt one.

For return values and error behavior, see
[SYSTEM$VERIFY\_EXTERNAL\_SECRET\_INTEGRATION](/sql-reference/functions/system_verify_external_secret_integration).

If verification fails, check the following:

- The issuer, subject, and audience configured in the identity provider and the role’s trust policy match the
  current `DESCRIBE SECURITY INTEGRATION` output.
- The role ARN that you constructed in [Step 1](#label-external-secret-providers-aws-plan) matches the role that you
  created in [Step 4](#label-external-secret-providers-aws-configure-trust). A typo in the role name produces an ARN
  that doesn’t resolve.
- The role’s permissions policy grants `secretsmanager:ListSecrets` in the integration’s region.

Tip

New identity providers can take up to a minute to propagate. If verification fails immediately after you configure
trust, wait, and then try again before changing the configuration.

## Step 6: Grant access to the integration

Grant `USAGE` on the integration to the roles that need to read secrets:

Copy code

```
GRANT USAGE ON INTEGRATION aws_sm_integration TO ROLE app_runtime_role;
```

Warning

`USAGE` on the integration lets a Snowflake role read every secret that the IAM role can reach. Snowflake doesn’t
provide per-secret privileges, so the IAM role’s permissions policy is the only place to limit which secrets are
readable. Grant `USAGE` only to roles that should have access to all of them.

To give different Snowflake roles access to different secrets, create one integration for each group of secrets. For
more information, see
[Access control](/user-guide/external-secret-providers#label-external-secret-providers-access-control).

## Step 7: Test reading a secret

Using a role that has `USAGE` on the integration, list the secrets that the integration can reach:

Copy code

```
SELECT SYSTEM$LIST_EXTERNAL_SECRETS('aws_sm_integration');
```

Copy a secret ARN from the result, and use it to fetch the secret. The following query fetches the secret value but
returns only the secret name:

Copy code

```
SELECT PARSE_JSON(
  SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION(
    'aws_sm_integration',
    '<secret_arn>')):name::STRING;
```

A successful query confirms that the IAM role can read the secret value. If verification in Step 5 succeeded but this
query fails, check the role’s `secretsmanager:GetSecretValue` permission and, for a customer-managed KMS key, its
permission to decrypt with the key. For more examples, see
[Read a secret value](/user-guide/external-secret-providers#label-external-secret-providers-read-secret).

## Limitations

- Snowflake reads string secrets only. AWS Secrets Manager binary secrets aren’t supported.
- `SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION` returns the latest version of a secret. You can’t request an
  earlier version.
- `SYSTEM$LIST_EXTERNAL_SECRETS` returns secret ARNs, and `SYSTEM$FETCH_EXTERNAL_SECRET_FROM_INTEGRATION` requires
  one. Passing a secret name fails, and so does an ARN that has a version or stage qualifier appended.

For limitations that apply to every provider, see
[Limitations and considerations](/user-guide/external-secret-providers#label-external-secret-providers-limitations).
