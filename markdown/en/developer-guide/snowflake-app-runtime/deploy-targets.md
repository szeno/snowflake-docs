# Deploy targets

Use named [`targets`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-targets)
in one [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml) when the
same project needs more than one deploy configuration. Select a target with
`--target`, and give each target a unique Application Service `name`.

Use a `dev` target in a
[personal database](/user-guide/personal-databases) (`database: USER$`) and
`stage` and `prod` targets in a shared database after
[account administrator setup](/developer-guide/snowflake-app-runtime/account-admin-setup).
The same keys work for other variants, such as several accounts or different
audiences.

If the project still has `snowflake.yml`, complete
[Migrate from snowflake.yml to app.yml](/developer-guide/snowflake-app-runtime/migrate-to-app-yml) first.

## Development, stage, and production

Set shared values at the top level. Each target lists only what differs.
Don’t put a fully qualified database name in app SQL: a `USER$` target and a
shared database target won’t share that name.

Copy code

```
version: 2

database: SNOWFLAKE_APPS
schema: PUBLIC
query_warehouse: SNOWFLAKE_APPS_QUERY_WH

label: Warehouse monitor
icon: public/icon.svg

ignore:
  - node_modules
  - .env*
  - .next
  - .git

default_target: dev

targets:
  dev:
    name: WAREHOUSE_MONITOR_DEV
    database: USER$
  stage:
    name: WAREHOUSE_MONITOR_STAGE
  prod:
    name: WAREHOUSE_MONITOR_PROD
    query_warehouse: PROD_WH
    min_instances: 2
    max_instances: 5
```

After the CLI merges each target with the baseline, those three deploys
look like this:

| Field | `dev` | `stage` | `prod` |
| --- | --- | --- | --- |
| `name` | `WAREHOUSE_MONITOR_DEV` | `WAREHOUSE_MONITOR_STAGE` | `WAREHOUSE_MONITOR_PROD` |
| `database` | Caller’s personal database (`USER$`) | `SNOWFLAKE_APPS` | `SNOWFLAKE_APPS` |
| `schema` | `PUBLIC` | `PUBLIC` | `PUBLIC` |
| `query_warehouse` | `SNOWFLAKE_APPS_QUERY_WH` | `SNOWFLAKE_APPS_QUERY_WH` | `PROD_WH` |
| `min_instances` / `max_instances` | Omitted | Omitted | `2` / `5` |

Expand

Show lessSee more

`dev` overrides `name` and `database`. `stage` overrides only `name`, so
it deploys to the baseline database and warehouse. `prod` overrides
`name`, `query_warehouse`, and the instance counts. For what
`min_instances` and `max_instances` do, see
[Scale and suspend Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/scale-and-suspend).

Two targets that resolve to the same fully qualified name operate on the
same service.

## Deploy, open, and tear down a target

Because `default_target` is `dev`, a bare command selects that target:

Copy code

```
snow app validate
snow app deploy
snow app open
```

Pass `--target` to select another:

Copy code

```
snow app deploy --target stage
snow app open --target prod --print-only
snow app events --target stage --last 200
snow app teardown --target dev
```

Teardown removes only the selected target’s service. If that target was
never deployed, teardown reports that the service doesn’t exist.

## Personal-database targets

The CLI expands `USER$` to `USER$<current_user>`, the
[personal database](/user-guide/personal-databases) Snowflake already
created for that user. A session as `JSMITH` deploys to `USER$JSMITH`.
Don’t set a literal personal database such as `USER$ADMIN` or
`USER$JSMITH`; that value belongs to one user and fails for everyone
else.

If personal databases aren’t enabled, or the CLI can’t resolve the
current user, deploy fails with
`Target requests the personal database (USER$) but it could not be resolved for the current user.`

Leave `code_stage` and `code_workspace` unset. Personal databases support
workspaces only. If you set `code_stage`, the deploy fails. You can’t
grant other roles access to an Application Service in a personal
database.

## How the CLI resolves a target

`snow app deploy`, `snow app open`, `snow app events`,
`snow app teardown`, and `snow app validate` build one configuration in
this order:

1. **If `targets` is absent or empty**, use the top-level baseline. Passing
   `--target` fails with `Target '<name>' is not defined ... no targets are declared.`
2. **If `targets` has any keys**, select a name: `--target` if you passed
   it, otherwise the top-level `default_target`. A lone target is **not**
   an implicit default. With neither selection, the command fails with
   `No target selected. Pass --target or set 'default_target' in app.yml.`
3. Look that name up in `targets`. A missing name fails with
   `Target '<name>' is not defined in app.yml.` A `default` key inside
   `targets` isn’t supported; use top-level `default_target`.
4. **Merge.** Start from the baseline service and deploy fields. For each
   field the selected target sets, replace the baseline value. Unset
   fields inherit. Lists (`secrets`, `external_access_integrations`,
   `environment_variables`, `ignore`) replace the baseline list; they
   don’t concatenate.
5. **`code_stage` and `code_workspace` are one slot.** If the target sets
   either field, that pair replaces both baseline fields. If it sets
   neither, both inherit.
6. **Expand `database: USER$`** to the caller’s personal database
   (`USER$<current_user>`).
7. **Require** `name`, `database`, `schema`, and `query_warehouse` on the
   merged result.
