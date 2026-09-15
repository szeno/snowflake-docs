# app.yml manifest for Snowflake App Runtime

The **`app.yml`** manifest in your project root tells Snowflake CLI and the
remote builder **where to deploy** your app and **how to install, build, run,
and package** it. Place the file in the application source root, name it
**`app.yml`**, and include a top-level `version: 2` key.

To move an existing project onto `app.yml`, see
[Migrate from snowflake.yml to app.yml](/developer-guide/snowflake-app-runtime/migrate-to-app-yml).

Note

Cortex Code CLI and Cortex Code Desktop generate this file when scaffolding
Snowflake App Runtime projects. `snow app setup` writes an `app.yml` for new
projects.

The CLI doesn’t fill `database` or `schema` from the active connection. An
unset `database` or `schema` fails the deploy.

## Syntax

An `app.yml` is a list of top-level keys:

Copy code

```
version: 2

name: SALES_DASHBOARD
database: SNOWFLAKE_APPS
schema: PUBLIC
query_warehouse: SNOWFLAKE_APPS_QUERY_WH

label: Sales dashboard
description: Internal sales dashboard.
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

A project that needs to deploy more than one way adds a
[`targets`](#label-snowflake-apps-manifest-targets) block. Each named **target**
lists only the fields that differ, and the top-level keys become the
**baseline** that every target inherits. Any field except the builder phases can
be set at the top level, in a target, or both, and a target’s value wins over
the baseline.

Builder phases (`install`, `build`, and `run`) are **top-level only**.
Putting them under a target has no effect.

## Keys

Only `version`, `name`, `database`, `schema`, and `query_warehouse` are
required. Every other key is optional.

| Required field | Purpose |
| --- | --- |
| [`version`](#label-snowflake-apps-manifest-version) | Schema the CLI reads. Set `2` |
| [`name`](#label-snowflake-apps-manifest-name) | Application Service name |
| [`database`](#label-snowflake-apps-manifest-database) | Destination database. Use `USER$` for the caller’s [personal database](/developer-guide/snowflake-app-runtime/deploy-targets) |
| [`schema`](#label-snowflake-apps-manifest-schema) | Destination schema |
| [`query_warehouse`](#label-snowflake-apps-manifest-query-warehouse) | Warehouse the service uses for queries |

Expand

Show lessSee more

| Optional field | Purpose |
| --- | --- |
| [`default_target`](#label-snowflake-apps-manifest-targets) | Target used when you omit `--target` |
| [`targets`](#label-snowflake-apps-manifest-targets) | Named maps of field overrides |
| [`ignore`](#label-snowflake-apps-manifest-ignore) | Glob patterns excluded from upload |
| [`code_stage`](#label-snowflake-apps-manifest-code-storage), [`code_workspace`](#label-snowflake-apps-manifest-code-storage) | Uploaded-source storage. Mutually exclusive |
| [`package_name`](#label-snowflake-apps-manifest-package) | Package name in the artifact repository |
| [`artifact_repo`](#label-snowflake-apps-manifest-artifact-repo) | Repository that holds the built package |
| [`build_eai`](#label-snowflake-apps-manifest-build-eai) | External access integration for build-time egress beyond the default allowlist |
| [`build_job_location`](#label-snowflake-apps-manifest-build-job-location) | Database and schema where the remote builder runs the build job |
| [`label`](#label-snowflake-apps-manifest-profile), [`description`](#label-snowflake-apps-manifest-profile), [`icon`](#label-snowflake-apps-manifest-profile) | Presentation metadata on the deployed service |
| [`execute_as_role`](#label-snowflake-apps-manifest-execute-as-role) | Execution role for a personal-database app |
| [`auto_resume`](#label-snowflake-apps-manifest-auto-resume) | Resume the service when a request arrives |
| [`auto_suspend_secs`](#label-snowflake-apps-manifest-auto-suspend-secs) | Idle seconds before suspend |
| [`min_instances`](#label-snowflake-apps-manifest-min-instances), [`max_instances`](#label-snowflake-apps-manifest-max-instances) | Fewest and most instances while the app is up |
| [`environment_variables`](#label-snowflake-apps-manifest-environment-variables) | Non-sensitive container environment variables |
| [`secrets`](#label-snowflake-apps-manifest-secrets) | Snowflake secrets mounted under `/secrets/<name>/` |
| [`external_access_integrations`](#label-snowflake-apps-manifest-external-access-integrations) | External access integrations for the running service |
| [`install`](#label-snowflake-apps-manifest-install) | Commands run before the build. Top-level only |
| [`build`](#label-snowflake-apps-manifest-build) | Build commands. Top-level only |
| [`run`](#label-snowflake-apps-manifest-run) | Container entry point. Top-level only |

Expand

Show lessSee more

### version

Required. Set `version: 2`. The key can appear anywhere at the top
level. It is what makes the CLI read the rest of the file: omit it and
`name`, `database`, `schema`, `query_warehouse`, and `targets` have no effect.
A value greater than `2` fails with `Unsupported app.yml version`.
Malformed YAML fails with `Could not parse app.yml` or
`Invalid app.yml`.

The next four fields are required. Set them at the top level. If the
manifest declares [`targets`](#label-snowflake-apps-manifest-targets), a
target can override any of them, but all four must be set once the CLI
merges the selected target with the top-level values. A field still
missing after that merge fails the deploy with
`Missing required field(s)`.

### name

Application Service name. A fully qualified name (`DB.SCHEMA.NAME`)
overrides the separate `database` and `schema` fields. A bare name
inherits them.

### database

Destination database. The database must already exist. You can’t share
apps deployed to a personal database.

Set `database: USER$` for the caller’s
[personal database](/user-guide/personal-databases). See
[Deploy targets](/developer-guide/snowflake-app-runtime/deploy-targets).

### schema

Destination schema. The schema must already exist.

### query\_warehouse

Warehouse the Application Service uses for queries. The warehouse must
already exist.

### default\_target and targets

Optional. Omit both keys if the project has one deploy configuration.
Add `targets` when the same project needs to deploy more than one way.

Each target is a map of field overrides. A target can be empty (`stage:` or
`stage: {}`) to deploy the baseline unchanged under that name.

Copy code

```
default_target: dev

