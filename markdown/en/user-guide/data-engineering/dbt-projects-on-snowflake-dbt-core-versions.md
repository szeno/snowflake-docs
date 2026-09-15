# Supported dbt versions for dbt Projects on Snowflake

Snowflake provides managed runtimes for dbt Projects to ensure a secure and predictable execution environment. Because dbt releases can
introduce breaking changes or security vulnerabilities, Snowflake follows a structured lifecycle for each version. This policy allows users
to pin specific versions for governance and reproducibility while providing a clear timeline for required migrations.

**Supported versions for dbt Projects**

| dbt Version Supported | Snowflake Support Level | dbt Labs Support |
| --- | --- | --- |
| dbt Fusion 2.0.0-preview.186 | Active support | Active |
| dbt Fusion 2.0.0-preview.175 | Active support | Active |
| dbt Core 1.11.11 | Active support | Active support until Dec 18, 2026 |
| dbt Core 1.10.15 | Active support | Deprecated |
| dbt Core 1.9.4 | Active support | Deprecated |

Expand

Show lessSee more

The DBT\_VERSION parameter implicitly defines the execution engine based on the version, as shown in the table below.

**Version based engine mapping**

| User Input (DBT\_VERSION) | Condition | Resulting Engine |
| --- | --- | --- |
| `'1.x'` (for example, `1.9.4`) | Version `< 2.0` | dbt Core (Python-based) |
| `'2.x'` (for example, `2.0.0-preview.175`) | Version `>= 2.0` | dbt Fusion (Rust-based) |

Expand

Show lessSee more

## View supported dbt versions

To view supported dbt versions, run the [SYSTEM$SUPPORTED\_DBT\_VERSIONS](/sql-reference/functions/system_supported_dbt_versions) system function, as shown
in the following example:

Copy code

```
SELECT SYSTEM$SUPPORTED_DBT_VERSIONS();
```

```
[{"dbt_version":"1.9.4","type":"dbt Core"},{"dbt_version":"1.10.15","type":"dbt Core"},{"dbt_version":"1.11.11","type":"dbt Core"}]
```

## Set the account-level default version

Account administrators can set a default dbt version using the [DEFAULT\_DBT\_VERSION](/sql-reference/parameters#label-default-dbt-version)
account parameter. Changing this parameter doesn’t affect existing dbt project objects. It only applies to projects
created afterward when an explicit `DBT_VERSION` attribute is not specified. This lets you opt in to newer versions
without requiring users to specify `DBT_VERSION` in every CREATE DBT PROJECT statement.

Copy code

```
ALTER ACCOUNT SET DEFAULT_DBT_VERSION = '1.11.11';
```

This default version is also used by workspaces to set the initial dbt workspace runtime version.

Individual dbt project objects can still override the account default by specifying `DBT_VERSION` at creation time,
by using [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project), or during each execution with
[EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project).

## Alter the dbt execution version

To alter the dbt version that the dbt project object will execute, run the [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project) command as shown
in the following example:

Copy code

```
ALTER DBT PROJECT my_dbt_project SET DBT_VERSION = '1.11.11';
```

## Create a dbt project object pinned to a version

The following example creates a dbt project object pinned to the 1.11.11 dbt version:

Copy code

```
CREATE OR REPLACE DBT PROJECT my_dbt_project
  FROM '@my_stage/dbt_files'
  DBT_VERSION = '1.11.11';
```

Note

You can also override the dbt version for a single execution by specifying `DBT_VERSION` in the
[EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project) statement.

For more information and examples, see [CREATE DBT PROJECT](/sql-reference/sql/create-dbt-project) and [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project).

## Migrate to dbt Fusion

dbt Fusion 2.0.0-preview.175 is a ground-up Rust rewrite of the dbt runtime, designed to deliver significantly faster parse and compile times. The “preview” in the name reflects dbt Labs’ versioning convention, not the release status. This version is generally available on both dbt Platform and Snowflake.

To migrate from dbt Core to dbt Fusion, use the following resources:

- **Automated fixes with dbt-autofix:** Run `uvx dbt-autofix` in your local terminal to automatically resolve dbt Core deprecation warnings and check package compatibility before switching to Fusion. No installation is required. `uvx` runs the tool directly. For more information, see [dbt-labs/dbt-autofix](https://github.com/dbt-labs/dbt-autofix?tab=readme-ov-file#deprecations---the-main-one).
- **Official upgrade guide:** The [Upgrading to the dbt Fusion engine](https://docs.getdbt.com/docs/dbt-versions/core-upgrade/upgrading-to-fusion?version=1.11) guide on the dbt Developer Hub covers the full migration process.
- **AI-assisted migration:** The publicly available [dbt Core to Fusion migration skill](https://github.com/dbt-labs/dbt-agent-skills/blob/main/skills/dbt-migration/skills/migrating-dbt-core-to-fusion/SKILL.md) can be used by AI coding agents such as Cortex Code to guide migration work.

## How deprecation and decommissioning work

- Snowflake supported versions: These versions are available for all new and existing projects. Snowflake provides full technical support,
  including security patches.
- Snowflake deprecated versions: These versions have reached the end of their active development cycle. While they remain fully functional for
  existing projects, users are discouraged from starting new projects on a deprecated version.
- Snowflake decommissioned versions: These versions are officially removed from the Snowflake environment. At this stage, any project pinned to
  a decommissioned version will fail to execute until it’s updated to a currently supported version.
- dbt Core and dbt Fusion support levels: Even if a version reaches *Critical Support*, *Deprecated*, or *End of Life* status according to
  [dbt Labs](https://docs.getdbt.com/docs/dbt-versions/core#latest-releases), it remains supported on Snowflake. This means that you aren’t
  forced into immediate upgrades and can maintain your existing environment for as long as you choose.
