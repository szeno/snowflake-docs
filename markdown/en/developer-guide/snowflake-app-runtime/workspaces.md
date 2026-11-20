# Develop in Snowsight Workspaces

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Build, preview, and deploy a Snowflake App Runtime app from your browser, with
nothing to install. Create the app from **+ Add new** in a workspace or with
[Cortex Code in Snowsight](/user-guide/cortex-code/cortex-code-snowsight),
preview it as you edit, and deploy it from the same place.

For step-by-step instructions, see
[Get started with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/getting-started) and choose the
**Snowsight Workspaces** tab.

## How preview works

When you select **Preview**, Snowflake syncs your project to a dev server,
installs its dependencies (including `devDependencies`), and runs the project’s
`dev` script. Each user gets a dev server for each project, so a preview is
yours alone and has no shareable URL. To share the app, deploy it.

Workspaces saves your edits as you type and syncs them to the dev server within
a second, and the app reloads in place. Edits to `package.json` or a lockfile
(`package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock`) reinstall dependencies
and restart the dev server. Lockfiles that the installer writes sync back to
the workspace.

The dev server runs on Snowflake compute. It suspends after a period of
inactivity and resumes when you reopen **Preview**. Closing the Preview pane or
the browser tab leaves it running until then. To stop it now, select
**Shutdown** from the Preview pane’s menu.

## Supported projects

Workspaces supports Next.js projects. A project needs an
[`app.yml`](/developer-guide/snowflake-app-runtime/app-yml) manifest
and a `package.json` with a `dev` script. If the project uses `snowflake.yml`,
Workspaces offers to upgrade it. When you bring an existing project into a
workspace, don’t upload `node_modules`.

Other projects with a `dev` script that listens on the port Snowflake provides
might run, but they aren’t supported.

## Preview compared to a deployed app

| Capability | Preview | Deployed app |
| --- | --- | --- |
| Where it runs | One dev server for each user and project | An Application Service |
| Source | Synced from the workspace | Built into the deployed version |
| Command | `npm run dev` (or the equivalent for `pnpm`/`yarn`) | The `run` command in `app.yml` |
| `NODE_ENV` | `development` | `production` |
| Shareable | No | Yes, at the app’s URL |
| Logs | Live logs in the Preview pane | Live logs and the event table. See [Monitor a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/observability) |
| Caller’s rights | Not available | Available |

Expand

Show lessSee more

Because preview has no caller’s rights, test row access and masking policies in
a deployed app.

## Configure preview

Preview reads three fields from `app.yml`:

- `external_access_integrations`: the integrations the dev server can reach.
  Preview doesn’t start if your role can’t see one of them.
- `secrets`: `GENERIC_STRING`, `PASSWORD`, and `OAUTH2` secrets. Each one is
  mounted at `/secrets/<name>/<key>`, the same path a deployed app uses.
- `environment_variables`: passed to the dev server. You can’t use the names
  that preview sets: `SNOWFLAKE_HOST`, `NODE_OPTIONS`,
  `SNOWFLAKE_PREVIEW_ORIGIN`, `SNOWFLAKE_PREVIEW_FRAME_ANCESTORS`, and
  `SNOWFLAKE_PREVIEW_PARENT_ORIGIN`.

Preview accepts some names that deploy rejects, such as lowercase names, `PORT`,
and `NODE_ENV`. To use one `app.yml` for both, follow the naming rules for
[`environment_variables`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-environment-variables)
and [`secrets`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-secrets).

Preview applies these fields when it starts the dev server. Closing and
reopening the Preview pane, or resuming after inactivity, keeps the same dev
server, so changes don’t apply. To apply them, select **Shutdown** from the
Preview pane’s menu, then reopen **Preview**.

## More about Workspaces

- **Privileges:** [Workspaces preview privileges](/developer-guide/snowflake-app-runtime/privileges#label-snowflake-app-runtime-privileges-workspaces)
- **Logs:** [Read preview logs](/developer-guide/snowflake-app-runtime/observability#label-snowflake-app-runtime-observability-workspaces)
- **Cost:** [Find credit usage for Workspaces preview](/developer-guide/snowflake-app-runtime/cost#label-snowflake-app-runtime-cost-workspaces)
- **Limitations:** [Workspaces preview limitations](/developer-guide/snowflake-app-runtime/limitations#label-snowflake-app-runtime-limitations-workspaces)
- **Troubleshooting:** [Fix Workspaces preview problems](/developer-guide/snowflake-app-runtime/troubleshooting#label-snowflake-app-runtime-troubleshooting-workspaces)
