# snowflake.yml project definition for Snowflake App Runtime (legacy)

This page documents the older Snowflake App Runtime layout: a `snowflake.yml`
with a `type: snowflake-app` entity, plus a build-only `app.yml` for install,
build, and run. Current projects use a single
[`app.yml`](/developer-guide/snowflake-app-runtime/app-yml). To move an existing
project, see [Migrate from snowflake.yml to app.yml](/developer-guide/snowflake-app-runtime/migrate-to-app-yml).

Native App projects still use `snowflake.yml`. That schema is documented with
[snow app commands](/developer-guide/snowflake-cli/command-reference/native-apps-commands/overview),
not here.

If the project root contains an `app.yml` with `version: 2`, the CLI ignores
this `snowflake.yml` for the Snowflake App Runtime flow.

A `snowflake.yml` is a Snowflake CLI project definition. For entity keys,
identifiers, mixins, templating, and other patterns the CLI applies to all
project files, see
[Specify entities](/developer-guide/snowflake-cli/project-definitions/specify-entities).
The rest of this page covers only the Snowflake App Runtime `snowflake-app`
entity.

In this layout, `snowflake.yml` controls deployment (destination, code storage,
warehouse, and compute). The build-only `app.yml` controls the remote build
(install, build, run, artifacts, and display `profile`).

## Example

Copy code

```
definition_version: "2"

entities:
  myapp:
    type: snowflake-app
    identifier:
      name: MYAPP
      database: MY_DB
      schema: MY_SCHEMA
    artifacts:
      - src: ./*
        dest: ./
        ignore:
          - node_modules
          - .env*
          - .git
    query_warehouse: MY_WH
    code_stage: MYAPP_CODE
```

Use `code_workspace` instead of `code_stage` to store code in a workspace rather
than a stage. The two fields are mutually exclusive.

## snowflake.yml schema for snowflake-app entities

### Fields

The following fields are supported for `snowflake-app` entities:

| Field | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| `type` | `snowflake-app` | Yes | N/A | Selects the Snowflake App Runtime flow. |
| `identifier` | object or string | No | None | Either a string identifier or an object with `name` (required), `schema`, and `database`. |
| `artifacts` | list | Yes | N/A | Each entry is either a path string or an object with `src` (required), `dest`, `processors`, and `ignore` (glob patterns to exclude). A bare string is treated as `src`. |
| `query_warehouse` | string | No | None | Warehouse used for queries. Applied to the deployed Application Service. |
| `build_eai` | string, object, or null | No | None | External access integration for the build. Either a bare name or an object with a `name` property. External access integrations are account-level objects, so they don’t take a database or schema qualifier. Can be set to `null`. |
| `artifact_repository` | object | No | `<app-name>_REPO` | Object with `name` (required), `schema`, and `database`. Defaults to `<app-name>_REPO` at deploy time when omitted. |
| `code_stage` | string or object | No | None | Stage backend for code. Mutually exclusive with `code_workspace`. |
| `code_workspace` | string or object | No | None | Workspace backend for code. Mutually exclusive with `code_stage`. |

Expand

Show lessSee more

### Code storage object shapes

When you write `code_stage` or `code_workspace` as an object, use these fields:

- `code_stage`: `name` (required), `schema`, `database`, and `encryption_type`
  (default `SNOWFLAKE_SSE`).
- `code_workspace`: `name` (required), `schema`, and `database`.

### Validation rules

- **Code storage is mutually exclusive.** Setting both `code_stage` and
  `code_workspace` fails with `Specify either code_stage or code_workspace, not both`.
- **The external access integration is nullable.** `build_eai` accepts `null`,
  which is treated the same as omitting it.
- **Code storage accepts three forms.** Write `code_stage` and `code_workspace`
  as an object, a bare name, or a fully qualified `DB.SCHEMA.NAME` string. When
  you use a bare name (or omit the database or schema), the CLI resolves those
  parts against the app’s database and schema at deploy time.

## How field values are resolved

The CLI resolves each field’s value using a four-tier precedence. The first
source that provides a value wins:

1. **`snowflake.yml`**: Your entity fields (`query_warehouse`, `build_eai`,
   `artifact_repository`, and the app’s database and schema).
2. **Account parameters**: Your `DEFAULT_SNOWFLAKE_APPS_*` parameters (see the
   table below).
3. **Built-in defaults**: The CLI’s fallback values. For example,
   `artifact_repository` becomes `<app-name>_REPO`, and if you have a
   [personal database](/user-guide/personal-databases), `database` becomes that
   database and `schema` becomes `PUBLIC`.
4. **Current session**: Your connection’s warehouse, database, and schema.

If an account-configured destination database or schema is set but your current
role lacks the privileges to deploy there, the CLI warns you and falls back to
your personal database.

Account parameters you can set:

| Account parameter | Controls |
| --- | --- |
| `DEFAULT_SNOWFLAKE_APPS_QUERY_WAREHOUSE` | Query warehouse |
| `DEFAULT_SNOWFLAKE_APPS_BUILD_EXTERNAL_ACCESS_INTEGRATION` | Build external access integration |
| `DEFAULT_SNOWFLAKE_APPS_DESTINATION_DATABASE` | Destination database |
| `DEFAULT_SNOWFLAKE_APPS_DESTINATION_SCHEMA` | Destination schema |

Expand

Show lessSee more
