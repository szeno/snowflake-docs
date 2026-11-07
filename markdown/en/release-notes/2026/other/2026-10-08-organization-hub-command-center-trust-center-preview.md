# Oct 8, 2026: Organization Trust Center Configuration in Command Center (*Preview*)

Organization Trust Center Configuration is now in preview in Organization Command Center.

From the organization account, a user with the GLOBALORGADMIN role can open **Organization Hub** » **Command
center**, then the **Organization Trust Center Configuration** tile, to set organization-wide defaults for Trust Center
scanner packages and scanners. You can set schedules and notifications at the package or scanner level. Member accounts
apply these defaults after a short delay. Account administrators can still change settings within a member account.

In preview, organization defaults apply to all member accounts. Selecting a subset of accounts is coming soon. SQL
procedures for the same organization-level configuration are also available in preview. Using them requires the
SNOWFLAKE.TRUST\_CENTER\_ADMIN application role.

For more information, see [Organization Trust Center Configuration](/user-guide/organization-hub-command-center-trust-center) and
[Trust Center organization-level configuration procedures](/sql-reference/trust_center/trust-center-org-config).
