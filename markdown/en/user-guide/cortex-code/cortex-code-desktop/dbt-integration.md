# dbt integration in CoCo Desktop

CoCo Desktop turns any workspace that contains a `dbt_project.yml` into a full dbt development
environment. The controls you need live on the **Project Action Bar** at the bottom of the window.
Pick a project, choose how it runs, and start a command. The **Current Project** output channel
records the command transcript. After the command finishes, CoCo Desktop also focuses the surface
that holds that result: **SQL Results** for **Show**, and the **Current Project** channel for every
other operation. Compiled SQL is separate: after compile artifacts exist, **View Compiled SQL** in
the editor title bar opens the compiled file beside your model.

## Getting started

For guided, in-context help while you work, use the
[`dbt-projects-on-snowflake`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-dbt-projects-on-snowflake)
bundled skill. We recommend invoking the skill with `/dbt-projects-on-snowflake` and describing what you
want in plain language.

CoCo Desktop scans your workspace for `dbt_project.yml` files. When it finds at least one project,
the Project Action Bar appears at the bottom of the window with the first project it found selected.
Projects are listed by folder name. Use the project picker to switch. The bar shows in
[Editor view](/user-guide/cortex-code/cortex-code-desktop/agent-view-and-editor-view), not in Agent
view, and it stays hidden if you hid it yourself. The bar has two layouts, one for each execution
mode.

## Project Action Bar

### Snowflake-managed layout

In Snowflake-managed mode, the Project Action Bar shows the pickers that a server-side run needs,
plus a two-part operation control. The main part runs the selected operation. The chevron next to it
opens the list of operations.

