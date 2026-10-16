description:
:   Using the spark-migration Snowflake CoCo skill to migrate PySpark code to the Snowpark Python API with the SMA CLI

# Spark to Snowpark API with the Snowflake CoCo migration skill

You can migrate PySpark code to the native [Snowpark Python API](/developer-guide/snowpark/index) (`snowflake.snowpark`, snake\_case) by using the **spark-migration** skill in Snowflake CoCo. This path runs the [Snowpark Migration Accelerator (SMA)](/migrations/sma-docs/general/getting-started) CLI for conversion, then continues through a post-conversion pipeline (EWI dashboard, optional fixes, stage conversion, and validation).

This page covers the **Snowpark API** path (the bundled `snowpark-api` sub-skill). The default and recommended path is [Snowpark Connect](/migrations/sma-docs/migrating-with-cortex-code/spark-to-snowpark-connect), which preserves the PySpark API surface. For a phase-by-phase Snowpark Connect walkthrough, see [Migrating to Snowpark Connect walkthrough](/migrations/sma-docs/use-cases/migrating-to-snowpark-connect-walkthrough).

## When this path runs

The Snowpark API path is an **explicit opt-in**. The skill routes here only when you clearly ask for it, for example:

- Phrases such as “SMA”, “SMA CLI”, “run sma”, “Snowpark API”, or a `snowflake.snowpark` rewrite
- Work on already-migrated SMA output (“open sma dashboard”, “fix ewis”, “run stage conversion”, “resume dvp”)
- An existing project config with `conversion_type` set to `snowpark-api`

If the intent is ambiguous, the skill asks which path you want. It never silently defaults to the Snowpark API path.

Scala isn’t supported on this path. If Scala is detected, you’re prompted to switch to Snowpark Connect, which supports Scala.

### How the path is organized

Inside `spark-migration`, the Snowpark API work is handled by bundled sub-skills (loaded from the skill directory, not as separately registered skills). At a high level:

```
spark-migration/
├── SKILL.md                              Parent router
├── configurations/{project}.json         Per-project state
├── config.json                           Global state (including sma_cli_path)
├── snowflake-notebook-migration/         Shared notebook converter
└── snowpark-api/
    ├── migrate-pyspark-to-snowpark-api/  Fresh SMA run (M1–M6)
    ├── validate-pyspark-to-snowpark-api/ Post-conversion pipeline (V0–V8)
    ├── sma-dashboard-generator/
    ├── stage-conversion/
    └── dvp/                              Validation orchestrator and helpers
```

### Intent routing inside the path

After the parent skill delegates to the Snowpark API path:

1. Language is detected (imports, extensions, build files). You’re asked if it’s ambiguous.
2. Python with a migrate intent runs the SMA conversion steps (M1–M6), then hands off to the post-conversion pipeline.
3. Python with an already-migrated intent skips the SMA run and enters the post-conversion pipeline (V0–V8).
4. Scala stops and offers a switch to Snowpark Connect.

Control doesn’t return to the parent until the pipeline completes or you abort.

## Configuration

Every project has a JSON config at `{skill_directory}/configurations/{project_name}.json`, managed by the skill’s config helper (don’t edit these files by hand). The Snowpark API path reads a namespaced slice of that config.

**Shared keys** (owned by the parent skill): `project_name` (required; also passed as `-p` to the SMA CLI), `input_folder` (`-i`), `output_folder` (`-o`), `email` (`-e`), `company` (`-c`), `conversion_type`, `migration_status` (`migrate` or `already_migrated`), and `run_notebook_migration`.

**Snowpark API keys** (persisted and used as gates for later steps):

The Snowpark API path uses these keys:

| Key | Values | Default | Used for |
| --- | --- | --- | --- |
| `sql_flavor` | `SparkSql`, `HiveSql`, `Databricks` | `SparkSql` | SMA CLI `-f` |
| `enable_jupyter_conversion` | `yes` / `no` | `yes` | SMA CLI `-x` when `no` |
| `generate_checkpoints` | `yes` / `no` | `yes` | SMA CLI `-d` when `no` |
| `run_ewi_fixer` | `yes` / `no` | `yes` | Step V4 |
| `run_ewi_fixer.ewi_comments` | `mark` / `remove` | `mark` | V4 comment handling |
| `run_ewi_fixer.ewi_scope` | `only_pending`, `retry_not_resolved`, `all_reset` | `only_pending` | V4 scope |
| `run_stage_conversion` | `yes` / `no` | `yes` | Step V5 |
| `run_stage_conversion.stage_name` | any string | `migration_stage` | V5 stage prefix |
| `run_dvp_orchestrator` | `yes` / `no` | `yes` | Step V6 |

