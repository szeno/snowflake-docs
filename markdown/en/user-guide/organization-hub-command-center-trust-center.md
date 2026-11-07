# Organization Trust Center Configuration

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Use **Organization Trust Center Configuration** in Organization Command Center to set organization-wide Trust Center
scanner package and scanner defaults for member accounts. The Command Center landing tile shows how many scanner packages
are enabled and account scanner coverage.

Account administrators can still change scanner package and scanner settings inside a member account. For Trust Center
concepts and account-level steps, see [Trust Center](/user-guide/trust-center/overview) and
[Using the Trust Center](/user-guide/trust-center/using-the-trust-center).

## Before you begin

Confirm the following:

- You can sign in to the [organization account](/user-guide/organization-accounts) with the GLOBALORGADMIN role.

## Open Organization Trust Center Configuration

1. Use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to sign in to the organization account.
2. Switch to the GLOBALORGADMIN role.
3. In the navigation menu, select **Organization Hub** » **Command center**.
4. Select **Organization Trust Center Configuration** or **Configure trust center packages**.

On the Command Center landing page, the **Organization Trust Center Configuration** tile shows the following:

- **Scanner packages enabled**: How many scanner packages are enabled, shown as a count of the packages available to
  your organization (for example, **3 of 4**).
- **Account scanner coverage**: The percentage of accounts that have Trust Center scanner packages enabled.
- **Action items**: **Configure trust center packages**, which opens the configuration page.

The **Guides** panel includes **Using the Trust Center** and **Scanner Packages**.

## Manage scanner packages

From **Organization Trust Center Configuration**, you can do the following in Snowsight:

- Review the account scope, which is **All accounts** in public preview.
- Enable or disable a scanner package or an individual scanner as an organization default.
- Set schedules and notifications at the package level or for an individual scanner.
- Review **Unsynced accounts** and **Synced accounts** for a package.

For SQL procedures that set the same organization-level scanner and scanner package configuration, see
[Trust Center organization-level configuration procedures](/sql-reference/trust_center/trust-center-org-config). Those
procedures require the SNOWFLAKE.TRUST\_CENTER\_ADMIN application role.

## How organization defaults apply

Organization defaults cover whether a scanner package or scanner is enabled, its schedule, and its notifications.
Member accounts apply those defaults after a short delay. Until an account applies a default, it can appear under
**Unsynced accounts**.

Effective settings in an account can differ from the organization default for any of the following reasons:

- The default hasn’t been applied yet.
- An administrator in the member account overrode enablement, schedule, or notifications in that account.
- Applying the default failed.

When more than one setting exists, Trust Center uses the most specific one. Account-level scanner settings take
precedence over account-level package settings, which take precedence over organization-level scanner settings, which
take precedence over organization-level package settings. Built-in scanner and package defaults apply only when no
organization or account setting is present.