[![Project Action Bar in Snowflake-managed mode with the project picker, the profile picker set to dev, the Environment picker set to None, the additional flags box, the run-options control, the two-part operation control showing Build on the main part and a chevron for the operation list, and the Snowflake control](/static/images/user-guide/cortex-code/cortex-code-desktop/dbt/dbt-action-bar-managed.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/dbt/dbt-action-bar-managed.png)

| Control | What it does |
| --- | --- |
| Project picker | Selects the dbt project to run. The run uses your active CoCo Desktop Snowflake connection. |
| **profile** | Selects the **target** within the profile named in your project’s `dbt_project.yml`. The picker reads targets from [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) when that file is in the project root, and from `profiles.yml` otherwise. |
| **Environment** | Selects a named environment from `env.yml`, or `None`. See [SQL environment variables and private Git package support](#label-coco-desktop-dbt-env-vars). |
| Additional flags | Free-text flags appended to the dbt command, for example `--full-refresh` or `--vars '{"key": "value"}'`. |
| Operation control | A two-part control. Select the main part (labeled with the current operation, for example **Build**) to run that operation. Select the chevron to open the list and choose **Deps**, **Seed**, **Compile**, **Run**, **Test**, **Build**, **Retry**, **Parse**, **Docs generate**, **List**, **Show**, **Snapshot**, or **Run operation**. After you choose an operation, the main part runs it. While a run is in progress, the control becomes **Stop**. |
| Snowflake control | Opens **Settings** at `dbt.executionMode` so you can change the execution mode. It opens **Workspace Settings** when the workspace sets that value, and **User Settings** otherwise. |

Expand

Show lessSee more

Select the run options control next to the operation control to set the runtime and network access
for the run, and to turn on **Defer to Production**.

| Field | Purpose |
| --- | --- |
| **dbt Version** | The Snowflake-managed runtime for the run, for example dbt Core 1.12.3 or dbt 2.0.0. |
| **External Access Integration** | The EAI to attach when dbt needs network access to fetch packages declared in `packages.yml`. The list shows the integrations that `SHOW EXTERNAL ACCESS INTEGRATIONS` returns for your active role. Leave it empty if your project uses only local packages. |
| **Defer to Production** | Whether this project’s commands run with the artifacts of a production dbt project object, so that dbt can defer to production. See [Defer to production](#label-coco-desktop-dbt-defer). |

Expand

Show lessSee more

Note

With **dbt Core**, an EAI is required for `dbt deps`. With the **dbt Fusion engine**, `dbt deps` runs implicitly during `dbt compile` and `dbt run` if `dbt_packages` is missing, so the EAI may also be needed for those commands.

`dbt deps` is what populates `dbt_packages`. Nothing else installs or updates the packages in it, so a `packages.yml` edit such as a version bump doesn’t reach `dbt_packages` until deps runs again. With the dbt Fusion engine, the implicit run doesn’t cover that case, because it only happens when `dbt_packages` is missing. Run **Deps** after you change `packages.yml`. In Snowflake-managed mode, CoCo Desktop syncs `dbt_packages/` back to your project after a **Deps** run, or when your local packages folder is missing or empty.

See [Understand dependencies for dbt projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dependencies).

### Local layout

In local mode, the Project Action Bar is a compact command line for the local `dbt` CLI.

[![Project Action Bar in local mode with the project picker, the Python Interpreter picker showing Select interpreter, the command box, the Run button, and the Switch to Snowflake-managed button](/static/images/user-guide/cortex-code/cortex-code-desktop/dbt/dbt-action-bar-local.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/dbt/dbt-action-bar-local.png)

| Control | What it does |
| --- | --- |
| Project picker | Selects the dbt project to run. The local `dbt` CLI resolves `profiles.yml` for the run. |
| **Python Interpreter** | Selects the Python interpreter that provides the local `dbt` CLI. |
| Command box | Takes a free-form dbt command, for example `run --select my_model+`. Type the command without `dbt`, then press Enter or select **Run**. |
| **Run** | Runs the command you typed. Output streams line by line to the **Current Project** output channel. While the command runs, **Run** becomes **Stop** and the command box is disabled. |
| **Switch to Snowflake-managed** | Switches the execution mode to Snowflake-managed and swaps the bar to the Snowflake-managed layout. You can’t switch modes while a dbt command is running. |

Expand

Show lessSee more

When the window is too narrow for every control, the Project Action Bar hides controls instead of
overlapping them. In Snowflake-managed mode, the **Environment** picker shortens to **Env** and then
hides, and then the **profile** picker hides. In local mode, the **Python Interpreter** picker and
**Switch to Snowflake-managed** hide. Widen the window to bring them back.

### Show and hide the Project Action Bar

You can hide the Project Action Bar to get its row of vertical space back. There are three ways to
do it:

1. Run **View: Toggle Project Action Bar** from the Command Palette. This both hides and shows the
   bar.
2. In the menu bar, select **View** > **Appearance** > **Project Action Bar**. The check mark shows
   whether the bar is currently visible.
3. Right-click the project name at the left end of the Project Action Bar and select **Hide**. This
   method can only hide the bar.

When you hide the bar with the Command Palette or the View menu, CoCo Desktop remembers that
choice for this workspace on this machine. The bar stays hidden until you show it again with the
Command Palette or **View** > **Appearance** > **Project Action Bar**. Running an operation from
the editor title bar also shows the bar, but it doesn’t change your saved choice: the bar is hidden
again the next time you open the workspace. To keep the bar shown, turn it back on with the Command
Palette or the View menu.

If you’re in [Agent view](/user-guide/cortex-code/cortex-code-desktop/agent-view-and-editor-view) or
if CoCo Desktop doesn’t detect a dbt project, the Project Action Bar won’t be visible at that time.

## Execution mode

CoCo Desktop can run dbt commands two ways:

| Mode | Where dbt runs | What it requires |
| --- | --- | --- |
| **Local** (default) | The local `dbt` CLI on your machine | A working local dbt installation |
| **Snowflake-managed** | Inside Snowflake via `EXECUTE DBT PROJECT FROM WORKSPACE` | An active Snowflake connection, but no local dbt installation |

Expand

Show lessSee more

In Snowflake-managed mode, your dbt project files are synced to a Snowflake workspace under your
account, dbt executes server-side, and generated artifacts (`target/`, root files such as
`package-lock.yml`, and logs) are synced back to your local project directory when the run
finishes. Only generated files come back, not the project files you uploaded. `dbt_packages/` is
only synced back after a **Deps** run, or when your local packages folder is missing or empty. A run
that you cancel, or that fails before dbt itself runs, syncs no generated artifacts back. Output,
lineage, compiled SQL, and query results work the same way in both modes. The difference is where
the work happens.

The `dbt.executionMode` setting determines which mode CoCo Desktop uses to run the dbt project. You
can change the mode from the Project Action Bar: select **Switch to Snowflake-managed** in the local
layout, or select the Snowflake control in the Snowflake-managed layout, which opens **Settings** at
`dbt.executionMode`. You can also edit the setting directly in **User Settings** or **Workspace
Settings**.

Commands that connect to Snowflake need a valid profile, and each mode reads a different file. In
**Local** mode, the local `dbt` CLI reads only `profiles.yml`, exactly as documented by dbt, and
resolves it from your machine (`~/.dbt/profiles.yml` unless you point dbt somewhere else). In
**Snowflake-managed** mode, the workspace reads `dbt_projects_profiles.yml` when present and falls
back to `profiles.yml`, and at least one of those files must be in the project root. For the fields
each file needs, see
[Prerequisites for Snowflake-managed mode](#prerequisites-for-snowflake-managed-mode).

This split is deliberate. Both files can live in the project root at once, and the local `dbt` CLI
doesn’t recognize `dbt_projects_profiles.yml`, so adding it never disrupts anyone’s existing local
dbt workflow. That means hybrid teams (teams where some members run dbt with the local `dbt` CLI and
others use Workspaces) can share one Git-versioned project and switch modes without editing
connection settings for each other.

For the underlying Snowflake feature, see
[Workspaces for dbt projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces).

### What happens when you run a command

When you run a dbt command in Snowflake-managed mode, CoCo Desktop:

1. **Ensures a workspace exists** in your account at `USER$.PUBLIC` named
   `coco_smws_<folder>_<hash>`, where `<folder>` is the name of your local project folder and
   `<hash>` is a 6-character identity prefix derived from the project path. The workspace is
   created on first use and reused on subsequent runs.
2. **Syncs your project files** to the workspace. CoCo Desktop uploads the files at the project
   root and the files in the project’s resource folders: the `model-paths`, `seed-paths`,
   `test-paths`, `macro-paths`, `snapshot-paths`, `analysis-paths`, `function-paths`, `osi-paths`,
   `check-paths`, and `skill-paths` folders (or their dbt defaults), plus `docs-paths` and `asset-paths` when `dbt_project.yml` sets them.
   Other folders at the project root aren’t uploaded. CoCo Desktop also skips dotfiles other than
   the root `.dbtignore`, files that `.dbtignore` matches, and symbolic links. Only files that
   changed since the last sync are uploaded, so subsequent runs are fast. Your local `target/` and
   `dbt_packages/` folders aren’t uploaded. The workspace gets its own copy of the packages when you
   run **Deps**, which installs them server-side.
3. **Executes the dbt command** on Snowflake via `EXECUTE DBT PROJECT FROM WORKSPACE`. The
   warehouse, database, schema, and role specified in the active target (selected with the
   **profile** picker, defined in `dbt_projects_profiles.yml` or `profiles.yml` under the
   `profile:` named in `dbt_project.yml`) are used for the run.
4. **Syncs generated artifacts back** to your local project directory so compiled SQL and lineage
   reflect the server-side run. Only generated files come back. A run that you cancel, or that
   fails before dbt itself runs, syncs nothing back.

The **Current Project** output channel records the dbt execution: the command, the output, and the
status. The SQL statement is `EXECUTE DBT PROJECT FROM WORKSPACE` in Snowflake-managed mode. Select
**Stop** to cancel a running command.

### SQL environment variables and private Git package support

A single Git-versioned `env.yml` file lets you:

- Give each developer an isolated configuration through context functions.
- Build robust orchestration by pulling runtime metadata from live SQL into each run.
- Manage multiple environments and secrets, including authenticating `dbt deps` against private Git packages.

CoCo Desktop supports environment variables defined in an `env.yml` file, but only in Snowflake-managed mode.

When you run a command, Snowflake resolves `env.yml` before the run to inject the environment variables.

Use the **Environment** picker on the Project Action Bar to select a named environment, and override
individual environment variables for a single run. The resolved values flow into
`dbt_projects_profiles.yml` when that file is present, or into `profiles.yml` otherwise.

For env.yml authoring, environment selection, value precedence, secrets, and the full reference, see [Use SQL environment variables and private Git packages](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

### Defer to production

**Defer to Production** gives a Snowflake-managed run the artifacts from an earlier run of your
production dbt project object. If a model in your command refers to an upstream model that the
command doesn’t select and that doesn’t exist in your development target yet, dbt resolves the
reference to the production relation, so you don’t have to build the upstream model first. If the
upstream relation already exists in your development target, dbt uses it instead. **Defer to
Production** is available only in Snowflake-managed mode.

[![The run options popover with Defer to Production turned on, showing the helper text about the appended flags, the database and schema picker, the dbt project object picker, and Compare to set to Last successful run](/static/images/user-guide/cortex-code/cortex-code-desktop/dbt/dbt-run-options-defer.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/dbt/dbt-run-options-defer.png)

To set it up for a project:

1. Select the run options control next to the operation control.
2. Turn on **Defer to Production**.
3. Under **Select Project Object**, select the database and schema that contain your production dbt
   project object, and then select the object. The list shows the dbt project objects in that schema
   that your active role can see.
4. In **Compare to**, select the run whose artifacts dbt uses: **Last successful run** (the
   default), **Last run**, or **Last failed run**.

CoCo Desktop saves these choices for each project. While **Defer to Production** is on, every
Snowflake-managed command for the project runs with `--state ./imports/state --defer`, and Snowflake
imports the selected run’s artifacts into `./imports/state`. To build only the models you changed
and the models downstream of them, add `--select state:modified+` to the additional flags on the
Project Action Bar.

CoCo Desktop doesn’t start a run until you select a database, schema, and project object. The
production object also needs a run in the last 14 days that matches your **Compare to** selection,
and your role needs the `MONITOR` privilege on it. To set up the production object, see
[Use dbt artifacts for Slim CI and defer to production](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod).

### Prerequisites for Snowflake-managed mode

- **An active Snowflake connection** signed in via the connection picker.
- **A `dbt_projects_profiles.yml` or `profiles.yml` file** in each dbt project folder. The `type` must be `snowflake` and the
  `warehouse`, `database`, `schema`, and `role` fields must be set. Unlike dbt Core, the
  `account` and `user` fields can be left empty or with arbitrary values, because the workspace runs
  under your current Snowflake user and account context. See
  [Workspaces for dbt projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces#label-dbt-requirements-workspaces)
  for the full requirements. If both files are present, Snowflake uses `dbt_projects_profiles.yml` and ignores `profiles.yml` for compilation and subsequent commands. For more information, see [Use dbt\_projects\_profiles.yml for a unified development-to-production experience](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file).
- **Personal databases enabled** on your account. Snowflake workspaces are created in a
  personal database, which an account administrator must enable. See the
  [personal database requirement](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces#label-dbt-requirements-workspaces-personal-database).
- **An external access integration**, *only if* your `packages.yml` references remote packages
  (for example, packages from the dbt Packages hub or a Git repository). Select the EAI once from
  the Project Action Bar. CoCo Desktop remembers it for that project and reuses it on subsequent
  runs. Local-only dependencies don’t require one. See
  [Workspaces for dbt projects on Snowflake: dependencies](/user-guide/data-engineering/dbt-projects-on-snowflake-dependencies)
  for setup details.

### Project size limit

When you deploy a specific dbt project folder as a dbt
project object, that folder can contain at most 100,000 files across all folders, including
generated `target/` and `dbt_packages/` artifacts. See
[Limitations, requirements, and considerations for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-limitations).

### Inspecting your workspaces

Each project gets a dedicated Snowflake workspace named `coco_smws_<folder>_<hash>`. The `<folder>`
part is the name of your local project folder, lowercased and with every non-alphanumeric character
replaced by an underscore. It isn’t the `name:` field in `dbt_project.yml`. The `<hash>` part is a
6-character identity prefix derived from the project path, so two folders with the same name get
different workspaces. To list the workspaces CoCo Desktop has created in your account:

Copy code

```
SHOW WORKSPACES LIKE 'coco_%' IN SCHEMA USER$.PUBLIC;
```

Workspaces persist between sessions, so the next sync only uploads what’s changed. If a workspace is
dropped externally, for example by an administrator, CoCo Desktop re-creates it and performs a full
sync on the next run.

## Editor title actions

With a dbt model open in the editor, the editor title bar adds a **Run Project File** button (its
tooltip reads **Run dbt for Current Model**). Open its menu to run **Compile**, **Run**, **Test**,
**Build**, **List**, or **Show** for that model. Running an operation this way also selects that
model’s project in the Project Action Bar, shows the bar if it’s hidden, and fills it with the
operation and `--select <model>`, so the bar shows the command that’s running. Focus stays in the
editor while the command runs. The button is disabled while a dbt command is running for the project or while packages
aren’t in the Snowflake workspace yet. In Snowflake-managed mode, it’s also disabled while **Defer
to Production** is on for the project but its production database, schema, and project object aren’t
all selected, with the tooltip **Select a production database, schema, and project object before
running with Defer to Production.** Select the gear on a menu item, **Run with flags…**, to fill
the Project Action Bar with that operation and `--select <model>` without running it, so you can add
flags first. The Project Action Bar remains the main way to run a project.

[![Editor title bar for a dbt model with the run menu open on Compile, Run, Test, Build, List, and Show, each with a gear for running with flags](/static/images/user-guide/cortex-code/cortex-code-desktop/dbt/dbt-editor-title-actions.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/dbt/dbt-editor-title-actions.png)

A dbt SQL model also gets a **View Compiled SQL** action in the editor title bar. It’s disabled
until the compiled file exists, with the tooltip **Compile project to view compiled SQL.**, and it
opens the compiled SQL beside your model.

Models, seeds, and SQL snapshots also get a **Show in Lineage** action in the editor title bar and in
the editor’s context menu. It’s also in the Command Palette as **dbt: Show in Lineage**. It anchors
the [Lineage](#lineage) view on that file’s node, opens the view, and selects the file’s project in
the Project Action Bar. It’s disabled, with the tooltip **Compile project to show in Lineage**,
until the file appears in the project’s `manifest.json`. Snapshots defined in YAML don’t get the
action.

## Where results appear

dbt results land in the workbench views you already use for SQL work. **Output**, **SQL Results**,
and **Lineage** are panel views, so you can resize the panel, drag any of them into a sidebar, and
leave the one you want open next to your editor while a run finishes. Compiled SQL opens as a
regular editor pane.

| Surface | What it shows |
| --- | --- |
| **Output** | The **Current Project** channel records each run: the command that ran, a running status, the dbt output (including per-model progress during `dbt run` or `dbt build`), and a completed, failed, or cancelled status. Local runs stream as dbt writes them. Snowflake-managed runs return their output when the run finishes. |
| **SQL Results** | Rows returned by the **Show** operation (`dbt show`) open in SQL Results, where you can sort and scan them like any other query result. **Show** doesn’t open an editor pane. Results are the same in local and Snowflake-managed mode. |
| **Lineage** | A workbench view with the interactive dependency graph for your project. After a **Run** or a **Build**, nodes in the graph show their run status, while the transcript stays in the **Current Project** channel. CoCo Desktop doesn’t open the view on its own: open it yourself, or use **Show in Lineage**. |
| Compiled SQL | Compiled output opens as an editor pane when you select **View Compiled SQL** in the editor title bar, after the file exists in your project’s `target/compiled` folder. Because it’s an editor pane, you get syntax highlighting, search, and copy the same as any other file. This is the exact query dbt would run against your warehouse. Compiling doesn’t open the pane on its own. |

Expand

Show lessSee more

## Lineage

The Lineage view renders an interactive directed acyclic graph (DAG) of the project that’s selected
in the Project Action Bar. It shows how models, sources, and other resources relate to each other.
The view doesn’t follow the file you’re editing. Instead, you anchor it on a node.

[![Lineage view anchored on the int_customer_orders model at depth 5, showing the toolbar with back, forward, anchor history, refresh, the anchor chip, depth, and Columns controls, the selection hint bar, the staging models upstream and the dim_customers, fct_orders, and rpt_customer_summary models downstream, and the Project Action Bar in local mode below it](/static/images/user-guide/cortex-code/cortex-code-desktop/dbt/dbt-lineage-view.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/dbt/dbt-lineage-view.png)

The Lineage view anchored on a model at the default depth of 5.

With no anchor, the view shows the whole project, and a banner shows the project name and its
node count. To focus the graph on one node, anchor it: use **Show in Lineage** on an open model,
seed, or SQL snapshot (see [Editor title actions](#editor-title-actions)), double-click the node, which
also opens its file if it has one, or select the node and press Enter. An anchored graph shows the anchor and the
nodes upstream and downstream of it. The view draws at most 300 nodes. When there are more, a
banner says how many it’s showing.

- **Depth**: Set how many hops from the anchor to show, from 1 to 300 (default: 5). The control
  appears while the view is anchored.
- **Navigation**: Use the back and forward arrows, or press Option+Left and Option+Right (macOS) or
  Alt+Left and Alt+Right (Windows and Linux), to move between the anchors you used in this project,
  or open **Anchor history** to jump to one. Select the close button on the **Anchor** chip to clear the anchor and return to the whole project.
- **Refresh**: Reload the graph from the project’s `manifest.json`. Refresh doesn’t run dbt.
- **Columns**: Show or hide column details on the nodes.
- **Selection**: Click a node to select it. Shift+click, Command+click (macOS), or Ctrl+click
  (Windows and Linux) adds or removes a node, Shift+drag selects a region, Command+A or Ctrl+A
  selects everything, and Esc clears the selection, then the anchor. The hint bar in the view labels
  these with the macOS keys on every platform.

If the project doesn’t have a valid `manifest.json` yet, the view says there’s no lineage for the
project yet and shows a **Compile project** button that runs `dbt compile`. The button compiles the
project that’s selected in the Project Action Bar.

Tip

Select one or more nodes in the lineage graph, then use the “Add to Chat” action to attach the
selected models as context to your AI conversation. This helps the agent understand your project
structure when answering questions or generating code.

## Project detection

CoCo Desktop automatically detects dbt projects by scanning your workspace for `dbt_project.yml`
files, up to 10 folders deep. It skips folders whose names start with a dot, such as `.git` or
`.venv`, and folders named `target`, `dbt_packages`, `dbt_internal_packages`, `node_modules`, `env`,
`venv`, and `site-packages`. To search one of these folders, list its path in
`dbt.allowListFolders`. The allow list limits discovery to the folders it lists, so also list any
other folders that contain projects. Opening a dbt file doesn’t change which project the Project Action Bar
targets: use the project picker for that, or run an operation or **Show in Lineage** from the editor
title bar, which selects that file’s project. The Lineage view doesn’t follow the file you’re
editing. To focus the graph on a file’s node, use **Show in Lineage**. See [Lineage](#lineage).

For the profile file each execution mode reads, and the project-root requirement in
Snowflake-managed mode, see [Execution mode](#execution-mode).

## Settings

| Setting | What it controls |
| --- | --- |
| `dbt.enabled` | Turns dbt integration and project discovery off. It’s on by default. Set it to `false` when you want CoCo Desktop to stop scanning for `dbt_project.yml` files. With discovery off, the project list clears and the Project Action Bar has nothing to show. |
| `dbt.allowListFolders` | Restricts project discovery to the listed folders under each workspace root, for example `analytics` or `analytics/core`. An empty list scans everything. Matching is case-sensitive and by path segment: `analytics` includes `analytics/core`, not `analytics-old/core`. `.` or `/` means the workspace folder root and matches everything, the same as an empty list. Discovery skips dot-folders and folders such as `target` and `dbt_packages` (see [Project detection](#project-detection)). List one by its path, for example `.worktrees/feature`, to search it. |
| `dbt.executionMode` | The execution mode for dbt commands, either `local` or `snowflake-managed`. **Switch to Snowflake-managed** writes to it: to **Workspace Settings** when the workspace already sets it, and to **User Settings** otherwise. |
| `dbt.executionTimeout` | How long, in seconds, a dbt run can take before CoCo Desktop cancels it and reports it as failed. It applies to local runs and to Snowflake-managed runs (`EXECUTE DBT PROJECT`). The default is 14400 (4 hours) and the minimum is 60. This setting replaces `dbt.snowflakeManaged.executionTimeout`. CoCo Desktop moves a value set under the old name to the new one automatically. |

Expand

Show lessSee more