Expand

Show lessSee more

**Global key:** `sma_cli_path` in `config.json`: absolute path to the `sma` binary. It’s auto-detected or you supply it; the skill validates that the path is executable.

Gated steps use the same rules: `no` skips the step; `yes` uses saved values without re-asking; unset asks once, then persists. Answers aren’t re-asked on later runs.

## What to expect, phase by phase

Progress lines are timestamped. Interactive questions appear only for unset config keys.

### Phase 0: Prerequisites (parent)

- **Git**: installed if missing when possible; hard stop if unavailable.
- **SMA CLI** (this path only): the skill looks for `sma` on the PATH and in common install locations. If it isn’t found, you’re asked for the absolute path (typically under the SMA install’s `orchestrator/sma`). The pipeline doesn’t continue without a verified executable.

### Phase 1: Config load and dispatch (parent)

A start time is recorded for the final summary. You’re offered existing project configs or create a new one (project name is required up front). You can review and accept or edit settings, then routing follows `migration_status` and `conversion_type`.

### Phase 2: SMA conversion (M1–M6)

The migrate sub-skill runs these steps:

| Step | Action | Detail |
| --- | --- | --- |
| **M1** | Validate SMA CLI | Loads `sma_cli_path` from global config; re-runs parent detection if missing or invalid |
| **M2** | Collect CLI fields | Reads `sql_flavor`, `enable_jupyter_conversion`, and `generate_checkpoints`; asks only for unset keys |
| **M3** | Run SMA CLI | Always in the background for large workloads. Canonical form: `sma -i {input} -o {output} -e {email} -c {company} -p {project} -y [flags]` |
| **M4** | Monitor | Polls until success (`Conversion was successful.` and exit 0) or failure. Progress comes from SMA step lines in the log |
| **M5** | Resolve output layout | Detects v1, v2, or v3 layout (see below), finds the workload root, and verifies `Output/`, `Reports/`, and `Reports/Issues.csv` |
| **M6** | Hand off | Loads the post-conversion validator with full context |

Expand

Show lessSee more

**Flag derivation:** `enable_jupyter_conversion=no` adds `-x`; a non-default `sql_flavor` adds `-f {flavor}`; `generate_checkpoints=no` adds `-d`. License acceptance (`-y`) is always passed.

**Failure handling:** Error lines or a non-zero exit stop the run and surface the error. If SMA produces no new output for more than about 10 minutes, you’re asked whether to wait or abort. Common fixes: make the binary executable, check for another `sma` process, and confirm the input path is a directory rather than a single notebook.

### Phase 3: Post-conversion pipeline (V0–V8)

The validator runs these steps after conversion (or when you start from already-migrated SMA output):

| Step | What happens | Gate |
| --- | --- | --- |
| **V0** | Resolve output layout (already-migrated only) and validate structure | None |
| **V1** | Initialize git if needed, keep pristine SMA output on `main`, and do all later edits on `sma/migration-process` | Always |
| **V2** | Build the EWI dashboard from `Reports/Issues.csv`, start a local server, and open the browser | Always |
| **V3** | Notebook migration for `.ipynb`, Databricks `.py`, `.scala`, and `.sql` notebooks when present | `run_notebook_migration` |
| **V4** | EWI fixer: resolve issue comments using the dashboard database (`mark` or `remove` comments; scope options for pending, retry, or reset) | `run_ewi_fixer` |
| **V5** | Stage conversion: rewrite embedded file paths to Snowflake stage references | `run_stage_conversion` |
| **V6** | Data validation pipeline (DVP): workspace setup, synthetic data, test registration, test run, and fix loop until tests pass | `run_dvp_orchestrator` |
| **V7** | Re-open the EWI dashboard | Always |
| **V8** | Final summary table | Always |

Expand

Show lessSee more

## SMA output layouts

The SMA CLI version determines the on-disk layout. The workload root is the directory that contains `Output/` and `Reports/`.

Layouts resolve as follows:

| Version | Layout | How it’s resolved |
| --- | --- | --- |
| **v1** | `{output}/Conversion-MM-DD-YYYY-THH-MM-SS/` (optional `.snowma` metadata) | Most recent `Conversion-*` folder, excluding v3-only names; `.snowma` path wins when present |
| **v2** | `{output}/sma-output/` | Use `sma-output/` as the workload root |
| **v3** | `{output}/Conversion_SnowparkAPI/sma-code-process-{timestamp}/` | Always `Conversion_SnowparkAPI` for this path (not `Conversion_SnowparkConnect`); most recent `sma-code-process-*` child |

