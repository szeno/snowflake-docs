Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_CMK\_CONFIG\_SNOWFLAKE\_MANAGED\_VOLUME

Returns the cloud-provider configuration you need to authorize Snowflake to use your customer-managed key (CMK) with
Tri-Secret Secure for Snowflake storage for Iceberg tables. On AWS, this is a KMS key-policy statement. On Microsoft Azure, this is an Azure CLI command to create a service principal in your tenant.

See also:
:   [Tri-Secret Secure for Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-snowflake-storage-tss)

## Syntax

Copy code

```
SYSTEM$GET_CMK_CONFIG_SNOWFLAKE_MANAGED_VOLUME()
```

## Arguments

None.

## Returns

For AWS, returns a KMS key-policy statement that grants Snowflake the permissions it needs to use your CMK. The `Principal.AWS` value in the
returned statement is specific to your Snowflake account. For example:

Copy code

```
{
  "Sid": "Allow Snowflake managed storage to use the key",
  "Effect": "Allow",
  "Principal": { "AWS": "arn:aws:iam::123456789012:user/snowflake-stage-user" },
  "Action": [ "kms:Decrypt", "kms:GenerateDataKey" ],
  "Resource": "*"
}
```

Important

Call the function to get the ARN for your account. Don’t copy the principal ARN from the preceding example.

For Microsoft Azure, returns an Azure CLI command that creates a service principal for Snowflake in your Azure tenant. For example:

```
az ad sp create --id 3f8a2c1d-7b4e-4f9a-a6d2-5e1c9b0f7a34
```

Important

Call the function to get the application ID for your account. Don’t copy the application ID from the preceding example.

After you run the command, grant the service principal the following permissions on your key:

- `Microsoft.KeyVault/vaults/keys/read`
- `Microsoft.KeyVault/vaults/keys/wrap/action`
- `Microsoft.KeyVault/vaults/keys/unwrap/action`

For details, see [Activate Tri-Secret Secure for Snowflake storage for Iceberg tables](/user-guide/tables-iceberg-snowflake-storage-tss#label-activate-snowflake-storage-tss).

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Usage notes

You must register a CMK with [SYSTEM$REGISTER\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_register_cmk_info_snowflake_managed_volume) before calling this function.

## Examples

Obtain the cloud-provider configuration for the CMK registered on your Snowflake account:

Copy code

```
SELECT SYSTEM$GET_CMK_CONFIG_SNOWFLAKE_MANAGED_VOLUME();
```