For the full precedence list, see
[Scanner configuration precedence](/sql-reference/trust_center/trust-center-org-config#label-trust-center-scanner-config-precedence).

## Account scope

Under **Scanner Packages**, the **Account scope** card shows **Current scope**: **All accounts** and the number of
member accounts. In public preview, organization defaults apply to all member accounts. Selecting a subset of accounts
is coming soon.

## Review scanner packages

The **Manage Scanner Packages** table lists scanner packages provided by Snowflake. It doesn’t list packages from
[Trust Center extensions](/user-guide/trust-center/trust-center-extensions) that third-party security partners provide.
Trust Center scanners can be provided by Snowflake or by third-party security partners. For more information, see
[Trust Center organization-level configuration procedures](/sql-reference/trust_center/trust-center-org-config). In
public preview, all member accounts run these Snowflake packages using organization defaults unless a local
administrator changes settings in a member account.

Each row includes the following:

- **NAME**: The package name. Availability depends on your edition and entitlements. Snowflake packages can include
  [CIS Benchmarks](/user-guide/trust-center/overview#label-cis-benchmarks-scanner-package),
  [Security Essentials](/user-guide/trust-center/overview#label-security-essentials-scanner-package),
  [Threat Intelligence](/user-guide/trust-center/overview#label-threat-intelligence-scanner-package), and
  [AI Security](/user-guide/trust-center/overview#label-ai-security-scanner-package).
- **SCANNERS**: Two counts with status indicators for scanners in that package.
- **Configure**, which opens a side panel for that package. **Configure** can be unavailable when the package is
  turned off as an organization default.
- A toggle that turns the package on or off as an organization default.

## Enable or disable a package or scanner

You can set the organization default for a whole scanner package or for an individual scanner. A scanner-level setting
outranks the package-level setting. For precedence, see
[How organization defaults apply](#label-org-hub-cc-trust-center-how-defaults-apply).

1. In **Manage Scanner Packages**, do one of the following:
   - For the whole package, use the toggle on the package row.
   - For one scanner, select **Configure** on the package row, then use the toggle on that scanner row in the
     **Scanners** tab.
2. Confirm the change:
   - When you turn a package or scanner off, Snowsight shows **Disable organization default?** The message
     explains that you’re turning off the organization default, and that the change applies to all accounts except those
     that have manually overridden the setting at the account level. Select **Disable** or **Cancel**.
   - When you turn a package or scanner on, Snowsight shows **Update organization default?** The message
     explains that the setting becomes the default for all accounts, and that accounts with local configurations already
     in place aren’t affected. Select **Update** or **Cancel**.

After a successful change, Snowsight can show a confirmation, for example **CIS Benchmarks has been disabled**
or **CIS Benchmarks has been enabled.**

## Configure a package or scanner

Use **Configure** to set schedules and notifications at the package level (**Standard schedule** and **Standard
notification**) or on an individual scanner row. Scanner-level schedule and notification settings outrank the package
standard settings for that scanner.

1. In **Manage Scanner Packages**, select **Configure** on a package row.
2. In the side panel, review the package name and status badge (**Enabled** or **Disabled**). If the package is
   disabled, select **Enable** to turn it on as an organization default. Confirm as described in
   [Enable or disable a package or scanner](#label-org-hub-cc-trust-center-toggle).
3. At the package level, review the following:
   - **Scope**: **All accounts** in public preview. Selecting a subset of accounts is coming soon.
   - **Standard schedule**, for example a daily time in UTC. Select the edit control to change the package default.
   - **Standard notification**. If none is configured, the panel can show that no notification is set up for this
     scanner. Select the edit control to change the package default.
   - A description of what the package evaluates and **Source**, for example Snowflake.
4. Use the tabs to review the following:
   - **Scanners**: Individual checks in the package. Each row can include an info control, a toggle, a schedule such as
     **Daily**, and a notification setting such as **No notification set**. Use the toggle to enable or disable that
     scanner as described in [Enable or disable a package or scanner](#label-org-hub-cc-trust-center-toggle). Select the
     edit control on the row to change that scanner’s schedule or notification.
   - **Unsynced accounts**: Accounts whose effective settings don’t match the organization default yet, including
     accounts that still have a local override. The table can list **Accounts**, **Scanners**, **Schedule** (for example
     **Custom** or **Daily**), **Notification** (for example **Custom** or **Off**), and **Status** (for example
     **Disabled**).
   - **Synced accounts**: Accounts that are using the organization default.

## Account-level overrides

An administrator in a member account can still change scanner package and scanner settings in that account. Those local
settings outrank the organization default. Turning an organization default on or off for a package or a scanner doesn’t
change accounts that already have a local configuration.

For account-level scanner package steps, see
[Manage scanner packages](/user-guide/trust-center/using-the-trust-center#label-trust-center-managing-scanners).

## Review coverage in Insights

After you set organization defaults, use [Organization Hub Insights](/user-guide/organization-hub-insights) to review
scanner package coverage and related Trust Center rollups across accounts so you can spot accounts that are out of sync
with the baseline you expect.

## Access control requirements

Organization Trust Center Configuration in Command Center requires the GLOBALORGADMIN role. ORGANIZATION\_USAGE
application roles can open [Insights](/user-guide/organization-hub-insights), but they can’t open Command Center or this
tile.
