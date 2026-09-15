# Snowflake AIM Agent for Data Warehouses

The Snowflake AIM Agent for Data Warehouses is an AI assistant for [Snowflake CoCo](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code) that guides you through an end-to-end database migration to Snowflake. It provides a conversational, interactive workflow — from connecting to your source database through code conversion, deployment, data migration, and validation.

Migrations take time. A full migration — especially for large workloads with hundreds of objects — is not completed in a single session. The Snowflake AIM Agent for Data Warehouses automatically tracks your progress at every step. Each time you start a session, it reads your project state and picks up exactly where you left off. There is no need to start over.

---

## Why use the Snowflake AIM Agent for Data Warehouses

Snowflake CoCo on its own is a capable coding agent, but a database migration involves coordination across dozens of tools, stages, and hundreds of objects over days or weeks. The Snowflake AIM Agent for Data Warehouses adds the structure, automation, and domain expertise that a general-purpose agent doesn’t have.

### What the Snowflake AIM Agent for Data Warehouses gives you

| Benefit | What it means for you |
| --- | --- |
| **Guided end-to-end workflow** | You don’t need to know the right sequence. The Snowflake AIM Agent for Data Warehouses moves through connection, extraction, conversion, assessment, deployment, data migration, and validation automatically. |
| **Session persistence** | Close your terminal and come back tomorrow. The Snowflake AIM Agent for Data Warehouses picks up exactly where you left off — no repeated setup, no lost progress. |
| **SnowConvert integration** | Source SQL is translated deterministically by SnowConvert before AI touches it. You start from a high-quality baseline, not a best-effort LLM rewrite. |
| **Dependency-aware deployment** | The Snowflake AIM Agent for Data Warehouses analyzes object dependencies and builds deployment waves so objects are deployed in the right order. You don’t manually sort hundreds of tables and views. |
| **Two-sided testing** | Functions and procedures are tested against source-side baselines automatically. Failures trigger a fix loop — the agent diagnoses, patches, and re-tests until the output matches. |
| **Reusable fix rules** | Every correction you make can be extracted into a rule and propagated across the entire project. The Snowflake AIM Agent for Data Warehouses gets smarter as you go. |
| **Zero setup** | All dependencies (Python packages, SnowConvert AI, ODBC drivers) are installed automatically the first time the Snowflake AIM Agent for Data Warehouses runs. |

Expand

Show lessSee more

### Snowflake AIM Agent for Data Warehouses vs. plain Snowflake CoCo

|  | Snowflake AIM Agent for Data Warehouses | Plain Snowflake CoCo |
| --- | --- | --- |
| Structured multi-stage workflow | Yes — six stages from connect to migrate | No — you drive every step manually |
| Automatic state tracking | Yes — resumes across sessions | No — you restart context each session |
| SnowConvert deterministic conversion | Yes — integrated | No — you run it yourself and import results |
| Source database connectivity | Yes — connects, extracts, and migrates data | No — no built-in database connectors |
| Deployment wave planning | Yes — dependency analysis and interactive wave editor | No — you plan deployment order manually |
| Automated testing loop | Yes — baseline capture, two-sided validation, auto-fix | No — you write and run tests yourself |
| Reusable fix rules | Yes — extract, search, apply, propagate | No — fixes are one-off |

Expand

Show lessSee more

---

## How to use the Snowflake AIM Agent for Data Warehouses

### Prerequisites

Before starting a migration, ensure you have:

