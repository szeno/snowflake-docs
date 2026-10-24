# Enable and manage Cortex Code for your account

The CoCo Admin page in Snowsight is the console for enabling and managing Cortex
Code (CoCo) for your Snowflake account. From one place, an account administrator
can turn CoCo on, control who can use it and which models they can use, publish
role-based profiles, connect tools and integrations, and monitor adoption.

This topic describes the CoCo Admin page: how to enable Cortex Code, and how to
manage it after it is enabled.

## Overview

The CoCo Admin page has two modes:

- **Before CoCo is enabled**, the page shows a guided **Enable CoCo for your
  account** checklist that walks you through the required setup.
- **After CoCo is enabled**, the page becomes a tabbed management console with
  these tabs: Overview, Access, and Profiles.

Every setting you change through the console is expressed as SQL. Setup dialogs
include a SQL preview toggle so you can review the exact statements before they
run, or copy them for change management. You don’t need to write SQL by hand.

Note

Granting access to Cortex, models, or tools doesn’t change what data a user can
see. Users continue to see only the data that their Snowflake roles already
allow.

## Prerequisites

You must use the ACCOUNTADMIN role, or a role with equivalent privileges, to
enable Cortex Code and to change its setup, profiles, connectors, and
integrations.

## Open the CoCo Admin page

1. Sign in to Snowsight.
2. In the left navigation, select **AI & ML**.
3. Select **CoCo Admin**.

## Part 1: Enable Cortex Code

### Before you begin

When CoCo has never been enabled, the CoCo Admin page shows **CoCo is not
enabled** with a short description of Cortex Code and a single **Enable CoCo**
button. Selecting it opens the setup flow for the three required tasks:

1. **Enable cross-region inference**: let requests reach the full set of models.
2. **Grant user and role access**: give users and roles access to Cortex.
3. **Grant model access**: choose which models can handle requests.

The flow tracks your progress (for example, 0 of 3 completed, then 2 of 3
completed) with a progress bar. As you finish a task, its row shows a summary of
what you configured and an **Edit** button. If coverage is partial, a warning
such as **5,560 users don’t have access to CoCo** appears so you can decide
whether to widen access. The page also shows **how other teams are using CoCo**
and **Useful resources** to help you get started.

Each setup screen includes a SQL preview toggle. CoCo runs standard SQL grant and
account statements on your behalf; turn on SQL preview to see (and copy) the
exact statements before they run. You never have to write the SQL yourself.

Note

The flow may appear as a single checklist with inline dialogs, or as a full-page
wizard with a **Setup steps** rail. In the wizard, each screen ends with **Save
and continue** (and **Save and finish** on the last step); in the dialog version
you select **Save changes** or **Grant access**. Both cover the same three tasks
and produce the same result.

### Step 1: Enable cross-region inference

**What it does.** Cross-region inference controls where Cortex may process an
inference request. By default a request can be served only by models hosted in
your account’s own region, and many models aren’t hosted in every region, so
without it your users can reach only a subset of models. Enabling it lets
Snowflake route a request to a supported model in another region when that model
isn’t hosted locally, which makes the most models available. It is an
account-level setting: it can’t be set per user or per session, only ACCOUNTADMIN
can change it, and ORGADMIN can’t. Your stored data never leaves your account’s
region.

To configure it:

1. Open **Enable cross-region inference** (select **Enable**, or **Edit** if it
   is already set).
2. Choose where inference can run. You can select an entire cloud group, or
   expand a group and choose specific regions within that group:

   | Option | What it means |
   | --- | --- |
   | `ANY_REGION` | Any Snowflake-supported region on any cloud. Gives the broadest model selection, highest throughput, and lowest cost. This is the recommended option. |
   | `AWS_GLOBAL` | Keeps inference within AWS. You can also choose specific AWS regions: `AWS_US`, `AWS_EU`, `AWS_AU`, `AWS_JP`, or `AWS_APJ`. |
   | `AZURE_GLOBAL` | Keeps inference within Azure. You can also choose specific Azure regions: `AZURE_US` or `AZURE_EU`. |
   | `GCP_GLOBAL` | Keeps inference within Google Cloud (`GCP_US`). |

   Expand

   Show lessSee more
3. (Optional) Turn on SQL preview to review the statement that will run.
4. Select **Apply**.

Note

