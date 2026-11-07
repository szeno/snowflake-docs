# Account administrator setup for Snowflake App Runtime

We recommend that an account administrator complete Snowsight **App Development
Setup** once per account. Setup sets account-level defaults for where apps deploy
and grants the roles you choose permission to build and deploy. It points
`snow app setup` and `snow app deploy` at a destination database, schema, and query
warehouse, so your team’s apps land in a shared database from the start.

Setup configures **deploy destination** defaults. It does not change where the
build job runs, how artifact repositories are provisioned, or default build
egress. See
[Deploying with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/deploy).

Until an administrator completes setup,
[`snow app setup`](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/setup)
and
[`snow app deploy`](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/deploy)
deploy to a [personal database](/user-guide/personal-databases). You can build and
test apps there, but you can’t grant other roles access to them.

After setup, those same CLI commands use the destination database, schema, and
warehouse you configure here. Quick start uses the `SNOWFLAKE_APPS` database,
`PUBLIC` schema, and `SNOWFLAKE_APPS_QUERY_WH` warehouse.

[Preview Feature](/release-notes/preview-features) — Open

The App Runtime admin page is in preview. Features and workflows might change before general availability.

## Prerequisites

- A paid Snowflake account (not a
  [trial account](/user-guide/admin-trial-account)).
- A role that can change account settings, usually `ACCOUNTADMIN`.

## Open the App Runtime page

In Snowsight, select **Apps** in the navigation menu, then select **App Runtime admin**.

![Snowsight navigation menu with Apps selected and App Runtime admin shown in the submenu](/static/images/screens/snowflake-apps-admin-setup-nav-menu.png)

On the App Runtime page, select **Settings** in the page header. The **Settings**
button appears only for users with the `ACCOUNTADMIN` role.

![App Runtime page header showing the Settings button](/static/images/screens/snowflake-apps-admin-setup-settings-button.png)

If setup hasn’t run yet, the Settings panel shows **App development is not set up** and a
**Begin Setup** button.

![Settings panel showing App development is not set up and the Begin Setup button](/static/images/screens/snowflake-apps-admin-setup-begin-setup.png)

## Run App Development Setup

Select **Begin Setup** to open **App Development Setup**.

### Choose roles

Under **What roles will be making apps?**, select every role that should build
and deploy apps (for example `PRODUCT_MANAGER` and `DATA_ENGINEER`).

![App Development Setup dialog with Selected roles chosen and DATA_ENGINEER and PRODUCT_MANAGER listed under Who will be making apps, with the Resources section collapsed](/static/images/screens/snowflake-apps-admin-setup-choose-roles.png)

Until at least one role is selected, **Preview SQL** stays disabled.

### Choose resources

Expand **Resources** and pick **Quick start** or **Custom**.

**Quick start** creates new objects with recommended defaults:

- **Destination database**: `SNOWFLAKE_APPS`
- **Destination schema**: `PUBLIC`
- **Query warehouse**: `SNOWFLAKE_APPS_QUERY_WH`

Snowsight also sets account defaults so `snow app setup` and deploy resolve to
these objects.

![App Development Setup dialog with Selected roles set to DATA_ENGINEER and PRODUCT_MANAGER, Quick start selected, and SNOWFLAKE_APPS, PUBLIC, and SNOWFLAKE_APPS_QUERY_WH filled in](/static/images/screens/snowflake-apps-admin-setup-quick-start-filled.png)

**Custom** uses databases, schemas, and warehouses you already have. Pick values
from the dropdowns for destination database, destination schema, and query
warehouse.

![App Development Setup with Custom selected, showing Use existing resources from your Snowflake account and destination database, schema, and query warehouse dropdowns](/static/images/screens/custom-resources.png)

### Preview and run setup

Select **Preview SQL** to open the statements Snowsight will run. The list
includes `CREATE` for the database, schema, and warehouse; `ALTER ACCOUNT SET`
for default destination and query warehouse; and `GRANT` for each role you chose.

![Preview SQL view of App Development Setup showing CREATE, ALTER ACCOUNT SET, and GRANT statements, with Cancel, Back, and Execute Setup buttons](/static/images/screens/snowflake-apps-admin-setup-review-sql.png)

Select **Execute Setup** to apply the configuration. Use **Back** to return and
change roles or resources.

## After setup

The **Settings** panel on the App Runtime page shows two sections you can change later with **Update**:

1. **Destination database**, **Destination schema**, and **Query warehouse**
   (defaults for where apps are stored and which warehouse runs in-app queries).
2. **Roles with access** (roles that can create apps using those defaults).

![App Runtime Settings panel after setup with destination database SNOWFLAKE_APPS, schema PUBLIC, query warehouse SNOWFLAKE_APPS_QUERY_WH, and roles with access](/static/images/screens/snowflake-apps-admin-setup-complete.png)

When setup finishes, send developers to
[Getting started with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/getting-started).

## Restrict app creation in personal databases

Until an administrator completes **App Development Setup**,
[`snow app deploy`](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/deploy)
deploys to the calling user’s [personal database](/user-guide/personal-databases).
If your account policy doesn’t permit users to create apps in personal databases,
use a [feature policy](/sql-reference/sql/create-feature-policy) to block the
underlying object types.

The following example creates a feature policy that blocks App Runtime object
types and attaches it to every personal database in the account:

Copy code

```
CREATE FEATURE POLICY block_apps_in_pdb
  BLOCKED_OBJECT_TYPES_FOR_CREATION = (APPLICATION_SERVICES, ARTIFACT_REPOSITORIES);

ALTER ACCOUNT SET FEATURE POLICY block_apps_in_pdb FOR ALL PERSONAL DATABASES;
```

After you set the policy, attempts to create an Application Service or Artifact
Repository in a personal database fail. Users can still build and deploy apps to
the shared destination database you configure with **App Development Setup**.

To remove the restriction, unset the policy:

Copy code

```
ALTER ACCOUNT UNSET FEATURE POLICY FOR ALL PERSONAL DATABASES;
```

For details about feature policy syntax and lifecycle, see
[CREATE FEATURE POLICY](/sql-reference/sql/create-feature-policy),
[ALTER FEATURE POLICY](/sql-reference/sql/alter-feature-policy), and
[ALTER ACCOUNT](/sql-reference/sql/alter-account).

## See also

- [Snowflake App Runtime privileges](/developer-guide/snowflake-app-runtime/privileges): privileges for deploy, sharing, and operations
- [Access control for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/access-control): grant `USAGE`, `OPERATE`, and `MONITOR` on deployed apps
- [Securing Snowflake App Runtime applications](/developer-guide/snowflake-app-runtime/security): caller grant restrictions, feature policies, and external access controls
- [Snowflake App Runtime limitations](/developer-guide/snowflake-app-runtime/limitations): known limits
