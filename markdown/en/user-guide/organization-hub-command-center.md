# Organization Command Center

**Command center** in [Organization Hub](/user-guide/organization-hub) is labeled **Organization command center** in
Snowsight. Use it to configure organization-wide settings from the organization account. Command Center is
separate from the [Insights](/user-guide/organization-hub-insights) page.

Command Center requires an [organization account](/user-guide/organization-accounts). Access is limited to the
GLOBALORGADMIN role.

## Get started

1. Use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to sign in to the organization account.
2. Switch to the GLOBALORGADMIN role.
3. In the navigation menu, select **Organization Hub** » **Command center**.

## Command Center tiles

- [Organization Features](/user-guide/organization-hub-command-center-features): See which organization-level
  capabilities are enabled, starting with premium views. Organizations that have a capacity contract have premium views
  enabled by default. To enable or disable premium views, contact Snowflake Support.
- [Organization users and user groups](/user-guide/organization-hub-command-center-users): Create organization users and
  organization user groups, assign users to groups, and make those groups visible to member accounts.
- [3rd party access configuration](/user-guide/organization-hub-command-center-third-party): Classify member accounts as
  internal or external, set the default tenant type for new accounts, and maintain allowed email domains.
- [Organization Trust Center Configuration](/user-guide/organization-hub-command-center-trust-center): Set
  organization-wide Trust Center scanner package and scanner defaults, schedules, and notifications for member accounts.

## Access control requirements

Command Center, including Organization Features, 3rd party access configuration, and Organization Trust Center
Configuration, requires the GLOBALORGADMIN role.
ORGANIZATION\_USAGE application roles can open [Insights](/user-guide/organization-hub-insights), but they can’t open
Command Center.
