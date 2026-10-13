description:
:   Step-by-step walkthrough for migrating a PySpark codebase to Snowpark Connect using the Snowflake CoCo spark-migration skill

# Snowpark Migration Accelerator: Migrating to Snowpark Connect Walkthrough

This walkthrough explains how to migrate a PySpark codebase to [Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-getting-started) using the [**spark-migration** skill](/migrations/sma-docs/migrating-with-cortex-code/README) in Snowflake CoCo. It follows the skill’s migration phases end to end, including what to expect at each gate and what to do after conversion.

**Sample workload used in this guide:** the open-source `pyspark-examples` collection (about 97 Python files). Timings and counts in later sections are from that sample so you can scale expectations to your own project size.

For Snowpark Connect product documentation, see [Snowpark Connect for Apache Spark](/developer-guide/snowpark-connect/snowpark-connect-apache-spark). For the Snowpark API conversion path (SMA CLI), see the [conversion walkthrough](/migrations/sma-docs/use-cases/conversion-walkthrough).

Note

Some folder names, comment prefixes, and script names in this guide still include the string `SCOS` (for example, `Conversion-SCOS-*`, `# SCOS: TODO`, and `generate_scos_reports.py`). Those are literal outputs from the migration tooling. In prose, this guide uses **Snowpark Connect**.

## Introduction

### What is Snowpark Connect?

Snowpark Connect for Spark is a Snowflake runtime that lets you run PySpark code on Snowflake’s engine. It preserves the PySpark API surface (`withColumn`, `groupBy`, `spark.createDataFrame`, `pyspark.sql.functions`) so you do not have to rewrite your code to the Snowpark Python snake\_case API. The migration replaces the SparkSession connection layer (`sc`, `SparkContext`, Databricks utilities) with Snowpark Connect equivalents while keeping your actual data transformation logic intact.

### Two conversion paths

The `spark-migration` skill has two paths. This guide covers the default path leveraging Snowpark Connect:

| Path | Description | When to use |
| --- | --- | --- |
| **Snowpark Connect** | Preserves the PySpark API | Default. Recommended for the vast majority of workloads. |
| **Snowpark API (SMA)** | Rewrites PySpark to snake\_case Snowpark Python (`.with_column`, `.group_by`) | Only if you explicitly want native Snowpark Python syntax. |

Expand

Show lessSee more

Unless you say otherwise, the skill uses the Snowpark Connect path.

### The orchestration model

The skill runs as a **coordinator**. Context-heavy work (analysis, adjudication, code fixing, report rendering) is delegated to parallel sub-agents so each one operates on a bounded slice of the workload. Mechanical phases (pre-processing, SQL rewrite, imports, validation) run as deterministic scripts directly. Every phase is validated by a quality gate before the coordinator advances.

You interact only with the coordinator. Sub-agents are invisible to you unless something goes wrong.

## Prerequisites

| Requirement | Why needed | How to install |
| --- | --- | --- |
| **git** | Conversion folder baseline; compilation gate uses it to revert bad files | `brew install git` (macOS), `apt-get install git` (Linux) |
| **uv** | Runs the skill’s Python scripts in a reproducible venv | `curl -LsSf https://astral.sh/uv/install.sh | sh` |
| **Active Snowflake connection** | Readiness report’s Ask chat; uploading output to stages/Workspace | `cortex connections list` |
| **Source code** | Local directory of `.py` files and/or Databricks notebooks | (not applicable) |
| **spark-migration skill loaded** | Auto-loads on migration keywords, or explicit request | Easiest: type `/spark-migration` then your request. Or ask: *“use the spark-migration skill to migrate [dir] to snowpark-connect”* |

Expand

Show lessSee more

## Starting the migration

The easiest way to start is to invoke the skill directly with `/spark-migration`, then describe what you want. You can also use a plain-language prompt; the skill auto-loads on migration keywords.

**Common prompts:**

```
/spark-migration migrate the files in [path] to snowpark-connect
```

```
/spark-migration assess compatibility of [path] with snowpark-connect
```

```
/spark-migration migrate [path] to snowpark-connect, skip synthetic data validation
```

```
/spark-migration migrate [path] to snowpark-connect, run everything including synthetic data validation without asking questions
```

Other natural-language variants work too, for example:

```
Migrate the files in [path] to snowpark-connect
```

```
Show me how compatible this directory is with snowpark-connect: [path]
```

