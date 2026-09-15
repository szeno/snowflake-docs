Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_GCP\_KMS\_CMK\_GRANT\_ACCESS\_CMD

Returns a Google Cloud gcloud command to obtain policy information for the Google Cloud Key Management Service for use with
customer-managed keys.

You can use the policy information for your customer-managed keys with [Tri-Secret Secure](/user-guide/security-encryption-tss) for Snowflake accounts on Google Cloud
Platform.

See also:
:   [Understanding Encryption Key Management in Snowflake](/user-guide/security-encryption-manage)

## Syntax

> Copy code
>
> ```
> SYSTEM$GET_GCP_KMS_CMK_GRANT_ACCESS_CMD()
> ```

## Arguments

None.

## Usage notes

- This function is for use in Snowflake accounts on Google Cloud Platform only.
- Only account administrators (i.e. users with the ACCOUNTADMIN role) or a role that is granted the MONITOR SECURITY privilege can call
  this function.

## Examples

Return the gcloud command to obtain GCP KMS policy information for customer-managed keys. Note that the example
gcloud command does not contain real option values, some of which are replaced by angle brackets.

For details about the gcloud command, see the documentation for [gcloud kms](https://cloud.google.com/sdk/gcloud/reference/kms).

> Copy code
>
> ```
> select SYSTEM$GET_GCP_KMS_CMK_GRANT_ACCESS_CMD();
> ```

Returns:

> Copy code
>
> ```
> gcloud kms keys add-iam-policy-binding <key-name> --project <project-id> --location <location> --keyring <key-ring> --member serviceAccount:<service-account-email> --role roles/cloudkms.cryptoKeyEncrypterDecrypter
> ```
