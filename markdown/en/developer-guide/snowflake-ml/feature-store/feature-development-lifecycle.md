# Declarative feature store overview

The Snowflake Feature Store supports a declarative, code-first workflow for developing,
testing, and deploying features to production. Instead of writing imperative Python scripts
that create objects one at a time, you describe your feature store (entities, data
sources, feature views, and feature groups) as files in a project directory, preview the
changes with `snow feature plan`, and apply them with `snow feature apply`.

This approach brings the benefits of infrastructure as code to feature engineering:
version control, code reviews, repeatable deployments, and safe rollbacks.
Because feature definitions are plain files in a project directory, you can integrate them
into CI/CD pipelines to automatically validate, test, and promote features across
development, staging, and production environments.

A typical development cycle looks like this:

1. **Define** features as YAML or Python in a local project directory.
2. **Plan** changes to preview what would be created, updated, or deleted.
3. **Apply** the plan to deploy features to a Snowflake target environment.
4. **Test** by ingesting events and querying the online store.
5. **Iterate** by editing definitions and repeating the plan-apply loop.

## Authoring forms

Each object in a project can be authored in one of three forms. The two declarative forms,
YAML and Python, compile to byte-identical on-wire specs, so you can pick whichever fits
your workflow. The imperative form is a separate API that runs immediately against a live
Snowflake session with no plan or apply step. The following table compares the three forms:

| Form | When to use | Where it runs |
| --- | --- | --- |
| YAML | Source-of-truth declarative spec that’s easy to diff and review. | Read by `snow feature plan` and `apply`. |
| Python (declarative) | When you want IDE completion, type checking, inline user-defined functions as callables, or cross-references between objects by Python import. Uses the lightweight `snowflake.ml.feature_store.decl` models. | Read by `snow feature plan` and `apply`. Loads as plain Python with no Snowflake session. |
| Imperative (`snowflake-ml-python`) | Notebook or script flows where you already have a `FeatureStore` session and want to register objects directly. | Calls `FeatureStore.register_*` against a live Snowflake session. |

Expand

Show lessSee more

For details on authoring each object kind, see
[Declarative authoring](/developer-guide/snowflake-ml/feature-store/feature-store-declarative-authoring).
If you already have objects registered through the imperative API, see
[Migrating to declarative](/developer-guide/snowflake-ml/feature-store/feature-store-declarative-migration).

## Prerequisites

The `snow feature` command group is part of the Snowflake CLI. The commands need the
`snowflake-ml-python` library with the `feature_store` extra on the same interpreter:

Copy code

```
pip install -U "snowflake-ml-python[feature_store]"
snow feature --help
```

Each command takes its target from the active Snowflake connection plus the project’s
`manifest.yml`. The active connection supplies the account identifier, warehouse, and the
programmatic access token used by `ingest` and `query`. The manifest target supplies the
database, schema, and role used for plan and apply.

## 1. Initialize a project

A feature store project is a directory that contains a `manifest.yml` and a `sources/`
tree. Each entity, data source, feature view, and feature group gets its own file (YAML or
Python). This structure keeps definitions modular, reviewable, and easy to manage in
version control.

Scaffold a new project in the current directory:

Copy code

```
mkdir my_feature_store
cd my_feature_store
snow feature init
```

`snow feature init` runs in the current directory (it has no project name argument). It
writes `manifest.yml` from the active connection, scaffolds the `sources/` tree, ensures
the schema and feature-store metadata exist, and exports every deployed object into
`sources/`. Exports are written as Python spec files by default; pass `--yaml` to author in
YAML instead.

The command creates the following layout:

```
my_feature_store/
├── manifest.yml
└── sources/
    ├── entities/
    ├── datasources/
    ├── feature_views/
    └── feature_groups/
```

`snow feature init` is idempotent. Re-running it preserves your `manifest.yml`
byte-for-byte and refreshes `sources/` from whatever is currently deployed, so you can use
it any time to pull the deployed state into your local project.

