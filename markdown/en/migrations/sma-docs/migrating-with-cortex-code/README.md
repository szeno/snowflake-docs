description:
:   Migrating code with Snowflake CoCo and the Snowpark Migration Accelerator

# Migrating with Snowflake CoCo

Snowflake CoCo is the primary migration tool for any migration from Apache Spark
(or Spark-based source platform) to Snowflake. The primary orchestrator is the
**spark-migration** skill bundled directly with Snowflake CoCo. The
[Snowpark Migration Accelerator (SMA)](/migrations/sma-docs/general/getting-started)
is still available to be used for offline or non-CoCo based migrations.

This page is focused on the **spark-migration** skill, which is the primary
orchestration layer for running a migration from Spark. However, there are
additional subskills orchestrated by this primary skill (such as the
[**snowpark-connect** focused migration sub skill](/migrations/sma-docs/migrating-with-cortex-code/spark-to-snowpark-connect)),
but most of these skills will have documentation pages added as necessary.

## Overview of the spark-migration skill

The `spark-migration` skill migrates PySpark, Spark Scala, and Spark Java
workloads to Snowflake. It is a *thin router* that detects intent and language,
then delegates all execution to one of several bundled sub-skills. The default
and recommended path is to migrate to [**Snowpark Connect**](/developer-guide/snowpark-connect/snowpark-connect-getting-started),
which preserves the PySpark API surface so existing code runs on Snowflake with minimal changes.

However, there are multiple migration paths possible, including migrating to the
[Snowpark API](/developer-guide/snowpark/index) (which rewrites code to the `snowflake.snowpark` API).
To access a different path, you will have to ask for this path when you initiate your migration or are setting up your configuration.
This documentation will focus initially on the recommended path.

### Migration approach

It is important to understand the different phases of a migration before the migration even begins.
There are many steps and sub-steps that the spark-migration skill will walk you through, but at a high level, it’s approaching the migration in this way:

- **Assessment** - Understand what you have
- **Conversion** - Move it to Snowflake
- **Validation** - Test that it worked

Following on from the intiial testing, **optimizing** and ultimately **deploying** the code in a way that makes sense for your new workflow in Snowflake.
Those steps are also accounted for in the migration tooling.

## Using the spark-migration skill

Now that you know what it is, let’s walkthrough how to use it.

### Invoking the skill

There are several invocation paths:

- Direct triggers — any of these phrases in a Cortex Code session will load the skill:
  - **Migration related**: “convert spark”, “migrate pyspark”, “migrate spark”, “migrate to snowpark”
  - **Activity (such as assessment or deployment) related**: “assess pyspark”, “assess spark”, “spark assessment”, “deploy notebook”, “deploy code bundle”, “migrate spark to dbt”
- The skill does NOT need to be invoked directly by name. It’s a bundled skill loaded by Cortex Code’s skill registry when the user’s intent matches those triggers.
  You don’t need to run skill(“spark-migration”) as the the routing will happen automatically.

This skill invokes multiple subskills as it runs. There will be a configuration step that is described later, but
it is important to keep in mind that the initial prompt that you give will direct the
skill on how to approach your migration project.

A few things to keep in mind:

1. **Intent decides the flow**: prompting the skill and requesting a specific activity will direct the skill to move directly to that step:
   - Assessment words (such as “assess”, “analyze”, and/or “readiness”) would direct the skill to enter assessment-only reporting mode.
   - Conversion words (“migrate”, “convert”, “rewrite”) will generate a full end-to-end conversion.
   - Validation words (“validate”, “verify”) will look to validate an already-migrated output.
   - Deployment words (“deploy notebook”, “deploy code bundle”, “migrate spark to dbt”) will skip the conversion entirely, and go straight to the deployment steps.
2. **Language decides the sub-skill**: there are multiple migration paths through this spark-migration skill. The language present in the code will invoke the appropriate subskill such as *Python*, *Scala*, *Java*, or *SQL*. Any mix of those sources will work too.
3. **Conversion path defaults to Snowpark Connect**: unless the user explicitly says “use the SMA”, “Snowpark API”, or “migrate to SQL”. Only then does it route to another migration path.
4. **Direct-intent shortcuts are accepted**: things like “fix ewis”, “open sma dashboard”, or “run stage conversion” will bypass the normal routing and go straight to that part of the flow. Generally, this is not recommended.

