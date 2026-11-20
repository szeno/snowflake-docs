# Snowflake App Runtime

Snowflake App Runtime lets you go from an idea to a live, deployed web
application in minutes. No infrastructure to provision, no credentials to
configure, no Docker expertise required. Your app runs inside Snowflake, right
next to your data, with direct access to your tables, warehouses, and security
model.

Build the way you work:

- **[Snowsight Workspaces](/developer-guide/snowflake-app-runtime/workspaces)**
  (Public Preview): build and preview an app in your browser, with no local
  tools.
- **[Cortex Code](/developer-guide/snowflake-app-runtime/getting-started)**:
  describe what you want to build in Cortex Code CLI or Cortex Code Desktop,
  Snowflake’s AI coding agents. The agent scaffolds the project, wires up your
  Snowflake data, and deploys to a live URL.
- **[Snowflake CLI](/developer-guide/snowflake-app-runtime/getting-started)**:
  deploy code you already have with `snow app` commands.

Snowflake App Runtime supports **Node.js** apps (with a focus on **Next.js**) and
**Python** apps. It’s available in Amazon Web Services (AWS), Microsoft Azure,
and Google Cloud commercial regions. It isn’t available in government regions or
on [trial accounts](/user-guide/admin-trial-account).

## Why build on Snowflake?

- **Your data is already here.** Query Snowflake tables directly from your
  application code. No API layers, no ETL, no data egress.
- **Enterprise-ready by default.** SSO, role-based access control, audit
  logging, and governance are inherited from your Snowflake account. You don’t
  configure them; they’re already on.
- **Secure by design.** Your app runs inside Snowflake’s security perimeter.
  End users authenticate through Snowflake’s existing identity provider.
  Queries can run as the calling user for per-user access control, with no
  auth system to build.
- **Agentic build and deploy.** Describe the app in Cortex Code; the agent
  scaffolds the project, helps you test, and deploys when you’re ready.

## How it works

![Animated example of snow app deploy uploading your code, building it in Snowflake, storing a new version in the artifact repository, and pointing the running app at that version.](/static/images/screens/snowflake-app-runtime-deploy-pipeline.gif)

- **App service.** Each app is an
  [`APPLICATION SERVICE`](/sql-reference/sql/create-application-service) object
  in a database and schema in your account, with one URL that stays the same
  across redeploys.
- **Deploy and versions.** A deploy uploads your code to your account, and
  Snowflake builds it there, not on your machine. Each build is a new version
  that never changes, so rolling back means pointing the app at an older
  version. See [Deploy an app](/developer-guide/snowflake-app-runtime/deploy).
- **Compute.** Managed compute is generally available and the default: the app
  is always on until you suspend it. Serverless compute (Public Preview) starts
  the app on the first request, stops it after an idle period, and starts it
  again on the next request. See [Serverless compute](/developer-guide/snowflake-app-runtime/serverless).

## Quick start with Snowsight Workspaces

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

In a workspace, select **+ Add new** » **Next.js App**, then select
**Preview** and **Deploy**. See
[Build in Snowsight Workspaces](/developer-guide/snowflake-app-runtime/getting-started#label-getting-started-workspaces).

## Quick start with Cortex Code

Describe your app with the
[`snowflake-apps`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-snowflake-apps)
skill, and Cortex Code builds, runs, and deploys it.

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

See [Build with Cortex Code](/developer-guide/snowflake-app-runtime/getting-started#label-getting-started-cortex-code-path).

## Quick start with the CLI

From a project you already have:

Copy code

```
snow app setup
snow app deploy
```

See [Build with the Snowflake CLI](/developer-guide/snowflake-app-runtime/getting-started#label-getting-started-cli-path).

## How this relates to Streamlit in Snowflake

Streamlit in Snowflake and Snowflake App Runtime are both platforms for
building applications directly on your data. They’re designed for different use
cases:

- **Streamlit in Snowflake**: Python-first, opinionated, guardrailed. The right
  choice for dashboards, data exploration, and analyst self-serve tools. Fast
  path to a polished data app without writing frontend code.
- **Snowflake App Runtime**: Full power of the web. The right choice when you
  need custom UI, multi-step workflows, and rich interactions.

Choose based on what you’re building. Both run inside Snowflake’s security
perimeter, both inherit your RBAC, and both give you direct access to your data
without building API layers. Both are part of Snowflake Apps: deployed apps
surface in the same catalog regardless of how they were built.

## Next steps

- Build and deploy your first app: [Get started with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/getting-started).
- Account administrators: set up an account so teams can share apps:
  [Account administrator setup for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/account-admin-setup).
- Run an app on serverless compute: [Serverless compute for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/serverless).
