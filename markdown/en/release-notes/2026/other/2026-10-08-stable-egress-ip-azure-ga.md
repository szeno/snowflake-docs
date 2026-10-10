# Oct 8, 2026: Stable egress IP addresses on Azure (*General availability*)

Stable egress IP addresses are now generally available on Azure and are no longer in [Preview](/release-notes/preview-features). You can
generate Snowflake egress IP address ranges (as CIDR addresses) and add them to an external server’s allowlist so that Snowflake can make
requests to that server.

On Azure, [SYSTEM$GET\_SNOWFLAKE\_EGRESS\_IP\_RANGES](/sql-reference/functions/system_get_snowflake_egress_ip_ranges) returns additional metadata for each range, including a
published date and a `usage` field that describes how Snowflake uses the range. Allowlist `Stable Egress IP` prefixes for customer-hosted
endpoints. Allowlist `Network Identifier` prefixes for Azure Storage and Azure Key Vault. For more information, see
[Use Snowflake Network Identifiers in Azure allowlists for Azure Storage and Azure Key Vault (August 2026) (Pending)](/release-notes/bcr-bundles/un-bundled/bcr-2391).

This feature is also generally available on AWS Commercial deployments.

For more information, see [Securing ingress of Snowflake requests with egress IP addresses](/user-guide/egress-ip/network-egress).
