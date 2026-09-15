# SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS

Lists the [workload identity federation](/user-guide/workload-identity-federation) settings for a service user.

## Syntax

Copy code

```
SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS [ FOR USER <username> ]
```

## Parameters

`FOR USER username`
:   > Lists the workload identity federation settings for the specified user.

    If no user is specified, the command lists the settings for the current user.

## Output

| Column | Description |
| --- | --- |
| `name` | Name of the service user. |
| `type` | The identity provider that is issuing attestations for the service user. Possible values are:   - `AWS`: AWS Identity and Access Management (AWS IAM) is the identity provider, which indicates the workload is running on AWS. - `AZURE`: Microsoft Entra ID is the identity provider, which indicates the workload is running on Microsoft Azure. - `GCP`: Google Accounts is the identity provider, which indicates the workload is running on Google Cloud. - `OIDC`: An OpenID Connect (OIDC) provider is the identity provider. |
| `comment` | Reserved for future use. |
| `last_used` | Date and time that the service user last used workload identity federation to authenticate to Snowflake. |
| `created_on` | Date and time that someone ran a CREATE USER or ALTER USER command to set the `WORKLOAD_IDENTITY` parameter. |
| `additional_info` | Additional details about how the service user is configured to use workload identity federation. The details depend on the value in the `type` column.   - For `TYPE = 'AWS'`, the column contains an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:    - For the `awsPartition` key, the value is the AWS partition for the federated identity.   - For the `awsAccount` key, the value is the AWS account identifier for the federated identity.   - For the `type` key, the value is the type of the federated identity. This can be `IAM_USER` or `IAM_ROLE`.   - For the `iamRole` key, the value is the name of the federated IAM role or user. - For `TYPE = 'AZURE'`, the column contains an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:    - For the `issuer` key, the value is the Entra ID tenant’s Authority URL.   - For the `subject` key, the value is the Object ID (Principal ID) assigned to the Azure workload that is using a managed identity. - For `TYPE = 'GCP'`, the column contains an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pair:    - For the `subject` key, the value is the `uniqueId` property of the Google Cloud service account associated with the federated workload. - For `TYPE = 'OIDC'`, the column contains an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:    - For the `issuer` key, the value is the issuer URL of the OpenID Connect (OIDC) provider.   - For the `subject` key, the value is the identifier of the federated workload.   - For the `audienceList` key, the value is the custom audiences that are allowed in an OIDC ID token. An empty value means the default audience `snowflakecomputing.com` is required. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| MONITOR | User | Required only when displaying workload identity federation settings for a different service user. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Show workload identity authentication settings for the user `example_service_user`:

Copy code

```
SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS FOR USER example_service_user;
```