- [Python](https://www.python.org/downloads) installed.
- [Git](https://git-scm.com/install) installed.
- [Snowflake CoCo CLI](/user-guide/cortex-code/cortex-code-cli) installed (the Snowflake AIM Agent for Data Warehouses is bundled).
- A Snowflake account with a connection configured in `~/.snowflake/config.toml` or `~/.snowflake/connections.toml`.
- A source database accessible from your machine. Supported source connections include SQL Server, Amazon Redshift, Oracle, Teradata, and PostgreSQL.

All other dependencies (`uv`, SnowConvert, Python packages) are installed automatically when the Snowflake AIM Agent for Data Warehouses runs for the first time.

### Launch Snowflake CoCo

Create a directory for your migration project. From the project directory, start Snowflake CoCo CLI:

Copy code

```
cortex
```

### Start a migration

From within Snowflake CoCo CLI, there are a couple of common ways to start a migration:

1. **Start a new migration** (greenfield)  
   You have a source database and want to migrate it to Snowflake from scratch. The Snowflake AIM Agent for Data Warehouses walks you through every stage: connect to the source, extract objects, convert code, assess the workload, deploy, migrate data, and validate.

```
start a database migration
```

2. **Resume an in-progress migration**  
   You already started a migration in a previous session — maybe days or weeks ago. The Snowflake AIM Agent for Data Warehouses reads your project state and picks up at the exact point where you stopped. No re-extraction, no re-conversion.

```
continue my migration
```

### Import an existing migration

Once you start or continue a migration, you can import any `.sql` files you already have from a previous SnowConvert run or another source into the project to be picked up at the conversion or deployment stage.

```
import SQL files from ./my-exported-scripts/
```

Tip

As a migration project progresses, if you find that Snowflake CoCo is not triggering the Snowflake AIM Agent for Data Warehouses (this may sometimes happen due to context windowing compaction), you can directly trigger it by using “/migrate <your prompt>”

---

## What you can do

Snowflake AIM Agent for Data Warehouses guides you through the full migration lifecycle and lets you jump directly to any stage at any time. You can pause and resume across sessions, and multiple users can collaborate on the same project — it tracks which code units each person is working on so effort isn’t duplicated.

| Capability | Description |
| --- | --- |
| **Connect to source** | Set up a connection to your source database with credentials stored securely for reuse |
| **Extract source code** | Pull DDL and stored procedures directly from a live database, or import local `.sql` files |
| **Convert code** | Translate source SQL to Snowflake-compatible SQL via SnowConvert, with a full EWI report |
| **AI-assisted conversion** | AI explains remaining conversion issues, suggests fixes, and applies them interactively |
| **Assess workloads** | Generate an interactive HTML report covering deployment waves, object exclusions, dynamic SQL patterns, and SSIS/Informatica ETL analysis |
| **Deploy objects** | Deploy converted tables, views, functions, and procedures to Snowflake wave by wave |
| **Migrate data** | Copy rows from source tables to Snowflake with automatic row-count validation |
| **Test functions and procedures** | Capture source-side baselines and run two-sided validation to confirm output equivalence |
| **Improve fix rules** | Create reusable fix rules from corrections you make and propagate them across the project automatically |
| **Convert ETL pipelines** | Translate SSIS packages and Informatica workflows to dbt, using deterministic conversion with optional AI-assisted remediation |
| **Validate data** | Compare **schema (L1), metrics (L2), and optionally rows (L3)** between source and Snowflake tables after migration; cloud validation uses the same Orchestrator and Workers as data migration |
| **Repoint reports** | Repoint Power BI reports to use Snowflake as the data source |

Expand

Show lessSee more

---

## Supported source systems

Not all capabilities are available for all source systems. The following table shows what is supported today and what is coming soon.

| Capability | SQL Server | Redshift | Teradata | Oracle | PostgreSQL | Other source systems |
| --- | --- | --- | --- | --- | --- | --- |
| Code extraction | Yes | Yes | Planned | Planned | Yes | Planned |
| Deterministic code conversion | Yes | Yes | Yes | Yes | Yes | Yes |
| AI conversion and verification | Yes | Yes | Planned | Planned | Planned | Planned |
| Code deploy | Yes | Yes | Planned | Planned | Yes | Planned |
| SSIS to dbt (deterministic) | Yes | Yes | Yes | Yes | Yes | Yes |
| Informatica to dbt (deterministic) | Yes | Yes | Yes | Yes | Yes | Yes |
| AI conversion of SSIS to dbt | Yes | Yes | Yes | Yes | Yes | Yes |
| AI conversion of Informatica to dbt | Yes | Yes | Yes | Yes | Yes | Yes |
| Cloud data migration | Yes | Yes | Yes | Yes | Yes | Planned |
| Cloud data validation | Yes | Yes | Yes | Yes | Yes | Planned |
| Testing framework | Yes | Yes | Yes | Yes | Planned | Planned |
| AI assessment (via Snowflake CoCo) | Yes | Yes | Yes | Planned | Planned | Planned |
| Power BI report repointing | Yes | Yes | Yes | Yes | Yes | Synapse only |

Expand

Show lessSee more

**Other dialects with deterministic conversion support:** Azure Synapse, Sybase IQ, Google BigQuery, Greenplum, Netezza, Spark SQL, Databricks SQL, Vertica, Hive, IBM DB2

**Available extraction scripts:** Teradata, SQL Server, Synapse, Oracle, Redshift, Netezza, Vertica, DB2, Hive, BigQuery, Databricks, Sybase IQ

**SAS:** AI-assisted assessment and code conversion are available in preview — see [SAS Migration](/migrations/aim-for-datawarehouses/sas-migration).

---

## Migration workflow

The Snowflake AIM Agent for Data Warehouses guides you through six stages. Each session starts by detecting your current progress and resuming automatically.

| Stage | Name | What happens |
| --- | --- | --- |
| 1 | **Connect** | Set up a connection to your source database |
| 2 | **Init** | Create a local migration project |
| 3 | **Register** | Extract DDL and code from the source, or import local `.sql` files |
| 4 | **Convert** | Translate source SQL to Snowflake-compatible SQL via SnowConvert |
| 5 | **Assess** | Generate an interactive report covering waves, exclusions, dynamic SQL, and ETL |
| 6 | **Migrate** | Deploy objects, migrate data, validate output, and fix errors — wave by wave |

Expand

Show lessSee more

Stage 6 is where the bulk of the work happens. AI-driven testing, conversion remediation, and iterative fix loops run here — often across multiple sessions and days. This is also the stage where collaboration pays off most: multiple users can work on the same project simultaneously, each picking up different code units while the Snowflake AIM Agent for Data Warehouses coordinates to prevent duplicated effort.

Every session shows a live progress checklist so you always know where you stand:

```
✅  1. Connect             — Connected to SQL Server
✅  2. Init                — Project initialized
✅  3. Register            — 342 objects registered
◐   4. Initial Conv        — 280/342 converted
⬚   5. Assess              — Not run
⬚   6. Migrate Objects     — 0/120 tables deployed
```

---

## Snowflake AIM Agent for Data Warehouses reference

The Snowflake AIM Agent for Data Warehouses is organized as a skill tree. The root skill detects your project state and delegates to the right sub-skill. You can also invoke any sub-skill directly by describing what you want.

### Setup sub-skills (Stages 1–5)

#### midway-entry

For projects where source code has already been converted to Snowflake SQL outside the Snowflake AIM Agent for Data Warehouses. Import the pre-converted `.sql` files and start at the deployment stage, skipping extraction and conversion. Supported for SQL Server and Redshift.

#### connection

Walks you through connecting to your source database. Collects credentials, tests the connection, and saves it for reuse across sessions. Supports:

- **SQL Server** — configures ODBC driver, host, port, and authentication.
- **Amazon Redshift** — configures host, port, database, and IAM or password authentication.

#### register-code-units

Gets source code into the migration project. Two paths are available:

| Path | When to use |
| --- | --- |
| **Extract from database** | You have a live source connection and want the agent to pull DDL and object code directly |
| **Import local files** | You already have `.sql` files on disk and want to import them into the project |

Expand

Show lessSee more

#### convert

Runs SnowConvert to translate your source SQL (T-SQL or Redshift SQL) into Snowflake-compatible SQL. After conversion, the agent presents:

- Total objects converted successfully.
- EWI (Error Warning Issue) summary broken down by severity (errors, warnings, informational).
- A list of objects that require manual review.

#### assessment

Generates an interactive multi-tab HTML report. The assessment includes four analyses that can be run individually or together:

| Analysis | What it does |
| --- | --- |
| **Deployment Waves** | Analyzes object dependencies to produce an ordered deployment sequence. Objects within a wave have no inter-dependencies; waves are ordered so dependencies are always deployed first. |
| **Object Exclusion** | Identifies objects that do not need migration: temporary tables, staging objects, deprecated objects, and test artifacts. Reduces scope before deployment. |
| **Dynamic SQL Analysis** | Classifies and scores Dynamic SQL patterns in your converted code. Identifies patterns that Snowflake handles natively, patterns requiring manual rewrite, and patterns with elevated migration complexity. |
| **ETL/SSIS Assessment** | Analyzes SSIS packages individually: classifies each package (Ingestion, Transformation, Export, Orchestration, Hybrid), maps control and data flow, and estimates migration effort. |
| **Informatica Assessment** | Analyzes Informatica Power Center workflows and mappings: classifies each workflow, scores migration complexity, and estimates effort. |

Expand

Show lessSee more

The report is generated as a single self-contained HTML file. You can iterate on the wave plan interactively — for example, reprioritizing objects, adjusting wave sizes, or relocating specific objects — before locking it for deployment.

### Migration sub-skills (Stage 6)

#### migrate-etl

Entry point for stabilizing a converted ETL code unit (SSIS or Informatica). Claims the unit so it appears in your work queue, then delegates to the phase-based ETL stabilization engine — which applies fixes, runs tests, and iterates until the converted output is correct.

#### migrate-objects

The main deploy loop. Processes all objects in the current wave in dependency order:

| Object type | What happens |
| --- | --- |
| **Tables** | Deployed to Snowflake, then data is migrated from the source. |
| **Views** | Deployed to Snowflake. Blocked views retry after their dependent functions/procedures pass. |
| **Functions & Procedures** | Deployed, tested against source output, and fixed if tests fail. The loop repeats until tests pass or the user decides to skip. |

Expand

Show lessSee more

After each wave completes, the agent automatically advances to the next wave.

#### baseline-capture

Captures the expected output of source stored procedures and functions for use as test baselines. Two approaches are supported:

| Approach | When to use |
| --- | --- |
| **Query Logs** | You have CSV logs of real `EXEC` or `CALL` statements from your source system. The agent parses these to extract parameters and expected outputs. |
| **AI-Assisted** | No logs are available. A swarm of specialized agents generates test cases covering business logic, data-driven scenarios, and edge cases by analyzing the source SQL. |

Expand

Show lessSee more

Baselines are stored locally and uploaded to Snowflake so they can be used for two-sided validation (source output vs. Snowflake output) during the migrate-objects loop.

#### rule-engine

Manages reusable migration rules stored in Snowflake. Rules encode known source-to-Snowflake fix patterns and are shared across all objects in the project. Each rule can operate in two modes:

| Mode | How it works |
| --- | --- |
| **Regex** | A regex find-and-replace applied mechanically to SQL files |
| **AI-guided** | The rule provides context and strategy; the AI interprets and applies it |

Expand

Show lessSee more

The rule engine has four sub-capabilities:

| Sub-skill | What it does |
| --- | --- |
| **search** | Scans a SQL file against all rules using regex pattern matching and Cortex semantic search. Returns matched rules ranked by relevance. |
| **apply** | Applies matched rules to local SQL files. Regex rules are applied automatically; AI-mode rules are shown for review before applying. Supports single-file and batch application. |
| **extract** | Creates a new reusable rule from a fix you just made. Works from an interactive before/after comparison or retroactively from git history. |
| **propagate** | Given a rule, finds every code unit in the project it applies to (via reverse regex + semantic search), then hands off to batch apply. |

Expand

Show lessSee more

Rules accumulate over the lifetime of the project. Every time the agent fixes an object and extracts a rule, that rule becomes available to all subsequent objects — reducing manual effort as the migration progresses.

---

## What you can ask

You do not need to follow the prescribed path. You can ask for any capability at any time.

### Status and navigation

| Prompt | What happens |
| --- | --- |
| `"What is the current state?"` | Shows the progress checklist |
| `"What should I work on next?"` | Returns the next dependency-ready object |
| `"Continue"` | Picks up the prescribed migration path |

Expand

Show lessSee more

### Setup

```
"Connect to my SQL Server database"
"Extract objects from the source"
"Import SQL files from ./my-scripts/"
"Convert my source code"
```

### Assessment

```
"Run a full assessment"
"Generate deployment waves"
"I want a maximum of 30 objects per wave"
"Prioritize all Payroll objects in Wave 1"
"Identify temporary and staging objects"
"Analyze dynamic SQL patterns"
"Assess my SSIS packages"
"Assess my Informatica workflows"
```

### Migration

```
"Deploy tables"
"Migrate data"
"Validate data"
"Deploy and test the next function"
"Capture baselines for dbo.GetCustomerOrders"
```

### Rule engine

```
"Search rules for this file"
"Apply all matched rules"
"Extract a rule from my last fix"
"Propagate this rule across the project"
"Show me all rules"
```

---

## Example workload

You can use [AdventureWorksDW](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure) as an example source database to try the Snowflake AIM Agent for Data Warehouses end-to-end. Substitute any SQL Server or Redshift database you have access to — the Snowflake AIM Agent for Data Warehouses adapts to whatever source you connect.

---

## Troubleshooting

For common setup and migration issues — including what to do when the agent or its tooling isn’t installed, the skill doesn’t trigger, or setup fails — see [Troubleshooting](/migrations/aim-for-datawarehouses/troubleshooting).

---

## Support

For help with the Snowflake AIM Agent for Data Warehouses, contact: [**aim-support@snowflake.com**](mailto:aim-support@snowflake.com)