For the `manifest.yml` schema, deployment targets, and templating, see
[Declarative project configuration](/developer-guide/snowflake-ml/feature-store/feature-store-declarative-projects).

## 2. Define features

Edit the files under `sources/` to describe your entities, data sources, feature views, and
feature groups. Each file is a self-contained definition that maps to a single Snowflake
object. Source files can omit the `database` and `schema` keys: the planner injects the
resolved target into any spec that doesn’t carry them, so the same files work against any
target in `manifest.yml`.

Objects are identified as follows:

- **Entities and data sources** are unversioned, schema-level objects identified by name.
- **Feature views and feature groups** are identified by the pair `(name, version)`. Version
  `V1` and version `V2` of the same name are independent objects: editing, planning, or
  applying one has no effect on the other. To roll out a breaking change without downtime,
  publish it under a new version instead of editing the existing one.

For the full authoring reference for each object kind, see
[Declarative authoring](/developer-guide/snowflake-ml/feature-store/feature-store-declarative-authoring).

## 3. Plan changes

Before modifying anything in Snowflake, preview exactly what would happen:

Copy code

```
snow feature plan
```

The planner compares your local project definitions against the deployed state in the
target environment and prints a diff of the operations it would run, such as `CREATE_FV`,
`UPDATE_FV`, `RECREATE_FV`, and `DROP_FV`. It writes the plan to a JSON file under
`out/plan/`. `plan` is read-only: it never mutates Snowflake, and nothing is applied until
you run `snow feature apply`. This is the same plan-then-deploy model used by Snowflake’s
broader [infrastructure-as-code tooling](/developer-guide/builders/devops-with-snowflake).

Deletion detection is off by default: objects present in the deployed state but absent from
your local `sources/` tree are left untouched. Pass `--delete` to surface them as `DROP_*`
operations.

## 4. Apply changes

Once you’re satisfied with the plan, deploy your changes:

Copy code

```
snow feature apply
```

By default, `apply` runs the latest unapplied plan file from `out/plan/`. It creates or
updates all entities, data sources, feature views, and feature groups in the target
environment and reports per-operation status.

Destructive operations, such as `RECREATE_FV`, `DROP_FV`, `DROP_ENTITY`, and `DROP_FG`, are
refused unless you pass `--destructive`. For the full list, see
[snow feature apply](/developer-guide/snowflake-ml/feature-store/feature-store-cli-reference#label-feature-cli-apply). The gate is whole-plan: if any operation is destructive and you
don’t opt in, nothing executes.

Copy code

```
snow feature apply --destructive
```

## 5. Test and iterate

Streaming feature views and online batch feature views are served through an online service
in the same schema. Provision it once per schema:

Copy code

```
snow feature online-service create --producer-role MY_PRODUCER --consumer-role MY_CONSUMER
```

After you apply the plan, validate your deployment by pushing events to a streaming source
and querying features for a set of entity keys. Both commands authenticate to the online
service with a programmatic access token exported as `SNOWFLAKE_PAT`:

Copy code

```
snow feature ingest CLICKSTREAM_EVENTS --data events.json
snow feature query USER_CLICK_STATS_DECL --version V1 --keys '[{"USER_ID":"u1"}]'
```

Use `snow feature list` to see every deployed object, and `snow feature describe` to inspect
one:

Copy code

```
snow feature list
snow feature describe USER_CLICK_STATS_DECL --version V1
```

When you need to make changes, edit the files and repeat the plan-apply loop. The planner
detects only the differences and applies incremental updates. After someone else applies
changes, run `snow feature sync` to refresh your local `sources/` tree from the deployed
runtime.

## Command reference

For the full `snow feature` command group, including shared flags, per-command flags, and
the exit statuses that `apply` reports, see
[Declarative API (snow feature CLI) references](/developer-guide/snowflake-ml/feature-store/feature-store-cli-reference).
