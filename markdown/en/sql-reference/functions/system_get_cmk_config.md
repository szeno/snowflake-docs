Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_CMK\_CONFIG

Returns configuration information for use with customer-managed keys (CMKs) and Tri-Secret Secure.

See also:
:   [Understanding CMK self-registration with support activation of Tri-Secret Secure](/user-guide/security-encryption-tss#label-encryption-tss-self-register)

## Syntax

Amazon Web Services and Google Cloud Platform:

Copy code

```
SYSTEM$GET_CMK_CONFIG()
```

Microsoft Azure:

Copy code

```
SYSTEM$GET_CMK_CONFIG( '<tenant_id>' )
```

## Arguments

`tenant_id`
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
- For Microsoft Azure, a consent URL and the name of the Snowflake service principal:

  ```
  Consent url is: https://login.microsoftonline.com/tenantId/oauth2/authorize?client_id=c03edcfb-19f9-435f-92fa-e8ec9e24f40e&response_type=code and Snowflake Service Principal name is: trisec_cmk_azure"
  ```
- For Google Cloud Platform, a gcloud command:

  ```
  gcloud kms keys add-iam-policy-binding TriSecretGCPKey --project my-env --location us-west1 --keyring TriSecretTest --member serviceAccount:site-trisecret@my-env.iam.serviceaccount.com --role roles/cloudkms.cryptoKeyEncrypterDecrypter
  ```

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) or a role that is granted the MONITOR SECURITY privilege can call this function.

## Examples

Obtain the configuration information for the CMK for your Snowflake account on Microsoft Azure:

> Copy code
>
> ```
> SELECT SYSTEM$GET_CMK_CONFIG('b3ddabe4-e5ed-4e71-8827-0cefb99af240');
> ```
