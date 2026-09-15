Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_CMK\_CONFIG\_POSTGRES

Returns configuration information for use with customer-managed keys (CMKs) and Snowflake Postgres Tri-Secret Secure.

## Syntax

Amazon Web Services:

Copy code

```
SYSTEM$GET_CMK_CONFIG_POSTGRES()
```

Microsoft Azure:

Copy code

```
SYSTEM$GET_CMK_CONFIG_POSTGRES( '<tenant_id>' )
```

## Arguments

`'tenant_id'`
:   Specifies the unique identifier for the Azure Key Vault
    [tenant](https://docs.microsoft.com/en-us/azure/key-vault/general/basic-concepts) in your Microsoft Azure subscription.

    This value is in the GUID format, such as `b3ddabe4-e5ed-4e71-8827-0cefb99af240`. You can find this value by logging into the Portal
    and navigating to **Key Vault** » **Overview**. Select the **Directory ID** value.

## Returns

The output depends on the cloud platform that hosts your Snowflake account:

- For Amazon Web Services, a snippet of the statement identifier (`Sid`) for the CMK policy:

  ```
  {"Sid": "Allow use of the key by Snowflake","Effect": "Allow","Principal": {"AWS": "my-arn:name/TRISECRETTEST"},"Action": ["kms:Decrypt","kms:GenerateDataKeyWithoutPlaintext"],"Resource": "arn:aws:kms:us-west-2:736112632310:key/ceab36e4-f0e5-4b46-9a78-86e8f17a0f59"},
  ```
- For Microsoft Azure, use the Azure CLI to create service principals in your tenant for Snowflake multi-tenant apps that need to access the CMK:

  ```
  az ad sp create --id appId1
  az ad sp create --id appId2
  ```

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) or a role that is granted the MONITOR SECURITY privilege on the account can call this function.

## Examples

Obtain the configuration information for the CMK for your Snowflake account on Microsoft Azure:

Copy code

```
SELECT SYSTEM$GET_CMK_CONFIG_POSTGRES('b3ddabe4-e5ed-4e71-8827-0cefb99af240');
```
