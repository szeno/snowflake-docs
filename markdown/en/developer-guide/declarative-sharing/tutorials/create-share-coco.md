# Tutorial: Create a Declarative Share with Cortex Code

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

## Introduction

This tutorial walks you through creating a
[declarative share](/developer-guide/declarative-sharing/about) —
a data application package with *TYPE = DATA* and a
[manifest](/developer-guide/declarative-sharing/manifest-reference) — using
Cortex Code (CoCo), either from the
[CLI](/user-guide/cortex-code/cortex-code-cli) or the Web UI in
Snowsight. Consumers can install the result as an app and query the shared data.

The entire workflow uses a single prompt: CoCo validates your environment,
finds or creates data, builds auxiliary objects, generates a manifest, creates
and releases the application package, and publishes a private listing.

Along the way, the tutorial explains what CoCo does at each stage so you
understand the underlying SQL and concepts.

### What you’ll learn

In this tutorial, you’ll learn how to:

- Use a single prompt to have CoCo create a data product end-to-end:
  environment validation, data selection, secure views, a semantic view, a
  Cortex Agent, a manifest, an application package, a LIVE release, and a
  private listing.
- Verify the published app from a consumer account.
- Clean up provider and consumer resources when you’re done.

The prompt works identically in CoCo CLI and CoCo Web.

#### Declarative sharing background

If you’re new to declarative sharing, see
[About Declarative Sharing](/developer-guide/declarative-sharing/about)
for an overview of how it compares to
[traditional data sharing](/guides-overview-sharing) and
[full native apps](/developer-guide/native-apps/native-apps-about).

### Prerequisites

Before getting started, make sure that you meet the following requirements:

- Access to two Snowflake accounts:

  - A **provider account** that will create and publish the declarative share.
  - A **consumer account** that will install and verify the published app.
- **CoCo CLI** or **CoCo Web** (Snowsight):

  CoCo CLICoCo Web (Snowsight)

  [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli)
  installed and configured with connections to both accounts in your
  `connections.toml`:

  - macOS: `~/.snowflake/connections.toml`
  - Windows: `%USERPROFILE%\.snowflake\connections.toml`

  Sign in to Snowsight on your provider account and open a
  **Workspace** (**Projects** > **Workspaces**). CoCo is available
  from the sidebar. You must start the chat from inside a Workspace so
  CoCo can create and manage files such as the manifest.

### Open CoCo

CoCo CLICoCo Web (Snowsight)

Run CoCo from a terminal with your provider connection:

Copy code

```
cortex -c <your_provider_connection>
```

Sign in to Snowsight on your **provider account**, open a
**Workspace** (**Projects** > **Workspaces**), and launch CoCo
from the sidebar. Starting CoCo from a Workspace is required for
this tutorial — CoCo needs the Workspace file tools to write and
edit the manifest. CoCo started from outside a Workspace can’t write
files and falls back to a stage-based upload that isn’t covered here.

Important

CoCo Web support for Declarative Sharing is in preview. If the
skill isn’t available by default in your environment, upload it
from:
<https://github.com/snowflake-eng/cortex-code-skills/tree/main/apps/declarative-sharing>

Note

Notebook generation is supported only in CoCo CLI. The Workspace file
editor can corrupt notebook JSON, so don’t ask CoCo Web to write
`.ipynb` files. To bundle a notebook with your package from CoCo Web,
create the notebook directly in Snowsight and then add it to a
workspace directory in your package. For more information, see
[Share a workspace in a Declarative Native App](/developer-guide/declarative-sharing/workspaces).

## Run the prompt

A single prompt drives the entire workflow. Copy the prompt below and replace
the placeholders with your own values, or leave them as-is — CoCo will
validate your environment setup then create the declarative share.

1. Enter the following prompt:

   ```
   I want to create and publish a declarative share so consumers
   can explore and query the data in natural language. Show me
   what data I have and let me decide what to share — if nothing
   fits, offer to create a small synthetic dataset. Publish as a
   private listing to <CONSUMER_ORG.ACCOUNT>.
   ```

   - Replace `<CONSUMER_ORG.ACCOUNT>` with your consumer account’s data
     sharing identifier, which is typically the organization name and account
     name separated by a dot (for example, `MYORG.MYCONSUMER`). You can find
     this under **Admin** > **Accounts** in Snowsight.