The skill will ask for anything it needs unless you already answered those questions in the prompt. **Minimum required inputs:**

1. **Source code path**: the directory or file to migrate
2. **Project name**: used as the config filename and in reports
3. **Output folder**: where converted files and reports go *(defaults to a folder named like `your_source_scos` if omitted)*

**Optional but useful to provide upfront:**

- Customer email and company (appears in the dashboard CSV reports)

### Configuration is saved

Your answers are saved to:

```
~/.local/share/cortex/.../spark-migration/configurations/<project>.json
```

On subsequent runs the skill offers to load this config, so you can resume or re-run without re-entering everything.

## Phase 0: Setup and conversion folder

### What happens

The skill creates a timestamped conversion folder inside your output directory:

```
<output>/Conversion-SCOS-<MM-DD-YYYY>T<HH-MM-SS>/
├── Output/           # copy of all your source files (originals are never modified)
├── Reports/          # CSVs and readiness report land here
├── Logs/             # execution logs
└── migration_state.json  # single source of truth for phase progress
```

Your source files are copied into `Output/` and git-initialized there. The unmodified copy is tagged `phase-0-source`. This tag is important: the migration readiness report later materializes it to describe your **original** code, not the already-rewritten version.

### What to expect

The skill prints a summary of files found and sets `coordinator_mode`:

| Value | Meaning |
| --- | --- |
| `false` | Single file: phases run inline, no sub-agents |
| `true` | Multiple files: phases fan out to parallel workers |

Expand

Show lessSee more

For a workload of ~100 files, expect `coordinator_mode = true`.

### Common issue

If `git` is not found, the skill tries to install it. If that fails it stops. You must have git before proceeding. The Phase 2b compilation gate uses `git checkout` to revert files that fail after fixing.

## Phase 0.5: Deterministic pre-processing

### What happens

Before any LLM sees your code, registered LibCST recipes run over every Python file. These are byte-exact mechanical rewrites for patterns that are known to be safe to fix without judgment. The goal is to take mechanical work away from the LLM.

The driver is `preprocess_recipes.py`. It first runs a pre-flight compile check. Pre-existing syntax errors are recorded so the fixer later knows not to blame itself if a file fails to compile.

### Recipes that commonly fire

| Recipe | What it does |
| --- | --- |
| `spark_builder_drop_master_init_session_rewrite` | Removes `SparkSession.builder.master(...).getOrCreate()` and replaces with a stub. Phase 3 later replaces the stub with `snowpark_connect.init_spark_session()`. Fires on almost every file. |
| `sc_parallelize_to_createdataframe_rewrite` | Converts `sc.parallelize([...])` → `spark.createDataFrame([...])` where unambiguous. |
| `sparkcontext_property_fallback_rewrite` | Wraps `.sparkContext` property accesses in a `getattr()` fallback so diagnostic code continues running. |
| `tempview_multiuse_cache_rewrite` | Inserts `.cache()` before `createOrReplaceTempView()` when the view is queried multiple times. |
| `dataframe_partition_noop_strip_rewrite` | Removes `.repartition()` and `.coalesce()` calls : Snowflake manages partitioning, these are no-ops. |
| `rdd_exclusive_method_todo_annotate` | Annotates RDD methods with no Snowpark Connect equivalent with migration TODO markers. |
| `spark_io_detect` | Marks file I/O calls noting they must be repointed to a Snowflake stage. |

Expand

Show lessSee more

### What to expect

```
Files processed: 97
Files modified:  96
Total edits:     233
```

### Gate

Exit 0 with `Files processed >= 1` = PASS. If it fails, find and fix the un-parseable Python file it reports before retrying. The script is idempotent; re-running on already-processed files is safe.

## Phase 0.6: Standalone SQL rewrite

### What happens

Scans for standalone `.sql` files and applies deterministic rewrites for Snowpark Connect SQL gaps (EXPLAIN drops, GROUPING SETS folding, CACHE/UNCACHE removal). Judgment-heavy gaps are annotated with SQL migration TODO markers rather than auto-rewritten.

### What to expect

Most PySpark workloads have few or no standalone `.sql` files. If yours has none, the phase records `files_processed: 0` and passes immediately. This is expected. This is not a skip.

## Phase 1: Compatibility analysis

### What happens

