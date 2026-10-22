# Declarative project configuration

A declarative project is a directory of files that `snow feature plan` and
`snow feature apply` deploy to Snowflake. This page covers how a project is laid out and
how to configure deployment targets and templating in `manifest.yml`. For how to author
each object kind, see
[Declarative authoring](/developer-guide/snowflake-ml/feature-store/feature-store-declarative-authoring).
For the end-to-end workflow, see
[Declarative feature store overview](/developer-guide/snowflake-ml/feature-store/feature-development-lifecycle).

## Project layout

A project is a directory containing a single `manifest.yml` at its root and a `sources/`
tree beneath it. `snow feature init` creates the skeleton:

```
my_feature_store/
├── manifest.yml                 # targets, role, templating
├── sources/
│   ├── entities/                # one file per entity
│   ├── datasources/             # one file per streaming or batch source
│   ├── feature_views/           # one file per streaming or batch feature view
│   └── feature_groups/          # one file per feature group
└── out/plan/                    # generated plan files
```

Each file under `sources/` can be authored as YAML (`.yaml`) or Python (`.py`). Both forms
compile to the same on-wire spec. The directory holding `manifest.yml` is the project root.
Every command reads `manifest.yml` from that directory only: it doesn’t search parent
directories, so run commands from the project root or point at it with `--from`.

## Type names

Column types in the declarative forms are strings that mirror the Snowpark `types` module
without importing it:

- `StringType`, `BooleanType`
- `IntegerType`, `LongType`, `FloatType`, `DoubleType`, `DecimalType`
- `TimestampType`, `DateType`, `TimeType`

Some of these types accept an optional modifier:

- `StringType` accepts `length`.
- `DecimalType` accepts `precision` and `scale`.
- `TimestampType` accepts `tz`.

## Manifest and deployment targets

The `manifest.yml` tells `snow feature` where to deploy (account, database, schema, role)
and how to render any variable substitutions in your specs. A complete manifest looks like
this:

Copy code

```
manifest_version: 1                        # required, must be 1
type: feature_store                        # required, must be "feature_store"
default_target: DEV                        # required when more than one target

targets:                                   # required, one or more
  DEV:
    account_identifier: MY_ORG-MY_ACCOUNT  # required, canonical <ORG>-<ACCOUNT> form
    database: DEV_DB                        # required
    schema: DEV_SCHEMA                      # required
    role: DEV_DEVELOPER                     # optional
    templating_config: DEV                  # optional
  PROD:
    account_identifier: MY_ORG-MY_ACCOUNT
    database: PROD_DB
    schema: PROD_SCHEMA
    role: PROD_DEPLOYER
    templating_config: PROD
```

A **target** is one deployment destination: a single Snowflake schema in one account. Most
projects have at least two, such as a developer sandbox and production. Switch between them
with the `--target` flag on `snow feature plan` and `apply`. At apply time, the target’s
`account_identifier` is checked against the active connection, so you can’t accidentally
apply a dev plan to a prod account.

The following table describes each target field:

| Target field | Required | Meaning |
| --- | --- | --- |
| `account_identifier` | Yes | Canonical `<ORG>-<ACCOUNT>` form. Checked against the active connection at apply time. |
| `database` | Yes | Target database. Injected into specs that omit a `database` key. |
| `schema` | Yes | Target schema. Created by `snow feature init` if your role has `CREATE SCHEMA`. |
| `role` | No | Role used by `plan` and `apply`. Defaults to the active connection’s role. |
| `templating_config` | No | Names a block under `templating.configurations` to use for this target. |

Expand

Show lessSee more

Note

`warehouse` is not a target field. Warehouse selection comes from the active connection, not
the manifest. A target that declares a `warehouse` key is rejected at load time. To vary the
warehouse used by an individual feature view, use a templating variable.

## Templating

Templating lets you parameterize spec files with Jinja2 placeholders that are resolved at
plan time. For example, a dev target can cap source-row scans at 10 rows while prod scans
100, from the same on-disk specs. Variables are defined in the `templating` block and
selected per target with `templating_config`:

Copy code

```
templating:
  defaults:                 # fallback when a target has no templating_config
    row_limit: 1
    warehouse: DEV_XS_WH
  configurations:           # named groups; targets pick one via templating_config
    DEV:
      row_limit: 10
      warehouse: DEV_XS_WH
    PROD:
      row_limit: 100
      warehouse: PROD_M_WH
```

Reference variables with standard Jinja2 syntax inside spec files:

Copy code

```
-- sources/datasources/EVENTS.sql
SELECT * FROM RAW_EVENTS LIMIT {{ row_limit }}
```

A variable can be set in up to three places. When the same variable is set in more than one
place, `snow feature plan` uses the value from the highest-priority source:

1. **Command line (highest priority)**: a `--variable KEY=VALUE` flag on `snow feature plan`.
2. **Target configuration**: the block under `templating.configurations` that the target
   names in `templating_config`.
3. **Defaults (lowest priority)**: the values under `templating.defaults`. These apply only
   when neither of the other sources sets the variable.

For example, with the manifest above, `snow feature plan --target DEV` renders `row_limit` as
`10` from the `DEV` configuration, not `1` from `defaults`. Running
`snow feature plan --target DEV --variable row_limit=5` renders it as `5`, because the
command line overrides both.

Templating is resolved at plan time only. The rendered values are baked into the plan file,
so `snow feature apply` doesn’t accept `--variable`. To apply a different rendering, re-run
`plan` with the new override.

Tip

When you use templating with sidecar files (a `.sql` file for a batch source query, or a
`.py` file for a streaming user-defined function), keep the Jinja2 placeholder inside the
sidecar body, not in the parent YAML’s `query_file` or `udf.file` value.

## Next steps

With the project laid out and a target configured, author your entities, data sources,
feature views, and feature groups. See
[Declarative authoring](/developer-guide/snowflake-ml/feature-store/feature-store-declarative-authoring).