All of that to say that the simplest way to engage the skill is just to say something like “migrate my PySpark project to Snowflake”, and it takes over from there.

### Phase 0: Prerequisites

Once you have invoked the skill, it will first classify your intent. (This was described above.)

It then detects the source language from file extensions, imports, and build files:

| Signal | Language |
| --- | --- |
| `.py`, `from pyspark`, `import pyspark` | Python (PySpark) |
| `.scala`, `build.sbt`, `import org.apache.spark` | Scala |
| `.java`, `pom.xml`, `build.gradle` | Java |

Expand

Show lessSee more

It will also assess if some components are available wherever you are running CoCo,
but note that you can tell Snowflake CoCo to “use default values for all fields” if you do not want to save a specific configuration.

Before any phase runs, the skill checks:

1. **Git**: must be installed and on the PATH. If missing, the skill installs it
   automatically for the detected platform (Homebrew on macOS, apt/yum on Linux,
   winget on Windows), then verifies it.
2. [**SMA CLI**](need a link here): only checked when the Snowpark API path is explicitly selected.
   If not on the PATH, the skill searches a set of standard install locations
   and asks the user if still not found.
3. **`uv` package manager**: required for all Python scripts in the skill. If
   missing, the skill installs it automatically (macOS/Linux:
   `curl -LsSf https://astral.sh/uv/install.sh | sh`; Windows PowerShell:
   `irm https://astral.sh/uv/install.ps1 | iex`).

### Phase 1: Initial Configuration

After the prerequisites pass, this skill creates a configuration file
(or will check for saved project configurations from previous runs automatically)
to save settings and project characteristics that you may want to keep from project
to project.

Typically, the skill will load or create a **project configuration
file** stored as `{skill_directory}/configurations/{project_name}.json`.

If existing configurations are found, you will be presented with a numbered list
and asked whether to use an existing one or create new.

**If creating new**, you provide five fields:

| Field | Required |
| --- | --- |
| Project Name | Yes: used as the config filename |
| Source Code Path | Recommended (can defer) |
| Output Folder | Recommended (can defer) |
| Customer Email | Optional |
| Customer Company | Optional |

Expand

Show lessSee more

The configuration summary displays all 18 settings grouped into three sections:
Project, Conversion, and Post-Conversion. You can edit any setting before the
migration starts.

Key conversion settings:

- **Conversion Type**: `snowpark-connect` (default) or `snowpark-api`
- **Migration Status**: `migrate` (fresh conversion) or `already_migrated` (you
  already have output and want to continue)

Note that for all of these options, you can choose to accept default values and do
not have to specify each of these individually.

#### Note on migration phases

The `snowpark-connect` migration path executes as a sequence of numbered phases.
Progress is tracked in `{CONVERSION}/migration_state.json`: if the session is
interrupted at any point, the skill resumes from where it left off by reading
that file on startup.

All phases produce git checkpoints inside the conversion folder so every state
of the workload is recoverable.

## Automated workflow

In the first two phases, the skill was identifying what you have and getting some
more information. The next phases should be more automated.

### Phase 2: Setup and workspace creation

The following set of steps will happen once the configuration has been updated.

1. The skill creates a timestamped conversion folder:
   `{output_root}/Conversion-SCOS-{TIMESTAMP}/` with `Output/`, `Reports/`, and
   `Logs/` subdirectories.
2. The source directory is copied into `Output/` intact.
3. Any `.dbc` Databricks archive files are unpacked.
4. The skill builds a **file manifest**: a sorted list of all `.py` files and
   notebook files (`.ipynb`, Databricks native `.python`/`.scala`/`.sql`,
   Databricks exported `.py`) in the workload.
5. A **notebook index** is built in one pass, recording each notebook’s format,
   language, and per-cell language counts.
6. Dispatch mode is set: single-file workloads run inline; multi-file workloads
   use a parallel worker pool.
7. Git is initialized and the original source is tagged `phase-0-source`. This
   tag is used later to render the assessment report against the unmodified
   code.
8. `migration_state.json` is written with the full manifest, paths, and
   configuration.

**You can expect** the folllowing after the setup is complete:

- a new timestamped folder at your specified output location
- a git-initialized workspace
- a confirmation of how many files were found.

#### Phase 2.5: Deterministic pre-processing