The skill spawns an analyzer sub-agent (for multi-file workloads) to run `analyze_pyspark.py` over the entire `Output/` directory. This produces `analysis.json`, the artifact that drives every subsequent phase.

The analyzer uses the **offline “trigger” backend** by default: a curated knowledge base of known Snowpark Connect compatibility gaps. A rule fires only when its exact anchor (API name, method, SQL construct) appears in the customer code. This is fast, deterministic, and requires no network connection.

**The analyzer makes NO LLM calls.** Every non-decidable trigger match is emitted as a `needs_adjudication` row for Phase 1.1b to resolve.

Phase 0.5 recipe information is passed as grounding, so issues are tiered by `kind`:

| Kind | Meaning |
| --- | --- |
| `recipe_validated` | Recipe already fixed it; fixer will skip |
| `recipe_incomplete` | Recipe annotated but could not auto-fix; fixer completes |
| `recipe_adjacent` | Near a recipe fix; fixer gets context |
| `standard` | No recipe involvement |

Expand

Show lessSee more

A **supplementary blind-spot scan** runs after the script, checking for patterns the static analyzer may miss: `@udf`/`@pandas_udf` decorators, `applyInPandas`, `mapInPandas`, `checkpoint()`, map column subscript, and RDD aggregate/accumulator operations.

### What to expect

For a 97-file PySpark workload: ~700-900 entries in `analysis.json`, most of them `needs_adjudication`. The analyzer sub-agent takes 3-5 minutes.

### Gate

The gate runs its own blind-spot scan. A FAIL here usually means the supplementary scan missed something. The coordinator reads the gate’s `gaps` array, adds the missing entries, and re-runs automatically.

## Phase 1.1a: Unknown API classification

### What happens

The analyzer sometimes cannot determine whether an imported module is part of the Spark ecosystem. This phase lists those modules and asks you to classify each.

### What to expect

```
["pandas", "pyspark", "snowflake"]
```

Classify each as `spark_related` or `not_spark_related`:

| `spark_related` | `not_spark_related` |
| --- | --- |
| PySpark, Delta, Koalas, GraphFrames | Standard library, Snowflake connector |
| `pyspark.pandas`, Databricks SDK | boto3, requests, scikit-learn |
| `pandas` (when used with `pandas_udf` / `applyInPandas`) | Any non-Spark third-party lib |

Expand

Show lessSee more

Modules classified as `spark_related` move into the adjudication pool. `not_spark_related` rows are dismissed safely. If the list is empty this step is skipped.

## Phase 1.1b: Adjudication of deferred findings

### Why this phase exists

The analyzer’s trigger rules fire on **token presence**. When it sees `.save()` it does not know if that is `DataFrameWriter.save()` (supported) or a machine learning model save (not supported). Rather than guess, it emits a `needs_adjudication` row for a human-equivalent agent that can read the full file for context.

Without adjudication, the fixer would receive hundreds of noisy findings and produce spurious TODO comments or wrong fixes on already-correct code.

### What adjudicators do

- Read the **whole file** (not just the flagged line)
- Check context: receiver type, call chain, surrounding logic
- Decide: **dismiss** (false positive) or **confirm** (real incompatibility)
- Write only their own sidecar file (`Adjudication/chunk_N.json`); never touch `analysis.json` directly
- The coordinator merges all sidecars once after all workers finish

### Scale

For a ~100-file workload, expect:

| Metric | Typical value |
| --- | --- |
| `needs_adjudication` rows | 500-800 |
| Chunks | 12-16 across 3-4 waves |
| Workers per wave | 4 (concurrent) |
| Total time | 20-35 minutes |
| Dismissal rate | 85-95% |

Expand

Show lessSee more

**The high dismissal rate is normal.** The trigger rules cast a wide net; adjudication is where precision is restored.

### Calibration rules

**Always dismiss** unless code will concretely fail or behave differently on Snowpark Connect:

- Standard DataFrame transforms (`select`, `filter`, `groupBy`, `join`, `withColumn`, `orderBy`, `distinct`, `union`, window functions, `pyspark.sql.functions`) are **supported**. Token presence alone is not a reason to confirm.

**Always confirm** (mark as high risk):

- `dbutils.*` calls
- Delta Lake operations (`DeltaTable`, `.format("delta")`, `MERGE`, `OPTIMIZE`)
- DBFS/mount paths
- Unsupported libraries (GraphFrames, `pyspark.pandas`/Koalas, Spark-NLP)

