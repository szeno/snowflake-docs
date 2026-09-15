# Third party (publisher–subscriber) accounts

Feature — Generally Available

Currently available in all commercial cloud regions. Some capabilities aren’t available to organizations with a presence in a [U.S. government region](/user-guide/intro-regions#label-us-gov-regions); see [Legal and contractual notice](#label-third-party-legal-notice).

Note

Access and use of this feature is subject to the [Snowflake Customer-Controlled Data Sharing Functionality Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/data-sharing-terms/).

Snowflake has long supported giving organizations a way to grant access to *third parties*. In this document, a *third party* is a business
partner or other organization outside your own company that uses its own Snowflake account to work with data you share, as distinct from your
users on internal accounts. One option is [reader accounts](/user-guide/data-sharing-reader-create), which have intentional limits (for example, reader account users typically can’t
load their own data or create tables in the same way as a regular Snowflake account). Many organizations need fully functional Snowflake
accounts for *third parties*, still governed and managed by the publisher organization, so those parties can combine shared data with their own
data for analytics, applications, or supply-chain style collaboration.

The third-party account feature capabilities described in the following sections provide a toolset for streamlined governance and monitoring of access to
internal and external tenant accounts, which supports a stronger security posture for your organization.

## Core capabilities

### Tenant type

- Set an account tenant type (`INTERNAL` or `EXTERNAL`) to distinguish your organization’s users from third-party accounts.
- Set a default tenant type for all newly created accounts. The value can be `INTERNAL` or `EXTERNAL` (for example, by setting the organization default for new accounts).

### Domain names

- Maintain an allowlist of email domains for users of all internal accounts for the entire organization.
- Maintain an allowlist of email domains for users of each external account.

### Risk exposure via Trust Center

Snowflake scans user login emails for each account, validates them against the configured domain allowlists, and sends notifications through the
Trust Center when the [Security Essentials scanner package](/user-guide/trust-center/overview#label-security-essentials-scanner-package) is enabled.

Together, these controls help organizations that provide third-party applications and data sharing services manage access more systematically
and proactively detect violations, which improves your organization’s security posture.

## Legal and contractual notice

Important

Creating accounts with tenant type `EXTERNAL` requires acceptance of [Snowflake Customer-Controlled Data Sharing Functionality Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/data-sharing-terms/). If you get an error when trying to set
a tenant type, you may need to accept these terms. Contact your Snowflake account team for assistance.

Setting tenant type `EXTERNAL` isn’t available to organizations with a presence in a U.S. government region. This restriction applies across the organization, including accounts in commercial regions.

Tenant type and allowed domain values are stored as account and organization metadata. Follow your own data governance practices for metadata,
consistent with [metadata fields in Snowflake](/sql-reference/metadata).

## Concepts

The following table summarizes the main concepts for tenant types and domain allowlists:

| Concept | Description |
| --- | --- |
| Tenant type configuration for accounts | A property of an account: `INTERNAL` (for your organization’s users) or `EXTERNAL` (for third-party tenants). If not specified at creation, the default is `INTERNAL`. |
| Default tenant type for new accounts | When tenant type is not explicitly configured at the organization level, new accounts default to `INTERNAL`. Your organization can set a different default tenant type for new accounts. |
| Allowlist of email domains for internal users | A list of email domains associated with all internal accounts in your organization. Snowflake uses it when validating users who access internal accounts. |
| Allowlist of email domains for external users | A list of email domains defined for each external (third-party) account. Snowflake uses it when validating users who access each external account. |

Expand

Show lessSee more

Note

Snowflake terms of service require each external tenant (that is, each third-party customer or subscriber entity) to have its own account.

For background on how Snowflake organizations manage accounts, see [Introduction to organizations](/user-guide/organizations) and [Organization administrators](/user-guide/organization-administrators).

## Privileges and roles

Users with the `GLOBALORGADMIN` role in the [organization account](/user-guide/organization-accounts) or the `ORGADMIN` role in an
ORGADMIN role-enabled account can manage tenant type and allowed domains using the SQL summarized in the following sections. `ACCOUNTADMIN` can’t change
`TENANT_TYPE`; that action is limited to organization administrators and to roles that have been granted the `MANAGE TENANTS` privilege in the
organization account.

To delegate this work, grant the `MANAGE TENANTS` privilege to a custom role using [GRANT … TO ROLE](/sql-reference/sql/grant-privilege).
Confirm the supported securable scope for `MANAGE TENANTS` in [Access control privileges](/user-guide/security-access-control-privileges) and in
[GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) for your release (for example, `ON ACCOUNT` compared with organization-scoped syntax).

For example, from the organization account context and using a role that can grant account privileges:

Copy code

```
USE ROLE GLOBALORGADMIN;

GRANT MANAGE TENANTS ON ACCOUNT TO ROLE tenant_operations;
```

## SQL commands

Use the SQL command reference for authoritative syntax, required roles, and usage notes. The examples in the following sections summarize the properties
discussed here.

For other [ALTER ACCOUNT](/sql-reference/sql/alter-account) operations on the current account compared with the organization account, see
that command’s reference page. Tenant type can be changed only by using `ALTER ACCOUNT` as described in the following sections, from the
organization account or an ORGADMIN role-enabled account.

### View tenant type and external account domain information

[SHOW ACCOUNTS](/sql-reference/sql/show-accounts) output includes tenant type, allowed domain names for external accounts, and other
account fields that reflect tenant type and domain configuration.

[SHOW MANAGED ACCOUNTS](/sql-reference/sql/show-managed-accounts) output can include tenant type, allowed domain information, and other
fields for managed-account scenarios, depending on your account configuration.

### View allowed domains for the organization

`SYSTEM$SHOW_ORGANIZATION` returns organization details, including the allowlist of email domains for all internal accounts in your organization
and the default tenant type, when it is configured. Invoke it as a system function (for example, with `CALL` or `SELECT`), following the
pattern for other `SYSTEM$` helpers in [System functions](/sql-reference/functions-system).

Copy code

```
CALL SYSTEM$SHOW_ORGANIZATION();
```

For arguments, return values, required privileges, and any optional parameters, see the `SYSTEM$SHOW_ORGANIZATION` entry on
[System functions](/sql-reference/functions-system) (or the matching function topic for your Snowflake release).

### Create an account with a tenant type

[CREATE ACCOUNT](/sql-reference/sql/create-account) supports an optional tenant type:

Copy code

```
CREATE ACCOUNT <name>
  ADMIN_NAME = '<string_literal>'
  ADMIN_PASSWORD = '<string_literal>'
  EMAIL = '<string_literal>'
  EDITION = { STANDARD | ENTERPRISE | BUSINESS_CRITICAL }
  [ TENANT_TYPE = { INTERNAL | EXTERNAL } ];
```

If `TENANT_TYPE` is omitted, it defaults to `INTERNAL`, or to the organization default tenant type (`DEFAULT_TENANT_TYPE`) when your organization has configured one.

Note

For external accounts only, you can specify allowed domain names as part of the `CREATE ACCOUNT` syntax. See the [CREATE ACCOUNT](/sql-reference/sql/create-account) reference for your release.

For internal accounts, email domain allowlists are configured at the organization level and apply to all internal accounts; they are not set in `CREATE ACCOUNT`.

Only organization administrators can run `CREATE ACCOUNT`. The command reference lists all parameters (for example, region and key-pair
administration).

### Change tenant type on an existing account

`TENANT_TYPE` is an account property on [ALTER ACCOUNT](/sql-reference/sql/alter-account). `ACCOUNTADMIN` can’t update tenant type,
not for the account they administer and not by signing in to another account. Tenant type is set only by organization-level authority: users
with the `GLOBALORGADMIN` or `ORGADMIN` role (as described in the **Privileges and roles** section) or by custom roles that have been granted the `MANAGE TENANTS` privilege.

Those users run `ALTER ACCOUNT` using the syntax for altering a different account, from a context where they have the required organization
administrator privileges. Specify the target account with `<name>` as defined in [ALTER ACCOUNT](/sql-reference/sql/alter-account) and
[account identifiers](/user-guide/admin-account-identifier) from the organization account or an ORGADMIN role-enabled account:

Copy code

```
ALTER ACCOUNT <name> SET TENANT_TYPE = INTERNAL;

ALTER ACCOUNT <name> SET TENANT_TYPE = EXTERNAL;
```

For full syntax and privileges, see [ALTER ACCOUNT](/sql-reference/sql/alter-account).

### Set organization-level default tenant type and internal domain allowlists

From the organization account (or another context where you have organization administrator privileges), you can set the default tenant type
for new accounts and manage the allowlist of email domains for users of internal accounts. The default tenant type when one is not explicitly
configured is `INTERNAL`, but your organization can change the configured default to `EXTERNAL` based on account creation workflows (see `DEFAULT_TENANT_TYPE` in the command reference). All new
accounts use the configured default tenant type when tenant type is not explicitly provided at account creation time.

Provide domain names as a list of string literals (see the examples).

Copy code

```
ALTER ORGANIZATION SET DEFAULT_TENANT_TYPE = EXTERNAL;

ALTER ORGANIZATION SET DOMAIN_NAMES = ('domain1.com','domain2.org');

ALTER ORGANIZATION UNSET DOMAIN_NAMES;
```

Note

Each time you run `ALTER ORGANIZATION SET DOMAIN_NAMES`, it overrides `DOMAIN_NAMES` that were previously set for the organization. The statement sets the full list and does not append to an earlier list.

### Set or clear allowed domain names for external accounts

Provide domain names as a list of string literals (see the examples).

Copy code

```
ALTER ACCOUNT <account_name> SET DOMAIN_NAMES = ('domain1.com','domain2.org');

ALTER ACCOUNT <account_name> UNSET DOMAIN_NAMES;
```

Note

Each time you run `ALTER ACCOUNT … SET DOMAIN_NAMES` for an account, it overrides `DOMAIN_NAMES` that were previously set for that account. The statement sets the full list and does not append to an earlier list.

For full syntax and privileges, see [ALTER ACCOUNT](/sql-reference/sql/alter-account).

Note

This command can be executed only from the organization account or the ORGADMIN role-enabled account by users with the `GLOBALORGADMIN` or
`ORGADMIN` role, or by users with the `MANAGE TENANTS` privilege.

## Operational visibility

For organization-wide usage and security monitoring, you can use:

- [Organization Usage](/sql-reference/organization-usage) views in the shared `SNOWFLAKE` database (latency and access requirements are
  documented per view).
- [Trust Center](/user-guide/trust-center/overview), where available for your account.

## Comparison with reader accounts

| Topic | Reader accounts | Publisher–subscriber (third-party) accounts (this feature) |
| --- | --- | --- |
| Typical use | Consumption-focused access with provider-controlled limits | Full-account workloads where the third party loads and combines their own data |
| Documentation | [Configure a reader account](/user-guide/data-sharing-reader-config), [Manage reader accounts](/user-guide/data-sharing-reader-create) | This topic (tenant type and allowed domains) |
| Contractual or legal | Requires acceptance of the [Snowflake Customer-Controlled Data Sharing Functionality Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/data-sharing-terms/) | Requires acceptance of the [Snowflake Customer-Controlled Data Sharing Functionality Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/data-sharing-terms/) |

Expand

Show lessSee more

## Configure tenant types and domains in Command Center

In preview, you can classify member accounts and maintain allowed email domains from Organization Command Center in the
organization account. For the Snowsight steps, see
[Organization Command Center](/user-guide/organization-hub-command-center) and
[Command Center 3rd party access configuration](/user-guide/organization-hub-command-center-third-party).

## Related Snowflake documentation

- [Introduction to organizations](/user-guide/organizations)
- [Organization administrators](/user-guide/organization-administrators)
- [Organization Command Center](/user-guide/organization-hub-command-center)
- [Command Center 3rd party access configuration](/user-guide/organization-hub-command-center-third-party)
- [User management](/user-guide/admin-user-management)
- [CREATE ACCOUNT](/sql-reference/sql/create-account)
- [ALTER ACCOUNT](/sql-reference/sql/alter-account)
- [SHOW ACCOUNTS](/sql-reference/sql/show-accounts)
- [SHOW MANAGED ACCOUNTS](/sql-reference/sql/show-managed-accounts)
- [Access control privileges](/user-guide/security-access-control-privileges)
- [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege)
- [Data sharing and collaboration in Snowflake](/guides-overview-sharing)
- [Configure a reader account](/user-guide/data-sharing-reader-config)
- [Organization Usage](/sql-reference/organization-usage)
- [System functions](/sql-reference/functions-system)
- [Behavior change management](/release-notes/bcr-bundles/managing-behavior-change-releases)
- [Snowflake Customer-Controlled Data Sharing Functionality Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/data-sharing-terms/)

## Getting help

If you need help with errors, enablement, or contractual questions, contact your Snowflake account team or [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) according to
your support agreement.
