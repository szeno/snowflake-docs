# Snowflake App Runtime

Snowflake App Runtime lets you go from an idea to a live, deployed web
application in minutes. No infrastructure to provision, no credentials to
configure, no Docker expertise required. Your app runs inside Snowflake, right
next to your data, with direct access to your tables, warehouses, and security
model. Describe what you want to build in
[Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli) or
[Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop), Snowflake’s AI
coding agents. The agent scaffolds the project, wires up your Snowflake data, and
deploys to a live URL.

Snowflake App Runtime builds **Node.js** apps (with a focus on **Next.js**).
**Python** support is **planned**. It’s available in Amazon Web Services
(AWS), Microsoft Azure, and Google Cloud commercial regions. It isn’t
available in government regions or on
[trial accounts](/user-guide/admin-trial-account).

## Why build on Snowflake?

- **Your data is already here.** Query Snowflake tables directly from your
  application code. No API layers, no ETL, no data egress.
- **Enterprise-ready by default.** SSO, role-based access control, audit
  logging, and governance are inherited from your Snowflake account. You don’t
  configure them; they’re already on.
- **Agentic build and deploy.** Describe the app in Cortex Code; the agent
  scaffolds the project, helps you test locally, and deploys when you’re ready.
  You get a live, authenticated URL without managing Dockerfiles, container
  registries, or CI/CD pipelines.
- **Secure by design.** Your app runs inside Snowflake’s security perimeter.
  End users authenticate through Snowflake’s existing identity provider.
  Queries can run as the calling user for per-user access control, with no
  auth system to build. No secrets to manage.

## Quick start with Cortex Code

The fastest way to build and deploy is with
[Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli) or
[Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop/building-apps).
Both bundle the
[`snowflake-apps`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-snowflake-apps)
skill; you invoke it a little differently in each client.

Cortex Code CLICortex Code Desktop

Describe your app in chat with the `$snowflake-apps` prefix:

```
> $snowflake-apps Build me a warehouse monitor that shows all my
  warehouses with their current state and credit usage today
```

Type `/` in chat and select **snowflake-apps**, or use the **Build an app**
starter card, then describe your app:

```
/snowflake-apps Build me a warehouse monitor that shows all my
warehouses with their current state and credit usage today
```

Cortex Code generates a Next.js project, wires up Snowflake data access, tests
locally, and deploys with `snow app deploy`. Your app is live in minutes.

See
[Getting started with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/getting-started)
for environment setup, the Snowflake CLI-only path, and connecting apps to
Snowflake data.

## Quick start with the CLI

If you already have application code, initialize and deploy:

Copy code

```
snow app setup
snow app deploy
```

`snow app setup` generates an [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml)
manifest. `snow app deploy`
runs the upload, build, and deploy phases and returns a live Application
Service URL. See
[Getting started with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/getting-started)
for the full walkthrough.

## How this relates to Streamlit

Streamlit in Snowflake and Snowflake App Runtime are both ways to build
applications directly on your data. They’re designed for different use cases:

- **Streamlit**: Python-first, opinionated, guardrailed. The right choice for
  dashboards, data exploration, and analyst self-serve tools. Fast path to a
  polished data app without writing frontend code.
- **Snowflake App Runtime**: Full power of the web. The right choice when you
  need custom UI, multi-step workflows, rich interactions, or the broader
  JavaScript and TypeScript ecosystem (React, Next.js).

Choose based on what you’re building. Both run inside Snowflake’s security
perimeter, both inherit your RBAC, and both give you direct access to your data
without building API layers. Both are part of Snowflake Apps: deployed apps
surface in the same catalog regardless of how they were built.

For more about scaling apps and suspending them, see
[Scale and suspend Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/scale-and-suspend).

## Where to go next

- Install the tools and deploy your first app:
  [Getting started with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/getting-started).
- Set shared deploy defaults and role grants for a team (account
  administrators): [Account administrator setup for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/account-admin-setup).
- Configure the deploy in `app.yml`:
  [app.yml manifest for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/app-yml).
- Query your data from the running app:
  [Query Snowflake](/developer-guide/snowflake-app-runtime/query-snowflake).
- Check current limits:
  [Snowflake App Runtime limitations](/developer-guide/snowflake-app-runtime/limitations).

The sidebar lists the rest of the doc set, grouped by task.
