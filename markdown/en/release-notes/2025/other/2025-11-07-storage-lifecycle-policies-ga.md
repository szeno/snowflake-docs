# Nov 07, 2025: Storage lifecycle policies (*General availability*)

Storage lifecycle policies are now generally available.
These schema-level objects let you manage data retention for standard Snowflake
tables by archiving or expiring rows based on your defined conditions.

Storage lifecycle policies provide the following key capabilities:

- **Reduced storage costs**: Move older data to more cost-effective archive storage tiers.
- **Regulatory compliance**: Automate data archival and deletion to help meet compliance requirements.
- **Automated data management**: Archive and delete data automatically using Snowflake-managed compute resources.
- **Flexible data retrieval**: Retrieve archived data by creating a new table that contains only the
  rows you need.

For more information, see [Storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies).