targets:
  dev:
    name: MY_APP_DEV
    database: USER$
  stage:
    name: MY_APP_STAGE
  prod:
    name: MY_APP_PROD
    min_instances: 2
```

Give each target its own Application Service `name` when two targets would
otherwise land in the same database and schema. Two targets that resolve
to the same fully qualified name operate on the same service.

For how the CLI selects and merges a target, see
[Deploy targets](/developer-guide/snowflake-app-runtime/deploy-targets).

### ignore

Glob patterns excluded from the uploaded project root. The CLI always
uploads the whole project root minus these patterns.

Copy code

```
ignore:
  - node_modules
  - .env*
  - .next
  - .git
```

### code\_stage and code\_workspace

Optional strings (a bare name or `DB.SCHEMA.NAME`). They are mutually
exclusive; setting both is rejected.

Prefer leaving both unset. At deploy time the CLI chooses storage: a workspace
if the destination is a personal database (personal databases don’t support
stages) or if the role can `CREATE WORKSPACE`; otherwise a `<NAME>_CODE` stage.
Setting `code_stage` on a personal-database target fails the deploy.

If you need a specific name, set only that field:

Copy code

```
code_stage: SALES_DASHBOARD_CODE
```

Copy code

```
code_workspace: SALES_DASHBOARD_WS
```

### package\_name

Package name in the artifact repository. When omitted, the CLI uses the
bare `name`.

### artifact\_repo

Artifact repository that holds the built package (bare name or
`DB.SCHEMA.NAME`). When omitted, the CLI uses `<NAME>_REPO` in the app’s
database and schema.

### build\_eai

External access integration for **build-time** egress beyond the default
remote-build allowlist. Remote builds already allow npm and Google Fonts.
Add `build_eai` only when the build must reach extra hosts (for example a
private registry).

### build\_job\_location

Database and schema (`<database>.<schema>`) where the remote builder runs the
build job. When omitted, the build job runs in the caller’s
[personal database](/user-guide/personal-databases) (`USER$<login_name>`).

Copy code

```
build_job_location: SNOWFLAKE_APPS.BUILDS
```

Set it when the build job has to run somewhere you control instead of the
caller’s personal database. The deploying role needs the `CREATE SERVICE`
[schema privilege](/user-guide/security-access-control-privileges#label-security-access-control-privileges-schema-privileges)
on the target schema.

Qualify the value with both a database and a schema. A bare schema name is
rejected. The field moves only the build job: the Application Service still
lands in the resolved `database` and `schema`, and package versions still go to
[`artifact_repo`](#label-snowflake-apps-manifest-artifact-repo).

### label, description, and icon

Presentation metadata for the deployed service. Set these as top-level fields,
with optional per-target overrides.

- `icon`: Relative path to a `.png`, `.svg`, or `.webp` file inside the package.
  The path must not contain `..`, and it can’t be an absolute path.
- `label`: Short display label.
- `description`: Longer human-readable description.

Copy code

```
label: Customer Portal
description: Web UI for the customer-facing portal.
icon: assets/logo.png
```

Don’t put the sequence `$$` in `label`, `description`, or environment-variable
values.

### execute\_as\_role

Use this only for an app in a
[personal database](/user-guide/personal-databases). It is the role
Snowflake uses for owner’s rights queries and for caller’s rights grants.
Omit it on a standard database: the execution role is the role that owns
the app. If you omit it on a personal database, Snowflake uses the
creator’s session primary role. Grant the role to the owning user. You
can’t change it after the app is created. See
[Execution context](/developer-guide/snowflake-app-runtime/access-control#label-snowflake-app-runtime-access-control-execute-as-role).

### auto\_resume

`true` or `false`. Defaults to `true`.

### auto\_suspend\_secs

Idle seconds before suspend. Defaults to `0`, which means never
auto-suspend. The minimum non-zero value is `300`. See
[Scale and suspend Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/scale-and-suspend).

### min\_instances and max\_instances

The fewest and most instances Snowflake runs while the app is up.
Equivalent to setting
`MIN_INSTANCES` and `MAX_INSTANCES` in
[CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service).

- Both must be at least `1`, and `max_instances` can’t exceed `10`.
- `min_instances` can’t exceed `max_instances`.
- Both default to `1`.

Copy code

```
min_instances: 2
max_instances: 5
```

For what these do to a running service, see
[Scale and suspend Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/scale-and-suspend).

### environment\_variables

Non-sensitive configuration values that Snowflake exposes as environment
variables inside the application container. Each entry has:

- `name`: Environment variable name. Must match the POSIX pattern
  `[A-Z_][A-Z0-9_]*` (uppercase letters, digits, and underscores; must start
  with a letter or underscore). Duplicate names aren’t allowed.
- `value`: String value. Unquoted scalars are coerced to strings (`8080`
  becomes `"8080"`, `true` becomes `"true"`).

Copy code

```
environment_variables:
  - name: LOG_LEVEL
    value: "INFO"
  - name: APP_REGION
    value: "us-west-2"
