# Organization Hub

Organization Hub is the organization-account home for organization-wide monitoring and configuration. From Organization
Hub, choose one of the following:

- **Insights** (generally available): Monitor and analyze cost, security posture, query health, and storage across all
  accounts. See [Organization Hub Insights](/user-guide/organization-hub-insights).
- **Command center** (preview): Configure organization-wide settings, including Organization Features and 3rd party
  access configuration. See [Organization Command Center](/user-guide/organization-hub-command-center).

Organization Hub requires an [organization account](/user-guide/organization-accounts).
[Insights](/user-guide/organization-hub-insights) also requires
[premium views](/user-guide/organization-accounts-premium-views).

## Get started

1. Use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to sign in to the organization account.
2. Switch to the GLOBALORGADMIN role. To open **Insights** only, you can instead switch to a role that has been granted
   the appropriate
   [ORGANIZATION\_USAGE application roles](/sql-reference/organization-usage#label-org-usage-access-org-account).
3. In the navigation menu, select **Organization Hub**, then **Insights** or **Command center**. **Command center**
   requires the GLOBALORGADMIN role.

## Insights

Use **Insights** to review interactive tiles for billing and cost, security, and query health, and to analyze those
signals in Cortex Code. For tile descriptions, access control, and Cortex Code prompts, see
[Organization Hub Insights](/user-guide/organization-hub-insights).

## Command Center

Use **Command center** to configure organization-wide settings. Command Center is in preview. For access requirements
and the Organization Features and 3rd party access configuration tiles, see
[Organization Command Center](/user-guide/organization-hub-command-center).
