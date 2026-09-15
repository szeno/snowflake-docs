# Getting started with Snowflake App Runtime

Install [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli) or
[Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop/building-apps)
and the Snowflake CLI, then deploy your first app. Use Cortex Code to build
from a description, or the Snowflake CLI if you already have code.

## Set up your environment

Before you can build or deploy, install **Cortex Code** (CLI or Desktop) and the
**Snowflake CLI** on your machine. Use the install guides below, then confirm the
Snowflake Apps command surface in the next section.

### Cortex Code

Use [Cortex Code](/user-guide/cortex-code/cortex-code) CLI or Desktop to scaffold,
test, and deploy apps from natural language. Both bundle the [`snowflake-apps`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-snowflake-apps)
skill and use the Snowflake CLI for deployment.

**Cortex Code CLI** (macOS, Linux, and Windows):

- **Install and connect**: [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli)
  (including Windows instructions)
- **Custom skills and extensions**: [CoCo CLI extensibility](/user-guide/cortex-code/extensibility)

**Cortex Code Desktop** (macOS and Windows):

- **Install and sign in**: [Installation, onboarding, and authentication](/user-guide/cortex-code/cortex-code-desktop/onboarding-and-authentication)
- **Build and deploy Snowflake App Runtime apps**: [Building apps](/user-guide/cortex-code/cortex-code-desktop/building-apps)
  (starter card, in-IDE live preview, Apps view, and `snow app deploy`)
- **Product overview**: [Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop)

### Snowflake CLI

Install the Snowflake CLI using [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation).

Confirm you’re on the latest version with
[`snow helpers check-version`](/developer-guide/snowflake-cli/command-reference/helpers-commands/check-version):

Copy code

```
snow helpers check-version
```

If that command isn’t recognized, your CLI is too old: follow the installation
guide and upgrade. The command reports the version you have, the latest
published version, and whether an upgrade is available.

### Other requirements

- **Snowflake account**: Use a paid account ([trial accounts](/user-guide/admin-trial-account)
  don’t support App Runtime).
- **Shared deploy defaults (recommended for team apps)**: For apps you plan to
  share, ask an account administrator to complete
  [account administrator setup](/developer-guide/snowflake-app-runtime/account-admin-setup)
  once, so deploys land in a shared database the whole team can use. Before those
  defaults are configured, you can deploy to your
  [personal database](/user-guide/personal-databases) to build and experiment; you
  just can’t grant other roles access to apps there.