Before any analysis or LLM work touches the code, a set of **LibCST recipes**
runs over every Python file in the manifest. These recipes handle patterns that
LLMs historically get wrong. An example would be silently dropping
`SparkSession.builder.config("spark.sql.session.timeZone", "UTC")` when
collapsing a builder chain, which shifts every timestamp in the migrated
workload by hours.

A **pre-flight syntax check** runs first: every code unit is compiled with
`compile()` before LibCST parses it. Pre-existing syntax errors (for example,
stray indentation in a notebook cell) are auto-fixed where a whitespace-only
correction is safe, and recorded in `migration_state.json["preexisting_syntax"]`
otherwise. This prevents LibCST from silently skipping broken files and lets
downstream phases treat pre-existing errors as warnings rather than migration
failures.

**You can expect** the folllowing when this phase is done:

- `# WARN:` or `# TODO:` or `# EWI:` annotations in files where mechanical patterns were detected
- a summary of files processed and modified
- `migration_state.json` updated with a `recipe_edits` block recording every mechanical change with its source line

#### Phase 2.6: Standalone SQL rewrite

Standalone `.sql` files are rewritten deterministically using **sqlglot** before
the analyzer sees them. Patterns with safe, semantics-preserving fixes are
applied automatically such as `EXPLAIN` drops, `GROUPING SETS` folding, and
`CACHE`/`UNCACHE` removal. Patterns that require judgment, such as window
functions missing an `ORDER BY` or multi-column `NOT IN`, are annotated with
`-- TODO -` statements for the LLM fixer in a subsequent phase to handle. An audit
block is prepended to each `.sql` file.

Note that this phase is skipped for workloads that do not have any SQL.

**You can expect** the following when this phase is done:

- modified `.sql` files with automatic rewrites applied
- judgment-deferred (to the LLM fixer) cases will be annotated directly in the file

### Phase 3: Compatibility analysis

At this point, all pre-processing should be complete, and the analysis phase begins
in earnest. The analyzer script (`analyze_pyspark.py`) runs over every file in the manifest.
It uses a deterministic knowledge base (`kb_rules.json`) of known
compatibility divergences and a `safe_apis.json` allowlist (reconciled against
the KB at load time, so documented divergences are never silently skipped) to conduct
the analysis.

The analyzer **does not call any LLM**. It classifies every code block into one
of three outcome categories:

- **Decidable**: this trigger definitively identifies a real incompatibility, and
  writes this directly into the `analysis.json` file with a risk score.
- **`needs_classification`**: this references an API not covered by any
  detection source. Listed for the subsequent classification phase.
- **`needs_adjudication`**: this trigger is token-based and can be false-positive-prone.
  These compatibility issues are deferred to the subsequent adjudicator for
  human-level judgment.

A **supplementary blind-spot scan** runs after the script, looking for patterns
the script may miss such as UDF and `pandas_udf` decorators, `applyInPandas`,
`checkpoint`, JVM `._jdf`/`._jvm` access, `sparkContext`, Hadoop/HDFS paths,
Delta operations, and ML pipeline patterns.

For multi-language Databricks notebooks, `analyze_scala.py` also runs and its
results are merged into the same `analysis.json`, with each row tagged by
language.

A deterministic gate validates `analysis.json` before the phase is recorded as
passed.

**What you can expect:** a large amount of assessment information generated in
the `analysis.json` file at the conversion root directory. This will contain a
row per compatibility issue found with risk scores, EWI codes, source line
numbers, and KB rule references.

#### Phase 3.1a: Unknown API classification

If any `needs_classification` rows exist in `analysis.json` (APIs not covered by
the KB or safe-API list), the skill classifies each unknown module name from its
own knowledge, recognizing whether it belongs to the Spark/PySpark/Delta/Azure
Synapse ecosystem or is unrelated to Spark. Spark-related modules are promoted
to `needs_adjudication` for the next phase. Non-Spark modules are marked
`resolution:safe` and skipped by the fixer.

**What you can expect:** previously uncategorized vendor SDK calls (for example, AWS
Glue’s `glueContext` and Azure Synapse’s `mssparkutils`) will be surfaced in the
`analysis.json` file and queued for adjudication.

#### Phase 3.1b: Adjudication

A pool of adjudicator agents review every `needs_adjudication` row in
`analysis.json`. The pool is sized by splitting the work into bounded
chunks (capped by both file count and row count per
chunk to prevent a single overloaded agent from over-confirming).