To restrict inference to your account’s home region only (the strictest
data-residency posture), set `CORTEX_ENABLED_CROSS_REGION` to `DISABLED`. This
option isn’t offered in the enablement dialog; set it with ALTER ACCOUNT if you
need it. For more information, see
[Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference).

Tip

Choose the broadest setting that still meets your data-residency requirement,
preferring a cloud-scoped group over a single region, and reserving `ANY_REGION`
for genuine multi-cloud routing. The narrower you go, the fewer models your users
can reach. Government, FedRAMP High, and DoD regions should use `AWS_US` so
requests stay inside the compliance boundary on FIPS-validated infrastructure.

### Step 2: Grant user and role access

**What it does.** This task grants access to Cortex to the roles and users you
choose. Cortex access is what lets a person open and use Cortex Code at all.
Granting access doesn’t expose any new data: each user still sees only the data
their existing Snowflake roles allow.

To configure it:

1. Open **Grant user and role access** (select **Grant access**, or **Edit**).
2. Under **Who can use CoCo?**, choose the audience:

   | Option | What it means |
   | --- | --- |
   | **Everyone in the account** | Grants access to the built-in PUBLIC role, so every current and future user in the account can use CoCo. This is the Snowflake default and the simplest way to reach full adoption. |
   | **Specific roles and users** | Grants access only to the roles and users you choose. Use this for a staged rollout or when policy limits who may use AI features. |

   Expand

   Show lessSee more
3. If you choose **Specific roles and users**, you can:

   - **Select roles**: pick one or more existing account roles from the list (for
     example PUBLIC, DATA\_SCIENCE, PRODUCT\_MANAGER, ANALYST, ACCOUNTADMIN). A
     role grant covers every user who has that role.
   - **A pilot group (new role)**: create a brand-new role for a limited pilot,
     so you can grant and later revoke access to the pilot cohort without
     touching existing roles.
4. Under **Access level**, choose how much of Cortex the grant includes:

   | Option | What it grants | When to use |
   | --- | --- | --- |
   | **CoCo & Cortex Agents only** | Grants the `CORTEX_AGENT_USER` database role. Users can only create Cortex Agents or access CoWork if agent object permissions are separately granted. | Recommended when you want to roll out Cortex Code specifically and keep the footprint minimal. |
   | **All Cortex AI features** | Grants the `CORTEX_USER` database role, which gives access to CoCo, Cortex Agents, Cortex Search, AI functions, and all Cortex AI features. | Use when the selected roles should also use the rest of Cortex AI, not only CoCo. |

   Expand

   Show lessSee more
5. (Optional) Turn on SQL preview to review the grants that will run.
6. Select **Save changes** (or **Save and continue**).

If some users still lack access after you save, the screen shows a warning (for
example, **5,560 users don’t have access to CoCo**) with a one-click shortcut to
grant the PUBLIC role and enable everyone in the account.

Tip

For a controlled rollout, start with **Specific roles and users** and a pilot
role at the **CoCo & Cortex Agents only** access level, then widen to **Everyone
in the account** once you are confident. You can always return to the Access tab
later to expand or tighten access.

### Step 3: Grant model access

**What it does.** This task controls which large language models (LLMs) are
allowed to handle requests. Model access is governed by model RBAC: each model
has an access role, and a user can use a model only if one of their roles holds
it. This task grants those roles for you. It is independent of data access:
choosing a model only decides which model processes a prompt, never what data the
user can see. A model your role can reach by RBAC can still be unavailable if
cross-region inference (Step 1) doesn’t cover a region where that model is
hosted, so the two steps work together.

To configure it:

1. Open **Grant model access** (select **Grant access**, or **Edit**).
2. Under **Which models can people use?**, choose which models are allowed:

   | Option | What it means |
   | --- | --- |
   | **All models** | Allow every available model, and automatically include new models as Snowflake releases them. This maps to the account-wide model role that covers all models, including ones released later, so it is the equivalent of the former allowlist value of All. This is the recommended option, because it avoids gaps when newer models ship. A Documentation link in the UI explains the current model list. |
   | **Choose specific models** | Allow only the models you list. Select a **Model** and an **Access scope** for it, then select **Add model** to add more model rows. Grant more than one model so a single model deprecation doesn’t take CoCo down. |

   Expand

   Show lessSee more