```

Some names are reserved and fail the deploy: any name starting with
`SF_SNOWFS_`, plus `SNOWFLAKE_AUTH_MODE`, `SNOWFLAKE_INSECURE_MODE`,
`NODE_ENV`, `NEXT_PRIVATE_STANDALONE`, `PORT`, and `HOSTNAME`. For listen
and connection variables Snowflake sets, see
[Built-in environment variables](/developer-guide/snowflake-app-runtime/runtime-environment#label-runtime-environment-env-vars).

### secrets

Snowflake [secret](/sql-reference/sql/create-secret) objects to make available
to the application at runtime. Each entry has:

- `name`: Mount name used to locate the secret files inside the container. Must
  match the POSIX pattern `[A-Z_][A-Z0-9_]*`. Duplicate names aren’t allowed.
- `secret`: Fully qualified name of an existing Snowflake secret
  (`<database>.<schema>.<secret_name>`). A bare secret name is qualified with
  the target’s database and schema.

Copy code

```
secrets:
  - name: API_KEY
    secret: db.schema.api_key_secret
```

Snowflake mounts each secret as one or more files under `/secrets/<name>/`
rather than as an environment variable. For the files each secret type
produces and how to read them, see
[Secret files](/developer-guide/snowflake-app-runtime/runtime-environment#label-runtime-environment-secret-files).

Generic string, password, and OAuth2 secrets are supported. Symmetric key and
cloud provider secret types aren’t.

OAuth2 secrets require an
[external access integration](/developer-guide/external-network-access/creating-using-external-network-access)
that lists the secret in `ALLOWED_AUTHENTICATION_SECRETS`. Attach that
integration with
[`external_access_integrations`](#label-snowflake-apps-manifest-external-access-integrations).
Password and generic string secrets don’t require an integration.

### external\_access\_integrations

Names of [external access integrations](/developer-guide/external-network-access/creating-using-external-network-access)
that the **running** app service uses to reach external hosts (for example,
third-party APIs or [Snowflake Postgres](/user-guide/snowflake-postgres/about)
instances). External access integrations are account-level objects, so
each entry is the name of an existing integration.

Copy code

```
external_access_integrations:
  - my_api_integration
  - my_slack_integration