For each row, the adjudicator reads the **full source file** for context,
examines the matched code and the candidate KB rules that fired, and issues one
of the below verdicts:

- **`confirm`**: the code will genuinely fail or diverge with Snowpark Connect.
  The fixer will implement a fix in a subsequent phase.
- **`dismiss`**: the token match was a false positive in this context.

Each adjudicator writes its verdicts to a private sidecar file
(`Adjudication/chunk_{N}.json`). The coordinator merges all sidecars into the
`analysis.json` file once the full pool completes, ensuring no concurrent write
conflicts.

It is importnat to note that **Calibration rules** will prevent over-confirming
bu the adjudicator step. Ordinary DataFrame transforms
(`select`, `filter`, `groupBy`, `join`, window functions) must be dismissed
unless there is a specific documented divergence. Only hard-floor APIs
(`dbutils`, DBFS/Delta, GraphFrames, distributed `pyspark.ml`) are always
confirmed regardless of context.

**What you can expect:** the `analysis.json` file is updated so every
formerly-deferred row is now either confirmed (risk score, recommended fix)
or dismissed. A summary line reports confirmed and dismissed counts.

#### Phase 3.2: Assessment report

The reporter script renders two artifacts from `analysis.json` and the
**pre-analysis source** (materialized from the `phase-0-source` git tag so the
report reflects the original unmodified code):

1. **`Reports/MigrationReadinessReport.html`**: the primary assessment report generated.
   Thie HTML report shows per-file migration effort categories (Ready / Light Refactor / Active
   Refactor), a data dependency graph, the auto-resolved changes, and
   all confirmed compatibility findings with their source context.
2. **`Reports/AssessmentIR.json`**: a machine-readable intermediate
   representation with the full compatibility analysis, data lineage graph,
   unresolved edges, and file-level readiness classifications.

The report uses the following **effort categories** to reflect the status of each file:

- **Ready**: There are not compatibilty issues and this file is expected to run without
  any fixing by an LLM.
- **Light Refactor**: There are minor incompatibilities with low risk scores. The LLM
  fixer is expected to resolve these issues.
- **Active Refactor**: There are incompabilities that may not be able to be resolved
  by the LLM fixer. This could include issues that require user input such as repointing
  file paths to a new location.

Note that these are not numeric scores. A deterministic gate confirms both files
exist and have no unsubstituted template placeholders.

**What you can expect:** at this point you have a complete readiness report
before any code changes have been made. If you only wanted an
assessment and not a migration, you can stop here.

#### Phase 3.3 Data edge enrichment (optional)

Note that if the static AST scanner left unresolved data
dependency edges or dynamic imports, the skill offers an **LLM data-edge
enrichment** pass. This reads the entire workload, traces dynamic call paths,
and resolves unknowns (boto3 calls, SQL template files, `dbutils.taskValues`
handoffs). It requires no Snowflake connection, caches its results in the
`AssessmentIR.json` file, and typically takes a few minutes for large workloads. The
user is asked before it runs.

The results of this will be added to the `MigrationReadinessReport.html` file.

#### Note on EWIs

**EWI**s will be identified in the assessment phase. EWI stands for Errors,
Warnings, and Issues:

- **Conversion errors** are incompatibilies in the code that the agent recognize. Most
  errors should be resolved by the LLM fixer, unless they are errors that will require
  human input.
- **Warnings** are notes written into the codebase to alert the user that there is something
  that either changed or there is a potential behavior change in Snowflake. Warnings
  do not require any resolution, but they should be notes during testing.
- **Issues** is the final category referring to any potential issue that doesn’t directly
  fit into the above categories. Most EWIs will fall into the first two categories.

EWIs are placed in the code to inform the user about potential issues in the output code.
Most of them will be automatically resolved in subsequent steps.

### Phase 4: Apply fixes (parallel fixer pool)

This is the core code-conversion phase. The orchestrator splits the manifest into
**token-balanced chunks** (capped at 80,000 tokens per chunk) and dispatches up
to 6 **fixer sub-agents in parallel per wave**. Each fixer sub-agent receives
its assigned chunk of files, the confirmed findings from `analysis.json`,
and a full set of rules to follow for reference.

The fixer works through each file, applying the appropriate fix for each
confirmed finding:

- **EWI-coded inline annotations** (`# EWI: [SPRKCNTPY...] {message}`) are
  embedded at each changed line.