2. CoCo walks through each stage and asks you to approve the commands before
   running them. Review the proposed SQL at each step and confirm. If CoCo
   encounters issues (a missing warehouse or insufficient permissions), it walks
   you through how to resolve each one before proceeding.

The following sections describe what CoCo does at each stage.

### Identifying the dataset

CoCo validates your environment, then finds existing data or creates a small
synthetic dataset. It inspects table structures, samples a few rows, and
proposes a plan:

```
I found (or created) two tables in SALES_DB.PUBLIC:
- PRODUCTS (5 rows): name, category, price
- ORDERS (12 rows): product_id, quantity, order_date

Here's the plan:
1. Create schemas (data vs agent objects)
2. Create a secure summary view
3. Create a semantic view for natural-language querying
4. Create a Cortex Agent backed by the semantic view
5. Write manifest, create package, release, and publish
```

### Creating auxiliary objects

CoCo creates objects to enhance the consumer experience. You can accept or
decline each suggestion. Depending on your data, CoCo may offer:

**Secure views** — Aggregated or filtered views of the underlying tables.
Views must be created with `CREATE SECURE VIEW` to work in declarative shares.

**Semantic view** — Maps tables, columns, and metrics so consumers can query
the data using natural language through Cortex Analyst. For more information,
see [Semantic views](/user-guide/views-semantic/overview).

**Cortex Agent** — A chat interface backed by the semantic view, giving
consumers a conversational way to explore data without writing
SQL. For more information, see
[Cortex Agents](/user-guide/snowflake-cortex/cortex-agents).

CoCo may also create notebooks, UDFs, and other objects depending on what makes
sense for your dataset.

Note

Declarative sharing requires shared-by-reference objects (tables, views,
semantic views) and shared-by-copy objects (agents, UDFs) to live in separate
schemas. CoCo organizes this automatically.

### Writing the manifest

The [manifest](/developer-guide/declarative-sharing/manifest-reference) is a YAML file that declares which
objects are shared and which
[app roles](/developer-guide/declarative-sharing/app-roles) can access them. CoCo generates the manifest
based on your data and the objects it created. The manifest for your dataset
will be different from this example, and that’s the point: CoCo tailors the
structure to match your objects. All you need to do is review it. If there’s an
entry you don’t want to share, just tell CoCo to remove it.

Here’s an example of what the generated manifest might look like:

Copy code

```
roles:
  - app_user:
      comment: "Read-only access to shared data"

shared_content:
  databases:
    - SALES_DB:
        schemas:
          - AGENT_SCHEMA:
              roles: [app_user]
              cortex_agents:
                - SALES_AGENT:
                    roles: [app_user]
          - DATA_SCHEMA:
              roles: [app_user]
              views:
                - ORDER_SUMMARY:
                    roles: [app_user]
              semantic_views:
                - SALES_SEMANTIC_VIEW:
                    roles: [app_user]
          - PUBLIC:
              roles: [app_user]
              tables:
                - PRODUCTS:
                    roles: [app_user]
                - ORDERS:
                    roles: [app_user]
```

The manifest follows a `shared_content > databases > schemas > objects`
hierarchy. Shared-by-copy objects (agents) and shared-by-reference objects
(tables, views, semantic views) go in separate
schemas. For the full specification, see
[Manifest reference](/developer-guide/declarative-sharing/manifest-reference).

### Creating the application package

CoCo creates an
[application package](/developer-guide/declarative-sharing/package) with
`TYPE = DATA`, uploads the manifest, and releases the LIVE version:

Copy code

```
CREATE APPLICATION PACKAGE SALES_DATA_PKG TYPE = DATA;
```

Note

Application packages and databases share the same namespace, so the
package name can’t match an existing database. CoCo picks a unique name
(for example, `SALES_DATA_PKG` rather than `SALES_DB`) to avoid the
collision.

CoCo writes the manifest to the Workspace, then copies it into the package:

Copy code

```
COPY FILES INTO snow://package/SALES_DATA_PKG/versions/LIVE/
  FROM 'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/live/'
  FILES = ('manifest.yml');
```

Note

