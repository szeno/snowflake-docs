# Deploying with Snowflake App Runtime

When you’re ready to deploy your app to Snowflake, run
[`snow app deploy`](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/deploy).
The command uploads your source, builds it remotely, and creates or alters the
[Application Service](/sql-reference/sql/create-application-service) that serves
your app at a stable live URL. Use `--upload-only`, `--build-only`, or
`--promote-only` to run one phase at a time. (`--deploy-only` is a deprecated
alias for `--promote-only`.)

The build job and the Application Service are separate workloads with different
compute, database placement, and outbound access rules. A single
[`app.yml`](/developer-guide/snowflake-app-runtime/app-yml) file
defines both the deploy destination (including optional named
[`targets`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-targets))
and the install, build, and run commands. If you declare targets, pass
`--target` to select one.

## Deploy pipeline overview

| Phase | What happens | Phase flag |
| --- | --- | --- |
| Upload | Syncs local source files to an internal stage or workspace (the project root minus `ignore` in  `app.yml`). | `--upload-only` |
| Build | Runs `install` and `build` from  `app.yml` (or auto-detects from your project layout). Adds an immutable package version to the configured artifact repository. | `--build-only` |
| Deploy | Creates or alters the Application Service from that package (typically  `LATEST`). | `--promote-only` |

Expand

Show lessSee more

If a run fails partway through, retry just the failed phase instead of rerunning
the full pipeline. Only one phase flag can be used at a time.

## Upload phase

The upload phase copies the project root to Snowflake storage, minus the
`ignore` list in [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml).
When the resolved target sets `code_workspace`, uploaded source goes to that
**workspace**. When it sets `code_stage` instead, uploaded source goes to an
internal **stage**. Prefer leaving both unset so the CLI can pick: a workspace
for a [personal database](/user-guide/personal-databases) (personal databases
don’t support stages), or a stage when the role can’t create a workspace.

Specifying an existing `code_workspace` doesn’t require `CREATE WORKSPACE` by
itself; you need access to write to that workspace at deploy time.

The `ignore` list excludes local-only paths such as `node_modules` and `.next`
from upload.

## Build phase

The build phase runs a short-lived Snowpark Container Services **job** that
executes the `install` and `build` commands from your
[`app.yml`](/developer-guide/snowflake-app-runtime/app-yml) manifest (or
auto-detects those steps from your project layout). Each successful build adds
an immutable **package version** to the artifact repository configured for the
app.

The build job and the Application Service that serves your app are separate
workloads with different network policies and lifetimes.