- For fixable constructs, the code is rewritten in-place. Examples include HOF lambda
  capture to flattened equivalent, `to_protobuf` to Python UDF, `spark.catalog`
  to lowercased comparison, but there are many fixes that could exist.
- For unfixable constructs: `# EWI: TODO` annotations are placed, and the
  finding is recorded as `needs_human_action`.

The coordinator is the **sole writer** of `migration_state.json`. Fixers return
a `CHUNK_RESULT` line with their per-chunk summary, and the coordinator updates the
state after each wave completes. This prevents race conditions on the shared
state file during parallel execution.

After all waves complete, a deterministic **fixer gate** runs. It compiles every
`.py` file with `py_compile`, validates every notebook as a well-formed JSON,
confirms no migrated file is empty or missing, and checks
that every high-risk finding (`final_risk >= 0.7`) has a fix or `# EWI:`
marker.

Note that **RDD chains** are handled holistically. The recipes deliberately skip
`sc.*` entry points that flow into RDD-only operations so the fixer can convert
the entire chain as a unit rather than partially migrating it.

**What you can expect:** converted Python files in `Output/` with `# EWI:`
inline annotations at every changed or flagged line, and a gate confirmation
that all files compile.

#### Phase 4a: Coverage verification gate

Confirms 100% of the manifest files are present in `Output/`. If any file is
missing, the migration stops and updates the user. This is a fast, deterministic check
that runs as part of the orchestrator output.

#### Phase 4b: Compilation verification gate

Re-runs the fixer gate with `--revert-failing`. Any `.py` file that still does
not compile is **reverted** to its baseline. A working
original is always better than broken half-migrated syntax. Reverted files are
reported as `fix_reverted` findings in the outpur reporting. Files that cannot
be reverted are blocking failures. Up to 3 targeted re-fix iterations are allowed
before escalating to the user.

**What you can expect:** a guarantee that every file in `Output/` either
compiles or has been explicitly reverted and reported.

#### Phase 4c: Evidence-based verification gate

This phase cross-checks the coordinator’s self-reported progress in
`migration_state.json` against actual on-disk evidence. A file is classified as:

- **`migrated`**: a genuine `# EWI:` fixer marker is present, or the file is
  recorded done with Spark surface.
- **`partial`**: there are Spark surface and confirmed findings, but no genuine fixer
  edit and the file is not recorded as done.
- **`trivial`**: no Spark elements.
- **`not_attempted`**: missing from `Output/`.

**`partial` files** get a `SPRKCNTPY0099` EWI, and are recorded in the `analysis.json`
file. Ther are also added to `needs_human_action`. This gate is the **sole writer** of
partial migration findings and runs exactly once after all fixer retries are complete.

### Phase 5: Imports and headers

A deterministic script targeting import statements runs over every file in the
manifest. It will:

1. Replace `SparkSession.builder...getOrCreate()` and the `DatabricksSession`
   variant with `snowpark_connect.init_spark_session()`.
2. Insert `from snowflake import snowpark_connect`.
3. Comment out unsupported `databricks` and `delta` imports. Standard `pyspark`
   imports are kept.
4. Prepend a **Snowpark Connect migration header docstring** to each file, built from the
   `# EWI:` annotations already embedded by the fixer, so the header’s
   `Changes Overview` and `Known Limitations` sections are grounded in the
   actual per-file findings.

The transforms are the same for any execution of the agent. A gate
verifies every file has the header, has no live `SparkSession.builder` statements
remaining, has no unsupported imports, and references `snowpark_connect`.

**What you can expect:** every output file stamped with its migration header, and
`SparkSession` initializations replaced throughout.

### Phase 6: Generate reports

The report generator produces the three primary CSV artifacts consumed by the
reporting dashboard:

1. **`Reports/Issues.csv`**: every compatibility issue with EWI codes
   (`SPRKCNTPY*`), severity, source file, and line number. EWI codes are read
   from the `# EWI: [SPRKCNTPY...]` inline annotations in the migrated files,
   so the report and the code are always in sync.
2. **`Reports/InputFilesInventory.csv`**: one row per source file with path,
   size, and migration status.
3. **`Reports/ArtifactDependencyInventory.csv`**: all import dependencies found
   in the workload.

A gate confirms all three files exist and have data rows.

