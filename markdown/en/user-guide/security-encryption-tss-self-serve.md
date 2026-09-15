# Tri-Secret Secure self-service in Snowflake

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Tri-Secret Secure overview

Using a dual-key encryption model together with Snowflake’s built-in user authentication enables three levels of data protection, known as
*Tri-Secret Secure*. Tri-Secret Secure offers you a level of security and control above Snowflake’s standard encryption.

Our dual-key encryption model combines a Snowflake-maintained key and a customer-managed key (CMK), which you create on the cloud provider
platform that hosts your Snowflake account. The model creates a composite master key that protects your Snowflake data. This composite master key
acts as an account master key by wrapping all of the keys in your account hierarchy. The composite master key is never used to encrypt raw data.
For example, the composite master key wraps table master keys, which are used to derive file keys that encrypt the raw data.

Attention

Before enabling Tri-Secret Secure
for your account, you should carefully consider your responsibility for safeguarding your key as mentioned in [Customer-managed keys](/user-guide/security-encryption-manage#label-customer-managed-keys).
If the CMK in the composite master key hierarchy is revoked, your data can no longer be decrypted by Snowflake.

If you have any questions or concerns, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Snowflake also bears the same responsibility for the keys that we maintain. As with all security-related aspects of our service, we treat
this responsibility with the utmost care and vigilance.

All of our keys are maintained under strict policies that have enabled us to earn the highest security accreditations, including SOC 2
Type II, PCI-DSS, HIPAA and [HITRUST CSF](/user-guide/intro-cloud-platforms#label-hitrust-csf-cert).

### Tri-Secret Secure compatibility with hybrid tables

You must enable Dedicated Storage Mode if you intend to create hybrid tables in your account and TSS is already enabled or
will be enabled. For information, see [Hybrid Tables Dedicated Storage Mode for TSS](/user-guide/tables-hybrid-dedicated-storage-mode).

### Understanding Tri-Secret Secure self-service

You can use Snowflake system functions to first register a CMK and then activate Tri-Secret Secure to use the CMK.
If you decide to replace a CMK for use with Tri-Secret Secure, the SYSTEM$GET\_CMK\_INFO function informs you whether your new
CMK is registered and activated. You can continue to use your account during the rekeying process.

Tri-Secret Secure self-service provides the following benefits to you:

- Facilitates working with the key management service (KMS) in the cloud platform that hosts your Snowflake account.
- Streamlines the steps to register and authorize your CMK.
- Provides transparency to your CMK registration and Tri-Secret Secure activation status.
- Enables you to manage Tri-Secret Secure without any downtime of your Snowflake account.

## Activate Tri-Secret Secure

This procedure works on all cloud provider platforms that Snowflake supports. See your specific cloud provider documentation for any steps
taken on the cloud provider platform.

To create and register your CMK, and then activate Tri-Secret Secure, complete the following steps:

1. On the cloud provider, create a CMK.

   Do this step in the key management service (KMS) on the cloud platform that hosts your Snowflake account.
2. In Snowflake, call the [SYSTEM$REGISTER\_CMK\_INFO](/sql-reference/functions/system_register_cmk_info) system function.

   - This system function registers your CMK with your Snowflake account.
   - Double-check the system function arguments to make sure they are correct for the cloud platform that hosts your Snowflake account.
   - When you call the SYSTEM$REGISTER\_CMK\_INFO function, Snowflake sends an email message to account administrators who have a validated email
     address. The message notifies the account administrator when to call the SYSTEM$ACTIVATE\_CMK\_INFO function to activate Tri-Secret Secure.

   Important

   You must wait 72 hours before activating Tri-Secret Secure (step 7). If you attempt to activate Tri-Secret Secure during this waiting
   period, you see an error message that advises you to wait.
3. In Snowflake, call the [SYSTEM$GET\_CMK\_INFO](/sql-reference/functions/system_get_cmk_info) system function.

   This system function returns the registration status and details for the CMK that you registered.
4. In Snowflake, call the [SYSTEM$GET\_CMK\_CONFIG](/sql-reference/functions/system_get_cmk_config) system function.

   This system function generates the information required for your cloud provider to allow Snowflake to access your CMK.

   Note

   If Microsoft Azure hosts your Snowflake account, you must pass the `tenant_id` value into the function.
5. On your cloud provider platform, use the output of the SYSTEM$GET\_CMK\_CONFIG function to authorize your CMK.
6. In Snowflake, call the [SYSTEM$VERIFY\_CMK\_INFO](/sql-reference/functions/system_verify_cmk_info) system function.

   This system function confirms connectivity between your Snowflake account and your CMK.
7. In Snowflake, call the [SYSTEM$ACTIVATE\_CMK\_INFO](/sql-reference/functions/system_activate_cmk_info) system function.

   This system function activates Tri-Secret Secure with your registered CMK. This system function starts the rekeying process and
   generates an email message that notifies system administrators when the process finishes. The rekeying process can complete in under an
   hour, but might require up to 24 hours.

   Warning

   Snowflake uses the old CMK until the rekeying process completes. Do not remove access to the old CMK until receiving email notification
   that the rekeying process completed.

To enable private connectivity for a CMK already activated with Tri-Secret Secure, see [Enable a private connectivity endpoint for an active CMK](/user-guide/security-encryption-tss-self-serve-private#label-tss-enable-pl-for-active-cmk).

## View the status of your CMK

You can call [SYSTEM$GET\_CMK\_INFO](/sql-reference/functions/system_get_cmk_info) at any time, to check the registration and activation status of your CMK.

For example, depending on when you call SYSTEM$GET\_CMK\_INFO, the function returns the following output:

- Immediately after activating Tri-Secret Secure, returns `...is being activated...`. This means that rekeying isn’t complete.
- After the Tri-Secret Secure activation process completes, returns output that includes `...is activated...`. This means that your
  Snowflake account is using Tri-Secret Secure with the CMK that you registered.

## Change the CMK for Tri-Secret Secure

Snowflake system functions support changing your customer-managed key (CMK), based on your security needs. Use the same steps to register a new CMK as the
steps that you followed to register your initial CMK. When you complete those steps again by using a new key, the output of the system functions
differs. Read the output from each system function that you call during self-registration to confirm that you have changed your key. For
example, when you change your CMK, calling the SYSTEM$GET\_CMK\_INFO function returns a message that contains `...is being rekeyed...`.

## Use Tri-Secret Secure self-service with automatic key rotation

If you use your cloud provider’s automatic key rotation feature to maintain the lifecycle of your customer-managed keys (CMKs), you can rekey with
the latest version of your CMK by calling the SYSTEM$ACTIVATE\_CMK\_INFO function and providing the `'REKEY_SAME_CMK'` argument.

For more information, see [Customer-managed keys](/user-guide/security-encryption-manage#label-customer-managed-keys).

## Deactivate Tri-Secret Secure

To deactivate Tri-Secret Secure in your account, call the [SYSTEM$DEACTIVATE\_CMK\_INFO](/sql-reference/functions/system_deactivate_cmk_info) system function.

## Deregister your current CMK

You can only register one CMK at a time with Tri-Secret Secure. When you register your CMK, if the [SYSTEM$REGISTER\_CMK\_INFO](/sql-reference/functions/system_register_cmk_info)
function fails because a different CMK exists, call the [SYSTEM$DEREGISTER\_CMK\_INFO](/sql-reference/functions/system_deregister_cmk_info) system function, as prompted.

## Integrate Tri-Secret Secure with AWS external key stores

Snowflake supports integrating Tri-Secret Secure with AWS external key stores to securely store and manage a customer-managed
key outside AWS. Snowflake officially tests and supports only Thales Hardware Security Modules (HSM) and Thales CipherTrust Cloud Key Manager (CCKM) data encryption products.

For more information about setting up and configuring Tri-Secret Secure with Thales solutions, see [How to use Thales External Key Store for Tri-Secret Secure on an AWS Snowflake account](https://community.snowflake.com/s/article/thales-xks-for-tss-aws#e3).
