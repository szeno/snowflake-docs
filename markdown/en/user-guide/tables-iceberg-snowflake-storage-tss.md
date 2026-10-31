# Tri-Secret Secure for Snowflake storage for Apache Iceberg™ tables

[Business Critical Feature](/user-guide/intro-editions)

Requires Business Critical Edition (or higher). To ask about upgrading, please contact
[Snowflake Support](/user-guide/contacting-support).

Note

Tri-Secret Secure for Snowflake storage for Iceberg tables is available for Snowflake accounts hosted on AWS or Microsoft Azure. This feature isn’t enabled by
default. To enable it for your account, contact [Snowflake Support](/user-guide/contacting-support).

[Tri-Secret Secure](/user-guide/security-encryption-tss) is supported for [Snowflake storage for Iceberg tables](/user-guide/tables-iceberg-internal-storage). Tri-Secret Secure for Snowflake storage for Iceberg tables uses a self-service registration process similar to that outlined in [Tri-Secret Secure self-service in Snowflake](/user-guide/security-encryption-tss-self-serve), with the following differences:

- Tri-Secret Secure for Snowflake storage for Iceberg tables uses dedicated Snowflake system functions for CMK registration and activation.
- Tri-Secret Secure for Snowflake storage for Iceberg tables doesn’t require a waiting period before activation.
- Tri-Secret Secure for Snowflake storage for Iceberg tables doesn’t send email notifications on registration or activation.
- Tri-Secret Secure for Snowflake storage for Iceberg tables doesn’t rekey existing data when a CMK is activated or changed.
- Tri-Secret Secure for Snowflake storage for Iceberg tables doesn’t support private connectivity for CMK access. This doesn’t affect private connectivity to the Snowflake-managed storage volume itself, which you can reach through AWS VPC interface endpoints. For more information, see [AWS VPC interface endpoints for Snowflake-managed storage volumes](/user-guide/private-managed-volumes-aws).

## Key lifecycle and rekeying

Tri-Secret Secure for Snowflake storage for Iceberg tables encrypts each object on your Snowflake-managed storage volume with the CMK that’s active when the object is written. Snowflake doesn’t re-encrypt data that’s already on the volume, so the volume can hold data under several keys at once:

- Data written before you activated any CMK stays under Snowflake-managed encryption.
- Data written while a CMK was active stays encrypted under that CMK until it’s overwritten or migrated, even after you activate a different key or deactivate the feature.
- Only data written after you activate a CMK uses that CMK.

Warning

You can rotate keys as often as your security policy requires, but you must keep every CMK you’ve activated available in AWS KMS for as long as you need to read the data written under it. Activating a new key doesn’t let you retire the old one. Revoking, disabling, or deleting a CMK makes the data written under it unreadable.

This is the main behavioral difference from Tri-Secret Secure for Snowflake native tables, which rekeys your existing data when you change the CMK.

Attention

