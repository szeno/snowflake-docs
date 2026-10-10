# SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS

Lists the [workload identity federation](/user-guide/workload-identity-federation) settings for a service user.

See also:
:   [ALTER USER … ADD WORKLOAD IDENTITY](/sql-reference/sql/alter-user-add-workload-identity),
    [ALTER USER … MODIFY WORKLOAD IDENTITY](/sql-reference/sql/alter-user-modify-workload-identity),
    [ALTER USER … REMOVE WORKLOAD IDENTITY](/sql-reference/sql/alter-user-remove-workload-identity)

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
| `name` | Name of the workload identity. The workload identity assigned with the `WORKLOAD_IDENTITY` user property is named `DEFAULT`. |
| `type` | The identity provider that is issuing attestations for the service user. Possible values are:   - `AWS`: AWS Identity and Access Management (AWS IAM) is the identity provider, which indicates the workload is running on AWS. - `AZURE`: Microsoft Entra ID is the identity provider, which indicates the workload is running on Microsoft Azure. - `GCP`: Google Accounts is the identity provider, which indicates the workload is running on Google Cloud. - `OIDC`: An OpenID Connect (OIDC) provider is the identity provider. |
| `comment` | Comment for the workload identity. Empty when no comment is set. You can set a comment on a named workload identity with [ALTER USER … MODIFY WORKLOAD IDENTITY](/sql-reference/sql/alter-user-modify-workload-identity). You can’t set a comment on the `DEFAULT` workload identity with that command. |
| `last_used` | Date and time when this workload identity was last used to authenticate to Snowflake. |
| `created_on` | Date and time when the workload identity was created. |
| `additional_info` | Additional details about how the service user is configured to use workload identity federation. The details depend on the value in the `type` column.   - For `TYPE = 'AWS'`, the column contains an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:    - For the `awsPartition` key, the value is the AWS partition for the federated identity.   - For the `awsAccount` key, the value is the AWS account identifier for the federated identity.   - For the `type` key, the value is the type of the federated identity. This can be `IAM_USER` or `IAM_ROLE`.   - For the `iamRole` key, the value is the name of the federated IAM role or user. - For `TYPE = 'AZURE'`, the column contains an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:    - For the `issuer` key, the value is the Entra ID tenant’s Authority URL.   - For the `subject` key, the value is the Object ID (Principal ID) assigned to the Azure workload that is using a managed identity. - For `TYPE = 'GCP'`, the column contains an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pair:    - For the `subject` key, the value is the `uniqueId` property of the Google Cloud service account associated with the federated workload. - For `TYPE = 'OIDC'`, the column contains an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value with the following key-value pairs:    - For the `issuer` key, the value is the issuer URL of the OpenID Connect (OIDC) provider.   - For the `subject` key, the value is the identifier of the federated workload.   - For the `audienceList` key, the value is the custom audiences that are allowed in an OIDC ID token. An empty value means the default audience `snowflakecomputing.com` is required. |
| `status` | Status of the workload identity. Possible values are `ACTIVE` and `DISABLED`. A disabled workload identity can’t be used to authenticate. You can change the status of a named workload identity with [ALTER USER … MODIFY WORKLOAD IDENTITY](/sql-reference/sql/alter-user-modify-workload-identity). You can’t change the status of the `DEFAULT` workload identity with that command. |

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