### Merge result

```
submitted=708 applied=708 confirmed=31 dismissed=677
```

If `applied < submitted`, some verdicts were dropped. This is a hard error. The coordinator re-dispatches the affected chunk. Do not proceed with a partial merge.

## Phase 1.2: Migration readiness report

### What happens

The skill renders two artifacts from `analysis.json` and the **original** (pre-Phase-0.5) source code, materialized from the `phase-0-source` git tag:

| Artifact | Description |
| --- | --- |
| `Reports/MigrationReadinessReport.html` | Stakeholder-facing HTML report. Self-contained; opens in any browser. |
| `Reports/AssessmentIR.json` | Structured IR for downstream tooling. |

Expand

Show lessSee more

The HTML report has five tabs:

- Executive summary and migration effort category
- Per-file readiness status
- Issue breakdown by EWI code
- Data dependency graph
- Phase 0.5 auto-resolved panel

**Open this report as soon as Phase 1.2 finishes.** It tells you what you are dealing with before any code changes start. It is safe to share with stakeholders.

### Migration effort categories

The report uses three categories (not a numeric score):

| Category | Meaning |
| --- | --- |
| **Ready** | File uses only supported Snowpark Connect APIs |
| **Light Refactor** | Minor adjustments needed |
| **Active Refactor** | Significant rework required (typically RDD-heavy files) |

Expand

Show lessSee more

A numeric 0-100 “readiness score” used to exist but was removed because it was driven by LLM confidence and was non-deterministic.

### Phase 1.3 (optional): Data-edge enrichment

After the seed render, the skill checks if the static data dependency graph has unresolved edges. If `N + M > 0`, it stops and asks:

Copy code

```
"The data dependency graph has N unresolved read/write edge(s) and M unresolved
dynamic imports. Run LLM data-edge enrichment? (Y/n)"
```

- **Yes**: reads every source file, traces dynamic paths. Takes ~5 minutes, scales with workload size.
- **No**: report ships with the static-only DAG (clearly labeled). You can run enrichment later.

For most workloads, skipping is fine unless accurate data lineage in the report is important to your stakeholders.

## Phase 2: Apply code fixes

### What happens

1. `orchestrate_phases.py` computes token-balanced chunks (default: 80,000 tokens/chunk, 4-6 parallel workers)
2. All of the wave’s fixer sub-agents are dispatched **concurrently in a single turn**
3. The coordinator waits for the whole wave to return
4. Updates `migration_state.json` **once** as the single writer; fixers return `CHUNK_RESULT` lines, they never touch shared state
5. Git checkpoints after each wave
6. Repeats if `pending_files` is non-empty

### What fixers do

For each file, fixers:

- Read the file and its `analysis.json` issues
- Skip `recipe_validated` issues (Phase 0.5 already fixed them)
- Skip `resolution="safe"` issues (adjudicator dismissed them)
- For every remaining confirmed issue: apply the fix or add a migration TODO comment (see annotation format below)

**Critical rule:** Fixers **never** re-decide whether an issue is real. Adjudication already happened. Fixers implement, not adjudicate.

### Annotation format

Copy code

```
# Applied fix:
# SCOS: [SPRKCNTPY####-Fixed] <explanation>

# Manual action required:
# SCOS: TODO - [SPRKCNTPY####-Error] <specific API> | <why unsupported> | <Snowflake alternative>

# I/O repoint needed:
# SCOS: TODO - [SPRKCNTPY####-IO] <path> | must use Snowflake stage | PUT file to @stage then read from @stage/...
```

### What can go wrong

**1. API 400 / Context Overrun**

A chunk’s sub-agent dies if its files collectively exceed the model’s context limit. The coordinator automatically detects the missing chunk, re-runs `orchestrate_phases.py` with smaller chunks from the remaining `pending_files`, and re-dispatches. No action required.

**2. Fixer Gate FAIL**

After all chunks complete, the fixer gate runs. Common failure codes:

| Code | Meaning |
| --- | --- |
| `unsupported_construct_live` | A call that crashes at runtime is still live (not commented out) |
| `high_risk_unmarked` | High-risk issue with no migration comment marker or `resolution` field |
| `convertible_not_converted` | A convertible RDD op left as TODO when a DataFrame equivalent exists |

Expand

Show lessSee more