Before engaging with Snowflake to enable Tri-Secret Secure for Snowflake storage for Iceberg tables for your account, you should carefully consider your responsibility for
safeguarding your key as mentioned in [Customer-managed keys](/user-guide/security-encryption-manage#label-customer-managed-keys). If the customer-managed key (CMK) in the composite master key
hierarchy is revoked, your data can no longer be decrypted by Snowflake.

If you have any questions or concerns, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Snowflake also bears the same responsibility for the keys that we maintain. As with all security-related aspects of our service, we treat
this responsibility with the utmost care and vigilance.

All of our keys are maintained under strict policies that have enabled us to earn the highest security accreditations, including SOC 2
Type II, PCI-DSS, HIPAA and [HITRUST CSF](/user-guide/intro-cloud-platforms#label-hitrust-csf-cert).

## Activate Tri-Secret Secure for Snowflake storage for Iceberg tables

This procedure works on AWS and Azure. Steps taken on the cloud provider platform differ by provider, as noted in each step.

To create and register your CMK, and then activate Tri-Secret Secure for Snowflake storage for Iceberg tables, complete the following steps:

1. On the cloud provider, create a CMK.

   Do this step in the key management service on the cloud platform that hosts your Snowflake account:

   - **AWS:** Create a symmetric encryption key in AWS Key Management Service (KMS). The key must be in the same AWS region as your Snowflake account.
   - **Azure:** Create an RSA key (2048, 3072, or 4096 bits) in an Azure Key Vault that has soft delete and purge protection enabled.

   Use a key that’s dedicated to Tri-Secret Secure for Snowflake storage for Iceberg tables. You can’t use a key that’s used by Tri-Secret Secure on your Snowflake account or by Snowflake Postgres Tri-Secret Secure.
2. In Snowflake, call the [SYSTEM$REGISTER\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_register_cmk_info_snowflake_managed_volume) system function.

   The arguments depend on the cloud platform that hosts your Snowflake account:

   - **AWS:** Pass the ARN of the KMS key. The function accepts both `key/<uuid>` and `alias/<name>` ARN formats.

     Copy code

     ```
     SELECT SYSTEM$REGISTER_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME('<cmk_arn>');
     ```
   - **Azure:** Pass the URI of your Key Vault and the name of your key. Don’t include a key version.

     Copy code

     ```
     SELECT SYSTEM$REGISTER_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME('<vault_uri>', '<key_name>');
     ```

   This function records your CMK but doesn’t apply it to storage yet, so calling it doesn’t affect active Iceberg table reads or writes.
3. In Snowflake, call the [SYSTEM$GET\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_get_cmk_info_snowflake_managed_volume) system function.

   Copy code

   ```
   SELECT SYSTEM$GET_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME();
   ```

   Confirm the output includes `is pre-registered` before continuing.
4. In Snowflake, call the [SYSTEM$GET\_CMK\_CONFIG\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_get_cmk_config_snowflake_managed_volume) system function.

   Copy code

   ```
   SELECT SYSTEM$GET_CMK_CONFIG_SNOWFLAKE_MANAGED_VOLUME();
   ```

   This function generates the information your cloud provider needs to allow Snowflake to access your CMK. The output depends on the
   cloud platform that hosts your Snowflake account:

   - **AWS:** A KMS key-policy statement that grants Snowflake the permissions it needs to use your CMK. The `Principal.AWS` value in the
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
   - **Azure:** An Azure CLI command that creates a service principal for Snowflake in your Azure tenant. For example:

     ```
     az ad sp create --id 3f8a2c1d-7b4e-4f9a-a6d2-5e1c9b0f7a34
     ```

   Important

   Call the function to get the values for your account. Don’t copy the principal ARN or application ID from these examples.
5. On your cloud provider platform, use the output of `SYSTEM$GET_CMK_CONFIG_SNOWFLAKE_MANAGED_VOLUME` to authorize your CMK.

   - **AWS:** Open the KMS key policy in the AWS Management Console and add the statement returned in step 4.
   - **Azure:** Run the command returned in step 4 in the tenant that contains your Key Vault. Then grant the service principal the
     following permissions on your key:

     - `Microsoft.KeyVault/vaults/keys/read`
     - `Microsoft.KeyVault/vaults/keys/wrap/action`
     - `Microsoft.KeyVault/vaults/keys/unwrap/action`
6. In Snowflake, call the [SYSTEM$VERIFY\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_verify_cmk_info_snowflake_managed_volume) system function.

   Copy code

   ```
   SELECT SYSTEM$VERIFY_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME();
   ```

   This function confirms that Snowflake can reach your CMK. It returns a descriptive string rather than raising an error when verification fails, so you must read the output before continuing.

   Successful output begins: `CMK verification successful for Snowflake-managed storage.`

   If verification fails, review the configuration you applied in step 5 and call the function again.
7. In Snowflake, call the [SYSTEM$ACTIVATE\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_activate_cmk_info_snowflake_managed_volume) system function.

   Copy code

   ```
   SELECT SYSTEM$ACTIVATE_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME();
   ```

   This function sets your CMK as the default encryption key on your account’s Snowflake-managed storage volume. Activation is immediate. All data written to the volume after activation uses your CMK.

   Important

   Activation isn’t retroactive. Iceberg table data written before activation isn’t re-encrypted under the new key. For more information, see [Key lifecycle and rekeying](#label-key-lifecycle-snowflake-storage-tss).

## View the status of your CMK

You can call [SYSTEM$GET\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_get_cmk_info_snowflake_managed_volume) at any time to check the registration and activation status of your CMK.

Copy code

```
SELECT SYSTEM$GET_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME();
```

The function returns one of the following messages:

- `CMK info has not been pre-registered in this account yet.`: no CMK is registered or active.
- `CMK with <identifier> is pre-registered for Snowflake-managed storage.`: a CMK is registered but not yet activated.
- `CMK with <identifier> is activated for Snowflake-managed storage.`: a CMK is active.
- `CMK with <identifier> is active and another <identifier> is pre-registered for Snowflake-managed storage.`: a CMK is active and a different CMK is registered for an upcoming key change.

## Change the CMK

To replace your active CMK, use the same steps you followed to register and activate the initial key. When you activate the new key, it replaces the currently active key.

If a key is already in the registered slot, registration fails and directs you to deregister that key first. See [Deregister your current CMK](#label-deregister-cmk-snowflake-storage-tss).

Warning

Keep the previous CMK available in AWS KMS as long as you need to read data written under it. For more information, see [Key lifecycle and rekeying](#label-key-lifecycle-snowflake-storage-tss).

## Deactivate Tri-Secret Secure for Snowflake storage for Iceberg tables

To revert your Snowflake-managed storage volume to Snowflake-managed encryption, call [SYSTEM$DEACTIVATE\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_deactivate_cmk_info_snowflake_managed_volume).

Copy code

```
SELECT SYSTEM$DEACTIVATE_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME();
```

Warning

Data written while the CMK was active stays encrypted under that key after deactivation. Keep the key available in AWS KMS for as long as you need to read that data.

## Deregister your current CMK

You can register only one CMK at a time. If [SYSTEM$REGISTER\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_register_cmk_info_snowflake_managed_volume) fails because a different CMK is already registered, call [SYSTEM$DEREGISTER\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_deregister_cmk_info_snowflake_managed_volume) to remove it.

Copy code

```
SELECT SYSTEM$DEREGISTER_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME();
```

Deregistering removes the CMK from the registered slot. It doesn’t deactivate a key that’s already active, and it doesn’t affect data encrypted under any active or previously active key.

## Limitations and considerations

- Tri-Secret Secure for Snowflake storage for Iceberg tables isn’t available in government regions or in the People’s Republic of China.
- You can register one CMK and have one active CMK per account at a time.
- The CMK for Tri-Secret Secure for Snowflake storage for Iceberg tables must be unique. You can’t use the same key for Tri-Secret Secure on your Snowflake account or for Snowflake Postgres Tri-Secret Secure. Registration and activation fail if the key is already used by either feature.
- Both the failsafe and non-failsafe Snowflake-managed storage volumes in your account use the same CMK. You can’t configure them independently.
- Snowflake doesn’t rekey existing data. For details on what this means for key retention, see [Key lifecycle and rekeying](#label-key-lifecycle-snowflake-storage-tss).
