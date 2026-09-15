# Organization Features

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Use **Organization Features** in Organization Command Center to see which organization-level capabilities are enabled
in the organization account. In preview, the main control is
[premium views](/user-guide/organization-accounts-premium-views) for cross-account telemetry. Organizations that have a
capacity contract have premium views enabled by default. To enable or disable premium views, contact
[Snowflake Support](/user-guide/contacting-support). You can’t turn them on or off from the card.

## Before you begin

Confirm the following:

- You can sign in to the [organization account](/user-guide/organization-accounts) with the GLOBALORGADMIN role.

## Open Organization Features

1. Use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to sign in to the organization account.
2. Switch to the GLOBALORGADMIN role.
3. In the navigation menu, select **Organization Hub** » **Command center**.
4. Select the **Organization Features** tile.

On the page, breadcrumbs read **Organization command center** » **Organization Features**. The page title is
**Organization Features**.

## Enable premium views

The **Enable Premium Views** card shows whether enhanced ORGANIZATION\_USAGE views are available so you can aggregate
historical query, login, and metering data across all accounts in your organization.

- **Status**: The card shows whether premium views are enabled or disabled for your organization. Organizations that
  have a capacity contract have premium views enabled by default.
- **Enable or disable**: You can’t enable or disable premium views from this card. To turn them on or off, contact
  [Snowflake Support](/user-guide/contacting-support). Changing this setting affects other organization-account
  experiences that depend on that telemetry, including [Insights](/user-guide/organization-hub-insights). Work with
  Snowflake Support so you understand the tradeoffs before you change the setting.

For conceptual background and view lists, see
[Premium views in the organization account](/user-guide/organization-accounts-premium-views).

## Access control requirements

Organization Features requires the GLOBALORGADMIN role. ORGANIZATION\_USAGE application roles can open
[Insights](/user-guide/organization-hub-insights), but they can’t open Command Center or Organization Features.
