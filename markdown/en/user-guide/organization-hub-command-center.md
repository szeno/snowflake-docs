# Organization Command Center

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

**Command center** in [Organization Hub](/user-guide/organization-hub) is labeled **Organization command center** in
Snowsight. Use it to configure organization-wide settings from the organization account. Command Center is in
preview and is separate from the generally available [Insights](/user-guide/organization-hub-insights) page.

Command Center requires an [organization account](/user-guide/organization-accounts). Access is limited to the
GLOBALORGADMIN role.

## Get started

1. Use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to sign in to the organization account.
2. Switch to the GLOBALORGADMIN role.
3. In the navigation menu, select **Organization Hub** » **Command center**.

## Command Center tiles

The following Command Center tiles are in preview:

- [Organization Features](/user-guide/organization-hub-command-center-features): See which organization-level
  capabilities are enabled, starting with premium views. Organizations that have a capacity contract have premium views
  enabled by default. To enable or disable premium views, contact Snowflake Support.
- [3rd party access configuration](/user-guide/organization-hub-command-center-third-party): Classify member accounts as
  internal or external, set the default tenant type for new accounts, and maintain allowed email domains.

## Access control requirements

Command Center, including Organization Features and 3rd party access configuration, requires the GLOBALORGADMIN role.
ORGANIZATION\_USAGE application roles can open [Insights](/user-guide/organization-hub-insights), but they can’t open
Command Center.
