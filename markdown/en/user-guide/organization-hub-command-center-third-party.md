# Command Center 3rd party access configuration

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Use **3rd party access configuration** in Organization Command Center to classify member accounts as internal or
external, set the default tenant type for new accounts, and maintain allowed email domains. Logins from domains that
aren’t on the allowlist can raise Trust Center security violations.

For concepts, tenant types, privileges, SQL, and
[legal and contractual limits](/user-guide/third-party-publisher-subscriber-accounts#label-third-party-legal-notice),
see [Third party (publisher–subscriber) accounts](/user-guide/third-party-publisher-subscriber-accounts).

## Before you begin

Confirm the following:

- You can sign in to the [organization account](/user-guide/organization-accounts) with the GLOBALORGADMIN role.

## Open 3rd party access configuration

1. Use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to sign in to the organization account.
2. Switch to the GLOBALORGADMIN role.
3. In the navigation menu, select **Organization Hub** » **Command center**.

On the Command Center landing page, the **3rd party access configuration** tile shows how many organization domains you
have configured and how many accounts are still unassigned. Unassigned accounts can appear with a **Needs attention**
indicator and a **Categorize accounts** action.

4. Select the **3rd party access configuration** tile.

On the configuration page, breadcrumbs read **Organization command center** » **3rd party access configuration**.
The page title is **3rd party access configuration**. **View all accounts** opens the organization account list. The
**Guides** panel includes **Third party accounts**.

A banner on the page notes that starting in August 2026, Snowflake sends notifications for violations that depend on
this configuration. Set tenant types and domain names so those notifications match how your organization classifies
access.

## Organization access configuration for internal accounts

This card summarizes internal coverage (for example, internal account count and organization domain count) and contains
the following controls.

### Set the default tenant type for new accounts

The card shows the current default (Internal or External) and notes that existing accounts aren’t affected.

1. Select **Set default**.
2. Under **Select default tenant type for new accounts**, choose one of the following:
   - **Internal**: New accounts default to internal, typically for employees with full access. Existing accounts stay
     unchanged.
   - **External**: New accounts default to external, typically for third-party customers with more limited access.
     Existing accounts stay unchanged.
3. Select **Save** or **Cancel**.

After a successful save, Snowsight can show **Organization default tenant type updated**.

### Manage internal accounts and allowed domains

This section lets you specify domains authorized for all internal accounts you select. Logins from unlisted domains on
those accounts can trigger a Trust Center security violation.

The table lists **Scope** (for example, **All internal accounts** and a count) and **Allowed domains**.

1. Select **Manage**.
2. In **Internal accounts & allowed domains**, enter domain names separated by commas.
3. Under **Select accounts to configure as internal**, use **All** or **Selected**, search, and filters (**Cloud**,
   **Region**, **Allowed domains**) to choose accounts. A count shows how many accounts are selected.
4. Optionally select **Download account list (.csv)** to review accounts offline, then confirm selections in the UI.
5. Select **Save** or **Cancel**.

After a successful save, Snowsight can show **Organization allowed domains and tenant type settings updated**.

## Access configuration for external accounts

This card summarizes external coverage, including how many external accounts have no allowed domains yet. Flag accounts
as external first, then add the domains authorized for each external account.

The table lists **Scope** (one account or a group of accounts) and **Allowed domains**. Each row has **Edit**.

1. Select **Manage**, or select **Edit** on a row to change that grouping.
2. In **Allowed domains for external accounts**, enter domain names separated by commas.
3. Under **Select accounts to configure as external**, use search and filters. For a first-time pass across many
   accounts, use **Select all unassigned** when that control is available.
4. If you reclassify an account from internal to external, Snowsight warns that the change can affect user
   access in that account. Confirm before you save.
5. Optionally select **Download account list (.csv)**.
6. Select **Save** or **Cancel**.

After a successful save, Snowsight can show **Account domain and tenant type settings updated**.

## What to do next

After you set tenant types and domains, review related findings in [Trust Center](/user-guide/trust-center/overview).
Domain-allowlist notifications depend on the
[Security Essentials scanner package](/user-guide/trust-center/overview#label-security-essentials-scanner-package).
Account administrators still remediate some issues in member accounts.

For SQL, privileges, and
[legal and contractual limits](/user-guide/third-party-publisher-subscriber-accounts#label-third-party-legal-notice)
(including organizations with a U.S. government region presence), see
[Third party (publisher–subscriber) accounts](/user-guide/third-party-publisher-subscriber-accounts).
