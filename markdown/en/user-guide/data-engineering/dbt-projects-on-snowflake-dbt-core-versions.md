# Supported dbt versions for dbt Projects on Snowflake

Snowflake provides managed runtimes for dbt Projects to ensure a secure and predictable execution environment. Because dbt releases can
introduce breaking changes or security vulnerabilities, Snowflake follows a structured lifecycle for each version. This policy allows users
to pin specific versions for governance and reproducibility while providing a clear timeline for required migrations.

Important

**dbt Labs end-of-life dates don’t affect your dbt project objects on Snowflake.** Any dbt project object pinned to a dbt version will
continue to run on Snowflake, even after dbt Labs deprecates that version or ends support for it. Snowflake decommissions a version only through its own
lifecycle, and announces any decommission at least three months in advance through the behavior change release process. For more
information, see [How Snowflake handles older dbt versions](#label-dbt-version-lifecycle).

**Supported versions for dbt Projects**

| dbt Version Supported | Snowflake Support Level | dbt Labs Support |
| --- | --- | --- |
| dbt 2.0.0 | Active support | Active |
| dbt Fusion 2.0.0-preview.210 | Active support | Active |
| dbt Fusion 2.0.0-preview.186 | Active support | Active |
| dbt Fusion 2.0.0-preview.175 | Active support | Active |
| dbt Core 1.12.3 | Active support | Active support until Jul 15, 2027 |
| dbt Core 1.11.11 | Active support | Active support until Dec 18, 2026 |
| dbt Core 1.10.15 | Active support | Deprecated |
| dbt Core 1.9.4 | Active support | Deprecated |

Expand

Show lessSee more

The **dbt Labs Support** column is for reference only. It shows each version’s support status from dbt Labs and doesn’t affect whether
the version runs on Snowflake.

The DBT\_VERSION parameter implicitly defines the execution engine based on the version, as shown in the table below.

**Version based engine mapping**

| User Input (DBT\_VERSION) | Condition | Resulting Engine |
| --- | --- | --- |
| `'1.x'` (for example, `1.9.4`) | Version `< 2.0` | dbt Core (Python-based) |
| `'2.x'` (for example, `2.0.0`) | Version `>= 2.0` | dbt Fusion (Rust-based) |

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
[{"dbt_version":"1.9.4","type":"dbt Core"},{"dbt_version":"1.10.15","type":"dbt Core"},{"dbt_version":"1.11.11","type":"dbt Core"},{"dbt_version":"1.12.3","type":"dbt Core"},{"dbt_version":"2.0.0-preview","type":"dbt Fusion"},{"dbt_version":"2.0.0-preview.175","type":"dbt Fusion"},{"dbt_version":"2.0.0-preview.186","type":"dbt Fusion"},{"dbt_version":"2.0.0-preview.210","type":"dbt Fusion"},{"dbt_version":"2.0.0","type":"dbt Fusion"}]
```

## Set the account-level default version

Account administrators can set a default dbt version using the [DEFAULT\_DBT\_VERSION](/sql-reference/parameters#label-default-dbt-version)
account parameter. Changing this parameter doesn’t affect existing dbt project objects. It only applies to projects
created afterward when an explicit `DBT_VERSION` attribute is not specified. This lets you opt in to newer versions
without requiring users to specify `DBT_VERSION` in every CREATE DBT PROJECT statement.

Copy code

```
ALTER ACCOUNT SET DEFAULT_DBT_VERSION = '1.12.3';
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
ALTER DBT PROJECT my_dbt_project SET DBT_VERSION = '1.12.3';
```

## Create a dbt project object pinned to a version

The following example creates a dbt project object pinned to the 1.12.3 dbt version:

Copy code

```
CREATE OR REPLACE DBT PROJECT my_dbt_project
  FROM '@my_stage/dbt_files'
  DBT_VERSION = '1.12.3';
```

Note

You can also override the dbt version for a single execution by specifying `DBT_VERSION` in the
[EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project) statement.

For more information and examples, see [CREATE DBT PROJECT](/sql-reference/sql/create-dbt-project) and [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project).

## Migrate to dbt Fusion

dbt Fusion is a ground-up Rust rewrite of the dbt runtime, designed to deliver significantly faster parse and compile times. Fusion runs dbt 2.x versions, including dbt 2.0.0. The “preview” in earlier `2.0.0-preview` version names reflects dbt Labs’ versioning convention, not the release status. These versions are generally available on both dbt Platform and Snowflake.

To migrate from dbt Core to dbt Fusion, use the following resources:

- **Automated fixes with dbt-autofix:** Run `uvx dbt-autofix` in your local terminal to automatically resolve dbt Core deprecation warnings and check package compatibility before switching to Fusion. No installation is required. `uvx` runs the tool directly. For more information, see [dbt-labs/dbt-autofix](https://github.com/dbt-labs/dbt-autofix?tab=readme-ov-file#deprecations---the-main-one).
- **Official upgrade guide:** The [Upgrading to the dbt Fusion engine](https://docs.getdbt.com/docs/dbt-versions/core-upgrade/upgrading-to-fusion?version=1.11) guide on the dbt Developer Hub covers the full migration process.
- **AI-assisted migration:** The publicly available [dbt Core to Fusion migration skill](https://github.com/dbt-labs/dbt-agent-skills/blob/main/skills/dbt-migration/skills/migrating-dbt-core-to-v2/SKILL.md) can be used by AI coding agents such as Cortex Code to guide migration work.

## How Snowflake handles older dbt versions

Snowflake manages dbt versions independently of dbt Labs. You can leave existing dbt project objects on their pinned version or upgrade them on your
own schedule. When your team is ready, you can create new dbt project objects on newer versions.

On Snowflake, each version is in one of the following states:

- **Supported:** The version is available for new and existing dbt project objects. Snowflake provides full technical support, including security
  patches.
- **Deprecated:** The version has reached the end of its active development cycle. dbt project objects pinned to a deprecated version keep running,
  but Snowflake recommends that you don’t create new dbt project objects on it.
- **Decommissioned:** Snowflake has removed the version. dbt project objects pinned to a decommissioned version fail to execute until you update them
  to a supported version. If Snowflake decides to decommission a dbt version, we will provide at least three months of lead time before
  the decommission takes effect. We will announce any decommissions through the standard [behavior change release process](/release-notes/behavior-change-policy).

When dbt Labs changes the support status of a dbt version, the version’s support status on Snowflake doesn’t change. Even if a version
reaches *Critical Support*, *Deprecated*, or *End of Life* status according to
[dbt Labs](https://docs.getdbt.com/docs/dbt-versions/core#latest-releases), it remains supported on Snowflake. You don’t need to upgrade
because of a dbt Labs date.