The coordinator does a **targeted re-fix**, not a full re-run. It passes the gate’s `gaps` array verbatim as `TARGET_ISSUES` to a re-dispatched fixer instructed to touch only those specific lines and leave everything else byte-for-byte unchanged.

Caution

Never do a full stateless re-run on a gate failure. Full re-runs have been observed to regress already-correct code. Always use targeted re-fix.

Default retry budget: 2 attempts, then escalate to you.

### RDD operations

RDD operations are the most common source of TODOs. Snowpark Connect does not support the RDD API.

**Convertible RDDs** (`rdd_class=convertible`), the fixer rewrites the entire chain:

Copy code

```
# Before:
rdd = sc.parallelize([1, 2, 3])
result = rdd.flatMap(lambda x: [x, x*2]).collect()

# After:
from pyspark.sql.functions import explode, array, lit
df = spark.createDataFrame([(1,), (2,), (3,)], ["value"])
result = df.select(explode(array(col("value"), col("value")*2))).collect()
```

**No-equivalent RDDs** (`rdd_class=no_equivalent`), commented out with a TODO:

Copy code

```
# rdd.saveAsTextFile("path")
# SCOS: TODO - [SPRKCNTPY1500-Error] RDD.saveAsTextFile() not supported in Snowpark Connect;
#   use df.write.csv("@my_stage/output/") to write to a Snowflake stage instead
```

Caution

Watch for dangling references. If Phase 0.5 comments out the RDD entry point (`rdd = sc.parallelize(...)`) but downstream code calling `.getNumPartitions()` or similar on that variable is still live, it will raise `NameError` at runtime. The gate targets these, but check your output manually too.

## Phase 2a: Coverage verification

Verifies every file in the manifest is present in `Output/`. Expected outcome:

```
Coverage: 97/97 (100%)
```

A missing file is a hard stop. In practice this is almost never an issue.

## Phase 2b: Compilation gate

Re-runs the fixer gate in `--revert-failing` mode. Any `.py` that still does not compile after Phase 2’s fixes is reverted to its pre-Phase-2 baseline (the `phase-1-complete` git tag). A working original beats broken half-migrated syntax.

### What to expect

```
verdict=PASS_WITH_GAPS reverted_count=0
```

A non-zero `reverted_count` means those files compiled before Phase 2 but did not compile after. They are reverted and need manual attention. The report marks them clearly.

## Phase 2c: Evidence-based verification

Cross-checks self-reported completion state against on-disk evidence. File classifications:

| Classification | Meaning |
| --- | --- |
| `migrated` | Has a genuine migration fixer comment marker; LLM actually engaged |
| `partial` | Has Spark surface / real findings but no fixer edit |
| `trivial` | No Spark surface (utility file, schema-only, etc.) |
| `not_attempted` | File missing from `Output/` |

Expand

Show lessSee more

This gate is also the **sole writer** of Partial Migration findings in `analysis.json`. It clears stale entries from previous runs.

### What to expect

```
97/97 migrated, disagreements = 0, not_attempted = 0
```

## Phase 3: Imports and migration headers

### What happens (fully deterministic, no LLM)

`update_imports.py` runs over every manifest file and does three things:

**1. Replaces the SparkSession builder stub** with:

Copy code

```
from snowflake import snowpark_connect
spark = snowpark_connect.init_spark_session()
```

**2. Comments out unsupported imports** (`databricks`, `delta.tables`)

**3. Prepends a rich Snowpark Connect migration header** to each file:

Copy code

```
"""
Snowpark Connect Migration Output
=====================
Source File: pyspark-join.py
Migrated on: 2026-08-24

Changes Overview:
- [Line 45] [SPRKCNTPY5100-Fixed] to_timestamp format corrected from SSSS to FF4

Known Limitations:
- [Line 72] [SPRKCNTPY1500-Error] sc.broadcast() not supported; use Snowflake
  native broadcast join hints instead
"""
```

The header’s sections are built directly from the inline migration annotations the fixer left in Phase 2. The header always accurately reflects the actual state of the file.

Caution

Do not add your own migration headers during Phase 2. If a fixer adds a header, Phase 3 will see it as a duplicate and suppress the real one.

### What to expect

```
97 file(s) processed, 97 header(s) added, 2 session init(s) replaced,
0 unsupported import(s) commented
```

Gate: **PASS**

## Phase 4: Dashboard CSV reports

### What happens

