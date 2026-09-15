# Aug 3, 2026: Organization Hub (*General availability*)

The **Insights** page under Organization Hub presents interactive tiles that show trends, alerts, and summary data for your entire
organization. The feature is now generally available to customers who have
[ORGANIZATION\_USAGE premium views](/user-guide/organization-accounts-premium-views) enabled, and is no longer in
[Preview](/release-notes/preview-features).

Insights gives you one place to govern cost, security, and query health across all accounts, so you don’t have to sign in to each
account separately.

You can also investigate those organization-wide signals in [Cortex Code](/user-guide/cortex-code/cortex-code). In Cortex Code, type
`/organization-management` to invoke the
[`organization-management` skill](/user-guide/cortex-code/bundled-skills#label-bundled-skill-organization-management), then
describe what you want to analyze. For more information, see
[Analyze organization insights with Cortex Code](/user-guide/organization-hub-insights#label-org-hub-cortex-code).

Users with the GLOBALORGADMIN role can access Organization Hub. Designated users and roles that have been granted the appropriate
[ORGANIZATION\_USAGE application roles](/sql-reference/organization-usage#label-org-usage-access-org-account), such as
ORGANIZATION\_BILLING\_VIEWER for cost data and ORGANIZATION\_SECURITY\_VIEWER for security data, can also access it.

You should see the following sections:

- **Billing and Cost**: Review total cost, cost by service type, total storage, and contract utilization for your organization.
- **Security**: Monitor Trust Center violations and scanner package coverage, Strong Authentication progress, login failures,
  authentication methods for human and service users, account and security admins, and dormant users.
- **Query health**: Investigate failed queries, warehouse queued load, warehouse congestion, and your most expensive grouped
  queries.

For more information, see [Organization Hub Insights](/user-guide/organization-hub-insights).
