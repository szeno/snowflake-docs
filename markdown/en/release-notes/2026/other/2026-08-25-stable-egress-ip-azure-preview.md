# August 25, 2026: Stable egress IP addresses on Azure (*Preview*)

Stable egress IP addresses are now available in preview on Azure. You can generate Snowflake egress IP address ranges (as CIDR
addresses) and add them to an external server’s allowlist so that Snowflake can make requests to that server.

On Azure, [SYSTEM$GET\_SNOWFLAKE\_EGRESS\_IP\_RANGES](/sql-reference/functions/system_get_snowflake_egress_ip_ranges) also returns additional metadata for each range, including
a published date and a `usage` field that describes how Snowflake uses the range.

This feature is generally available on AWS Commercial deployments.

For more information, see [Securing ingress of Snowflake requests with egress IP addresses](/user-guide/egress-ip/network-egress).