`generate_scos_reports.py` reads the final migrated files and produces:

| File | Contents |
| --- | --- |
| `Reports/Issues.csv` | One row per issue. Columns: Code, Description, Category, FileId, Line, Status, AffectedFiles |
| `Reports/InputFilesInventory.csv` | One row per source file with metadata |
| `Reports/ArtifactDependencyInventory.csv` | Import dependency graph |
| `Reports/EWISummary.csv` | Aggregate counts by EWI code |

Expand

Show lessSee more

**Note:** `MigrationReadinessReport.html` and `AssessmentIR.json` are **not** generated here; they were produced in Phase 1.2. Phase 4 generates only the CSVs.

### Status values in Issues.csv

| Status | Meaning | Action needed? |
| --- | --- | --- |
| **Fixed** | Migration applied a working equivalent | No |
| **Warning** | Advisory / behavioral note; code runs but may differ slightly | No |
| **Error** | Needs manual code change; no automated fix possible | Yes |
| **IO** | File I/O repoint required; must use a Snowflake stage | Yes |

Expand

Show lessSee more

### Typical status breakdown for a PySpark workload

| Status | Approx % |
| --- | --- |
| Fixed | ~60% |
| Warning | ~25% |
| Error | ~8% |
| IO | ~7% |

Expand

Show lessSee more

## Phase 4a: Post-run state validation

`validate_migration_state.py --strict` checks that all 9 required phases recorded evidence:

```
[OK] 0_5_preprocess         Phase 0.5. Deterministic pre-processing
[OK] 1_analysis             Phase 1. Analyzer
[OK] 1a_assessment_report   Phase 1.2. Assessment report
[OK] 2_fixes                Phase 2. Fixer
[OK] 2a_coverage            Phase 2a. Coverage verification
[OK] 2b_compilation         Phase 2b. Compilation gate
[OK] 2c_verification        Phase 2c. Evidence-based verification
[OK] 3_imports              Phase 3. Imports and headers
[OK] 4_reports              Phase 4. Reports

PASS: all required phases present. Exit code 0.
```

**Never declare a migration complete without a green run of this validator.**

## Phase 4b: Migration feedback file

`generate_migrate_feedback.py` produces:

| File | Contents |
| --- | --- |
| `Feedback/migrate_gaps.md` | Human-intervention markers for Jira triage. Every migration TODO with code snippet, reason, and suggested fix. |
| `Feedback/migrate_feedback.md` | General migration summary. |

Expand

Show lessSee more

**`migrate_gaps.md` is the file to attach to your Jira ticket or share with your engineering team.** It is your actionable remaining work list.

## Outputs summary

After a complete migration, your Conversion folder contains:

```
Conversion-SCOS-<timestamp>/
├── Output/                                 All migrated .py files
│   └── <file>.py                           Each has:
│                                             - Snowpark Connect migration header docstring
│                                             - from snowflake import snowpark_connect
│                                             - spark = snowpark_connect.init_spark_session()
│                                             - Inline migration comment annotations
│
├── Reports/
│   ├── MigrationReadinessReport.html       Stakeholder readiness report (open in browser)
│   ├── AssessmentIR.json                   Machine-readable version of the above
│   ├── Issues.csv                          Final issue list. your remaining work tracker
│   ├── InputFilesInventory.csv             Per-file inventory
│   └── ArtifactDependencyInventory.csv     Import dependency graph
│
├── Feedback/
│   ├── migrate_gaps.md                     Human-intervention items for Jira
│   └── migrate_feedback.md                 General migration summary
│
├── Adjudication/
│   └── chunk_*.json                        Adjudicator verdicts (one sidecar per chunk)
│
├── analysis.json                           Adjudicated findings with resolution status
└── migration_state.json                    Full phase-gate record
```

## Post-migration steps

### Step 1: Read migrate\_gaps.md

Open `Feedback/migrate_gaps.md`. This is your true remaining work list. Typical items:

**IO repoints (most common):**

Copy code

```
# Before:
df = spark.read.csv("resources/myfile.csv")

# Fix:
# 1. Create a stage:
#    CREATE STAGE IF NOT EXISTS my_stage;
# 2. Upload:
#    snow stage copy resources/myfile.csv @my_stage
# 3. Update path:
df = spark.read.csv("@my_stage/myfile.csv")
```

**RDD no-equivalents:**
The code is already commented out. Decide: do you need this output? If yes, use `df.write.csv("@my_stage/output/...")` instead.

