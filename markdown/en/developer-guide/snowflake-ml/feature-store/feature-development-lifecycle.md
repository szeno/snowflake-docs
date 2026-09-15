# Feature Development Lifecycle

Preview Feature — Private

Support for this feature is currently not in production and is available only to selected accounts.

The Snowflake Feature Store supports a declarative, code-first workflow for developing,
testing, and deploying features to production. Instead of writing imperative Python scripts
that create objects one at a time, you describe your entire feature store (entities, data
sources, and feature views) as YAML files in a project directory, preview the changes with
`snow feature plan`, and apply them with `snow feature apply`.

This approach brings the same benefits that infrastructure-as-code tooling provides for
infrastructure: version control, code reviews, repeatable deployments, and safe rollbacks.
Because feature definitions are plain files in a project directory, you can integrate them
into CI/CD pipelines to automatically validate, test, and promote features across
development, staging, and production environments.

A typical development cycle looks like this:

1. **Define** features as YAML and Python in a local project directory.
2. **Plan** changes to preview what would be created, updated, or deleted.
3. **Apply** the plan to deploy features to a Snowflake target environment.
4. **Test** by ingesting events and querying the online store.
5. **Iterate** by editing definitions and repeating the plan-apply loop.

## Prerequisites

Note

During preview, the CLI is distributed as a private wheel and isn’t yet on PyPI. Contact
your Snowflake account team to request access.

The `snow feature` CLI is built on top of Snowflake CLI. Install the declarative authoring
library and the CLI build that ships the `snow feature` plugin:

Copy code

```
pip install -U snowflake_ml_feature_store_decl-0.1.0-py3-none-any.whl
pip install -U snowflake_cli-*.whl
snow feature --help
```

## 1. Initialize a project

A feature store project is a directory that contains a `manifest.yml` and a `sources/` tree.
Each entity, data source, and feature view gets its own YAML file (and optionally a `.py`
file for transformation logic). This structure keeps definitions modular, reviewable, and
easy to manage in version control.

Scaffold a new project from a template:

Copy code

```
snow feature init my_feature_store
cd my_feature_store
```

This creates the following layout:

```
my_feature_store/
├── manifest.yml
└── sources/
    ├── entities/
    │   └── USER_ID.yaml
    ├── datasources/
    │   └── CLICKSTREAM_EVENTS.yaml
    └── feature_views/
        ├── USER_CLICK_STATS.yaml
        └── USER_CLICK_STATS.py
```

### Configure deployment targets

A deployment target is the Snowflake environment where your feature store resources
should be created: the account, database, schema, and role. Define multiple targets in
`manifest.yml` to represent different stages of your workflow, such as `dev`, `staging`, `prod`. Switch
between them with the `--target` flag when running `snow feature plan` or
`snow feature apply`.

Copy code

```
manifest_version: 1
type: feature_store
default_target: dev
targets:
  dev:
    account_identifier: MY_ORG-MY_ACCOUNT-DEV
    database: MY_FS
    schema: FEATURES
    role: DATA_SCIENTIST
  staging:
    account_identifier: MY_ORG-MY_ACCOUNT-STAGING
    database: MY_FS
    schema: FEATURES
    role: FS_ADMIN
  prod:
    account_identifier: MY_ORG-MY_ACCOUNT-PROD
    database: MY_FS
    schema: FEATURES
    role: FS_ADMIN
```

Source files under `sources/` can omit the `database` and `schema` keys. The planner
injects the resolved target into any spec that doesn’t carry them, so the same files
work against any target listed in `manifest.yml`.

## 2. Define features

Edit the YAML files under `sources/` to describe your entities, data sources, and feature
views. Each file is a self-contained definition that maps to a single Snowflake object.

For feature views that require transformation logic (for example, aggregations or
derived columns), place a Python file alongside the YAML file with the same base name.
The YAML file declares the metadata (entity, schedule, online config), while the Python
file contains the transformation function.

### Batch vs streaming transformations

Snowpark DataFrame is not currently supported for defining or deploying features with `snow feature`.

| Feature view type | Supported transformation |
| --- | --- |
| Batch | SQL string only |
| Streaming | pandas UDF only |

Expand

Show lessSee more

A batch feature view expresses its logic as a SQL string. A streaming feature view
expresses its transform as a pandas UDF that receives and returns a pandas DataFrame.

If you prototyped features with the imperative Python SDK using Snowpark DataFrames,
rewrite that logic before moving to declarative:

- **Batch:** express the feature as SQL (for example, the query behind a managed feature view).
- **Streaming:** express the transform as a pandas UDF (the same pattern as stream feature
  views in the imperative API).

Snowpark DataFrame has no declarative equivalent. Any logic you built with
Snowpark must be reimplemented as SQL or pandas to use `snow feature plan` and
`snow feature apply`.

For imperative SDK patterns (including Snowpark-managed feature views), see
[Working with feature views](/developer-guide/snowflake-ml/feature-store/feature-views)
and [Advanced feature engineering](/developer-guide/snowflake-ml/feature-store/advanced-feature-engineering).

## 3. Plan changes

Before modifying anything in Snowflake, preview exactly what would happen:

Copy code

```
snow feature plan
```

The planner compares your local project definitions against the deployed state in the
target environment and shows a diff of what would be created, updated, or deleted. Nothing
is applied until you explicitly run `snow feature apply`. This is the same plan-then-deploy
model used by Snowflake’s broader [infrastructure-as-code tooling](/developer-guide/builders/devops-with-snowflake).

## 4. Apply changes

Once you’re satisfied with the plan, deploy your changes:

Copy code

```
snow feature apply
```

This creates or updates all entities, data sources, and feature views in the target
environment. The CLI reports progress and confirms what was applied.

## 5. Test and iterate

After applying, you can validate your deployment by ingesting test events and querying the
online store directly from the CLI:

Copy code

```
snow feature ingest --source CLICKSTREAM_EVENTS --file test_events.json
snow feature query --feature-view USER_CLICK_STATS --keys '{"USER_ID": "user_1"}'
```

Use `snow feature describe` to inspect the deployed state of any object:

Copy code

```
snow feature describe --entity USER_ID
snow feature describe --feature-view USER_CLICK_STATS
```

When you need to make changes, edit the YAML or Python files and repeat the plan-apply
loop. The planner detects only the differences and applies incremental updates.

## Command reference

| Command | Description |
| --- | --- |
| `snow feature init` | Scaffold a new feature store project from a template. |
| `snow feature plan` | Preview the changes that would be applied to the target, without modifying Snowflake. |
| `snow feature apply` | Apply pending changes (entities, sources, feature views) to the target. |
| `snow feature describe` | Show the deployed state of an entity, source, or feature view. |
| `snow feature ingest` | Push events to a streaming source registered in the project. |
| `snow feature query` | Read features for a given set of entity keys from the online store. |
| `snow feature online-service` | Create or manage the online service that backs the project. |

Expand

Show lessSee more
