# Get started with Snowflake App Runtime

Build an app, deploy it, and share it with other roles. Follow the guide for
the way you want to build:

- [Snowsight Workspaces](#label-getting-started-workspaces) (Public Preview):
  build in the browser with nothing to install.
- [Cortex Code](#label-getting-started-cortex-code-path): describe the app, and
  the agent builds, tests, and deploys it.
- [Snowflake CLI](#label-getting-started-cli-path): deploy code you already have
  with `snow app` commands.

For a guided walkthrough, see the
[Getting started with Snowflake App Runtime quickstart](https://www.snowflake.com/en/developers/guides/getting-started-with-snowflake-app-runtime).

## Before you begin

- Use a paid Snowflake account.
  [Trial accounts](/user-guide/admin-trial-account) don’t support App Runtime.
- To share apps, ask an account administrator to complete
  [account setup](/developer-guide/snowflake-app-runtime/account-admin-setup)
  once. Until then, you deploy to your
  [personal database](/user-guide/personal-databases), and you can’t share apps
  from there.

Workspaces runs in Snowsight, so there’s nothing to install. To build on your
machine instead, install:

- [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli) or
  [Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop/onboarding-and-authentication),
  if you want the agent to build the app. Both include the
  [`snowflake-apps`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-snowflake-apps)
  skill.
- The [Snowflake CLI](/developer-guide/snowflake-cli/installation), with a
  [connection](/developer-guide/snowflake-cli/connecting/configure-connections).
  If you already have it, run `snow upgrade` to get the latest release.
- [Node.js](https://nodejs.org/en/download) 22 or later for Node.js apps, or
  [Python](https://www.python.org/downloads/) 3.13 for Python apps.

## Build in Snowsight Workspaces

Build, preview, and deploy in the browser. For how preview works and how to
configure it, see [Develop Snowflake App Runtime apps in Snowsight Workspaces](/developer-guide/snowflake-app-runtime/workspaces).

1. In the navigation menu, select **Projects** » **Workspaces**. In the file
   explorer, select **+ Add new** » **Next.js App**, and name the folder.
   To build with an agent, ask
   [Cortex Code in Snowsight](/user-guide/cortex-code/cortex-code-snowsight)
   instead.
2. Select **Preview**. Snowflake installs dependencies and starts a dev server,
   and your edits reload the running app.
3. Select **Deploy**.
4. Open the app at its URL, then [share it](#label-getting-started-cortex-code-share).

To redeploy changes, select **Deploy** again.

## Build with Cortex Code

Describe the app with the
[`snowflake-apps`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-snowflake-apps)
skill:

Cortex Code CLICortex Code Desktop

Name the skill in your prompt:

```
> $snowflake-apps Build me a warehouse monitor that shows my warehouses with their current
  state and credit usage today
```

Type `/` in chat, select **snowflake-apps**, and describe the app, or use the
**Build an app** starter card:

```
/snowflake-apps Build me a warehouse monitor that shows my warehouses with their current
state and credit usage today
```

For other ways to start, see
[entry points](/user-guide/cortex-code/cortex-code-desktop/building-apps#label-cortex-code-desktop-building-apps-entry-points).

Cortex Code creates a Next.js project with a working UI, Snowflake data access,
and an [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml) manifest.
Then continue in chat:

1. Ask it to run the app: `Run the dev server and open it in my browser`. In
   Cortex Code Desktop, the **Agent Browser** shows a
   [live preview](/user-guide/cortex-code/cortex-code-desktop/building-apps#label-cortex-code-desktop-live-preview).
   Describe changes in chat to update the app.
2. Ask it to deploy: `Deploy this app`. Cortex Code runs `snow app deploy` and
   gives you the app’s URL.
3. Ask it to open the app: `Open the app`. In Cortex Code Desktop, you can also
   use the **Apps** view.
4. Ask it to share the app: `Share this app with the ANALYST role`. See
   [Share the app](#label-getting-started-cortex-code-share).

To redeploy changes, describe them and ask Cortex Code to redeploy.

## Build with the Snowflake CLI

1. From your project directory, generate an
   [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml) manifest:

   Copy code

   ```
   snow app setup
   ```

   Setup uses the account defaults from account setup, or your personal
   database if they aren’t set. To choose the destination, pass `--database`,
   `--schema`, or `--warehouse`. To see the result without writing the file,
   pass `--dry-run`. If the project has a `snowflake.yml`, see
   [Migrate from snowflake.yml to app.yml](/developer-guide/snowflake-app-runtime/migrate-to-app-yml).
2. Add the `install`, `build`, and `run` commands for your language. See
   [Build a Node.js app for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/build-nodejs-app) or
   [Build a Python app for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/build-python-app).
3. Run the dev server locally, for example `npm run dev`. To check the project
   before you deploy, run `snow app validate`.
4. Deploy the app. The command prints the app’s URL:

   Copy code

   ```
   snow app deploy
   ```
5. Open the app:

   Copy code

   ```
   snow app open
   ```

To redeploy changes, run `snow app deploy` again.

## Deploy details

A deploy uploads the project, builds it, and starts the app at a URL that stays
the same across redeploys. Each deploy creates a new version. For what each
phase does, see [Deploy an app to Snowflake App Runtime](/developer-guide/snowflake-app-runtime/deploy).

To run the app on [serverless compute](/developer-guide/snowflake-app-runtime/serverless)
(Public Preview), set `compute_resource: SERVERLESS` in `app.yml` before you
deploy.

If a deploy fails, see
[Retry a failed deploy](/developer-guide/snowflake-app-runtime/deploy#label-snowflake-app-runtime-deploy-retry)
and [Troubleshoot Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/troubleshooting).

## Share the app

To let another role open the app, grant it `USAGE` on the database, schema, and
Application Service:

Copy code

```
GRANT USAGE ON DATABASE SNOWFLAKE_APPS TO ROLE ANALYST;
GRANT USAGE ON SCHEMA SNOWFLAKE_APPS.PUBLIC TO ROLE ANALYST;
GRANT USAGE ON APPLICATION SERVICE SNOWFLAKE_APPS.PUBLIC.MY_APP TO ROLE ANALYST;
```

To share from Snowsight instead:

1. In Snowsight, select **Apps** » **App Runtime admin**.
2. On the app’s card, select **Share**. You can also open the app and select
   the **Sharing** tab.
3. Under **Account roles**, select **Add role**, choose the role, and select
   **Save**.

Send the URL to users who hold the role. They open it and sign in to Snowflake.
For more patterns, see [Share a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/access-control).

## Next steps

- Query Snowflake from your app: [Query Snowflake from a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/query-snowflake).
- Learn what Snowflake provides to the running app: [Runtime environment for Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/runtime-environment).
- See every `snow app` command: [Snowflake App Runtime CLI commands](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/overview).
