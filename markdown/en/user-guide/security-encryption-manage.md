# Understanding Encryption Key Management in Snowflake

This topic provides concepts related to Snowflake-managed keys and customer-managed keys.

## Overview

Snowflake manages data encryption keys to protect customer data. This management can occur automatically without any need for customer
intervention.

Customers can also use the key management service in the cloud platform that hosts their Snowflake account to maintain their own additional
encryption key.

When enabled, the combination of a Snowflake-maintained key and a customer-managed key creates a composite
[master key](https://csrc.nist.gov/glossary/term/master_key) to protect customer data in Snowflake. This is called [Tri-Secret Secure](/user-guide/security-encryption-tss). For more information, see [Tri-Secret Secure overview](/user-guide/security-encryption-tss#label-encryption-tss-overview).

## Snowflake-managed keys

All Snowflake customer data is encrypted by default. Snowflake uses strong AES encryption with a hierarchical key model rooted in a
cloud-provider-hosted hardware security module.

Keys are automatically rotated on a regular basis by the Snowflake service, and customer data can be automatically re-encrypted (“rekeyed”)
on a regular basis. Customer data encryption and key management require no configuration or management.

### Hierarchical key model

A hierarchical key model provides a framework for Snowflake’s encryption key management. The hierarchy is composed of several layers of
keys in which each higher layer of keys (parent keys) encrypts the layer below (child keys). In security terminology, a parent key
encrypting all child keys is known as “wrapping”.

Snowflake’s hierarchical key model consists of four levels of keys:

- The root key
- Account master keys
- Table master keys
- File keys

Each customer account has a separate key hierarchy of account-level, table-level, and file-level keys, as shown in the following image:

![Snowflake's hierarchical key model](/static/images/hierarchical-key-model.png)

In a multi-tenant cloud service like Snowflake, the hierarchical key model isolates every account with the use of separate account master
keys. In addition to the [access control model](/user-guide/security-access-control-overview), which separates storage of customer
data, the hierarchical key model provides another layer of account isolation.

A hierarchical key model reduces the scope of each layer of keys. For example, a table master key encrypts a single table. A file key
encrypts a single file. A hierarchical key model constrains the amount of customer data each key protects and the duration of time for which
it is usable.

### Encryption key rotation

Keys in the Snowflake-managed key hierarchy are automatically rotated by Snowflake when they are more than 30 days old. Active keys are
retired, and new keys are created. When Snowflake determines the retired key is no longer needed, the key is automatically destroyed. When
active, a key is used to encrypt customer data and is available for usage by the customer. When retired, the key is used solely to decrypt
customer data and is only available for accessing the data.

When wrapping child keys in the key hierarchy, or when inserting customer data into a table, only the current, active key is
used to encrypt data. When a key is destroyed, it is not used for either encryption or decryption. Regular key rotation limits the
life cycle for the keys to a limited period of time.

The following image illustrates key rotation for one table master key (TMK) over a period of three months:

![Key rotation of one table master key (TMK) over a time period of three months.](/static/images/key-rotation.png)

The TMK rotation works as follows:

- Version 1 of the TMK is active in April. Customer data inserted into this table in April is protected with TMK v1.
- In May, this TMK is rotated: TMK v1 is retired, and a new, completely random key, TMK v2, is created. TMK v1 is now used only to decrypt
  customer data from April. New customer data inserted into the table is encrypted using TMK v2.
- In June, the TMK is rotated again: TMK v2 is retired and a new TMK, v3, is created. TMK v1 is used to decrypt customer data from April,
  TMK v2 is used to decrypt customer data from May, and TMK v3 is used to encrypt and decrypt new customer data inserted into the table in
  June.

As stated previously, key rotation limits the duration of time in which a key is actively used to encrypt customer data. In conjunction with
the hierarchical key model, key rotation further constrains the amount of customer data a key version protects. Limiting the lifetime of a
key is [recommended](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final) by the National Institute of Standards
and Technology (NIST) to enhance security.

### Periodic rekeying

[Enterprise Edition Feature](/user-guide/intro-editions)

Periodic rekeying requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This section continues with an explanation of the account and table master key lifecycle. [Encryption Key Rotation](#encryption-key-rotation) describes key rotation,
which replaces active keys with new keys on a periodic basis and retires the old keys. Periodic data rekeying completes the life cycle.

While key rotation ensures that a key is transferred from its active state to a retired state, rekeying ensures that a key is transferred
from its retired state to being destroyed.

If periodic rekeying is enabled, then when the retired encryption key for a table is older than one year, Snowflake automatically creates
a new encryption key and re-encrypts all customer data previously protected by the retired key using the new key. The new key is used to
decrypt the table data going forward.

Note

> For Enterprise Edition accounts, users with the ACCOUNTADMIN role can enable periodic rekeying for the account, using
> [ALTER ACCOUNT](/sql-reference/sql/alter-account) and the [PERIODIC\_DATA\_REKEYING](/sql-reference/parameters#label-periodic-data-rekeying) parameter, as shown in the following example.
>
> > Copy code
> >
> > ```
> > ALTER ACCOUNT SET ENABLE_TRI_SECRET_AND_REKEY_OPT_OUT_FOR_IMAGE_REPOSITORY = TRUE;
> >
> > ALTER ACCOUNT SET PERIODIC_DATA_REKEYING = TRUE;
> > ```

This does not apply additional security to any images stored in your Snowpark image repository.

The following image shows periodic rekeying for a TMK for a single table:

![Rekeying one table master key (TMK) after one year](/static/images/rekeying.png)

Periodic rekeying works as follows:

- In April of the following year, after TMK v1 has been retired for an entire year, it is rekeyed (generation 2) using a fully new random
  key.

  The customer data files protected by TMK v1 generation 1 are decrypted and re-encrypted using TMK v1 generation 2. Having no further
  purpose, TMK v1 generation 1 is destroyed.
- In May, Snowflake performs the same rekeying process on the table data protected by TMK v2.
- And so on.

In this example, the lifecycle of a key is limited to a total duration of one year.

Rekeying constrains the total duration in which a key is used for recipient usage, following NIST recommendations. Furthermore, when
rekeying customer data, Snowflake can increase encryption key sizes and utilize better encryption algorithms that may be standardized since
the previous key generation was created.

Snowflake rekeys customer data files online, in the background, without any impact to currently running customer workloads. Customer data
that is being rekeyed is always available to you. No service downtime is necessary to rekey the data, and you encounter no performance
impact on your workload. This benefit is a direct result of Snowflake’s architecture of separating storage and compute resources.

#### Impact of rekeying on Time Travel and Fail-safe

[Time Travel](/user-guide/data-time-travel) and [Fail-safe](/user-guide/data-failsafe) retention periods are not affected by
rekeying. However, some additional storage charges are associated with rekeying of customer data in Fail-safe (see next section).

#### Impact of rekeying on storage utilization

Snowflake customers are charged with additional storage for Fail-safe protection of customer data files that were rekeyed. For these
files, 7 days of Fail-safe protection is charged.

That is, for example, the customer data files with the old key on Amazon S3 are already protected by Fail-safe, and the customer data files
with the new key on Amazon S3 are also added to Fail-safe, leading to a second charge, but only for the 7-day period.

### Hardware security module

Snowflake relies on cloud-hosted hardware security modules (HSMs) to help ensure that key storage and usage are secure. Each cloud platform has
different HSM services, and that affects how Snowflake uses the HSM service on each platform:

- On AWS and Azure, Snowflake uses the HSM to create and store the root key.
- On Google Cloud, the HSM service is made available through the Google Cloud KMS (key management service) API. Snowflake uses Google Cloud
  KMS to create and store the root key in multi-tenant HSM partitions.

For all cloud platforms and all keys in the key hierarchy, a key that is stored in the HSM is used to unwrap a key in the hierarchy. For
example, to decrypt the table master key, the key in the HSM unwraps the account master key. This process occurs in the HSM. After this
process completes, a software operation decrypts the table master key with the account master key.

The following image shows the relationship between the HSM, the account master keys, the table master keys, and the file keys:

![Key hierarchy rooted in Hardware Security Module](/static/images/hardware-security-module.png)

## Customer-managed keys

A customer-managed key (CMK) is a master encryption key that the customer maintains in the key management service for the cloud provider that
hosts the customer’s Snowflake account. The key management services for each platform are:

- **AWS:** [AWS Key Management Service (KMS)](https://aws.amazon.com/kms/)
- **Google Cloud:** [Cloud Key Management Service (Cloud KMS)](https://cloud.google.com/kms)
- **Microsoft Azure:** [Azure Key Vault](https://azure.microsoft.com/en-us/services/key-vault/)

The CMK can then be combined with a Snowflake-managed key to create a composite master key. When this occurs, Snowflake refers to this
as Tri-Secret Secure. For more information, see [Tri-Secret Secure overview](/user-guide/security-encryption-tss#label-encryption-tss-overview).

You can call these system functions in your Snowflake account to obtain information about your keys:

- AWS: [SYSTEM$GET\_CMK\_KMS\_KEY\_POLICY](/sql-reference/functions/system_get_cmk_kms_key_policy)
- Microsoft Azure: [SYSTEM$GET\_CMK\_AKV\_CONSENT\_URL](/sql-reference/functions/system_get_cmk_akv_consent_url)
- Google Cloud: [SYSTEM$GET\_GCP\_KMS\_CMK\_GRANT\_ACCESS\_CMD](/sql-reference/functions/system_get_gcp_kms_cmk_grant_access_cmd)

Snowflake supports the following:

- **Configuring automatic key rotation in your cloud service provider.** Configuring key rotation creates a new version of the same CMK with
  updated encryption material. You can enable automatic key rotation using the key rotation feature specific to your cloud provider
  without any action in Snowflake.

  When your CMK is rotated, a new cryptographic version is created in your cloud provider. Snowflake does not immediately use this new version.
  Instead, Snowflake incorporates the new CMK version the next time it rotates its internal Account Master Key (AMK), which occurs automatically,
  every 30 days.

  After automatic key rotation occurs, Snowflake uses the new AMK to encrypt newly created database files. Existing files continue to be
  decrypted using prior CMK versions. If you wish to rekey all the existing files with the new CMK version, please see [Use Tri-Secret Secure self-service with automatic key rotation](/user-guide/security-encryption-tss-self-serve#label-tss-self-serve-auto-key-rotation).

  Important

  Do not delete or change or revoke permissions on older CMK versions in any cloud service provider. Deleting a rotated key can
  lead to data loss. Snowflake cannot decrypt data encrypted with a deleted key.

  For more information about configuring automatic key rotation for customer-managed keys in the cloud platform that supports your Snowflake
  account(s), see:

  - [AWS KMS automatic key rotation policy for Customer Managed Keys used by Snowflake Tri-Secret Secure](https://community.snowflake.com/s/article/Does-enabling-AWS-automatic-key-rotation-CMKs-feature-impact-the-snowflake-account-which-has-tri-secret-secure-enabled)
  - [Microsoft Azure automatic key rotation policy for Customer Managed Keys used by Snowflake Tri-Secret Secure](https://community.snowflake.com/s/article/azure-automatic-key-rotation-tss)
  - [GCP KMS automatic key rotation policy for Customer Managed Keys used by Snowflake Tri-Secret Secure](https://community.snowflake.com/s/article/GCP-KMS-automatic-key-rotation-tri-secret-secure)
- **Manually changing the CMK used by Tri-Secret Secure.** Changing your CMK for Tri-Secret Secure requires creating and self-registering a new
  CMK, and then updating Tri-Secret Secure to use it. Follow the self-registration steps in [Tri-Secret Secure](/user-guide/security-encryption-tss) and reach out to
  [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to coordinate the key change.

  Important

  Don’t revoke access to or delete the current CMK until Snowflake Support confirms it is safe to do so.

For more information about using Snowflake system functions to change your CMK, see [Understanding Tri-Secret Secure self-service](/user-guide/security-encryption-tss-self-serve#label-encryption-tss-self-register-la) and [Change the CMK for Tri-Secret Secure](/user-guide/security-encryption-tss-self-serve#label-change-cmk-tss).

### Benefits of customer-managed keys

Benefits of customer-managed keys include:

Control over customer data access:
:   You have complete control over your master key in the key management service and, therefore, your customer data in Snowflake. You must
    release this key to decrypt data stored in your Snowflake account.

Disable access due to a customer data breach:
:   If you experience a security breach, you can disable access to your key and halt all data operations running in your Snowflake account.

Ownership of the customer data lifecycle:
:   Using customer-managed keys, you can align your data protection requirements with your business processes. Explicit control over your key
    provides safeguards throughout the entire customer data lifecycle, from creation to deletion.

### Important requirements for customer-managed keys

Customer-managed keys provide significant security benefits, but they also have crucial, fundamental requirements that you must
continuously follow to safeguard your master key:

Confidentiality:
:   You must keep your key secure and confidential at all times.

Integrity:
:   You must ensure your key is protected against improper modification or deletion.

Availability:
:   To execute queries and access your data, you must ensure your key is continuously available to Snowflake.

By design, an invalid or unavailable key will result in a disruption to your Snowflake data operations until a valid key is made available
again to Snowflake.

Snowflake is designed to handle temporary availability issues (up to 10 minutes) caused by common issues, such as network
communication failures. After 10 minutes, if the key remains unavailable, all data operations in your Snowflake account will cease
completely. Once access to the key is restored, data operations can be started again.

Failure to comply with these requirements can significantly jeopardize the integrity of your data, ranging from your data being
temporarily inaccessible to it being permanently disabled. In addition, Snowflake cannot be responsible for 3rd-party
issues that occur or administrative mishaps caused by your organization in the course of maintaining your key.

For example, if an issue with the key management service results in your key becoming unavailable, your data operations will be impacted.
These issues must be resolved between you and the Support team for the key management service. Similarly, if your key is
tampered with or destroyed, all existing data in your Snowflake account will become unreadable until the key is restored.
