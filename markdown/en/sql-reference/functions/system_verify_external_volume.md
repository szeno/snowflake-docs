Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$VERIFY\_EXTERNAL\_VOLUME

Verifies the configuration for a specified [external volume](/user-guide/tables-iceberg-configure-external-volume).

For external volumes with write access, Snowflake attempts the following additional operations to verify the configuration:

- Write a test file.
- Read the test file.
- List the files in the storage location.
- Delete the test file.

See also:
:   [Storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-storage) , [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume) , [CREATE EXTERNAL VOLUME](/sql-reference/sql/create-external-volume)

## Syntax

Copy code

```
SYSTEM$VERIFY_EXTERNAL_VOLUME('<external_volume_name>')
```

## Arguments

`external_volume_name`
:   Name of the external volume to verify. If the identifier contains spaces or special characters,
    the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case sensitive.

## Returns

The function returns a JSON object with the properties described below:

| Property | Description |
| --- | --- |
| `success` | The status of the verification test. Returns `TRUE` if all actions finished; returns `FALSE` if any action didn’t finish as expected. |
| `storageLocationSelectionResult` | The [result](#label-system-verify-external-volume-result-options) of selecting an [active storage location](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-ext-vol-active-storage-location) for the external volume. Returns `TRUE` if Snowflake can successfully select an active location; otherwise, returns `FALSE`. |
| `storageLocationName` | The name of the active storage location. |
| `servicePrincipalProperties` | The properties of the Snowflake service principal for the cloud provider of the active storage location. |
| `location` | The `BASE_URL` of the active storage location. |
| `storageAccount` | For Azure, the storage account of the active storage location. |
| `region` | The region of the active storage location. |
| `writeResult` | The [result](#label-system-verify-external-volume-result-options) of writing a test file to the active storage location. Skipped for read-only external volumes. |
| `readResult` | The [result](#label-system-verify-external-volume-result-options) of reading a test file from the active storage location. Skipped for read-only external volumes. |
| `listResult` | The [result](#label-system-verify-external-volume-result-options) of listing the contents of the active storage location. Skipped for read-only external volumes. |
| `deleteResult` | The [result](#label-system-verify-external-volume-result-options) of deleting a test file written to the active storage location. Skipped for read-only external volumes. |
| `awsRoleArnValidationResult` | For Amazon S3, returns the [result](#label-system-verify-external-volume-result-options) of validating the Amazon Resource Name (ARN) for the IAM role used by the external volume. |
| `azureGetUserDelegationKeyResult` | For Azure, returns the [result](#label-system-verify-external-volume-result-options) of getting a user delegation key. |

Expand

Show lessSee more

### Result values

Return properties that indicate a result can have the following values:

| Result value | Description |
| --- | --- |
| `PASSED` | The operation succeeded. |
| `SKIPPED` | The operation isn’t applicable for the specified external volume. For example, the read, write, list, and delete operations are skipped for read-only external volumes. |
| `<error_message>` | A detailed error message. |

Expand

Show lessSee more

### Example output

Copy code

```
{
  "success": true,
  "storageLocationSelectionResult": "PASSED",
  "storageLocationName": "my-azure-westus-1",
  "servicePrincipalProperties": "AZURE_MULTI_TENANT_APP_NAME: powerful-azure-ad-auth-test-snowflake-app_...; AZURE_CONSENT_URL: https://login.microsoftonline.com...",
  "location": "azure://myStorageAccount.blob.core.windows.net/myStorageLocation/",
  "storageAccount": "myStorageAccount",
  "region": "westus",
  "writeResult": "PASSED",
  "readResult": "PASSED",
  "listResult": "PASSED",
  "deleteResult": "PASSED",
  "awsRoleArnValidationResult": "SKIPPED",
  "azureGetUserDelegationKeyResult": "PASSED"
}
```

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | External volume |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- For Amazon S3 external volumes:

  If you receive the following error, your account administrator must activate AWS STS in the Snowflake deployment region.
  For instructions, see
  [Manage AWS STS in an AWS Region](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html)
  in the AWS documentation.

  ```
  Error assuming AWS_ROLE:
  STS is not activated in this region for account:<external volume id>. Your account administrator can activate STS in this region using the IAM Console.
  ```

## Examples

Verify an external volume named `my_s3_external_volume`:

Copy code

```
SELECT SYSTEM$VERIFY_EXTERNAL_VOLUME('my_s3_external_volume');
```
