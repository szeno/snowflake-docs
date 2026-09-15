# Tri-Secret Secure in Snowflake

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

Before engaging with Snowflake to enable Tri-Secret Secure for your account, you should carefully consider your responsibility for
safeguarding your key as mentioned in [Customer-managed keys](/user-guide/security-encryption-manage#label-customer-managed-keys). If the customer-managed key (CMK) in the composite master key
hierarchy is revoked, your data can no longer be decrypted by Snowflake.

If you have any questions or concerns, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Snowflake also bears the same responsibility for the keys that we maintain. As with all security-related aspects of our service, we treat
this responsibility with the utmost care and vigilance.

All of our keys are maintained under strict policies that have enabled us to earn the highest security accreditations, including SOC 2
Type II, PCI-DSS, HIPAA and [HITRUST CSF](/user-guide/intro-cloud-platforms#label-hitrust-csf-cert).

### Tri-Secret Secure compatibility with hybrid tables

You must enable Dedicated Storage Mode if you intend to create hybrid tables in your account and TSS is already enabled or
will be enabled. For information, see [Hybrid Tables Dedicated Storage Mode for TSS](/user-guide/tables-hybrid-dedicated-storage-mode).

### Understanding CMK self-registration with support activation of Tri-Secret Secure

You can register a CMK for use with Tri-Secret Secure using Snowflake system functions. If you
decide to replace a CMK for use with Tri-Secret Secure, the SYSTEM$GET\_CMK\_INFO function informs you whether your new CMK is registered and
activated. After you self-register your CMK, you can contact Snowflake Support to enable your Snowflake account to use
Tri-Secret Secure with your CMK.

CMK self-registration with support activation provides the following benefits to you:

- Streamlines the steps to register and authorize your CMK.
- Provides transparency to the status of your CMK registration and activation with Tri-Secret Secure.
- Facilitates working with the key management service (KMS) in the cloud platform that hosts your Snowflake account.
- Enables you to rotate your CMK and register the new CMK for use with Tri-Secret Secure.

The following list shows how CMK self-registration with support activation works:

1. As the customer, you do the following actions:

   1. Create the CMK.
   2. Register the CMK.
   3. Generate information for the cloud provider.
   4. Apply the KMS policy.
   5. Confirm the connectivity between your Snowflake account and your CMK.
   6. Contact Snowflake Support to enable your Snowflake account to use Tri-Secret Secure.
2. Snowflake Support enables your Snowflake account to use Tri-Secret Secure based on the CMK that you register.

The steps in the following section avoid terms like *Amazon Resource Name* (ARN) to keep the procedure cloud agnostic. The steps are the
same regardless of the cloud platform that hosts your Snowflake account. However, the system function arguments for some of the steps are
different because each cloud platform service is different.

## Self-register a CMK

To self-register your CMK for use with Tri-Secret Secure, complete the following steps:

1. On the cloud provider, create a CMK.

   Do this step in the key management service (KMS) on the cloud platform that hosts your Snowflake account.
2. In Snowflake, call the [SYSTEM$REGISTER\_CMK\_INFO](/sql-reference/functions/system_register_cmk_info) system function to register your CMK with the KMS
   integration.

   Double-check the system function arguments for the cloud platform that hosts your Snowflake account.
3. In Snowflake, call the [SYSTEM$GET\_CMK\_INFO](/sql-reference/functions/system_get_cmk_info) system function to view the details for the CMK that you registered.
4. In Snowflake, call the [SYSTEM$GET\_CMK\_CONFIG](/sql-reference/functions/system_get_cmk_config) system function to generate the required information for
   the cloud provider.

   This policy allows Snowflake to access your CMK.

   Note

   If Microsoft Azure hosts your Snowflake account, you must pass the `tenant_id` value into the function.
5. On your cloud provider platform, use the output of the SYSTEM$GET\_CMK\_CONFIG function to authorize your CMK.
6. In Snowflake, call the [SYSTEM$VERIFY\_CMK\_INFO](/sql-reference/functions/system_verify_cmk_info) system function to confirm the connectivity between your
   Snowflake account and your CMK.
7. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) and request that your Snowflake account be enabled to use Tri-Secret Secure.

   Be sure to mention the specific account that you want to use with Tri-Secret Secure.

If you want to enable private connectivity for a CMK that is already activated with Tri-Secret Secure, see [Enable a private connectivity endpoint for an active CMK](/user-guide/security-encryption-tss-self-serve-private#label-tss-enable-pl-for-active-cmk)
for more information.

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

## Integrate Tri-Secret Secure with AWS external key stores

Snowflake supports integrating Tri-Secret Secure with AWS external key stores to securely store and manage a customer-managed
key outside AWS. Snowflake officially tests and supports only Thales Hardware Security Modules (HSM) and Thales CipherTrust Cloud Key Manager (CCKM) data encryption products.

For more information about setting up and configuring Tri-Secret Secure with Thales solutions, see [How to use Thales External Key Store for Tri-Secret Secure on an AWS Snowflake account](https://community.snowflake.com/s/article/thales-xks-for-tss-aws#e3).