**`getNumPartitions`:**
Snowflake manages partitioning automatically. Remove these calls entirely; there is no equivalent.

### Step 2: Check for live code on commented-out variables

After Phase 0.5 comments out RDD entry points, downstream code using those variables is sometimes left live:

Copy code

```
# rdd = spark.sparkContext.parallelize(data)   # commented out
print(rdd.getNumPartitions())                  # STILL LIVE. will NameError
```

Search for this pattern:

Copy code

```
grep -n "getNumPartitions\|\.map(\|\.collect(" Output/*.py | grep -v "^\s*#"
```

Comment out any live references to variables whose assignment is commented out.

### Step 3: Repoint file I/O

For reads:

Copy code

```
# Before:
df = spark.read.json("resources/zipcodes.json")
# After:
df = spark.read.json("@my_stage/zipcodes.json")
```

For writes:

Copy code

```
# Before:
df.write.mode("overwrite").csv("/tmp/output/")
# After:
df.write.mode("overwrite").csv("@my_stage/output/")
```

Create stage and upload once:

Copy code

```
CREATE STAGE IF NOT EXISTS my_stage;
```

Copy code

```
snow stage copy resources/myfile.json @my_stage
snow stage copy resources/myfile.csv @my_stage
```

### Step 4: Set session context

Each migrated script calls `init_spark_session()` but does not set database, schema, or warehouse. Add this after the session init (or set account-level defaults):

Copy code

```
spark.sql("USE WAREHOUSE my_warehouse")
spark.sql("USE DATABASE my_database")
spark.sql("USE SCHEMA my_schema")
```

### Step 5: Test

Start with a simple file that has no IO and no TODOs:

Copy code

```
python pyspark-create-dataframe.py
```

Then test files with IO (after staging the resources):

Copy code

```
python pyspark-read-csv.py
```

Files with migration TODO markers will run but skip the commented-out sections. They will not crash on the TODO lines themselves.

## Running in Snowflake Workspace

### Uploading files

Copy code

```
cortex artifact create file "myfile.py" "/path/to/myfile.py"
```

### Paths with spaces break upload

If your output path contains spaces, the internal stage URI generation fails with a SQL compilation error. Work around it:

Copy code

```
cp "/path with spaces/myfile.py" /tmp/staging/myfile.py
cortex artifact create file "myfile.py" "/tmp/staging/myfile.py"
```

### Bulk upload

Copy code

```
# Copy to a space-free temp path first
cp -r "/path with spaces/Output/" /tmp/migration_output/

# Then bulk upload
for f in /tmp/migration_output/*.py; do
  name=$(basename "$f")
  cortex artifact create file "$name" "$f"
done
```

### Verifying files are present

Copy code

```
-- Step 1: list workspace
LIST 'snow://workspace/USER$.PUBLIC."DEFAULT$"/versions/live/';

-- Step 2: filter to your migrated files (adjust the date string)
SELECT
    COUNT(*)                          AS migrated_file_count,
    ROUND(SUM("size") / 1024, 1)      AS total_kb
FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
WHERE "name" LIKE '/versions/live/%.py'
  AND "name" NOT LIKE '%/__pycache__/%'
  AND "last_modified" LIKE '%25 Aug 2026%';
```

**Note:** `LIST` returns lowercase column identifiers. use `"name"`, `"size"`, `"last_modified"` with double quotes.

## Resuming a partial migration

If a migration is interrupted, the skill resumes from where it stopped. All progress is in `migration_state.json`, not in the conversation.

**To resume:**

Copy code

```
Migrate [source_path] to snowpark-connect
```

Use the same source path and output folder as the original run. The skill finds the existing conversion folder (for example, `Conversion-SCOS-*`), reads `migration_state.json`, and offers to continue from the first incomplete phase.

### What the state file records

| Field | Contents |
| --- | --- |
| `phases_completed` | Which phases passed and their gate verdicts |
| `manifest` | The full file list |
| `pending_files` | Files not yet processed by the fixer |
| `processed_files` | Files the fixer completed |
| `coordinator_mode` | `true` for multi-file workloads |

Expand

Show lessSee more

### Check progress manually

Copy code

```
python3 scripts/validate_migration_state.py \
  --state /path/to/Conversion-SCOS-*/migration_state.json
```

## Known issues and workarounds