- **Node.js 22+**: Version **22** or later on your machine for local development
  (`npm install`, tests, `npm run dev`). [Download Node.js](https://nodejs.org/en/download).

## Build and deploy with Cortex Code

Cortex Code assistants scaffold, build, test, and deploy Snowflake apps from a
natural language description.

### Step 1: Describe your app

Cortex Code CLICortex Code Desktop

Use the [`snowflake-apps`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-snowflake-apps)
skill in your prompt:

```
> $snowflake-apps Build me a warehouse monitor that shows all my
  warehouses with their current state, credit usage today, and queued
  queries.
```

In chat, type `/`, select **snowflake-apps**, and describe what you want to
build. See [entry points](/user-guide/cortex-code/cortex-code-desktop/building-apps#label-cortex-code-desktop-building-apps-entry-points)
for other ways to start.

```
/snowflake-apps Build me a warehouse monitor that shows all my
warehouses with their current state, credit usage today, and queued
queries.
```

The assistant scaffolds a Next.js project with a working UI, Snowflake data
access, and an [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml)
manifest.

### Step 2: Test locally

Ask the assistant to run the dev server and open the app in your browser. In
Cortex Code Desktop, the **Agent Browser** shows a
[live preview](/user-guide/cortex-code/cortex-code-desktop/building-apps#label-cortex-code-desktop-live-preview)
as you go. Describe changes in chat to update the app.

```
Run the dev server and open it in my browser
```

### Step 3: Deploy

When you’re happy with the app:

```
Deploy this app
```

The assistant runs `snow app deploy`, which runs the full upload, build, and
deploy pipeline. You get a live URL when the deploy phase completes.

### Step 4: Open the app

```
Open the app
```

Ask the assistant to open the app, or use the URL from deploy output. In Cortex
Code Desktop, you can also use the **Apps** view. The URL uses Snowflake SSO.

### Step 5: Share with other roles

To let other roles open your app, ask the assistant to share it. The app must
live in a standard database (for example `SNOWFLAKE_APPS` after
[account administrator setup](/developer-guide/snowflake-app-runtime/account-admin-setup)),
not a personal database.

```
Share this app with the ANALYST role
```

In Cortex Code Desktop, you can also use **Share** on the app in the **Apps**
view.

Behind the scenes, this grants `USAGE` on the database, schema, and Application
Service. To run it yourself (replace `MY_APP_NAME` and `ANALYST` with your
service name and role):

Copy code

```
GRANT USAGE ON DATABASE SNOWFLAKE_APPS TO ROLE ANALYST;
GRANT USAGE ON SCHEMA SNOWFLAKE_APPS.PUBLIC TO ROLE ANALYST;
GRANT USAGE ON APPLICATION SERVICE SNOWFLAKE_APPS.PUBLIC.MY_APP_NAME TO ROLE ANALYST;
```

For `OPERATE`, `MONITOR`, and revoke patterns, see
[Access control for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/access-control).

### Step 6: Iterate

Make changes and redeploy. Each deploy produces a new package version and
alters the running service in place. The URL stays the same.

```
Add a filter for warehouse state and redeploy
```

## Build and deploy with the CLI

If you have an existing application or prefer working directly with code, use
the Snowflake CLI. Cortex Code isn’t required for this path.

### Step 1: Initialize your project

From your project directory, run `snow app setup` to generate an
[`app.yml`](/developer-guide/snowflake-app-runtime/app-yml)
manifest:

Copy code

```
snow app setup
```

Pass `--app-name my_app_name` when you want an explicit Snowflake identifier
instead of the name derived from the current directory. To target a specific
destination, pass `--database`, `--schema`, or `--warehouse`. Setup writes those
values into `app.yml` as explicit overrides.

This creates an `app.yml` in the current directory that uses defaults from
[account administrator setup](/developer-guide/snowflake-app-runtime/account-admin-setup).
After setup, the file typically references the shared `SNOWFLAKE_APPS` database.
Leave `code_stage` and `code_workspace` unset unless you need to pin a backend;
the CLI picks a workspace or stage at deploy time. For example:

Copy code

```
version: 2

name: MY_APP_NAME
database: SNOWFLAKE_APPS
schema: PUBLIC
query_warehouse: SNOWFLAKE_APPS_QUERY_WH

ignore:
  - node_modules
  - .env*
  - __pycache__
  - "*.pyc"
  - .next
  - .git
  - snowflake.log
```

Setup resolves `database`, `schema`, and `query_warehouse` in this order: the
explicit `--database`, `--schema`, and `--warehouse` options; then account
defaults from administrator setup; then the personal database default (when
account defaults aren’t set). After account setup, you normally don’t pick
these manually. `app.yml` does **not** fill an unset `database` from the
active CLI connection. The `ignore` list excludes build output and local-only
files from upload.

Run with `--dry-run` to preview the resolved configuration without writing
the file.

If the project already has a `snowflake.yml`, see
[Migrate from snowflake.yml to app.yml](/developer-guide/snowflake-app-runtime/migrate-to-app-yml). Named `targets`
are optional; add them when one project needs more than one deploy
configuration, whether that’s a development, stage, and production lifecycle,
several accounts with slightly different configuration, or variants of the app
for different audiences. For a walkthrough, see
[Deploy targets](/developer-guide/snowflake-app-runtime/deploy-targets). For the
`snow app setup` options, see the
[snow app setup](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/setup)
command reference.

### Step 2: Deploy

From your project directory:

Copy code

```
snow app deploy
```

The CLI runs the full `snow app deploy` pipeline: upload, build, and deploy.
When the deploy phase finishes, it prints the live Application Service URL. The
URL looks
like:

```
https://<id>-<org>-<account>-<region>.snowflakecomputing.app/
```

This URL is stable across redeploys. It doesn’t change when you deploy a
new package version.

### Step 3: Open your app

Copy code

```
snow app open
```

Use `snow app open --print-only` to print the URL without opening a browser.
Use `snow app open --settings` to open the app in Snowsight instead of the live
endpoint.

### Step 4: Share with other roles

Grant `USAGE` on the database, schema, and Application Service so another role
can open the app. Use the database and schema from your `app.yml` (for example
`SNOWFLAKE_APPS.PUBLIC`):

Copy code

```
GRANT USAGE ON DATABASE SNOWFLAKE_APPS TO ROLE ANALYST;
GRANT USAGE ON SCHEMA SNOWFLAKE_APPS.PUBLIC TO ROLE ANALYST;
GRANT USAGE ON APPLICATION SERVICE SNOWFLAKE_APPS.PUBLIC.MY_APP_NAME TO ROLE ANALYST;
```

You can’t share apps deployed to a personal database. For more patterns, see
[Access control for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/access-control).

## What deploy does

[`snow app deploy`](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/deploy)
uploads source, builds remotely, and creates or alters the Application
Service. See
[Deploying with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/deploy)
for build infrastructure, artifact repository storage, egress, and phase details.

If a deploy fails partway through, retry one phase with `--upload-only`,
`--build-only`, or `--promote-only`. See
[Retrying a failed deploy](#label-getting-started-retry-deploy).

With [account administrator setup](/developer-guide/snowflake-app-runtime/account-admin-setup)
complete, `snow app setup` and `snow app deploy` use shared destination defaults.
You focus on application code; Snowflake handles packaging and service lifecycle.

## Query Snowflake from your app

After you have a live URL, your app can query Snowflake with no credentials
to manage. The `snowflake-apps` skill adds `lib/snowflake.ts`, which wraps
the driver; call `querySnowflake` from that module to run SQL.

For owner’s rights versus caller’s rights and caller grants, see
[Query Snowflake](/developer-guide/snowflake-app-runtime/query-snowflake). For what Snowflake
injects into the running app, see
[Runtime environment](/developer-guide/snowflake-app-runtime/runtime-environment). For how to design
those queries and secrets so they stay least-privilege, see
[Developing secure Snowflake App Runtime applications](/developer-guide/snowflake-app-runtime/secure-development).

## Other CLI commands

Beyond `snow app setup`, `snow app deploy`, and `snow app open`, the
CLI provides additional commands for managing your app lifecycle:

| Command | Description |
| --- | --- |
| `snow app validate` | Check that the target database and schema exist and that the project can be bundled. Use `--target` when `app.yml` defines named targets. |
| `snow app bundle` | Copy resolved artifacts into `output/bundle` so you can inspect what a deploy would upload. No Snowflake connection required. |
| `snow app events` | Fetch observability streams for the Application Service. Default is recent container logs (`--type log`, 500 lines, capped at 100 KB). Use `--type metric` or `--type lifecycle` for event-table telemetry, and `--since` / `--until` for a time window. See [Observability for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/observability). |
| `snow app teardown` | Drop the Application Service and clean up associated objects (stage or workspace files). Use `--force` to skip the confirmation prompt. |

Expand

Show lessSee more

### Retrying a failed deploy

If `snow app deploy` fails partway through, you can retry just the phase
that failed instead of starting over:

- `snow app deploy --upload-only`: re-upload source files without rebuilding
  or redeploying.
- `snow app deploy --build-only`: re-trigger the build without re-uploading
  or redeploying.
- `snow app deploy --promote-only`: create or alter the service without
  re-uploading or rebuilding. (`--deploy-only` is a deprecated alias.)

Only one of these flags can be used at a time.