3. Under **Who gets these models?**, choose who the model access applies to
   (shown when you allow **All models**):

   | Option | What it means |
   | --- | --- |
   | **Everyone (PUBLIC)** | Every user in the account can use the allowed models. |
   | **Same roles as CoCo access** | Reuse exactly the roles you granted in Step 2, so model access and CoCo access stay in sync. |
   | **Specific roles** | Only the roles you select from the account role list can use the allowed models. |

   Expand

   Show lessSee more
4. (Optional) Turn on SQL preview to review the statements that will run.
5. Select **Grant access** (or **Save and finish**).

Note

If you choose **Choose specific models**, any model you don’t add can’t handle
requests, even for users who otherwise have CoCo access. Selecting **All models**
avoids these gaps and keeps new models available automatically.

When all three tasks are complete, the page shows **CoCo is enabled for your
account** and switches to the management console described below.

## Part 2: Manage Cortex Code

After CoCo is enabled, the CoCo Admin page shows a tabbed console.

### Overview tab

The Overview tab summarizes the health and adoption of Cortex Code in your
account.

- **Status banner**: confirms CoCo is enabled and summarizes your setup, for
  example **All regions**, **5 roles**, **6,800 users enabled**, **12 models**.
  Select **View details** to see the full configuration, or **Expand access** to
  grant more users.
- **Recommended actions**: context-aware suggestions to help you get more value
  from CoCo. The recommendations change as your account matures. For example, as
  usage begins: **Create profiles** to configure default model and skills for
  users, and prompts to connect integrations (with **Create profiles** and
  **Connect** actions).
- **Metric tiles**:

  | Tile | Meaning |
  | --- | --- |
  | **Users enabled / eligible** | How many eligible users have been granted access (for example, 1,240 / 6,800). |
  | **Active users (28D)** | Users active in the last 28 days. Shows **No usage yet** for a new account. |
  | **Profile coverage** | The share of users covered by a profile. |

  Expand

  Show lessSee more
- **Usage charts**: Requests per week (last 8 weeks), Requests per day (30d), and
  Requests by surface (Snowsight, CLI, Desktop). Charts show **No usage yet**
  until requests are recorded.

### Access tab

The Access tab is the ongoing management view of the three settings you
configured during enablement. Each section has an **Edit** button that reopens
its dialog.

- **Cross-inference regions**: the cloud providers and regions where inference
  can run, using the same options as in
  [Step 1: Enable cross-region inference](#label-cortex-code-admin-cross-region)
  (for example `AWS_US`, `AWS_EU`, `AZURE_US`, `AZURE_EU`, or `GCP_US`).
- **User and role access**: each role that has access, its access level (**CoCo
  & Cortex Agents only** or **All Cortex AI features**), and the number of users
  it covers.
- **Model access**: each allowed model and the roles that can use it (for
  example mapped to Everyone or to specific roles).

To change any setting, select **Edit** on the corresponding section. See
[Part 1: Enable Cortex Code](#label-cortex-code-admin-enable) for the options in
each dialog.

### Profiles tab

A CoCo profile is a default configuration (model, skills, and behavior) that you
publish for selected roles. Roles control who can see and use the profile; which
profile actually applies depends on the account default and on any selection the
user makes in their client (Snowsight, Desktop, or CLI). Users can override,
customize, or opt out at session time, so a profile sets good defaults without
locking users in.

Each profile defines:

| Field | Description |
| --- | --- |
| **Profile name** | The name of the profile. |
| **Roles** | The roles that can use this profile. Which profile applies depends on the account default and on the user’s own selection. |
| **Model** | The default model, for example Auto or a specific model you choose. |
| **Skills** | The skills enabled by default. |
| **System instructions** | Guidance for how the profile should behave. |
| **Response instructions** | Guidance for how responses should be written. |

Expand

Show lessSee more

#### Create a profile

1. On the Profiles tab, select **Create profile**.
2. Enter a **Profile name** and an optional **Description**.
3. Under **Roles with access**, select the roles this profile applies to.
4. Select a default **Model** (or leave **Auto** to let CoCo choose).
5. (Optional) Select **Add** to add one or more skills.
6. (Optional) Enter **System instructions** and **Response instructions**.
7. Select **Create profile**.

#### View, edit, or delete a profile

- Select **Quick view** on a profile row to open a details panel showing its
  roles, model, and skills, with **Edit** and **Delete** actions.
- Select the row’s **More actions** menu for **Edit** and **Delete profile**.