### 1. API 400 error on fixer chunks

**Cause:** Combined token count of the files in a chunk exceeded the model’s context limit.

**Resolution:** Automatic. The coordinator detects the missing chunk, re-runs `orchestrate_phases.py` on `pending_files`, and re-dispatches with smaller chunks. No action required.

### 2. Paths with spaces break Workspace upload

**Cause:** `cortex artifact create file` generates a stage URI from the local path; spaces produce invalid SQL.

**Fix:** Copy files to a temporary path without spaces (for example `/tmp/migration_output/`) before uploading (see [Running in Snowflake Workspace](#running-in-snowflake-workspace)).

### 3. Live code on commented-out RDD variables

**Cause:** Phase 0.5 comments out the RDD entry-point line but not downstream code using that variable.

**Fix:** Search the output for live references, then comment out any hits that reference a variable whose assignment line is commented out:

Copy code

```
grep -n "getNumPartitions\|\.map(\|\.collect(" Output/*.py | grep -v "^\s*#"
```

## Quick reference: phase timeline

| Phase | Name | Approx duration (97 files) | Gate |
| --- | --- | --- | --- |
| 0 | Setup | ~2 min | (not applicable) |
| 0.5 | Deterministic pre-processing | ~3 min | **HARD** |
| 0.6 | Standalone SQL rewrite | less than 1 min | **HARD** |
| 1 | Compatibility analysis | ~4 min | **HARD** |
| 1.1a | Unknown API classification | less than 1 min | (not applicable) |
| 1.1b | Adjudication | ~20-30 min | Merge check |
| 1.2 | Migration readiness report | ~5 min | **HARD** |
| 1.3 | Data-edge enrichment *(optional)* | ~5 min | Soft |
| 2 | Apply fixes | ~30-45 min | **HARD + retry** |
| 2a | Coverage verification | less than 1 min | **HARD** |
| 2b | Compilation gate | ~2 min | **HARD** |
| 2c | Evidence-based verification | ~2 min | **HARD** |
| 3 | Imports and headers | ~2 min | **HARD** |
| 4 | Dashboard CSV reports | ~3 min | **HARD** |
| 4a | State validation | less than 1 min | **HARD** |
| 4b | Feedback file | less than 1 min | (not applicable) |
| **Total** |  | **~80-100 min** |  |

Expand

Show lessSee more

The majority of time is in **Phase 1.1b** (adjudication) and **Phase 2** (fixing), both of which use parallel worker pools and scale with workload size.

## Glossary

| Term | Definition |
| --- | --- |
| **EWI** | Early Warning Indicator: a numbered compatibility finding code (for example `SPRKCNTPY5100`). The `SPRKCNTPY` prefix indicates a Python Snowpark Connect issue. |
| **`analysis.json`** | The central artifact produced by Phase 1. Contains every detected compatibility issue with risk score, adjudication verdict, and final resolution status. |
| **`migration_state.json`** | The phase-gate record. Single source of truth for what has run and what the outcome was. Used to resume interrupted migrations. |
| **recipe** | A LibCST rewrite rule that makes a deterministic, byte-exact code transformation. Runs in Phase 0.5 before any LLM sees the code. |
| **adjudication** | The Phase 1.1b process of confirming or dismissing deferred trigger matches using full-file context. |
| **coordinator** | The main agent that orchestrates the migration. Delegates to specialists but is the sole writer of `migration_state.json`. |
| **`coordinator_mode`** | `true` = multi-file workload, uses parallel sub-agent pools. `false` = single file, all phases run inline. |
| **`phase-0-source`** | The git tag of your unmodified original code. The readiness report materializes this tag to describe what you actually wrote. |
| **`recipe_validated`** | An `analysis.json` `kind` indicating the Phase 0.5 recipe already fixed this issue. The fixer skips it. |
| **`recipe_incomplete`** | The recipe annotated the issue but could not fully fix it. The fixer completes the fix. |
| **targeted re-fix** | A retry mode where the fixer receives only the specific `file:line` pairs from the gate’s `gaps` array and is told to touch nothing else. Prevents regression of already-correct code. |
| **IO repoint** | Replacing a local file path (`resources/myfile.csv`, `/tmp/output`) with a Snowflake stage path (`@my_stage/myfile.csv`). Required because Snowpark Connect cannot read from the local filesystem. |

Expand

Show lessSee more