```

For administrator controls on which integrations a role can use, see
[Governing outbound network access](/developer-guide/snowflake-app-runtime/security#label-snowflake-app-runtime-security-outbound-network).

### install

Commands Snowflake runs during the install phase, before the build. Each
entry under `commands` is an argv-style list, passed directly without a
shell. Use `install` for setup steps such as installing dependencies.

Top-level only. Optional; defaults to `npm ci` when omitted.

Copy code

```
install:
  commands:
    - [npm, ci]
```

### build

Commands Snowflake runs during the build phase. Each entry under `commands`
is an argv-style list. Top-level only. Optional; defaults to `npm run build`
when omitted.

Copy code

```
build:
  commands:
    - [npm, run, build]
```

### run

The entry-point command that starts the application container. `command`
is an argv-style list. Top-level only. Optional; defaults to `npm start`
when omitted. Templates that need a different command (for example Next.js
`node .next/standalone/server.js`) must declare `run` explicitly.

Copy code

```
run:
  command: [node, dist/server.js]
```

## Validation

When you run `snow app deploy`, the CLI validates `app.yml`
before upload. Snowflake also loads and validates builder sections from
uploaded source during the build phase.

If `app.yml` is present but invalid, the build fails before a new package
version is published. Common causes include:

- YAML syntax errors.
- Invalid `icon` values (path traversal, absolute paths, or unsupported
  image formats).
- Missing required fields on the resolved target.

Names in `secrets` and `external_access_integrations` are resolved when
Snowflake creates or alters the Application Service. An unresolvable name
fails that step, not the build phase.

Deploy uses `CREATE OR ALTER APPLICATION SERVICE ... SPECIFICATION`, so
the manifest is the full intended state. A field you leave out goes back
to its default, including a value set with `ALTER APPLICATION SERVICE`.
The exception is `execute_as_role`, which you can’t change after the app
is created.

## Common errors

| Symptom | Cause | What to do |
| --- | --- | --- |
| Deploy fields in `app.yml` have no effect; deploy uses old values | No top-level `version: 2` | Add `version: 2` |
| `Unsupported app.yml version` | `version` is greater than 2 | Set `version: 2`, or upgrade the CLI if you intend a newer schema |
| `--target is only supported ... version 2` | `--target` on a `snowflake.yml` project | Drop `--target`. See the migrate guide. |
| `No target selected` | `targets` declared with no selection | Pass `--target`, or set `default_target` |
| `Target '<x>' is not defined` | Typo, or no `targets` block | Check the listed available targets |
| `Missing required field(s)` | `app.yml` doesn’t fill `database` from the CLI connection | Set `name`, `database`, `schema`, and  `query_warehouse` on the baseline or the target |
| `Set only one of 'code_stage' or 'code_workspace'` | Both configured | Keep one, or omit both |
| `Application service specification must not contain '$$'` | A `label`, `description`, or environment-variable value contains `$$` | Remove that sequence |
| Label, description, or icon disappeared after deploy | A leftover `profile:` block in `app.yml` | Move `label`, `description`, and  `icon` to the top level. See  [Migrate from snowflake.yml to app.yml](/developer-guide/snowflake-app-runtime/migrate-to-app-yml)  . |
| Missing-project-definition error on an `app.yml`-only project | CLI doesn’t support this `app.yml` layout | Run `snow helpers check-version` and upgrade the Snowflake CLI. |

Expand

Show lessSee more

## Example

A baseline-only file for a single destination:

Copy code

```
version: 2

name: CUSTOMER_PORTAL
database: SNOWFLAKE_APPS
schema: PUBLIC
query_warehouse: SNOWFLAKE_APPS_QUERY_WH

label: Customer Portal
description: Customer portal web UI.
icon: assets/logo.png

ignore:
  - node_modules
  - .env*
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

environment_variables:
  - name: LOG_LEVEL
    value: "INFO"
secrets:
  - name: API_KEY
    secret: SNOWFLAKE_APPS.PUBLIC.api_key_secret
external_access_integrations:
  - my_api_integration
```

To deploy the same project more than one way, keep that baseline and add
`default_target` and `targets`. Each target overrides only what differs:

Copy code

```
default_target: dev

targets:
  dev:
    name: CUSTOMER_PORTAL_DEV
    database: USER$
  stage:
    name: CUSTOMER_PORTAL_STAGE
  prod:
    name: CUSTOMER_PORTAL_PROD
    query_warehouse: PROD_WH
    min_instances: 2
    max_instances: 5
```