If you are using CoCo CLI (local filesystem), CoCo uses `PUT` instead:

Copy code

```
PUT file:///workspace/manifest.yml
    snow://package/SALES_DATA_PKG/versions/LIVE/
    OVERWRITE=TRUE AUTO_COMPRESS=false;
```

Copy code

```
ALTER APPLICATION PACKAGE SALES_DATA_PKG RELEASE LIVE VERSION;
```

These commands upload files into the package’s
[LIVE version stage](/developer-guide/declarative-sharing/live-editing).
Unlike versioned native apps, declarative shares use LIVE versions that update
automatically when you re-upload and re-release. For more information about the
`CREATE APPLICATION PACKAGE` command, see
[CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package).

### Publishing the listing

CoCo creates a private
[listing](/developer-guide/declarative-sharing/listing) targeted at your
consumer account and publishes it:

Copy code

```
CREATE EXTERNAL LISTING SALES_DATA_LISTING
APPLICATION PACKAGE SALES_DATA_PKG AS
$$
title: "Sales Data Product"
subtitle: "Product catalog, orders, and a Cortex Agent"
description: "Two tables, a secure summary view, and a Cortex Agent
              for conversational analytics."
listing_terms:
  type: "OFFLINE"
targets:
  accounts: ["MYORG.MYCONSUMER"]
$$
PUBLISH = FALSE
REVIEW = FALSE;

ALTER LISTING SALES_DATA_LISTING PUBLISH;
```

For details on listing configuration, see
[Creating a listing](/developer-guide/declarative-sharing/listing).

At this point the declarative share is fully published. CoCo verifies the
package and listing, then presents a summary of everything it created.

## Verify as a consumer

After CoCo finishes, confirm that the app is visible and working from your
consumer account.

Note

Before installing, make sure the consumer user has `first_name`,
`last_name`, and `email` set (otherwise the install fails with error
`090655`) and a default warehouse assigned (otherwise agents and
functions silently return no results). CoCo flags both during install
and offers `ALTER USER` statements to fix them.

1. Sign in to Snowsight on your consumer account.
2. Navigate to **Data Products** > **Apps**.
3. Find the installed app and explore the schemas, tables, and views it
   exposes.
4. Open a worksheet and run a quick query:

   Copy code

   ```
   SELECT * FROM <app_name>.DATA_SCHEMA.ORDER_SUMMARY LIMIT 10;
   ```
5. To try the Cortex Agent, open **AI & ML** > **Snowflake CoWork**
   in Snowsight and select the agent bundled with the app. Ask a question
   like “Which product had the most orders?”

Note

If the consumer account is in a different region or cloud, find the
listing under **Data Products** > **Marketplace** >
**Shared With You** and install it manually. Cross-region sharing
requires [listing auto-fulfillment](/collaboration/provider-listings-auto-fulfillment)
to be enabled on both accounts. Application packages with
`TYPE = DATA` must use `SUB_DATABASE_WITH_REFERENCE_USAGE` for the
cross-region `auto_fulfillment.refresh_type` — the older
`SUB_DATABASE` value works for traditional shares only. CoCo uses the
correct value when it detects a cross-region target.

## Troubleshooting and limitations

### Privileges

- If you see errors about `CREATE APPLICATION PACKAGE`, switch to a role with
  that privilege or have an admin grant it before retrying.

### Manifest issues

- If consumers can’t see objects, check `manifest.yml` to ensure the
  `shared_content.databases: schemas: objects` hierarchy is correct. For the
  full specification, see
  [Manifest reference](/developer-guide/declarative-sharing/manifest-reference).

### Schema mixing

- Don’t mix shared-by-copy and shared-by-reference objects in the same schema;
  use separate schemas. Shared-by-copy objects include agents, UDFs, and
  procedures. Shared-by-reference objects include tables, views, and semantic
  views.

### Object limits

- A single application package supports up to 1,000 objects in
  `shared_content`. For details, see
  [Limitations](/developer-guide/declarative-sharing/limitations).

### Notebooks

Deprecated

Sharing individual notebooks with `application_content.notebooks` shares
[Legacy Notebooks](/user-guide/ui-snowsight/notebooks), and is deprecated. Starting
August 18, 2026, you can’t create new application packages that share notebooks this way. Starting
November 2026, Legacy Notebooks can no longer be run or edited. For the full timeline, see
[Disable Legacy Notebook creations](/release-notes/bcr-bundles/un-bundled/bcr-disable-legacy-notebooks).