| Aspect | Build phase (install/build job) | Deploy phase (Application Service) |
| --- | --- | --- |
| Workload type | Ephemeral SPCS job | Long-running service |
| Inbound web access | None | Public endpoint on the Application Service. The container listens on port 8080; users reach the app over HTTPS at a  `*.snowflakecomputing.app` URL (Snowflake terminates TLS on port 443). See  [Listen address](/developer-guide/snowflake-app-runtime/runtime-environment#label-runtime-environment-listen-address). |
| Default outbound (internet) access | Scoped allowlist for package registries and Google Fonts (see below). Snowflake injects allowed destinations by build origin. | No automatic internet egress. Outbound access requires an [External Access Integration (EAI)](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress) with matching network rules on the Application Service. Inbound access uses the public endpoint described above. |
| Lifetime | Completes when the build finishes | Runs until suspended, altered, or dropped |

Expand

Show lessSee more

Build-time outbound access doesn’t carry over to the running app. Each phase
has its own egress policy.

### Where the build runs

Snowflake provisions build infrastructure for you. You don’t create a dedicated
compute pool for the build when you use the standard `snow app deploy` workflow.

#### Compute

The build runs as a short-lived Snowpark Container Services **job** on a
Snowflake-managed
[compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool)
that Snowflake provisions for your account.

#### Where each workload runs

The build **job**, the **artifact repository**, and the **Application Service**
land in different places:

| Workload | Where it runs |
| --- | --- |
| Build job (install/build) | By default, your [personal database](/user-guide/personal-databases) ( `USER$<login_name>`). This placement doesn’t follow your deploy destination. Set  [`build_job_location`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-build-job-location)  in `app.yml` to run the build job in a database and schema you choose instead. |
| Application Service | Your **deploy destination**: the resolved  `database` and `schema` in  [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml) (baseline plus selected target). See  [CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service). |
| Artifact repository | Where you configure  [`artifact_repo`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-artifact-repo). If you omit it, the default is `<app-name>_REPO` in the deploy destination. Independent of where the Application Service runs. |

Expand

Show lessSee more

By default the build job runs in your personal database so you can install and
build before your account has shared deploy defaults or broad privileges on a
team schema. To run it elsewhere, set
[`build_job_location`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-build-job-location)
in `app.yml`; the deploying role then needs the `CREATE SERVICE` privilege on
that schema. The Application Service runs in your deploy destination. Package
versions are stored in the artifact repository you configure.

#### Artifact repository

By default, Snowflake stores package versions in an
[artifact repository](/sql-reference/sql/create-artifact-repository) named
`<app-name>_REPO` in your deploy destination (same database and schema as the
Application Service). On the first build, Snowflake creates the repository if
it doesn’t already exist (`CREATE ARTIFACT REPOSITORY IF NOT EXISTS ... TYPE = APPLICATION`).

Set a different name or location in `app.yml` with
[`artifact_repo`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-artifact-repo).
Multiple apps can point at the same repository if you configure them that way.
The deploy phase references that repository when it creates or alters the
Application Service; the repository location doesn’t determine where the
service runs.

Each successful build adds a new immutable **package version**. The deploy phase
loads a package from that repository (typically `LATEST`) into the Application
Service in your deploy destination.

### Default outbound access during build

By default, remote builds can reach a small set of external hosts so Node.js
projects can download npm packages and common frontend assets (Google Fonts).

Snowflake applies an origin-based allowlist for remote build jobs. Allowed
destinations are scoped to specific host and port pairs, not open internet
access. Remote builds can reach these hosts by default:

| Host | Purpose |
| --- | --- |
| `registry.npmjs.org` | npm dependency resolution (`npm install` / `npm ci` ) |
| `fonts.googleapis.com` | Google Fonts CSS, commonly referenced by web frameworks |
| `fonts.gstatic.com` | Google Fonts font files |

Expand

Show lessSee more

These defaults cover most Node.js app builds.

### Custom outbound access during build

If your build must reach additional hosts (for example, a private package
registry or a third-party CDN), create a
[network rule](/sql-reference/sql/create-network-rule) and an
[External Access Integration (EAI)](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress),
then reference the EAI in your `app.yml` with
[`build_eai`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-build-eai):

Copy code

```
version: 2

name: MY_APP
database: SNOWFLAKE_APPS
schema: PUBLIC
query_warehouse: SNOWFLAKE_APPS_QUERY_WH
build_eai: MY_CUSTOM_EAI
```

The EAI must reference a network rule with `MODE = EGRESS` and `TYPE = HOST_PORT`.
Snowflake merges EAI-derived hosts with the default allowlist when both apply.

You can also set a default build EAI at the account level with
`DEFAULT_SNOWFLAKE_APPS_BUILD_EXTERNAL_ACCESS_INTEGRATION`, or pass
[`--build-eai`](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/setup)
during `snow app setup`. Set `build_eai` in `app.yml`, or pass `--build-eai`
to `snow app setup`.

### Disabling default build egress

Account administrators can turn off automatic outbound access during remote
builds. When default egress is disabled, builds that rely on npm or Google
Fonts fail at the dependency-fetch step unless the developer supplies an EAI
(for example, through `build_eai`) that covers the required hosts. Use these
account parameters:

| Goal | Account parameter | Effect |
| --- | --- | --- |
| Disable all automatic build egress | `ENABLE_REMOTE_BUILD_SERVICE_EGRESS_DESTINATIONS` =  `false` | No registry or CDN hosts are added to remote build jobs automatically |
| Disable npm and Google Fonts only | `ALLOW_NPM_PACKAGE_DOWNLOAD` = `false` | Removes the default npm and Google Fonts hosts; other upstream toggles unchanged |

Expand

Show lessSee more

Example (requires a role that can change account parameters, such as `ACCOUNTADMIN`):

Copy code

```
ALTER ACCOUNT SET ENABLE_REMOTE_BUILD_SERVICE_EGRESS_DESTINATIONS = FALSE;
```

To re-enable npm and Google Fonts without turning the master switch back on,
create an EAI and set `build_eai` in `app.yml` as described in
[Custom outbound access during build](#label-deploy-build-custom-egress).

## Deploy phase

The deploy phase is when your app goes live. Snowflake takes the package version
from the build phase and runs it as an
[Application Service](/sql-reference/sql/create-application-service) at your
deploy destination (the resolved `database` and `schema` in
[`app.yml`](/developer-guide/snowflake-app-runtime/app-yml)).

On the **first deploy**, Snowflake issues
`CREATE OR ALTER APPLICATION SERVICE` from the package in your artifact
repository (typically the `LATEST` version) and applies the full specification
from `app.yml`. On later deploys, the same statement **converges** the service
to the manifest: fields omitted from `app.yml` go back to their defaults. Your
app URL doesn’t change. For instance counts and suspend, see
[Scale and suspend Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/scale-and-suspend).

The artifact repository holds the built packages; the Application Service runs
where the resolved target points. Those locations are configured
independently. See [Where each workload runs](#label-deploy-build-infrastructure)
above.

Note

For team deploys, complete account administrator setup so defaults target a
shared database and schema you can grant to other roles. Without setup, deploy
may default to your [personal database](/user-guide/personal-databases), which
you can’t share with teammates.

## How configuration files fit together

These files and settings define the pipeline:

| File or setting | Role in the pipeline |
| --- | --- |
| [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml) | Deploy destination, `ignore` list, optional  `artifact_repo`, `build_eai`, and  `build_job_location`, service configuration, and install / build / run commands |
| [Account administrator setup](/developer-guide/snowflake-app-runtime/account-admin-setup) | Shared deploy destination defaults; doesn’t change where the build job runs or how build egress works |

Expand

Show lessSee more

## See also

- [Getting started with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/getting-started):
  end-to-end walkthrough with Cortex Code or the CLI
- [`snow app deploy` command reference](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/deploy):
  syntax, phase flags, and examples
- [app.yml manifest](/developer-guide/snowflake-app-runtime/app-yml):
  deploy and build configuration
- [Migrate from snowflake.yml to app.yml](/developer-guide/snowflake-app-runtime/migrate-to-app-yml):
  move a `snowflake.yml` project
- [Scale and suspend](/developer-guide/snowflake-app-runtime/scale-and-suspend):
  instance counts and stopping a running app
- [Deploy targets](/developer-guide/snowflake-app-runtime/deploy-targets)
- [Snowflake App Runtime limitations](/developer-guide/snowflake-app-runtime/limitations):
  build timeout and other limits
- [Configure service egress](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress):
  creating network rules and EAIs for SPCS workloads
- [Governing outbound network access](/developer-guide/snowflake-app-runtime/security#label-snowflake-app-runtime-security-outbound-network):
  account controls for build egress and runtime integrations
