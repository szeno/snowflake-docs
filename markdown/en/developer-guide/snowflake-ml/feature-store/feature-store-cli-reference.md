# Declarative API (snow feature CLI) references

Every command is a subcommand of the `feature` plugin in the Snowflake CLI. Run
`snow feature --help` for a synopsis. For installation requirements, see
[Prerequisites](/developer-guide/snowflake-ml/feature-store/feature-development-lifecycle#label-feature-dev-lifecycle-prerequisites).
For the end-to-end workflow these commands support, see
[Declarative feature store overview](/developer-guide/snowflake-ml/feature-store/feature-development-lifecycle).

The following table summarizes the command group. Prefix each command with `snow feature`
when you run it (for example, `snow feature init`). Each command is described in detail in
the sections that follow:

| Command | Description |
| --- | --- |
| [`init`](#label-feature-cli-init) | Scaffold a project in the current directory, bootstrap the schema, and export deployed objects into `sources/`. |
| [`sync`](#label-feature-cli-sync) | Refresh `sources/` from the deployed runtime without re-running the schema bootstrap. |
| [`plan`](#label-feature-cli-plan) | Preview the operations that would be applied to the target, without modifying Snowflake. |
| [`apply`](#label-feature-cli-apply) | Run a plan file against the target. |
| [`list`](#label-feature-cli-list) | List every object deployed in the target schema. |
| [`describe`](#label-feature-cli-describe) | Show the deployed state of one object. |
| [`online-service`](#label-feature-cli-online-service) | Manage the online service that backs streaming and online feature views. |
| [`ingest`](#label-feature-cli-ingest) | Push records to a streaming source registered in the project. |
| [`query`](#label-feature-cli-query) | Read features for a set of entity keys from the online store. |

Expand

Show lessSee more

## Shared flags

Two flags are shared by every command except `init`, which always operates on the current
directory:

- `--from <DIR>`: the project root, the directory that directly contains `manifest.yml`.
  Defaults to the current directory. The CLI doesn’t search parent directories, so running
  from a subdirectory such as `sources/` fails rather than binding to an ancestor’s
  manifest.
- `--target <NAME>`: the manifest target to use. Defaults to `manifest.yml`’s
  `default_target`.

The Snowflake CLI framework also provides `--connection <NAME>` to pick a named connection,
`--format json` (or `csv`) for machine-readable output, and `--role`, `--database`, and
`--schema` overrides. `--format json` suppresses human display banners so stdout is a clean,
parseable payload.

## snow feature init

Scaffold a project in the current directory. `init` has no `--from`: run it inside the
directory you want to become the project root.

Copy code

```
snow feature init
```

`init` resolves the manifest target from the active connection, scaffolds
`sources/{entities,datasources,feature_views,feature_groups}/`, ensures the schema and
feature-store metadata exist, and exports every deployed object into `sources/`. It’s
idempotent: re-running it preserves your `manifest.yml` byte-for-byte and refreshes the
export, so you can use it any time to pull the deployed state into your project.

The command takes the following flags:

| Flag | Purpose |
| --- | --- |
| `--python` | Export as `.py` Pydantic constructors. This is the default. |
| `--yaml` | Export as YAML instead of the default `.py` files. |

Expand

Show lessSee more

`--python` and `--yaml` are mutually exclusive.

## snow feature sync

Refresh `sources/` from the deployed runtime. `sync` runs `init`’s export phase without the
schema bootstrap, so it requires an existing `manifest.yml` and an already-initialized
feature store.

Copy code

```
snow feature sync
snow feature sync --name MY_FV
snow feature sync --yaml
```

The command takes the following flags:

| Flag | Purpose |
| --- | --- |
| `--name <OBJECT>` | Sync by exact (case-insensitive) name. Omit to sync everything. |
| `--python` or `--yaml` | Export form. Defaults to `.py`. |

Expand

Show lessSee more

## snow feature plan

Compare the project’s `sources/` tree against the deployed state and write an ordered list
of operations (`CREATE_FV`, `UPDATE_FV`, `RECREATE_FV`, `DROP_FV`, `CREATE_ENTITY`,
`NO_CHANGE`, and so on) to a plan file. `plan` is read-only: it never mutates Snowflake.

Copy code

```
snow feature plan
snow feature plan --target PROD --variable row_limit=42
```

The command takes the following flags:

| Flag | Purpose |
| --- | --- |
| `--out <PATH>` | Override the plan file path. Defaults to `out/plan/feature_plan_<timestamp>.json`. |
| `--delete` | Enable full-sync deletion: emit `DROP_*` operations for deployed objects absent from `sources/`. Off by default. |
| `--variable KEY=VAL` (`-D KEY=VAL`) | Set a templating variable. May be repeated. |

Expand

Show lessSee more

## snow feature apply

Run a plan file against Snowflake. By default, `apply` runs the latest unapplied plan
under `out/plan/`.

Copy code

```
snow feature apply
snow feature apply --plan path/to/plan.json
snow feature apply --destructive
```

Destructive operations (`RECREATE_FV`, `DROP_FV`, `DROP_ENTITY`, `DROP_FG`) are refused
unless you pass `--destructive`. The gate is whole-plan: if any operation is destructive and
you don’t opt in, nothing executes.

The command takes the following flags:

| Flag | Purpose |
| --- | --- |
| `--plan <PATH>` | Run this exact plan file instead of auto-discovering one. |
| `--destructive` | Allow operations that drop, recreate, or overwrite existing objects. |

Expand

Show lessSee more

`apply` prints a terminal status to stderr and exits non-zero on failure, so scripts can
branch on the exit code:

| Status | Meaning | Exit code |
| --- | --- | --- |
| `applied` | All operations ran (or were skipped as `NO_CHANGE`). | 0 |
| `partial_failure` | At least one operation failed. | Non-zero |
| `refused` | The plan contains destructive operations and `--destructive` wasn’t passed. | Non-zero |
| `target_mismatch` | The plan’s target doesn’t match the active connection’s account. | Non-zero |
| `no_plan` | No unapplied plan file under `out/plan/`. | 0 (idle) |
| `validation_failed` | Spec validation failed before the plan ran. | Non-zero |

Expand

Show lessSee more

## snow feature list

List every object deployed in the target schema (entities, data sources, feature views,
feature groups), with name, kind, and version. The scope is the target schema only: `list`
doesn’t walk the local `sources/` tree.

Copy code

```
snow feature list
```

## snow feature describe

Print a multi-section view of one deployed object: entity columns, features, user-defined
function metadata, and online endpoints.

Copy code

```
snow feature describe USER_CLICK_STATS_DECL --version V1
```

Pass `--version` to pick between deployed versions of the same name. It’s optional when only
one version exists; when several versions exist, passing a bare name fails and the command
lists the available versions.

## snow feature online-service

Manage the Snowpark Container Services deployment that hosts the streaming ingest endpoint
and the Postgres-backed online feature tables. One service runs per schema. The service is
required by any `online: true` batch feature view, every streaming feature view, and every
feature group. Offline-only batch feature views don’t need it.

Copy code

```
snow feature online-service status
snow feature online-service create --producer-role MY_PRODUCER --consumer-role MY_CONSUMER
snow feature online-service drop --force
```

- `status`: print the current service status and the ingest and query endpoint URLs. Pass
  `-v` for per-component detail.
- `create`: provision the service, roles, secret, network rules, and endpoints.
  `--producer-role` defaults to the manifest target’s role; `--consumer-role` defaults to
  `PUBLIC`. `create` is idempotent.
- `drop`: destroy the service and every online feature table it backs. Offline artifacts
  survive. Requires a typed confirmation unless you pass `--force`.

## snow feature ingest

POST records to the online service’s ingest endpoint for a named streaming source. The
payload is a JSON array of objects, one key per source column. A client-side preflight
rejects payloads that don’t match the registered source schema before any HTTP call.

Copy code

```
snow feature ingest CLICKSTREAM_EVENTS --data events.json
```

The command takes the following flag:

| Flag | Purpose |
| --- | --- |
| `--data <FILE>` | Path to a JSON file, or `-` to read JSON from stdin. |

Expand

Show lessSee more

Requires `SNOWFLAKE_PAT` (a programmatic access token) exported in the environment.

## snow feature query

Read online features for one or more entity keys from a named feature view.

Copy code

```
snow feature query USER_CLICK_STATS_DECL --version V1 --keys '[{"USER_ID":"u1"}]'
```

`--version` is required: the online lookup is keyed on `(name, version)` with no `latest`
fallback. `--keys` is a JSON array of key objects whose keys are the feature view’s entity
join-key column names. Like `ingest`, `query` requires `SNOWFLAKE_PAT`.