Note: `MigrationReadinessReport.html` and `AssessmentIR.json` are **not**
generated here. They were already produced in an earlier phase.

**What you can expect:** the full CSV report set.

#### Phase 6a: Post-run state validation

A check is done to ensure that all required phase keys are
present and non-empty in `migration_state.json`. Required keys are:

- `0_5_preprocess`
- `0_6_sql_rewrite`
- `1_analysis`
- `1a_assessment_report`
- `2_fixes`
- `2a_coverage`
- `2b_compilation`
- `2c_verification`
- `3_imports`
- `4_reports`

A skipped phase must have a `skip_reason`. A missing key or a skip
with no reason is a hard failure. This is the canonical, machine-checkable
success criterion for the migration.

#### Phase 6b: Migration feedback file (non-fatal)

At this point, a structured summary of gaps in the migration is generated:
`{CONVERSION}/Feedback/migrate_gaps.md`. This file can be shared with Snowflake
in the interest of improving the skills. The simplest way to submit this would be
to share with [sma-support@snowflake.com](mailto:sma-support@snowflake.com).

Note that this is not a checked step. If it fails, the migration
result is unaffected.

### Phase 7: Validation (optional)

After the migration completes, you are asked if you want to run the **validation
sub-skill**. The validation skill
executes the migrated workload end-to-end with synthetic data against a live
Snowflake connection and compares results to the original Spark output. If
validation completes, a `validate_feedback.md` file is generated in
`{CONVERSION}/Feedback/`.

More on this validation step is coming soon.

### Phase 8: Secondary notebook conversion

If the migration was invoked directly (not as part of the broader
`spark-migration` orchestrator), you are offered the option to only run the
`snowflake-notebook-migration` sub-skill on the migrated output. This converts
Databricks-format notebooks to Snowflake Workspace `.ipynb` format.

Note that this phase is silently skipped when invoked from the parent
orchestrator, which handles notebook conversion as its own step.

## Final output layout

Copy code

```
{output_root}/
  Conversion-SCOS-{timestamp}/
    Output/                                ← Converted files (same structure as source)
    Reports/
      Issues.csv                           ← EWI issues (SPRKCNTPY* codes)
      InputFilesInventory.csv              ← Source file inventory
      ArtifactDependencyInventory.csv      ← Import dependencies
      MigrationReadinessReport.html        ← Stakeholder readiness report (pre-migration view)
      AssessmentIR.json                    ← Machine-readable assessment IR
    Logs/                                  ← Migration log
    Adjudication/                          ← Adjudicator sidecar verdicts
    Feedback/
      migrate_gaps.md                      ← Gap summary for triage
      validate_feedback.md                 ← Validation result (if run)
    migration_state.json                   ← Phase gate tracking and resume state
    analysis.json                          ← Fully adjudicated compatibility analysis
```

## Deployment paths (post-migration)

After the migration completes, the skill can deploy the output directly to Snowflake
via three sub-skills:

### Deploy as a Notebook

Uploads the migrated `.ipynb` and supporting files to a Snowflake stage and
creates a `NOTEBOOK` object with a live version. Returns a Snowsight deeplink.
Opt-in headless validation is available via `EXECUTE NOTEBOOK`.

### Deploy as a Code Bundle

Generates a `code_bundle.yml` spec, uploads the `.py` project to a stage, and
creates a `CODE BUNDLE` object. Supports both warehouse-runtime and compute pool
targets. Opt-in validation via `EXECUTE CODE BUNDLE`.

### Migrate to dbt

Generates a full dbt project structure: `dbt_project.yml`, `profiles.yml`, model
files (`.py` wrappers or `.sql`), source/model YAMLs, singular parity
tests, and divergence scaffolds. Deploys as a `DBT PROJECT` object via
`snow dbt deploy`. Opt-in `dbt build` and parity testing on explicit request.

## Resumption

The skill probes the output root on every startup for a `Conversion-*`
folder with a completed assessment
(`migration_state.json :: phases_completed.1a_assessment_report.status == "passed"`).
If found, it offers to continue rather than restarting from
Phase 0. Mid-migration context loss (for example, a long-running session that
gets summarized) is recovered the same way. All coordinator state is restored
from `migration_state.json`.

## Additional questions

For any questions or concerns on the `spark-migration` skill or migrating with Cortex Code,
reach out to [sma-support@snowflake.com](mailto:sma-support@snowflake.com).
