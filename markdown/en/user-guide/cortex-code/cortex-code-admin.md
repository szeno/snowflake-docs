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

Only users who are granted the ACCOUNTADMIN role can see the CoCo Admin page and
use it to enable Cortex Code and change its setup, connectors, and integrations.

A role that is granted the CREATE AGENT privilege on the `CORTEX_CODE.CONFIG`
schema can also open the CoCo Admin page, to manage profiles on the Profiles tab.
Before you open the page, switch to that role in Snowsight. The page checks your
current role, so a privilege that you hold only through a role that isn’t active
doesn’t count. For the privileges that each profile task requires, see
[Access control requirements](/user-guide/cortex-code/cortex-code-snowsight/profiles#label-cortex-code-agent-profiles-access).

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

A profile sets the model, skills, and instructions that CoCo uses for the users
it applies to. Users don’t need to install or configure anything. You can create
two kinds of profile:

- **Default profile:** sets default settings, such as the model and skills, for
  everyone in the account who uses CoCo. It’s the profile named `DEFAULT`, and
  it’s granted to the PUBLIC role. An account has one default profile.
- **Team profile:** sets shared settings for a specific team, such as data
  scientists or data engineers. You grant it to the roles that the team’s users
  have, such as `DATA_SCIENTIST` or `DATA_ENGINEER`.

Users don’t need to do anything to get a profile. CoCo applies one to their new
chats automatically when either of these is true:

- The default profile exists and the user’s role can see it.
- The user’s role can see exactly one profile.

In [CoCo mode](/user-guide/cortex-code/cortex-code-snowsight/coco-mode), users
choose a profile for each session, or set a default profile for new sessions in
CoCo mode settings.

Users can still choose another profile, choose another model for a chat, or add
their own skills. For the full rules, see
[How a profile is chosen automatically](/user-guide/cortex-code/cortex-code-snowsight/profiles#label-cortex-code-agent-profiles-selection).

The Profiles tab lists the profiles in the `CORTEX_CODE.CONFIG` schema, with the
default profile first. If the account has no profiles, the tab shows a
**Default profile** card and a **Team profile** card to start from. You can
return to the Profiles tab at any time to change a profile’s model, skills,
instructions, or roles, or to delete it.

#### Set up profiles for the first time

1. Enable Cortex Code for your account and grant users access to it, as
   described in [Part 1: Enable Cortex Code](#label-cortex-code-admin-enable).
2. Decide which kind of profile you need:
   - To give everyone the same model and skills, create the default profile.
   - To give different teams different settings, create a team profile for
     each team.
3. If a profile uses skills, make sure that each skill is on a Snowflake stage
   or in the skill catalog. For more information, see
   [Skill locations](/user-guide/cortex-code/cortex-code-snowsight/profiles#label-cortex-code-agent-profiles-skill-sources).
4. Create the profile, as described in
   [Create the default profile](#label-cortex-code-admin-create-default-profile)
   or [Create a team profile](#label-cortex-code-admin-create-profile).
5. Test the profile as a user would. For the steps, see
   [Verify a profile](/user-guide/cortex-code/cortex-code-snowsight/profiles#label-cortex-code-agent-profiles-verify).

The Profiles tab is available to users who are granted the ACCOUNTADMIN role. To
let another role manage profiles without ACCOUNTADMIN, grant it the CREATE AGENT
privilege on the `CORTEX_CODE.CONFIG` schema. If the `CORTEX_CODE` database and
`CONFIG` schema don’t exist yet, create the first profile as a user who is
granted ACCOUNTADMIN, which creates them, or create them with
`CREATE DATABASE` and `CREATE SCHEMA`. Then run the following statements as
ACCOUNTADMIN:

Copy code

```
GRANT USAGE ON DATABASE CORTEX_CODE TO ROLE <role_name>;
GRANT USAGE ON SCHEMA CORTEX_CODE.CONFIG TO ROLE <role_name>;
GRANT CREATE AGENT ON SCHEMA CORTEX_CODE.CONFIG TO ROLE <role_name>;
```

#### Create the default profile

1. On the Profiles tab, do one of the following:

   - If the account has no profiles, select **Create default profile** on the
     **Default profile** card.
   - Otherwise, open the **Create profile** menu, and then select **Create
     default profile**. This option appears only while the account has no
     default profile.

   The profile name `DEFAULT`, the description, and the PUBLIC role are filled
   in and can’t be changed.
2. Select a **Default model**, or leave **Auto** to let Snowflake choose.
3. Optionally, under **Skills**, select **Add**, and then select **Add from
   stage** or **Add from skill catalog**.
4. Optionally, enter **Orchestration instructions** and **Response
   instructions**.
5. Select **Create profile**.

To change the default profile later, return to the Profiles tab and edit the
`DEFAULT` profile. Only the role that owns `DEFAULT` can edit it, which is
ACCOUNTADMIN if you created it as a user who is granted ACCOUNTADMIN. For more
information, see
[The default profile](/user-guide/cortex-code/cortex-code-snowsight/profiles#label-cortex-code-agent-profiles-default).

#### Create a team profile

1. On the Profiles tab, select **Create profile**. If the account has no
   profiles, select **Create profile for a team** on the **Team profile** card.
2. Enter a **Profile name**, such as `DATA_ENGINEERING`, and an optional
   **Description**.
3. Under **Roles with access**, select the roles that can use the profile, such
   as `DATA_ENGINEER`.
4. Select a **Model**, or leave **Auto** to let Snowflake choose.
5. Optionally, under **Skills**, select **Add**, and then select **Add from
   stage** or **Add from skill catalog**.
6. Optionally, enter **Orchestration instructions** and **Response
   instructions**.
7. Select **Create profile**.

The default profile is granted to PUBLIC, and every role inherits PUBLIC. So if
the account has a default profile, the team’s users get the default profile
until they choose the team profile. To have a team get its profile
automatically, make the team profile the only one that the team’s role can see:
on the Profiles tab, edit the `DEFAULT` profile and, in its **Manage** section,
replace PUBLIC with the roles that should use it. Only the role that owns
`DEFAULT` can edit it. For more information, see
[Plan profiles for your account](/user-guide/cortex-code/cortex-code-snowsight/profiles#label-cortex-code-agent-profiles-plan).

#### Grants that CoCo Admin adds

If your user is granted the ACCOUNTADMIN role, CoCo Admin creates the profile as
ACCOUNTADMIN, whatever your active role is, so ACCOUNTADMIN owns the profile. It
also creates the `CORTEX_CODE` database and `CONFIG` schema if they don’t
exist. It grants USAGE on the database, the schema, and the profile to the
roles that you selected.

If your user isn’t granted ACCOUNTADMIN, CoCo Admin grants USAGE on the profile
only. Grant USAGE on the `CORTEX_CODE` database and the `CORTEX_CODE.CONFIG`
schema to the same roles, or their users can’t see the profile:

Copy code

```
GRANT USAGE ON DATABASE CORTEX_CODE TO ROLE <role_name>;
GRANT USAGE ON SCHEMA CORTEX_CODE.CONFIG TO ROLE <role_name>;
```

For how CoCo chooses a profile, the privileges each task requires, how users
choose a profile, and how to manage profiles with SQL, see
[CoCo Profiles](/user-guide/cortex-code/cortex-code-snowsight/profiles).

#### View, edit, or delete a profile

Only the role that owns a profile, or a role that inherits the owning role, can
edit or delete it. Other roles see the profile, but **Edit** and **Delete** aren’t
available. For example, a role that has CREATE AGENT on `CORTEX_CODE.CONFIG` can’t
edit or delete profiles that ACCOUNTADMIN created, including `DEFAULT`. To let
another role manage such a profile, transfer ownership of the profile to that
role:

Copy code

```
GRANT OWNERSHIP ON AGENT CORTEX_CODE.CONFIG.<profile_name>
  TO ROLE <role_name> COPY CURRENT GRANTS;
```

- Select **Quick view** on a profile row to open a details panel showing its
  roles, model, and skills, with **Edit** and **Delete** actions.
- Select the row’s **More actions** menu for **Edit** and **Delete profile**.
- To change which roles can use a profile, edit the profile and open its
  **Manage** section. A role that you add there gets USAGE on the profile only.
  If the role doesn’t already have USAGE on the `CORTEX_CODE` database and the
  `CORTEX_CODE.CONFIG` schema, grant it.
