# October 30, 2026: Tri-Secret Secure for Snowflake storage for Apache Iceberg™ tables (*General availability*)

Tri-Secret Secure for Snowflake storage for Iceberg tables is now generally available for accounts hosted on AWS or Microsoft Azure. You can encrypt the
data that [Snowflake storage for Iceberg tables](/user-guide/tables-iceberg-internal-storage) writes to your account’s
Snowflake-managed storage volume by using a customer-managed key (CMK) that you create in AWS Key Management Service (KMS) or
in Azure Key Vault.

You register, verify, and activate your CMK by using dedicated system functions such as
[SYSTEM$REGISTER\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_register_cmk_info_snowflake_managed_volume) and
[SYSTEM$ACTIVATE\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_activate_cmk_info_snowflake_managed_volume). Activation is immediate and applies to data
written after you activate the key.

This feature requires Business Critical Edition (or higher) and isn’t enabled by default. To enable it for your account,
contact [Snowflake Support](/user-guide/contacting-support).

For more information, see [Tri-Secret Secure for Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-snowflake-storage-tss).
