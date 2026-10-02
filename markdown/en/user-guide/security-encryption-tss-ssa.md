# Tri-Secret Secure with secure share area accounts in Snowflake

[Business Critical Feature](/user-guide/intro-editions)

Requires Business Critical Edition (or higher). To ask about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Tri-Secret Secure overview

Using a dual-key encryption model together with Snowflake’s built-in user authentication enables three levels of data protection, known as
*Tri-Secret Secure*. Tri-Secret Secure offers you a level of security and control above Snowflake’s standard encryption.

Our dual-key encryption model combines a Snowflake-maintained key and a customer-managed key (CMK), which you create on the cloud provider
platform that hosts your Snowflake account. The model creates a composite master key that protects your Snowflake data. This composite master key
acts as an account master key by wrapping all of the keys in your account hierarchy. The composite master key is never used to encrypt raw data.
For example, the composite master key wraps table master keys, which are used to derive file keys that encrypt the raw data.

Attention

Before enabling Tri-Secret Secure for your secure share area account, carefully consider your responsibility for
safeguarding your key, as described in [Customer-managed keys](/user-guide/security-encryption-manage#label-customer-managed-keys). If the customer-managed key (CMK) in the composite master key
hierarchy is revoked, your data can no longer be decrypted by Snowflake.

If you have any questions or concerns, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Snowflake also bears the same responsibility for the keys that we maintain. As with all security-related aspects of our service, we treat
this responsibility with the utmost care and vigilance.

All of our keys are maintained under strict policies that have enabled us to earn the highest security accreditations, including SOC 2
Type II, PCI-DSS, HIPAA and [HITRUST CSF](/user-guide/intro-cloud-platforms#label-hitrust-csf-cert).

### Tri-Secret Secure compatibility with hybrid tables

You must enable Dedicated Storage Mode if you intend to create hybrid tables in your account and TSS is already enabled or
will be enabled. For information, see [Hybrid Tables Dedicated Storage Mode for TSS](/user-guide/tables-hybrid-dedicated-storage-mode).

### Understanding secure share area accounts

When you publish a listing and enable cross-cloud auto-fulfillment, Snowflake can automatically create one or more secure share area (SSA) accounts in consumer regions. These SSA accounts have the following qualities:

- Are owned and billed to you, the provider.
- Are managed by Snowflake; you cannot access them directly.
- Store replicated copies of your data product for use by consumers in other regions.

Because SSA accounts contain your data, you can protect them with Tri-Secret Secure, just like your primary accounts. However:

- TSS must be enabled separately on each SSA account.
- You can’t run Snowflake commands directly inside an SSA account.
- You may still want KMS API events (for example, GenerateDataKeyWithoutPlaintext and Decrypt) for these accounts to appear consistently in your cloud provider logs for alerting and audit.

## Identify your SSA accounts

SSA accounts for auto-fulfillment follow a standard naming pattern and appear as global accounts in your organization.

To list your SSA accounts, run the following commands:

> Copy code
>
> ```
> USE ROLE ORGADMIN;
>
> SHOW GLOBAL ACCOUNTS LIKE '%AUTO_FULFILLMENT_AREA%' IN ORGANIZATION <org_name>;
> ```

The output returns all accounts whose names include `AUTO_FULFILLMENT_AREA`; for example:

- `AUTO_FULFILLMENT_AREA$PUBLIC_AWS_US_EAST_1`
- `AUTO_FULFILLMENT_AREA$PUBLIC_AZURE_EASTUS2`

These account names are the values you will pass into the Tri-Secret Secure system functions when working with SSA accounts.

Note

Older deployments might still contain SSA accounts with names that start with `SNOWFLAKE_MANAGED$PUBLIC_<CLOUD>_<REGION>`. You can include both patterns in your filters if needed.

### Understanding Tri-Secret Secure with secure share area accounts

You can use Tri-Secret Secure with SSA accounts to provide enhanced security for data shared through SSAs.
SSA accounts benefit from the same three-layer encryption protection as standard accounts, with the customer-managed key
(CMK) providing an additional layer of control over the encryption keys.

Tri-Secret Secure with secure share area accounts provides the following benefits:

- Enhanced security for data shared through secure share areas
- Control over encryption keys for secure share area data
- Compliance with regulatory requirements for data protection
- Ability to revoke access to encrypted data by revoking the CMK

## Activate Tri-Secret Secure for secure share area accounts

Important

Activating Tri-Secret Secure for an SSA account is not a self-service operation. You must
[contact Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to enable TSS for your SSA accounts.
When you open a support ticket, provide the following information:

- Your organization name and the SSA account name (see [Identify your SSA accounts](#identify-your-ssa-accounts)).
- The cloud provider and region of the SSA account.
- Your CMK details (key ARN for AWS, key vault URI for Azure, or key resource ID for GCP).

After Snowflake Support activates Tri-Secret Secure for your SSA account, you can use the following system functions to
check the status of your CMK:

- Call the [SYSTEM$GET\_CMK\_INFO](/sql-reference/functions/system_get_cmk_info) system function with the SSA account name to view the details for the
  registered CMK.
- Call the [SYSTEM$VERIFY\_CMK\_INFO](/sql-reference/functions/system_verify_cmk_info) system function with the SSA account name to confirm the connectivity
  between your Snowflake account and your CMK.

Note

The following system functions are not available for SSA accounts:
[SYSTEM$REGISTER\_CMK\_INFO](/sql-reference/functions/system_register_cmk_info),
[SYSTEM$GET\_CMK\_CONFIG](/sql-reference/functions/system_get_cmk_config), and
[SYSTEM$ACTIVATE\_CMK\_INFO](/sql-reference/functions/system_activate_cmk_info).
To register, configure, or activate a CMK for an SSA account,
[contact Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## View the status of your CMK

You can call [SYSTEM$GET\_CMK\_INFO](/sql-reference/functions/system_get_cmk_info) at any time, to check the registration and activation status of your CMK.

For example, depending on when you call SYSTEM$GET\_CMK\_INFO, the function returns the following output:

- Immediately after activating Tri-Secret Secure, returns `...is being activated...`. This means that rekeying isn’t complete.
- After the Tri-Secret Secure activation process completes, returns output that includes `...is activated...`. This means that your
  Snowflake account is using Tri-Secret Secure with the CMK that you registered.

## Change, deactivate, or deregister the CMK for Tri-Secret Secure

To change, deactivate, or deregister your CMK for an SSA account,
[contact Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The following system functions are not available for SSA accounts:
[SYSTEM$DEACTIVATE\_CMK\_INFO](/sql-reference/functions/system_deactivate_cmk_info) and
[SYSTEM$DEREGISTER\_CMK\_INFO](/sql-reference/functions/system_deregister_cmk_info).