Share [Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview)
in a workspace instead. Consumers can run and interact with those notebooks the same way, and a
workspace can also share documentation, images, and sample data files. For more information, see
[Share a workspace in a Declarative Native App](/developer-guide/declarative-sharing/workspaces).

- Share notebooks in a workspace directory, not with `application_content.notebooks`. For more
  information, see [Share a workspace in a Declarative Native App](/developer-guide/declarative-sharing/workspaces).
- Notebooks can only access data inside the same application package.
- Ensure each code cell has correct `language` metadata; otherwise SQL cells
  may be interpreted as Python and fail.

## Summary, clean up, and additional resources

Congratulations! You’ve completed this tutorial.

### Summary and key points

Using a single prompt in CoCo (CLI or Web), you:

- Had CoCo validate your environment, find (or create) a dataset, build a
  secure view, a semantic view, a Cortex Agent, a
  manifest, a `TYPE = DATA` application package, a LIVE release, and a
  private listing — all in one workflow.

#### Additional prompt examples

After you finish the tutorial, you can use prompts like these to extend or
adapt the workflow. Replace placeholders (`<...>`) with your own object
names.

- **Publish a private listing for an existing package** —
  `Create a private listing for my application package <PACKAGE> targeting <CONSUMER_ORG.ACCOUNT>.`
- **Distribute cross-region** —
  `My consumer for <PACKAGE> is in a different region. Update the listing so it auto-fulfills cross-region.`
  CoCo configures `auto_fulfillment.refresh_type: SUB_DATABASE_WITH_REFERENCE_USAGE`
  for you, which is required for `TYPE = DATA` packages.
- **Convert a traditional data share** —
  `Take my data share <SHARE_NAME>, generate a declarative sharing manifest from it, then create the application package and release LIVE.`
- **Combine multiple data shares into one** —
  `Combine my data shares <SHARE_A> and <SHARE_B> into a single declarative manifest spanning both databases, then package and release.`
  Declarative shares can span multiple databases; traditional shares cannot.
- **Audit drift between manifest and listing** —
  `Compare the objects exposed by my published listing for <PACKAGE> against the manifest. Flag anything missing or out of sync.`
- **Iterate on the manifest** —
  `Add <SCHEMA>.<TABLE> to my <PACKAGE> manifest and release a new LIVE version.`
- **Add a Cortex Agent over a shared semantic view** —
  `Add a Cortex Agent over <SCHEMA>.<SEMANTIC_VIEW> to my <PACKAGE>. Put it in its own agent schema, update the manifest, and release LIVE.`
- **Bundle a getting-started notebook in a workspace** (CoCo CLI only) —
  `Create a notebook with three sample queries against the shared views in <PACKAGE>, put it in a workspace directory, declare the workspace in the manifest, and re-release LIVE.`

### Cleanup (optional)

CoCo can generate the cleanup SQL for you.

#### Consumer account

1. In CoCo, connect to the consumer account.
2. Use a cleanup prompt:

   ```
   Clean up the data app installed from the tutorial.
   Drop the tutorial application if it exists.
   ```

#### Provider account

1. In CoCo, connect to the provider account.
2. Use a cleanup prompt:

   ```
   Clean up the tutorial resources I created on the provider side:
   unpublish and drop the listing first, then drop the application
   package, then drop any tables, views, semantic views, agents, and
   schemas created only for this tutorial.
   ```

   The order matters — you can’t drop a package while a published
   listing still references it.

### Learn more

To learn more about Declarative Native Apps, see the following topics:

- [About Declarative Sharing in the Native Application Framework](/developer-guide/declarative-sharing/about)
- [Tutorial: Getting started with Declarative Native Apps](/developer-guide/declarative-sharing/tutorials/getting-started)
- [Manifest reference](/developer-guide/declarative-sharing/manifest-reference)
- [Application packages](/developer-guide/declarative-sharing/package)
- [Creating a listing](/developer-guide/declarative-sharing/listing)
- [Command reference](/developer-guide/declarative-sharing/command-reference)
