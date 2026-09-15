# Hybrid Tables Dedicated Storage Mode for TSS

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

This section explains how to start using [Tri-Secret Secure (TSS)](/user-guide/security-encryption-tss) in accounts that contain hybrid tables.

Note

For information about billing and costs for this feature, consult your Snowflake account team.

## Introduction

In a standard storage configuration for hybrid tables, underlying multi-tenant storage is used for all hybrid table data. This means that different databases and data that belongs to different customers use a shared storage layer. This shared storage configuration does not work if you have enabled or plan to enable TSS because TSS protects your data with encryption keys owned by individual customers. Enabling TSS encryption for hybrid tables requires a storage configuration known as Hybrid Tables Dedicated Storage Mode. You can also use periodic rekeying for additional encryption support, but periodic rekeying does not require this Dedicated Storage Mode.

When an account has both Dedicated Storage Mode and TSS enabled, all of the data that is stored in a hybrid table is protected with your TSS composite master key, which combines a Snowflake-maintained key with a customer-managed key. This protection covers hybrid table data in the underlying operational row store, the copy of the data in object storage, data retained for Time Travel, and metadata. You can use hybrid tables with the same serverless experience as you would with a standard storage configuration, and no additional management or provisioning is required.

## Using Dedicated Storage Mode

You must enable Dedicated Storage Mode if you intend to create hybrid tables in your account and TSS is already enabled or will be enabled. Enabling Dedicated Storage Mode is a one-time action on the account. Before you take this action, you will not be able to create hybrid tables with TSS protection.

Note the following important considerations:

- To ensure that your data is fully TSS-protected, you can’t enter a state where a TSS-enabled account contains hybrid tables that are stored in a standard multi-tenant storage configuration. Only one storage mode can be active at any given time.
- Data that exists in hybrid tables before TSS is enabled can never be encrypted with TSS-compliant keys. TSS protection is guaranteed only for data written to hybrid tables after Dedicated Storage Mode and TSS are both enabled.
- You can’t enable TSS if your account already contains hybrid tables. You have to drop individual hybrid tables or any databases that contain hybrid tables, then request enablement of Dedicated Storage Mode and TSS.

  Note

  To ensure that all hybrid table data is fully removed from your account, Snowflake recommends the following steps:

  1. Set the [data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period) to `0` for either individual hybrid tables or any databases that contain hybrid tables.
  2. Drop either individual hybrid tables or any databases that contain hybrid tables.
- For information about billing and costs for this feature, consult your Snowflake account team.

### Enabling Dedicated Storage Mode and TSS

To enable Dedicated Storage Mode on an account, follow these steps:

1. Contact your account team and request enablement of Hybrid Tables Dedicated Storage Mode with TSS support on your account.
   Assuming that no hybrid tables exist in your account, the team will enable Dedicated Storage Mode (and enable TSS if it’s not already enabled).
2. Create and use hybrid tables in your account, following the [standard documentation](/user-guide/tables-hybrid).
3. Repeat this process for any additional TSS-enabled Snowflake accounts in which you want to use hybrid tables.

### Disabling Dedicated Storage Mode

To ensure that your data is fully TSS-protected, disabling Dedicated Storage Mode in a TSS-enabled account requires the following steps:

1. Set the [data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period) to `0` for either individual hybrid tables or any databases that contain hybrid tables.
2. Drop either individual hybrid tables or any databases that contain hybrid tables.
   If you need to retain the data, you can copy it to standard tables in your account before dropping tables or databases.
3. Contact your account team and request that Dedicated Storage Mode be disabled on your account.
   The team will disable Dedicated Storage Mode, but if your account still contains hybrid tables, you will be asked to remove them first.
