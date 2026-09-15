# Migrate from snowflake.yml to app.yml

[`app.yml`](/developer-guide/snowflake-app-runtime/app-yml) is the manifest
Snowflake App Runtime supports going forward. Older projects split
configuration across a
[`snowflake.yml`](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/snowflake-yml)
(where the app deploys) and a build-only `app.yml` (install, build, and
run). Named targets and `database: USER$` live only in `app.yml`.

Add a top-level `version: 2`. The CLI then reads deployment configuration
from `app.yml` and ignores `snowflake.yml`.

## Breaking changes to plan for

`app.yml` isn’t a rename of `snowflake.yml`. These differences change how
the project behaves:

- **Deploys become declarative.** Every deploy applies the full
  manifest. A field you leave out is cleared, including a value set with
  `ALTER APPLICATION SERVICE`. See
  [Declarative deploys](#label-migrate-to-app-yml-declarative).
- **`profile:` stops being read.** A leftover `profile:` block is
  ignored, so label, description, and icon are cleared on the next
  deploy. Promote those keys to the top level.
- **There’s no connection fallback.** `snowflake.yml` filled in an unset
  `database` or `schema` from the active connection. `app.yml` doesn’t:
  `name`, `database`, `schema`, and `query_warehouse` all have to resolve from
  the manifest.
- **The build service no longer copies Next.js standalone assets for you.** The
  previous builder copied `.next/static` and `public/` into the standalone
  directory automatically. The current build service runs only the commands you
  declare. If your Next.js app sets `output: 'standalone'` in `next.config.*`
  and you omit those copy steps, static assets 404 after deploy. See
  [Next.js standalone builds](#label-migrate-to-app-yml-nextjs).

## Before you start

1. Confirm you’re on the latest Snowflake CLI with
   [`snow helpers check-version`](/developer-guide/snowflake-cli/command-reference/helpers-commands/check-version):

   Copy code

   ```
   snow helpers check-version
   ```

   If that command isn’t recognized, upgrade the Snowflake CLI. An older
   CLI ignores every deployment key in `app.yml` and still expects
   `snowflake.yml`.
2. Use the same CLI version in CI and any other environment that deploys
   this project.
3. Keep a copy of the current `snowflake.yml` and `app.yml` until an `app.yml`
   deploy succeeds.

## Migrate with Cortex Code

[Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli) and
[Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop/building-apps)
bundle the
[`snowflake-apps`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-snowflake-apps)
skill, which can do this migration. Ask for it from the project
directory.

Cortex Code CLICortex Code Desktop

```
> $snowflake-apps Migrate this project from snowflake.yml to app.yml
```

Type `/` in chat, select **snowflake-apps**, then ask for the migration:

```
/snowflake-apps Migrate this project from snowflake.yml to app.yml
```

The agent proposes a plan and waits for approval before editing. Review
the manifest it writes against the
[field mapping](#label-migrate-to-app-yml-mapping) before you deploy.

## Migrate the project by hand

1. Read the current values from `snowflake.yml` and `app.yml`.

   - If `snowflake.yml` holds a single `snowflake-app` entity, produce a
     **baseline-only** manifest (no `targets` block).
   - If it holds **several** entities that deploy the same project different
     ways, map one target per entity and set `default_target` to the one you
     deploy most often.
2. Write the merged `app.yml`:

   - Add a top-level `version: 2`.
   - Add the deployment keys from the
     [field mapping](#label-migrate-to-app-yml-mapping).
   - Promote `profile.*` to top-level `label`, `description`, and `icon`.
   - Keep existing `install`, `build`, and `run` blocks. If the project relied
     on the default `npm run build`, see
     [Next.js standalone builds](#label-migrate-to-app-yml-nextjs).
   - Drop compute-pool and `runtime_image` fields.
   - Omit `code_stage` and `code_workspace` unless the project needs a
     specific stage or workspace name.

   Example after a single-entity migrate:

   Copy code

   ```
   version: 2

   name: MY_APP
   database: SNOWFLAKE_APPS
   schema: PUBLIC
   query_warehouse: SNOWFLAKE_APPS_QUERY_WH

   label: My app
   description: Migrated from snowflake.yml.
   icon: public/icon.svg

   ignore:
     - node_modules
     - .next
     - .git

   install:
     commands:
       - [npm, ci]
   build:
     commands:
       - [npm, run, build]
   run:
     command: [node, dist/server.js]
   ```
3. Validate before deploying:

   Copy code

   ```
   snow app validate
   ```

   Add `--target <name>` when the manifest defines targets. Validate checks that
   the database and schema exist and that the bundle resolves.
4. Deploy and confirm the endpoint still serves the app:

   Copy code

   ```
   snow app deploy
   snow app open --print-only
   ```
5. Delete `snowflake.yml` after that deploy succeeds. The CLI ignores it
   once `app.yml` has `version: 2`.

## Next.js standalone builds

The previous build service copied `.next/static` and `public/` into the
standalone directory for you when a Next.js app used `output: 'standalone'`.
The current build service runs only the commands in your `build:` block, so
that copy no longer happens unless you declare it.

Many older projects omitted `build:` and relied on the default `npm run build`
plus that automatic copy. After you migrate, a bare `npm run build` leaves
those assets outside `.next/standalone`, so the app loads but its CSS,
JavaScript, and images return 404.

Declare the copy steps explicitly:

Copy code

```
build:
  commands:
    - [npm, run, build]
    - [cp, -r, .next/static, .next/standalone/.next/static]
    - [cp, -r, public, .next/standalone/public]
    - [rm, -rf, node_modules]
```

Omit the `public` line if the project has no `public/` directory. The final
`rm` keeps the root `node_modules` out of the upload, because the standalone
output ships its own copy.

## Declarative deploys

With `snowflake.yml`, a deploy created the service or upgraded it and
left properties you set in SQL in place.

With `app.yml`, every deploy applies the full manifest. A field you omit
goes back to its default. A leftover `profile:` block is why label,
description, and icon are cleared. A change you make with
`ALTER APPLICATION SERVICE` (auto-suspend, query warehouse, integrations,
and similar) is reverted the next time anyone deploys.

`--promote-only` still skips upload and build. It now reapplies the
manifest instead of a `snowflake.yml`-style upgrade.

## Field mapping

| `snowflake.yml` / build-only `app.yml` | `app.yml` |
| --- | --- |
| `snowflake.yml``identifier.name` | `name` |
| `snowflake.yml``identifier.database` | `database` |
| `snowflake.yml``identifier.schema` | `schema` |
| `snowflake.yml``query_warehouse` | `query_warehouse` |
| `snowflake.yml``build_eai.name` | `build_eai` (plain string) |
| `snowflake.yml``service_eai.name` | `external_access_integrations` (list) |
| `snowflake.yml` `code_stage.name` /  `code_workspace` | `code_stage` / `code_workspace` (plain strings). Omit both unless you need a specific name. |
| `snowflake.yml``artifact_repository.name` | `artifact_repo` (plain string or fully qualified name) |
| `snowflake.yml``artifacts[].ignore` | `ignore` |
| `snowflake.yml` `artifacts[].src` /  `dest` | No equivalent. `app.yml` uploads the whole project root minus  `ignore`. |
| `snowflake.yml``meta.title` | `label` |
| `snowflake.yml` `build_compute_pool` /  `service_compute_pool` / `runtime_image` | No equivalent. Drop them; the server chooses. |
| `app.yml` `profile.label` /  `profile.description` /  `profile.icon` | Top-level `label` / `description` /  `icon` |
| `app.yml` `secrets` /  `environment_variables` | Same keys and shape |
| `app.yml``external_access_integrations` | Same key and shape |
| `app.yml` `install` / `build` /  `run` | Unchanged |
| One entity per `snowflake.yml`, selected with  `--entity-id` | One target per environment, selected with `--target` |

Expand

Show lessSee more