Expand

Show lessSee more

Detection order: `.snowma` → v1; `sma-output/` → v2; `Conversion_Snowpark*` with `sma-code-process-*` children → v3; legacy `Conversion-*` → v1; otherwise the skill asks you.

Two invariants:

- Work stays inside the resolved folder. The skill doesn’t copy `Output/`, `Reports/`, or `Logs/` upward.
- A missing `Reports/Issues.csv` after resolution means conversion failed silently. The skill stops, points you at `{output}/Logs/`, and asks about re-running.

## Results and artifacts

After a successful run, look for these artifacts:

| Artifact | Location |
| --- | --- |
| Converted Snowpark Python | `{output}/Output/` |
| EWI issues report | `{output}/Reports/Issues.csv` |
| Input file inventory | `{output}/Reports/InputFilesInventory.csv` |
| Dependency inventory | `{output}/Reports/ArtifactDependencyInventory.csv` |
| EWI tracking database | `{output}/sma_storage.sqlite3` |
| Interactive EWI dashboard | `{output}/sma-dashboard/` |
| Validation workspace | `{output}/dvp/` (including pytest suites under `dvp/03-tests`) |
| Git history | `main` (pristine SMA output) and `sma/migration-process` (all fixes) |

Expand

Show lessSee more

## Final summary

The run ends with a fixed-format summary table. Top-level rows cover the SMA CLI conversion, dashboard generator, notebook migration, EWI fixer, stage conversion, DVP orchestrator (with sub-steps through test run and test fixer), and reopening the dashboard. Each row is marked Done, Skipped, or Failed with counts where applicable.

The summary also includes the output location, the two git branches, wall-clock duration, the dashboard reopen command, and next steps such as re-running tests with `pytest {output}/dvp/03-tests/source -v`, remaining EWI fixes, and reviewing code in `Output/`.

The already-migrated variant changes only the first row (no fresh SMA CLI run).

## Entry points

These prompts route into the Snowpark API path:

| You say | Path taken |
| --- | --- |
| “convert with SMA” / “run sma” | Prerequisites and config → M1–M6 → V1–V8 (full pipeline) |
| “I already ran SMA” | Prerequisites and config → V0–V8 (skips the SMA run) |
| “fix ewis” | V0, V1, V2 if needed, V4 (default pending scope), V7, V8 |
| “open sma dashboard” | V0, V1, V2 if missing or stale, V7, V8 |
| “run stage conversion” | V0, V1, V5, V7, V8 |
| “resume dvp” | V0, V1, V6, V7, V8 |
| Scala + SMA | Stop; offer Snowpark Connect |

Expand

Show lessSee more

### Invoking the skill

```
/spark-migration migrate [path] to snowpark-api using the SMA CLI
```

```
/spark-migration I already ran SMA on [path]; continue with the Snowpark API post-conversion pipeline
```

```
/spark-migration open the SMA dashboard for [path]
```

Plain-language prompts that mention SMA or Snowpark API also route here when intent is clear.

## Known stopping points

- SMA CLI can’t be validated → detection runs again; the pipeline doesn’t proceed unverified
- SMA non-zero exit or `Error:` lines → error is shown as-is; retry only if you choose
- SMA silent for more than about 10 minutes → you’re asked to wait or abort (no automatic retry)
- Output layout can’t be resolved, or `Issues.csv` is missing → check `Logs/`; treat as a failed conversion
- Dirty git repo and you choose abort → stop for manual resolution
- Dashboard generator failure → later steps wait until that’s fixed
- Required bundled skill files missing → stop and reinstall the `spark-migration` skill

## Related documentation

- [Migrating with Snowflake CoCo](/migrations/sma-docs/migrating-with-cortex-code/README): spark-migration overview
- [Spark to Snowpark Connect](/migrations/sma-docs/migrating-with-cortex-code/spark-to-snowpark-connect): default conversion path
- [Migrating to Snowpark Connect walkthrough](/migrations/sma-docs/use-cases/migrating-to-snowpark-connect-walkthrough): phase walkthrough for Snowpark Connect
- [Snowpark Migration Accelerator](/migrations/sma-docs/general/getting-started): SMA install and getting started
- [Snowpark Developer Guide](/developer-guide/snowpark/index): Snowpark Python API
