# Securing ingress of Snowflake requests with egress IP addresses

You can securely allow ingress access from Snowflake to your external resources by allowing egress IP address ranges generated from
Snowflake through the resource’s network firewall.

You can generate a list of Snowflake egress IP address ranges (as Classless Inter-Domain Routing (CIDR) addresses) that you can use to
represent Snowflake in allowing access through your external server’s network firewall.

## Supported deployments

Stable egress IP addresses are generally available on AWS Commercial deployments.

[Preview Feature](/release-notes/preview-features) — Open

Support for stable egress IP addresses on Azure is in preview.

## Supported uses

Using egress IP addresses you generate with Snowflake, you can allow ingress access from the following Snowflake features:

- External access from [UDFs and procedures](/developer-guide/external-network-access/external-network-access-overview)
- [Snowpark Container Services external access](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress) and Snowflake Openflow on Snowpark Container Services
- [Snowflake Git integration](/developer-guide/git/git-setting-up) with IP-restricted Git servers

When the external resource is on a private network where IP allowlisting isn’t feasible (deny-all-inbound environments), use
[Data Connectivity Proxy](/user-guide/data-connectivity-proxy) instead of stable egress IPs.

## Generate egress IP address ranges

You can generate IP address ranges that Snowflake uses for egress traffic by using the
[SYSTEM$GET\_SNOWFLAKE\_EGRESS\_IP\_RANGES](/sql-reference/functions/system_get_snowflake_egress_ip_ranges) function.

The generated IP addresses expire, so for ongoing needs you should set up a means to automate refreshing your external server’s firewall
with fresh egress IP addresses, as described in [Automate IP address range refreshes](#label-network-egress-refreshing).

To generate and use Snowflake egress IP addresses, follow these steps:

1. Call [SYSTEM$GET\_SNOWFLAKE\_EGRESS\_IP\_RANGES](/sql-reference/functions/system_get_snowflake_egress_ip_ranges) to get the current and upcoming
   IP ranges and their expiration times.

   The following code shows example output of the function.

   Copy code

   ```
   SELECT
    value: "ipv4_prefix":: VARCHAR AS IP_CIDR_RANGE_FOR_REGION,
    value: "effective":: TIMESTAMP AS IP_CIDR_RANGE_EFFECTIVE,
    value: "expires":: TIMESTAMP AS IP_CIDR_RANGE_EXPIRATION
   FROM TABLE(FLATTEN (INPUT => PARSE_JSON(SYSTEM$GET_SNOWFLAKE_EGRESS_IP_RANGES())));
   ```

   Note, for Azure, `SYSTEM$GET_SNOWFLAKE_EGRESS_IP_RANGES()` returns a JSON with inline comments. Use the `hideAnnotations` argument: `PARSE_JSON(SYSTEM$GET_SNOWFLAKE_EGRESS_IP_RANGES(TRUE))`.

   ```
   +--------------------------+-------------------------+--------------------------+
   | IP_CIDR_RANGE_FOR_REGION | IP_CIDR_RANGE_EFFECTIVE | IP_CIDR_RANGE_EXPIRATION |
   +--------------------------+-------------------------+--------------------------+
   | 153.45.34.0/24           | 2025-08-01 00:00:00.000 | 2026-05-06 01:33:26.726  |
   | 153.45.77.0/24           | 2025-08-01 00:00:00.000 | 2026-05-06 01:33:26.726  |
   +--------------------------+-------------------------+--------------------------+
   ```

   - The `IP CIDR RANGE_EFFECTIVE` column shows the start date when a range starts carrying traffic. A new range should emerge in function output at least 60 days before being “effective”.
   - The `IP CIDR RANGE_EXPIRATION` column shows the date when an IP range stops carrying traffic.
2. Use the IP ranges you obtain to update firewall rules by using APIs, CLIs, or configuration management tools, as described in
   [Automate IP address range refreshes](#label-network-egress-refreshing).

## Automate IP address range refreshes

Snowflake egress IP addresses expire. To keep access secure, you must update the Snowflake egress IP addresses allowed through your
external server’s firewall so that they’re current.

To keep IP addresses fresh, implement a mechanism to trigger these updates to your external server regularly, such as daily or weekly.
You might do this, for example, by [using your environment’s tools](#label-network-egress-automation).

To make updates, follow these steps in your script:

1. Retrieve Snowflake egress IP address ranges by using [SYSTEM$GET\_SNOWFLAKE\_EGRESS\_IP\_RANGES](/sql-reference/functions/system_get_snowflake_egress_ip_ranges).
2. Compare the newly-retrieved ranges with those you’re currently using.

   You can avoid unnecessary changes by only making updates if the address ranges are different.

   - If they aren’t different, have your script use expiration dates to set a time to check again, such as a few days before the
     expiration.
   - If the newly-retrieved list is different, update your firewall rule programmatically with the new addresses. You can then have the
     script set a new date to check, such as a few days before the new expiration.
3. Log changes made by the script and set up alerts on successful updates or failures.

### Automate updates using your environment’s tools

You can automate the tasks needed to keep Snowflake IP addresses fresh by using scripts and tools. The following describes two examples:

- Scripting with APIs and CLIs on cloud providers such as AWS, Azure, and Google Cloud.

  For cloud environments, you can write scripts by using tools such as Python, PowerShell, and Bash. Your tools can perform the following
  tasks:

  1. Call [SYSTEM$GET\_SNOWFLAKE\_EGRESS\_IP\_RANGES](/sql-reference/functions/system_get_snowflake_egress_ip_ranges) to retrieve the latest IP
     address ranges and expiration dates.
  2. Use the cloud provider’s API or CLI to update security group rules, network ACLs, or firewall policies.
  3. Schedule scripts that perform these actions to run periodically (such as daily or weekly) or based on expiry dates using cron
     jobs. You can run these by using stored procedures with Snowflake tasks.
- Infrastructure-as-code (IaC) tools

  You can use tools such as Terraform, Ansible, or CloudFormation to manage firewall rules as code. The approach described below also
  provides version control and audit trails for firewall rule changes.

  Using these tools, you can perform the following tasks:

  1. Define firewall rules in IaC configurations.
  2. Call [SYSTEM$GET\_SNOWFLAKE\_EGRESS\_IP\_RANGES](/sql-reference/functions/system_get_snowflake_egress_ip_ranges) to retrieve the latest IP
     address ranges and expiration dates.
  3. When new Snowflake egress IP ranges are available, update your IaC configuration with the new ranges.
  4. Apply the changes by using your IaC tool, ensuring that firewall rules are updated programmatically and idempotently.
