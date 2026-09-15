Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# CREDENTIALS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view provides the credentials used for authentication across each account in your organization. Each row corresponds to a different credential.

This view includes rows for the following types of credentials:

- [Programmatic access tokens](/user-guide/programmatic-access-tokens)
- [Passkeys](/user-guide/security-mfa-second-factor#label-mfa-secondary-methods-passkey)
- [Time-based one-time passcodes (TOTPs)](/user-guide/security-mfa-second-factor#label-mfa-secondary-methods-totp)
- [Workload identity federation](/user-guide/workload-identity-federation)
- [Key pairs](/user-guide/key-pair-auth)

This view doesn’t include credentials that have been deleted.

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column | Data type | Description |
| --- | --- | --- |
| CREDENTIAL\_ID | NUMBER | Internal/system-generated identifier for the credential. |
| NAME | VARCHAR | Name of the credential. |
| USER\_NAME | VARCHAR | Name of the user associated with the credential. |
| TYPE | VARCHAR | Type of the credential. These types include:   - `PASSKEY`: [Passkey](/user-guide/security-mfa-second-factor#label-mfa-secondary-methods-passkey). - `PAT`: [Programmatic access token](/user-guide/programmatic-access-tokens). - `TOTP`: [Time-based one-time passcode](/user-guide/security-mfa-second-factor#label-mfa-secondary-methods-totp). - `AWS`: AWS Identity and Access Management (AWS IAM) is the identity provider, which indicates the workload is running on AWS. See   [Workload identity federation](/user-guide/workload-identity-federation). - `AZURE`: Microsoft Entra ID is the identity provider, which indicates the workload is running on Microsoft Azure. See   [Workload identity federation](/user-guide/workload-identity-federation). - `GCP`: Google Accounts is the identity provider, which indicates the workload is running on Google Cloud. See   [Workload identity federation](/user-guide/workload-identity-federation). - `OIDC`: An OpenID Connect (OIDC) provider is the identity provider. See [Workload identity federation](/user-guide/workload-identity-federation). - `KEYPAIR`: [Key pair](/user-guide/key-pair-auth). |
| DOMAIN | VARCHAR | Domain of the credential. The domains include:   - `MFA_METHOD`: The credential is used as a   [second factor of authentication](/user-guide/security-mfa-second-factor). - `PROGRAMMATIC_ACCESS_TOKEN`: [Programmatic access token](/user-guide/programmatic-access-tokens). - `WORKLOAD_IDENTITY_FEDERATION_METHOD`: [Workload identity federation](/user-guide/workload-identity-federation). - `KEYPAIR`: [Key pair](/user-guide/key-pair-auth).   A given domain can have one or more possible types (specified in the TYPE column). |
| COMMENT | VARCHAR | Comment about the credential. |
| STATUS | VARCHAR | Status of the credential. The status depends on the value in the TYPE column:   - For `TYPE = 'PAT'` ([programmatic access tokens](/user-guide/programmatic-access-tokens)), the status can be one   of the following:   - `ACTIVE`: The programmatic access token can be used to authenticate and has not expired yet. - `EXPIRED`: The programmatic access token cannot be used to authenticate because the expiration date has passed. - `DISABLED`: The programmatic access token is [disabled](/user-guide/programmatic-access-tokens#label-pat-disabled) because user login access is disabled or   the user is locked out of logging in.   - For `TYPE = 'KEYPAIR'` ([key pairs](/user-guide/key-pair-auth)), the status can be one of the following:   - `ACTIVE`: The key pair can be used for authentication. - `EXPIRED`: The key pair has passed its expiration time and cannot be used for authentication. - `DISABLED`: The key pair has been explicitly disabled and cannot be used for authentication.   If a key pair is both disabled and past its expiration time, the status is reported as `DISABLED`.   - For other types of credentials, the status can be one of the following:   - `PENDING`: The user started the enrollment process for an MFA method but has not completed the process. For example,     the user started registering an authenticator but never finished the setup process for the authenticator. As a result,     the MFA method is not considered to be valid yet.   - `ENROLLED`: The user has completed the enrollment process for the MFA method, and the MFA method can be used for     second-factor authentication. |
| ADDITIONAL\_DETAILS | OBJECT | Additional details about the credential. The additional details depend on the type of the credential (the value in the TYPE column):   - For `TYPE = 'PAT'` ([programmatic access tokens](/user-guide/programmatic-access-tokens)), the column contains   an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:   - For the `MINS_TO_BYPASS_NETWORK_POLICY_REQUIREMENT` key, the value is an integer representing the number of minutes     during which the [requirement of having a network policy](/user-guide/programmatic-access-tokens#label-pat-prerequisites-network) is bypassed. You can     specify this value when [generating the token](/user-guide/programmatic-access-tokens#label-pat-generate).   - For the `ROLE_RESTRICTION` key, the value is an array of the roles that are used for privilege evaluation and     object creation during the session authenticated with this token. You can specify these roles when     [generating the token](/user-guide/programmatic-access-tokens#label-pat-generate).   - For the `ROTATED_TO` key, the value is the name of the newer token that this token was replaced by during     [rotation](/user-guide/programmatic-access-tokens#label-pat-rotate).   These key-value pairs are present only if the corresponding properties are set in the token. For example:  Copy code  ``` {   "MINS_TO_BYPASS_NETWORK_POLICY_REQUIREMENT": 60,   "ROLE_RESTRICTION": ["MY_ROLE"],   "ROTATED_TO": "MY_PAT_NAME" } ```  If none of these are specified for the token, the column contains an empty object (`{}`).   - For `TYPE = 'PASSKEY'` ([passkey](/user-guide/security-mfa-second-factor#label-mfa-secondary-methods-passkey)), the column contains   an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the key-value pair `aaguid`. For example:   Copy code  ``` {   "aaguid": "a12345678-..." } ```   - For `TYPE = 'TOTP'` ([time-based one-time passcode](/user-guide/security-mfa-second-factor#label-mfa-secondary-methods-totp)), the column contains NULL. - For `TYPE = 'AWS'` ([workload identity federation](/user-guide/workload-identity-federation)), the column contains   an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:    - For the `aws_partition` key, the value is the AWS partition for the federated identity.   - For the `aws_account` key, the value is the AWS account identifier for the federated identity.   - For the `type` key, the value is the type of the federated identity. This can be `IAM_USER` or `IAM_ROLE`.   - For the `iam_role` key, the value is the name of the federated IAM role or user. - For `TYPE = 'AZURE'` ([workload identity federation](/user-guide/workload-identity-federation)), the column contains   an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:    - For the `issuer` key, the value is the Entra ID tenant’s Authority URL.   - For the `subject` key, the value is the Object ID (Principal ID) assigned to the Azure workload that is using a     managed identity. - For `TYPE = 'GCP'` ([workload identity federation](/user-guide/workload-identity-federation)), the column contains   an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:    - For the `subject` key, the value is the `uniqueId` property of the Google Cloud service account associated with the     federated workload. - For `TYPE = 'OIDC'` ([workload identity federation](/user-guide/workload-identity-federation)), the column contains   an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:    - For the `issuer` key, the value is the issuer URL of the OpenID Connect (OIDC) provider.   - For the `subject` key, the value is the identifier of the federated workload.   - For the `audience_list` key, the value is the custom audiences that are allowed in an OIDC ID token. An empty value means     the default audience `snowflakecomputing.com` is required. - For `TYPE = 'KEYPAIR'` ([key pair](/user-guide/key-pair-auth)), the column contains   an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:    - For the `KEY_TYPE` key, the value is the algorithm of the key pair (for example, `RSA`).   - For the `PUBLIC_KEY_FP` key, the value is the SHA-256 fingerprint of the public key. |
| CREATED\_BY | VARCHAR | Name of the user who created the credential. |
| LAST\_ALTERED\_BY | VARCHAR | Name of the user who last modified the credential. |
| CREATED\_ON | TIMESTAMP\_LTZ | Date and time when the credential was created. |
| LAST\_USED\_ON | TIMESTAMP\_LTZ | Date and time when the credential was last used for authentication. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the credential was last modified. |
| EXPIRATION\_DATE | TIMESTAMP\_LTZ | Date and time when the credential expires. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- If a programmatic access token is generated soon after a user is created, the information about that user in this view might
  be incomplete. It might take some time for the user information to be included in the view.
