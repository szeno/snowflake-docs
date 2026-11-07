# CoCo Profiles (*Preview*)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

A profile is a reusable configuration for CoCo. It bundles a model choice, instructions, and a set of
skills into a single named object. Instead of having each user configure models and skills
individually, an administrator defines a profile once, and users with access to it can select it in
the CoCo CLI, CoCo Desktop, or Snowsight, including the CoCo side panel and
[CoCo mode](/user-guide/cortex-code/cortex-code-snowsight/coco-mode).

There are two ways to use profiles:

- **Default profile:** one profile, named `DEFAULT`, that sets the default model and skills for
  everyone in the account who uses CoCo. For more information, see
  [The default profile](#label-cortex-code-agent-profiles-default).
- **Team profiles:** separate profiles for different teams and roles, such as a data science
  profile for the `DATA_SCIENTIST` role and a data engineering profile for the `DATA_ENGINEER`
  role.

For example, a data team can create an analysis profile that includes the team’s reporting
guidelines and a report-writing skill. Analysts select that profile and immediately get consistent
behavior, without installing anything themselves.

Note

Availability of profiles and of specific controls described in this topic depends on your account
and client version. If a control described here isn’t visible in your environment, contact your
Snowflake account team.

## How profiles work

Profiles are stored as AGENT objects in the `CORTEX_CODE.CONFIG` schema. Because they are ordinary
Snowflake objects, access to them is controlled with standard role-based access control:

- Administrators create and maintain profiles, and grant roles access to them.
- Users see only the profiles that their current role can access, and choose which one to use.

Keep the following in mind:

- Selecting a profile doesn’t change the profile definition. It only changes what you use.
- Selecting a profile doesn’t grant access to data. Queries still run with the privileges of your
  active role.
- A profile is a convenience, not a security control. To restrict what CoCo can do, use Snowflake
  access control and the controls on the
  [CoCo Admin page](/user-guide/cortex-code/cortex-code-admin).
- A profile is different from a connection configuration (account, authentication, role, and
  warehouse). Profiles don’t change which account or role you’re connected with.

### What a profile contains

| Component | Description |
| --- | --- |
| Model | The orchestration model that CoCo uses. Leave it unset, or set it to `auto`, to let CoCo choose. |
| Instructions | Optional guidelines that are applied to every conversation, such as team conventions or a preferred output style. |
| Skills | Optional list of skills, stored on a Snowflake stage or published in the skill catalog. |

Expand

Show lessSee more

### How skills in a profile are loaded

Users don’t need to download a profile or preinstall its skills. When you send a request:

1. CoCo checks which skills the selected profile makes available.
2. If a skill is relevant to your request, CoCo locates it.
3. The skill is read from its stage or catalog location and used for that request.

Skills are loaded only when they are relevant, so not every skill in a profile is loaded for every
request. Your role must be able to read the skill’s stage or catalog object.

## The default profile

The default profile is the profile named `DEFAULT` in the `CORTEX_CODE.CONFIG` schema. It sets the
default model and skills for everyone in the account who uses CoCo. When it’s granted to the PUBLIC
role, CoCo applies it to every user who hasn’t chosen another profile.

- The stored name must be `DEFAULT` in uppercase. In SQL, an unquoted name such as `default` is
  stored as `DEFAULT`, but a quoted lowercase name such as `"default"` creates an ordinary profile.
  CoCo Admin keeps the case that you type, so enter `DEFAULT`.
- The default profile is the same object that sets the account’s default model. For more
  information, see [Configure default model settings](/user-guide/cortex-code/configure-model-settings).
- To create it in Snowsight, select **Create default profile** on the **Profiles** tab of the CoCo
  Admin page. For the steps, see
  [Create the default profile](/user-guide/cortex-code/cortex-code-admin#label-cortex-code-admin-create-default-profile).
  To change it later, return to the **Profiles** tab and edit it.

## How a profile is chosen automatically

You don’t need to do anything to use a profile that your administrator set up for you. When you
start a new chat and haven’t chosen a profile yourself, CoCo picks one based on the profiles
visible to your current role:

| Profiles visible to your role | Profile used automatically |
| --- | --- |
| None | No profile |
| Exactly one | That profile |
| More than one, including one named `DEFAULT` | The `DEFAULT` profile |
| More than one, none named `DEFAULT` | No profile. Choose one manually. |

Expand

Show lessSee more

Because visibility depends on your role, switching roles can change which profile is used. Any
profile that you choose explicitly overrides the automatic choice. A profile applies to new chats;
chats that are already in progress keep the profile they started with.

In CoCo mode, a session uses the profile that you choose for it, or the default profile that you
set in CoCo mode settings. For more information, see [CoCo mode in Snowsight](#label-cortex-code-agent-profiles-use-coco-mode).

### Plan profiles for your account

Before creating, renaming, or granting access to profiles, consider how the change affects which
profile each role receives:

- **One configuration for everyone:** create the default profile and grant it to PUBLIC.
- **Different configurations for different teams:** create a team profile for each team, and
  grant it to that team’s role, such as `DATA_SCIENTIST` or `DATA_ENGINEER`.

Users get the best experience when their role can see exactly one profile. Every role inherits
PUBLIC, so if the default profile is granted to PUBLIC, users who also have a team profile get
`DEFAULT` until they choose the team profile. Granting a role access to a second profile also means
that role no longer gets a profile automatically unless one of the two is named `DEFAULT`.

## Use profiles

### CoCo CLI

Enter these commands at the CoCo prompt. They are in-app commands, not shell commands.

| Command | Description |
| --- | --- |
| `/profile list` | Lists the profiles available to your current role. |
| `/profile show <name>` | Shows the model, instructions, and skills of a profile. |
| `/profile use <name>` | Selects a profile for your sessions. |

Expand

Show lessSee more

To set or clear your profile from the settings menu:

1. Enter `/settings`.
2. Select **Agent Profile**.
3. Choose a profile, or select **Remove profile** to clear your selection.

### CoCo Desktop

1. Open **Settings**.
2. Select **Profiles**.
3. Choose a profile and apply it.

### CoCo side panel in Snowsight

1. In the CoCo side panel, open **Agent settings**.
2. Select **Profiles**.
3. Choose a profile and select **Apply**.

### CoCo mode in Snowsight

In [CoCo mode](/user-guide/cortex-code/cortex-code-snowsight/coco-mode), you choose a profile for each
session:

- To choose a profile for a session, in the message box, select **+**, select **Profile**, and then
  choose a profile. To run the session without a profile, choose **None**.
- To set the profile that new sessions start with, open the account menu in the CoCo mode sidebar,
  select **Settings**, and then choose a **Default profile**.

CoCo mode lists profiles that have a display name. Profiles created on the CoCo Admin page have
one. For profiles created with SQL, see [Create a profile](#label-cortex-code-agent-profiles-sql-create).

### Things to know

- Your choice in one client isn’t guaranteed to carry over to another. Set your profile in each
  client that you use.
- Changing your profile doesn’t change chats that are already in progress. Start a new chat to use
  the new profile.
- If an administrator updates a profile, it can take a short time for the change to appear, and
  existing chats might continue to use the earlier version.

### Troubleshooting

| Symptom | What to check |
| --- | --- |
| A profile you expect isn’t listed | Confirm that you’re connected to the right account and using a role that has access to the profile. Ask your administrator to verify the grant. Update your client if it’s out of date. In CoCo mode, the profile must also have a display name. |
| No profile is applied automatically | More than one profile is visible to your role and none is named `DEFAULT`. Choose one with `/profile use` or in settings. |
| A skill from the profile isn’t used | The skill is used only when it’s relevant to your request. If it should be used, confirm that your role can read the skill’s stage or catalog object, and report the issue to your administrator. |

Expand

Show lessSee more

## Manage profiles

### Access control requirements

| Task | Required privileges |
| --- | --- |
| Create a profile | CREATE AGENT on schema `CORTEX_CODE.CONFIG`, plus USAGE on the `CORTEX_CODE` database and the `CONFIG` schema |
| Update a profile | OWNERSHIP or MODIFY on the profile’s AGENT object. In CoCo Admin, only the owning role can edit a profile. |
| Delete a profile | OWNERSHIP on the profile’s AGENT object |
| Use a profile | USAGE on the profile’s AGENT object and on the `CORTEX_CODE` database and `CONFIG` schema, plus read access to the stages or catalog objects of its skills |

Expand

Show lessSee more

ACCOUNTADMIN isn’t required. Grant these privileges to a dedicated administrative role where
possible. The CoCo Admin page is visible only to users who are granted ACCOUNTADMIN, or to roles
that have CREATE AGENT on the `CORTEX_CODE.CONFIG` schema.

### Manage profiles in Snowsight

The recommended way to manage profiles is the **Profiles** tab of the CoCo Admin page. From there,
you can create the default profile or a team profile, and grant it to roles. You can return to the
**Profiles** tab at any time to change a profile’s model, skills, instructions, or roles, or to
delete it. For the steps, see
[Profiles tab](/user-guide/cortex-code/cortex-code-admin#label-cortex-code-admin-profiles-tab).

### Skill locations

Each skill in a profile has a name and a source:

| Skill source | `source.type` | `source.path` |
| --- | --- | --- |
| Snowflake stage | `STAGE` | `@<db>.<schema>.<stage>/<path>/<skill>/` |
| Skill catalog | `CORTEX_EXTENSION` | `<db>.<schema>.<name>`. To pin a version, also set `source.version`, such as `VERSION$1`. |

Expand

Show lessSee more

The skill name in the profile should match the name declared in the skill’s `SKILL.md` file. If the
names don’t match, CoCo might not find the skill.

Skills from GitHub repositories, local directories, or other non-Snowflake sources aren’t supported
in profiles.

### Profile specification

A profile specification supports the following keys:

Copy code

```
models:
  orchestration: auto
instructions:
  response: |
    Follow the team's analysis guidelines.
    Summarize results in a short table before any explanation.
skills:
  - name: report-writer
    source:
      type: STAGE
      path: "@ANALYTICS.SHARED.SKILLS/report-writer/"
  - name: sql-author
    source:
      type: CORTEX_EXTENSION
      path: ANALYTICS.SKILLS.SQL_AUTHOR
      version: VERSION$1
```

| Key | Required | Description |
| --- | --- | --- |
| `models.orchestration` | No | The orchestration model. Omit it, or set it to `auto`, to let CoCo choose. |
| `instructions.orchestration` | No | Guidelines for how CoCo works. Shown as **Orchestration instructions** in CoCo Admin. |
| `instructions.response` | No | Response guidelines applied to every conversation. Shown as **Response instructions** in CoCo Admin. |
| `skills` | No | List of skills. Each entry requires `name`, `source.type`, and `source.path`. When `source.type` is `CORTEX_EXTENSION`, `source.version` is optional. |

Expand

Show lessSee more

Other keys, such as `tools`, `tool_resources`, `budget`, or legacy profile settings such as
`plugins`, `hooks`, or `mcpServers`, aren’t supported.

### Manage profiles with SQL

Use SQL when a Snowsight control isn’t available in your account, or for automation. If the
`CORTEX_CODE` database and `CONFIG` schema don’t exist, create them first.

#### Create a profile

Copy code

```
CREATE AGENT CORTEX_CODE.CONFIG.ANALYST_PROFILE
  PROFILE = '{"display_name": "Analyst profile"}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: auto
  instructions:
    response: |
      Follow the team's analysis guidelines.
  skills:
    - name: report-writer
      source:
        type: STAGE
        path: "@ANALYTICS.SHARED.SKILLS/report-writer/"
  $$;

GRANT USAGE ON AGENT CORTEX_CODE.CONFIG.ANALYST_PROFILE TO ROLE ANALYST;
```

The `PROFILE` property sets the name that users see in CoCo mode. To add a display name to an
existing profile, run `ALTER AGENT ... SET PROFILE`.

Avoid `CREATE OR REPLACE` for existing profiles. Replacing the object can change ownership and
remove existing grants.

#### List and inspect profiles

Copy code

```
SHOW AGENTS IN SCHEMA CORTEX_CODE.CONFIG;
DESCRIBE AGENT CORTEX_CODE.CONFIG.ANALYST_PROFILE;
SHOW GRANTS ON AGENT CORTEX_CODE.CONFIG.ANALYST_PROFILE;
```

#### Update a profile

Copy code

```
ALTER AGENT CORTEX_CODE.CONFIG.ANALYST_PROFILE
  MODIFY LIVE VERSION SET SPECIFICATION =
  $$
  models:
    orchestration: auto
  instructions:
    response: |
      Follow the team's updated analysis guidelines.
  skills:
    - name: report-writer
      source:
        type: STAGE
        path: "@ANALYTICS.SHARED.SKILLS/report-writer/"
  $$;
```

Important

`ALTER AGENT ... SET SPECIFICATION` replaces the entire specification. Include every field that you
want to keep. Before updating, run `DESCRIBE AGENT` and save the current specification so that you
can restore it if needed.

Grants on the profile are preserved when you update it.

If you committed a version of the profile and made it the version in use, `MODIFY LIVE VERSION`
changes only the live version, which Snowsight shows as the draft. Users keep getting the version in
use until you commit the live version and make the new version the default. For more information,
see [Cortex Agent versioning](/user-guide/snowflake-cortex/cortex-agents-versioning).

#### Delete a profile

Copy code

```
DROP AGENT CORTEX_CODE.CONFIG.ANALYST_PROFILE;
```

Before deleting a profile, save its specification and grants, and check which roles use it.
Deleting a profile can change which profile those users receive automatically.

### Verify a profile

After creating or changing a profile:

1. Switch to a role that should use the profile.
2. In the client that your users use, run `/profile list` (CLI), open the **Profiles** settings
   (Desktop or the CoCo side panel), or open the **Profile** menu in the message box (CoCo mode), and
   confirm that the profile appears.
3. Select the profile, start a new chat, and send a simple request that should use one of the
   profile’s skills.
4. Confirm that the expected instructions and skills are applied.

Viewing the profile with `DESCRIBE AGENT` confirms the definition, but only a test in the client
confirms that users experience the expected behavior.
