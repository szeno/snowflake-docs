# Skills in CoCo Desktop

Skills extend the CoCo Desktop agent with reusable, prepackaged knowledge and workflows for specific tasks. A skill is a self-contained folder with a `SKILL.md` file describing what the skill does and the steps the agent should follow when it is invoked.

You can use the skills that ship with CoCo Desktop, install community skills from a Git repository, share skills with your team through a Snowflake stage, or author your own. All skills are managed from the **Agent Settings** panel and can be invoked automatically by the agent or explicitly from chat.

Note

Skills configuration is stored in `~/.snowflake/cortex/skills.json` and shared with the `cortex` command-line tool. A skill you add in CoCo Desktop is also available from the CLI, and vice versa.

## Prerequisites

- CoCo Desktop installed and signed in.
- For **Stage skills**: an active Snowflake connection with read access (and write access, to publish) on the target stage.
- For **GitHub skills**: network access to the Git host. Private repositories use your system Git credentials.

## Open the Agent Settings panel

Skills are managed from the **Agent Settings** panel. To open it, click the **Agent Settings** tab in the left sidebar.

In the Agent Settings panel, select the **Skills** category from the left sidebar. This is the recommended place to browse, add, update, favorite, disable, and remove skills.

[![Agent Settings panel with the Skills category selected, showing collapsible source sections and a search box](/static/images/user-guide/cortex-code/cortex-code-desktop/skills/skills-agent-settings.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/skills/skills-agent-settings.png)

The Skills tab groups every skill the agent can see into collapsible sections:

- **Shared Skills** — skills fetched from a Snowflake stage or Shared skills catalog.
- **Packaged Skills** — built-in skills shipped with CoCo Desktop.
- **Local Skills** — project skills (workspace-local) and any user-level skills you’ve registered.
- **GitHub Skills** — skills added from a Git repository.

A search box at the top of the Skills tab filters skills by name or description across all sections. Selecting a skill shows its description and exposes actions such as *Open SKILL.md*, *Favorite*, *Disable*, *Update*, *Publish to stage*, and *Remove*.

Tip

Other Agent Settings categories — **Plugins**, **Profiles**, **MCP**, **Subagents**, **Hooks**, and **Rules** — are also managed from the same panel. Plugins you install from the Plugins tab can contribute skills that show up automatically in the Skills tab.

## Skill sources

CoCo Desktop loads skills from several sources. All of them appear in the Skills tab of the Agent Settings panel and can be invoked the same way from chat.

### Built-in (packaged) skills

Built-in skills ship with CoCo Desktop and appear in the **Packaged Skills** section. They cover common Snowflake tasks such as creating a Cortex Agent, optimizing a Cortex Search service, building a Streamlit app, and authoring a new plugin.

You can browse, favorite, and disable packaged skills, but you cannot delete them — they are part of the application bundle. To stop the agent from auto-selecting a packaged skill, disable it (see Managing skills).

### Project skills

Project skills live inside a workspace folder you open in CoCo Desktop, typically under `.snowflake/cortex/skills/`. They are committed alongside your code or notebooks, so they travel with the project and apply only when that workspace is open.

Use project skills when you want a workflow scoped to a particular repository, for example:

- A “deploy this dbt project to Snowflake” runbook.
- Conventions specific to the codebase (lint commands, test commands, naming standards).
- A team-onboarding walkthrough that lives next to the code it documents.

Project skills are auto-discovered when the workspace is opened and appear in the **Local Skills** section. No manual registration is required.

### Local (user-created) skills

Local skills are stored in any folder on your machine that you register with CoCo Desktop. Use them when you want a personal skill that follows you across workspaces but isn’t published to a Git host or stage.

To add a local skill folder:

1. Open the **Agent Settings** panel and select the **Skills** category.
2. In the **Local Skills** section header, click the `+` button (*Add Local Skill*).
3. Pick a directory that contains one or more skills (each skill is a subdirectory with a `SKILL.md`).

CoCo recursively scans the folder for `SKILL.md` files (up to 10 directories deep) and registers every skill it finds. The folder path is saved to `~/.snowflake/cortex/skills.json`.

### Plugin-contributed skills

Plugins are bundles that can ship multiple skills, hooks, agents, and MCP servers in one package. When you install a plugin, every skill it contributes appears in the Skills view automatically.

You can install plugins from two sources:

- **GitHub** — clone a plugin repository (any Git URL works: GitHub, GitLab, Bitbucket, SSH, self-hosted).
- **Local folder** — register a directory that contains a `.cortex-plugin/` or `.claude-plugin/` manifest.

Plugin-contributed skills are listed alongside other skills, often prefixed with the plugin name (for example, `commit-commands:commit`). To install or remove a plugin, open the **Agent Settings** panel and select the **Plugins** category. Removing a plugin removes every skill it contributed.

### GitHub skills

You can add a single skill or a folder of skills directly from a Git repository. CoCo clones the repository into a cache directory under `~/.snowflake/cortex/remote_cache/` and discovers every `SKILL.md` it contains.

To add a GitHub skill:

1. Open the **Agent Settings** panel and select the **Skills** category.
2. In the **GitHub Skills** section header, click the `+` button (*Add from GitHub*).
3. Enter a source in any of these supported formats:
   - `owner/repo` — for example, `anthropics/skills`
   - `owner/repo#branch` — pin to a specific branch or tag
   - `https://github.com/owner/repo`
   - `https://github.com/owner/repo/tree/branch/path` — restrict discovery to a subfolder
4. Click **Add**.

Use the **Update** action on a GitHub skill (or **Update all** at the top of the section) to re-download the latest version. If the repository no longer contains a `SKILL.md`, CoCo surfaces an error and leaves your previous version in place.

Note

For private repositories, CoCo uses your system Git credentials. If a clone fails with an authentication error, run `git clone <url>` from your terminal first to confirm credentials are set up.

### Snowflake Stage skills

Stage skills let your team share skills through a Snowflake stage instead of a Git repository. This is the recommended way to distribute skills inside your organization when you want governance through Snowflake roles and grants rather than Git permissions.

To add a stage skill:

1. Make sure you are connected to a Snowflake account with read access to the stage.
2. Open the **Agent Settings** panel and select the **Skills** category.
3. In the **Shared Skills** section header, click the `+` button (*Add from Snowflake*).
4. Enter the stage path in the format `@DATABASE.SCHEMA.STAGE` or `@DATABASE.SCHEMA.STAGE/subfolder/`.
5. Click **Add**.

CoCo downloads the contents of the stage path into `~/.snowflake/cortex/stage_cache/`, scans for `SKILL.md` files, and registers every skill it finds. Use **Update** on a stage skill to re-fetch the latest contents.

Note

Stage paths must match `@DB.SCHEMA.STAGE` or `@DB.SCHEMA.STAGE/path`. Paths containing SQL or shell metacharacters such as `;`, `'`, `--`, `/* */`, `$`, or backticks are rejected to prevent SQL injection. Quoted identifiers (for example, `@"My DB".PUBLIC.SKILLS`) are supported.

## Using a skill in chat

Once a skill is registered, the agent can invoke it in two ways:

- **Automatically**, by matching your prompt against each skill’s `description`. If your message clearly matches a skill (for example, “create a new Cortex Agent” matches `create-cortex-agent`), the agent runs that skill’s instructions before doing anything else.
- **Explicitly**, by mentioning the skill in chat. Type `/` in the chat input and pick a skill from the picker, or reference it by name (for example, “use the `commit` skill to commit my changes”).

When the agent invokes a skill, you see a “Using skill `name`” indicator in the chat transcript. Click the skill name to open its `SKILL.md` and inspect what the agent loaded.

You can chain several `/skill` commands in a single message, and CoCo runs each one.

## Managing skills

All skill management actions are available from the **Skills** tab of the Agent Settings panel.

### Favorite a skill

Click the star icon next to a skill in the Skills tab to add it to favorites. Favorites are saved to `~/.snowflake/cortex/skills.json` and sync across windows of the desktop app.

### Disable a skill

Disabling a skill keeps it visible in the Skills tab but prevents the agent from invoking or auto-selecting it. Use this to silence a built-in skill you don’t want the agent to use, or to temporarily turn off a custom skill while you’re editing it.

Disabled skills are stored in the user setting:

Copy code

```
"snowflake.skills.disabledSkills": [
    "introduce-coco-desktop",
    "my-team:legacy-runbook"
]
```

### Update a skill

For GitHub and Stage skills, the **Update** action re-downloads the latest contents of the source. The **Update all** action at the top of each section refreshes every skill in that section in one pass. Project, local, and packaged skills update automatically when you edit the underlying files.

### Remove a skill

The **Remove** action behavior depends on the source:

| Source | What “Remove” does |
| --- | --- |
| Packaged | Not allowed. Disable the skill instead. |
| Project | Deletes the skill folder from your workspace. |
| Local | Unregisters one skill, or unregisters the entire local folder. Files on disk are left alone. |
| GitHub | Removes the entry from `skills.json` and deletes the cached clone under `remote_cache/`. |
| Stage | Removes the entry from `skills.json` and deletes the cached download under `stage_cache/`. Files in the stage itself are not touched. |
| Plugin | Uninstall the plugin from the Plugins view; all of its skills are removed together. |

Expand

Show lessSee more

## Publish a skill to a Snowflake stage

You can publish any local or project skill to a Snowflake stage so other Snowflake users in your organization can register it from their own CoCo Desktop installations.

To publish a skill:

1. Open the **Agent Settings** panel and select the **Skills** category.
2. Select the skill you want to publish.
3. Click **Publish to stage**.
4. Enter the destination stage path (for example, `@SHARED.SKILLS.TEAM_LIBRARY/release-notes/`).
5. Confirm whether to overwrite existing files, then click **Publish**.

CoCo uploads the entire skill directory — `SKILL.md` plus any supporting scripts or resources — to the stage. Teammates can then add it from the Skills view using the same stage path.

Tip

Use a dedicated database/schema with appropriate role grants for shared skills (for example, `SHARED.SKILLS` readable by `PUBLIC` and writable only by skill maintainers). This gives you fine-grained access control without requiring Git access for everyone on the team.

## Skills Catalog

The **Skills Catalog** is Snowflake’s built-in registry for sharing and discovering skills across your organization. Skills in the catalog are stored as versioned Cortex Extension objects, so access is governed by Snowflake roles and grants: no Git credentials or file sharing required.

### Browse the catalog

Click the **Browse Skills Catalog** link in the Skills view, or use the bundled `find-skill` skill in chat to search by description. The browse link opens the **Skills & Plugins** page in Snowsight, where you can search published skills, read their descriptions, and copy import links.

[![Browse Skills Catalog link in the Skills panel header](/static/images/user-guide/cortex-code/cortex-code-desktop/skills/skill-catalog-browse-link.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/skills/skill-catalog-browse-link.png)

Catalog-sourced skills appear in the **Shared** section of the Skills tab with a **CATALOG** badge instead of the usual **STAGE** badge.

### Import a skill from the catalog

1. In Snowsight, find the skill you want and copy its share link, a URI that starts with `snow://skill_catalog/`.
2. In CoCo Desktop, open the **Agent Settings** panel and select the **Skills** category.
3. In the **Shared** section header, click the **+** button and choose **Add from Skills Catalog**.

   [![Add from Skills Catalog option in the + menu](/static/images/user-guide/cortex-code/cortex-code-desktop/skills/skill-catalog-import-button.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/skills/skill-catalog-import-button.png)
4. Paste the `snow://` link into the **Import link** field and click **Import**.

   [![Import Skill dialog with a snow:// URI pasted in](/static/images/user-guide/cortex-code/cortex-code-desktop/skills/skill-catalog-import-dialog.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/skills/skill-catalog-import-dialog.png)

CoCo Desktop downloads the skill files from Snowflake, discovers the `SKILL.md`, and registers the skill. It appears in the **Shared** section with a **CATALOG** badge and can be invoked immediately.

Note

Import links must start with `snow://skill_catalog/` or `snow://cortex_extension/` and include a specific version number (for example, `.../versions/version$1/`). URIs that contain SQL metacharacters (`;`, `--`, `/* */`, backticks) are rejected.

### Publish a skill to the Skills Catalog

You can publish any local or project skill to the Skills Catalog so others in your organization can import it.

1. Open the **Agent Settings** panel and select the **Skills** category.
2. Select the skill you want to publish.
3. Click **Publish to Skills Catalog** (cloud-upload icon).

   [![Publish to Skills Catalog option on a skill](/static/images/user-guide/cortex-code/cortex-code-desktop/skills/skill-catalog-publish.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/skills/skill-catalog-publish.png)

A chat session opens and runs the publish workflow, which:

1. Creates a `CORTEX EXTENSION` object in your Snowflake account.
2. Uploads the skill files to Snowflake’s versioned storage.
3. Commits the version and grants read access (to PUBLIC, or to a role you specify).
4. Returns a `snow://skill_catalog/...` URI you can share with your team.

Note

The **Publish to Skills Catalog** option is available for local and project skills. Skills already imported from the catalog cannot be republished through this workflow. Use **Publish to stage** to push to a regular named stage instead.

### Remove a catalog skill

To remove a catalog skill, use the **Remove** action in the Skills tab. This unregisters the skill and deletes the local cache. The Cortex Extension object in your Snowflake account is not affected.

## Create your own skill

A skill is a folder with a `SKILL.md` file. The minimal layout looks like this:

Copy code

```
my-skill/
  SKILL.md            (required)
  scripts/            (optional helper scripts)
  reference.md        (optional supplementary docs)
```

### Anatomy of SKILL.md

`SKILL.md` starts with YAML front matter that gives the skill a **name** and a **description**, followed by a markdown body that the agent reads when the skill is invoked.

Copy code

```
---
name: release-notes
description: Generate a customer-facing release notes draft for a Cortex Code build
  by reading the changelog and PR titles since the last release.
---

# Release notes generator

When the user invokes this skill, follow these steps:

1. Run `git log --oneline` to find commits since the last tag.
2. Group commits by component prefix (`[analyst]`, `[codingagent]`, etc.).
3. Draft a markdown release notes section grouped by feature, fix, and chore.
4. Show the draft to the user and ask for edits before saving.
```

The **name** is what the user types to invoke the skill and what the agent matches against. The **description** is critical: the agent uses it to decide when to auto-invoke the skill, so it should clearly state what the skill does and when to use it.

### Use the plugin-creator skill

The fastest way to scaffold a new skill is to ask the agent to use the bundled `plugin-creator` skill. It walks you through an interactive wizard, generates the directory layout, and creates a starter `SKILL.md`.

In the chat panel, type:

Copy code

```
create a new plugin called my-team-skills with one skill
```

The agent invokes `plugin-creator`, asks for the plugin name, the skills it should contain, and any hooks or MCP servers, then writes the files to a folder you choose.

### Test your skill locally

1. Save your skill folder somewhere on disk (for example, `~/snowflake-skills/release-notes/`).
2. Open the **Agent Settings** panel, select the **Skills** category, and use the *Add Local Skill* button (`+`) in the **Local Skills** section to register the parent directory.
3. Open a chat and ask for the workflow your skill describes. Confirm the agent invokes the skill (you’ll see “Using skill” in the transcript).
4. Edit `SKILL.md` to refine instructions and re-run. Changes are picked up live.
5. When you’re satisfied, publish to a Git repository or Snowflake stage so others can use it.

## Settings reference

| Setting / path | Description |
| --- | --- |
| `snowflake.skills.disabledSkills` | Array of skill IDs the agent will not invoke or auto-select. Set per workspace or per user. |
| `snowflake.skills.recentStagePaths` | Recently used Snowflake stage paths, used for autocompletion in the Add-from-stage and Publish-to-stage dialogs. |
| `~/.snowflake/cortex/skills.json` | Persistent skill configuration: registered local folders, GitHub sources, stage entries, marketplace entries, and favorites. Shared with the `cortex` CLI. |
| `~/.snowflake/cortex/remote_cache/` | Local cache of cloned GitHub repositories backing GitHub skills. |
| `~/.snowflake/cortex/stage_cache/` | Local cache of files downloaded from Snowflake stages. |

Expand

Show lessSee more

## Troubleshooting

### “No SKILL.md found” when adding a folder or repo

CoCo recursively scans up to 10 directories deep for `SKILL.md` files. If you see this error, check that your skill folder contains a file named exactly `SKILL.md` (the name is case-sensitive on Linux and macOS) and that it is not nested inside an excluded hidden folder (any directory whose name begins with `.`).

### “Invalid stage path format”

Stage paths must start with `@` and follow the pattern `@DATABASE.SCHEMA.STAGE` or `@DATABASE.SCHEMA.STAGE/path`. They cannot contain shell metacharacters, semicolons, or `..`.

### GitHub clone fails

CoCo uses your system Git credentials. Try cloning the repository from a terminal first (`git clone <url>`); if that fails, fix your credentials there and retry the Add Skill flow. If the URL is correct but no skills are discovered, the repository likely doesn’t contain a `SKILL.md`; the cached clone is removed automatically in that case.

### Skill doesn’t appear in the chat picker

- Confirm the skill shows up in the Skills tab of the Agent Settings panel.
- Verify it isn’t listed in `snowflake.skills.disabledSkills`.
- Check the `name` in the skill’s YAML front matter — this is what the picker matches.

### “Cannot import skills from the packaged skills directory”

You tried to register the application’s bundled `resources/snowflake/skills/` directory as a local skill source. This is not allowed because the bundled skills are already loaded by CoCo. Pick a different folder for your custom skills, such as `~/snowflake-skills/`.
