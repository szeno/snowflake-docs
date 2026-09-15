# When you want to orchestrate the migration

Snowflake’s recommended way of migrating data warehouses is through the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview). Its CoCo-powered orchestration greatly accelerates the overall time it takes to complete a migration.

However, if you want full control, you can directly utilize the underlying SnowConvert engine that the Snowflake AIM Agent for Data Warehouses invokes via a command line interface. There’s no AI-powered orchestration available via this method. You will be responsible for driving and managing the overall migration.

That said, as long as your Snowflake account is CoCo-enabled, you can still take advantage of AI capabilities such as AI-assisted conversions.

# What is SnowConvert AI CLI?

With the SnowConvert AI CLI, migration engineers can:

- extract code from their source platform
- run a deterministic conversion on that code
- further advance their migration using AI conversion to cover objects that the deterministic engine could not translate
- deploy that code to Snowflake
- migrate data from the source system to Snowflake
- validate that data between the two systems

The SnowConvert AI CLI will also allow developers to create skills and agents that utilize the tool to automate their process.

## Prerequisites

- macOS, Windows, or Linux
- Snowflake CLI: recommended for Snowflake connection configuration [SnowCLI Install Guide](https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation)
- A source database to extract from, or a set of code to use

## Snowflake Connection Setup

The SnowConvert AI CLI reuses your Snowflake CLI connection configuration. The connection is used for functionality in ai-convert, deploy, and the cloud versions of data migration and validation. Your Snowflake account also authenticates you for SnowConvert AI CLI, skipping the need for an access code that was necessary in prior versions.

**Snowflake Account Requirement**

Before using scai init, scai code convert, scai code extract, scai ai-convert, or scai code deploy, ensure that you:

- Can connect to Snowflake with `snow connection test`
- Have a default Snowflake CLI connection configured (this is used when you don’t specify a name)

To configure a Snowflake connection:

Copy code

```
# Add a new connection using Snowflake CLI
snow connection add

# Set it as the default
snow connection set-default <connection_name>

# Test your connection
snow connection test
```

Once this is configured, commands needing a connection to Snowflake will use your Snowflake CLI connection automatically.

## Installation

## Installer scripts (recommended)

### macOS and Linux

Copy code

```
curl -fsSL https://snowconvert.snowflake.com/storage/linux/prod/cli/install.sh | bash
```

### Windows

Copy code

```
irm https://snowconvert.snowflake.com/storage/windows/prod/cli/install.ps1 | iex
```

## Homebrew Installation (macOS only - legacy)

If you do not have homebrew installed, follow the [instructions here](https://brew.sh/).

There are two public channels for builds: Preview and GA.

Stable Version (recommended)

Install the stable production (GA) release:

Copy code

```
brew tap snowflakedb/snowconvert-ai
brew install --cask snowconvert-ai
```

Preview Version

Install the Preview (pr) version with pre-release features from the beta/staging environment:

Copy code

```
brew tap snowflakedb/snowconvert-ai
brew install --cask snowconvert-ai-pr
```

Usage

After installation, you can use the SnowConvert AI CLI:

Copy code

```
scai --help
```

Managing Installations

View installed version

Copy code

```
brew info --cask snowconvert-ai
# or
brew info --cask snowconvert-ai-pr
```

Switch between versions

Copy code

```
# Uninstall current version
brew uninstall --cask snowconvert-ai #or snowconvert-ai-pr

# Install another version
brew install --cask snowconvert-ai
# or
brew install --cask snowconvert-ai-pr
```

Update to latest version
Important: you must run `brew update` first to sync the tap with the latest cask definitions:

Copy code

```
# Update tap definitions and upgrade to latest version
brew update && brew upgrade --cask snowconvert-ai

# For preview version
brew update && brew upgrade --cask snowconvert-ai-pr
```

Why both commands? `brew update` synchronizes your local tap with the latest cask definitions from GitHub. Without it, `brew upgrade` won’t see new versions even if they exist on the server.

## Installer Packages (macOS, Linux, Windows - legacy)

*GA Releases*

| OS | Installer |
| --- | --- |
| macOS | [Apple Silicon](https://snowconvert.snowflake.com/storage/darwin_arm64/prod/cli/snowflake-scai-cli-darwin-arm64.pkg) |
| macOS | [Intel](https://snowconvert.snowflake.com/storage/darwin_x64/prod/cli/snowflake-scai-cli-darwin-x64.pkg) |
| Linux | [arm64 .rpm](https://snowconvert.snowflake.com/storage/linux/prod/cli/snowflake-scai-cli-linux-arm64.rpm) |
| Linux | [arm64 .deb](https://snowconvert.snowflake.com/storage/linux/prod/cli/snowflake-scai-cli-linux-arm64.deb) |
| Linux | [x64 .rpm](https://snowconvert.snowflake.com/storage/linux/prod/cli/snowflake-scai-cli-linux-x64.rpm) |
| Linux | [x64 .deb](https://snowconvert.snowflake.com/storage/linux/prod/cli/snowflake-scai-cli-linux-x64.deb) |
| Linux | [x64 .tar.gz](https://snowconvert.snowflake.com/storage/linux/prod/cli/snowflake-scai-cli-linux-x64.tar.gz) |
| Linux | [arm64 .tar.gz](https://snowconvert.snowflake.com/storage/linux/prod/cli/snowflake-scai-cli-linux-arm64.tar.gz) |
| Windows | [arm64 .msi](https://snowconvert.snowflake.com/storage/windows_arm64/prod/cli/snowflake-scai-cli-windows-arm64.msi) |
| Windows | [x64 .msi](https://snowconvert.snowflake.com/storage/windows/prod/cli/snowflake-scai-cli-windows-x64.msi) |

Expand

Show lessSee more

*Preview Releases*

| OS | Installer |
| --- | --- |
| macOS | [Apple Silicon](https://snowconvert.snowflake.com/storage/darwin_arm64/beta/cli/snowflake-scai-cli-darwin-arm64-beta.pkg) |
| macOS | [Intel](https://snowconvert.snowflake.com/storage/darwin_x64/beta/cli/snowflake-scai-cli-darwin-x64-beta.pkg) |
| Linux | [arm64 .rpm](https://snowconvert.snowflake.com/storage/linux/beta/cli/snowflake-scai-cli-linux-arm64-beta.rpm) |
| Linux | [arm64 .deb](https://snowconvert.snowflake.com/storage/linux/beta/cli/snowflake-scai-cli-linux-arm64-beta.deb) |
| Linux | [x64 .rpm](https://snowconvert.snowflake.com/storage/linux/beta/cli/snowflake-scai-cli-linux-x64-beta.rpm) |
| Linux | [x64 .deb](https://snowconvert.snowflake.com/storage/linux/beta/cli/snowflake-scai-cli-linux-x64-beta.deb) |
| Linux | [x64 .tar.gz](https://snowconvert.snowflake.com/storage/linux/beta/cli/snowflake-scai-cli-linux-x64-beta.tar.gz) |
| Linux | [arm64 .tar.gz](https://snowconvert.snowflake.com/storage/linux/beta/cli/snowflake-scai-cli-linux-arm64-beta.tar.gz) |
| Windows | [arm64 .msi](https://snowconvert.snowflake.com/storage/windows_arm64/beta/cli/snowflake-scai-cli-windows-arm64-beta.msi) |
| Windows | [x64 .msi](https://snowconvert.snowflake.com/storage/windows/beta/cli/snowflake-scai-cli-windows-x64-beta.msi) |

Expand

Show lessSee more

## Accept Terms and Conditions

Issuing the following command will display the license terms for using the SnowConvert AI CLI. It is required that you do this in order to use the product.

Copy code

```
# display the scai terms and conditions
scai terms 

#displays terms and allows you to accept them
scai terms accept
```

## Understanding Projects

A project is required before you can use any other scai command. This is similar to how Git requires you to run git init before using other Git commands.

A project:

- Organizes your migration work in a dedicated folder structure
- Tracks your source dialect (Oracle, SQL Server, Teradata, etc.)
- Stores configuration, source code, converted code, and reports

When you run scai init, it creates this folder structure in the target directory.

- If you pass a PATH, scai will create that folder (if it doesn’t exist) and initialize the project inside it.
- If you omit PATH, scai initializes the current directory (which must be empty).

The following folder structure:

Copy code

```
project/
├── .git/
├── .gitignore
├── .scai/
│   ├── config/
│   │   ├── project.yml                        ← Team-shared config (Git)
│   │   ├── project.local.yml                  ← Personal config (gitignored)
│   │   └── conversion-context/
│   │       └── MigrationContext.json
│   └── registry/
│       ├── {uuid1}.json
│       ├── {uuid2}.json
│       ├── {uuid3}.json
│       └── .locks/                            ← SCRIPT STATE (Git)
│           └── registry.lock
├── settings/                ← User-managed settings (not created by default)
│   ├── extraction.yml
│   ├── deployment.yml
│   └── ai-verification.yml
├── source/                                    ← Source code Database objects
│   └── db1/
│       └── retail/                            -- schema1
│           ├── Tables/
│           │   ├── table_customers.sql
│           │   └── table_orders.sql
│           └── Stored Procedures/
│               └── proc_calculate.sql
├── snowflake/                                ← Working directory of converted code (may have manual edits, should not get overwritten)
│   ├── db1/
│   │   └── retail/                            -- schema1
│   │       ├── Tables/
│   │       │   ├── table_customers.sql
│   │       │   └── table_orders.sql
│   │       └── Stored Procedures/
│   │           └── proc_calculate.sql
│   └── dbt/                                   ← Converted scripts (optional)
│       └── models/
│           └── staging/
│               └── stg_customer_daily.sql
├── artifacts/                                 ← All artifacts related to objects
│   ├── source_raw/                            ← Original source code without changes
│   ├── db1/
│   │   ├── retail/                            -- schema1
│   │   │   └── table/             -- one folder per object kind
│   │   │       └── products/
│   │   │           ├── deterministic/         -- different runs from deterministic engine
│   │   │           │   ├── 20261201.350956/
│   │   │           │   │   └── proc_calculate.sql
│   ├── UDF Helpers/
│   └── ETL/
│   │     ├── DWH_EXAMPLE
│   │     │     ├── DWH_EXAMPLE.sql
├── reports/                                   ← Generated reports (optional in Git)
│   ├── SnowConvert/
│   │   ├── ObjectReferences.<timestamp>.csv
│   │   ├── TopLevelCodeUnits.csv
│   │   └── Issues.csv
│   ├── GenericScanner/
│   │   └── GenericScannerOutput/
│   │       ├── line_counts.pam
│   │       ├── files.pam
│   │       ├── FilesInventory.csv
│   │       ├── word_counts.pam
│   │       ├── KeywordCounts.csv
│   │       └── tool_execution.pam
│   └── ...
├── logs/
│   ├── GenericInfrastructureController/
│   ├── GenericScanner/
│   └── Snowconvert/
└── results/
    └── DataValidation/
```

Important: after creating a project, run all subsequent scai commands from within the project folder (where the .scai directory is).

CLI Logs are written to ~/.scai/logs/jobs.log by default

## Quick Start: Code Conversion Only

Use this workflow when you have existing SQL files to convert. Works with all supported dialects.

> [!IMPORTANT]
> You must already be in an empty directory to create a project.

#1. Create a project folder and initialize it (project name is inferred from folder name)

Copy code

```
scai init my-project -l Oracle
cd my-project
```

#2. Add your source code

Copy code

```
scai code add -i /path/to/your/sql/files
```

#3. Convert to Snowflake SQL

Copy code

```
scai code convert
```

#4. Deploy to Snowflake

Copy code

```
scai code deploy
```

Your converted code will be in the snowflake/ folder, and conversion reports in reports/.

## Quick Start: End-to-End Migration

Use this workflow to extract code directly from your source database. Only available for SQL Server and Redshift.

Step 1: Create Project
# Create a project folder and initialize it (project name is inferred from folder name)

Copy code

```
scai init my-project -l SqlServer # or Redshift
cd my-project
```

Step 2: Configure Source Connection

Copy code

```
#SQL Server (interactive mode - recommended)
scai connection add-sql-server
```

Copy code

```
#Redshift (interactive mode - recommended)
scai connection add-redshift
```

The interactive mode will prompt you for connection details.

Set a default source connection (used with scai code extract runs without –source-connection)

Copy code

```
scai connection set-default -l sqlserver --connection <NAME>
```

Or

Copy code

```
scai connection set-default -l redshift --connection <NAME>
```

Step 3: Extract, Convert, Deploy

#extract code from source database

Copy code

```
scai code extract
```

#convert to Snowflake SQL

Copy code

```
scai code convert
```

#deploy to Snowflake

Copy code

```
scai code deploy
```

---

## Filtering objects by name during extraction

By default, `scai code extract` extracts every object available on the source connection. Use `-n` / `--name` to extract only the objects you name.

### Name matching is exact

`-n` / `--name` matches object names **exactly** and is **case-insensitive**. A name without a wildcard selects only the object with that exact name. To match a prefix or a partial name, use `*` as a wildcard:

| Filter | Matches |
| --- | --- |
| `-n Employees` | Only the object named `Employees` |
| `-n Emp*` | Names starting with `Emp` |
| `-n *Employee*` | Names containing `Employee` |

Expand

Show lessSee more

> **Note:** Exact matching keeps similarly named siblings out of the extraction. For example, `-n SNAPM_EDB_MODEL_GROUPING` extracts only that table, not a sibling such as `SNAPM_EDB_MODEL_GROUPING_SWTCH`. SnowConvert doesn’t automatically add partition SWITCH or staging tables. To extract the whole family, opt in with a wildcard: `-n "SNAPM_EDB_MODEL_GROUPING*"`.

**Examples:**

Copy code

```
# Extract one table by its exact name
scai code extract -s myconn -t TABLE -n SNAPM_EDB_MODEL_GROUPING

# Extract the whole prefix family (explicit wildcard)
scai code extract -s myconn -t TABLE -n "SNAPM_EDB_MODEL_GROUPING*"
```

---

## Filtering Objects with the `--where` Clause

Many `scai` commands operate on the **Code Unit Registry** – a local index of every code unit (table, view, procedure, function, etc.) in your project. The `--where` flag lets you filter which objects a command acts on, using a SQL-like expression against that registry.

This section covers how the WHERE clause works, which commands support it, and how to use it effectively.

### How the Code Unit Registry works

1. When you run `scai code add` or `scai code extract`, source code is added to your project and split into individual code units.
2. When you run `scai code convert`, the CLI builds a registry entry for every code unit, tracking its source/target metadata, object type, and conversion status.
3. When you pass `--where` to a supported command, the CLI queries that registry and applies the operation only to matching objects.

**The registry must exist before `--where` can be used.** If you haven’t run at least `scai code add` (or `scai code extract`) yet, `--where` will fail with a “registry not found” error.

### Discovering queryable fields: `scai code where`

Run `scai code where` to see the full, up-to-date reference of all queryable fields, supported operators, and usage examples. The output is generated from the actual registry library, so it is always current.

Copy code

```
scai code where
```

The most commonly used fields (all field names are **camelCase**, all enum values are **lowercase**):

| Field | Description | Example values |
| --- | --- | --- |
| `source.name` | Object name in the source database | `'my_procedure'` |
| `source.objectType` | Object type in source | `'table'`, `'procedure'`, `'view'`, `'function'` |
| `source.database` | Source database name | `'my_db'` |
| `source.schema` | Source schema name | `'dbo'`, `'public'` |
| `target.name` | Object name in Snowflake | `'MY_PROCEDURE'` |
| `target.objectType` | Object type in Snowflake | `'table'`, `'procedure'`, `'view'`, `'function'` |
| `target.database` | Target database name | `'MY_DB'` |
| `target.schema` | Target schema name | `'PUBLIC'` |
| `codeStatus.conversion.status` | Conversion result | `'pending'`, `'completed'`, `'failed'`, `'excluded'` |
| `codeStatus.registration.status` | Registration/extraction result | `'pending'`, `'completed'`, `'failed'`, `'excluded'` |
| `codeStatus.aiVerification.status` | AI verification result | `'pending'`, `'completed'`, `'failed'`, `'excluded'` |

Expand

Show lessSee more

### Previewing results: `scai code find`

Before running a destructive or long-running operation, use `scai code find` to test your filter and see which objects match:

Copy code

```
# Show all code units in the registry
scai code find

# Test a WHERE filter
scai code find --where "target.objectType = 'table'"

# Show all results (default caps at 100)
scai code find --where "source.schema = 'dbo'" --no-limit
```

`scai code find` accepts the same `--where` syntax as all other commands that support it. Use it as a dry-run before committing to an operation.

### Commands that support `--where`

The following table summarizes every `scai` command that accepts the `--where` flag:

| Command | Purpose | `--where` notes |
| --- | --- | --- |
| `scai code find` | Preview/query code units in the registry | Primary tool for testing filters before using them elsewhere |
| `scai code convert` | Convert source code to Snowflake SQL | Only matched units are transformed; dependencies are still parsed for symbol resolution |
| `scai code deploy` | Deploy converted code to Snowflake | Also supports `--include-dependencies` to automatically include objects that filtered objects depend on |
| `scai code accept` | Accept latest artifact versions into the snowflake folder |  |
| `scai ai-convert start` | Start AI-powered conversion improvement | Cannot be combined with `--selector` (pick one) |
| `scai ai-convert accept` | Accept AI-suggested fixes | Filters which suggested fixes to review/accept |
| `scai data migrate` | Migrate data from source to Snowflake | Full migration projects only |
| `scai data validate` | Validate data between source and Snowflake | Full migration projects only |

Expand

Show lessSee more

Each of these commands uses the same WHERE clause syntax. The recommended workflow is:

Copy code

```
scai code where          (learn the fields)
        ↓
scai code find --where   (preview what matches)
        ↓
scai <command> --where   (run the operation)
```

---

### `scai code find --where`

Query the Code Unit Registry and display matching objects. This is the safest way to test a filter before using it with a command that makes changes.

Copy code

```
scai code find --where <WHERE_CLAUSE> [--no-limit]
```

| Flag | Description |
| --- | --- |
| `--where <WHERE_CLAUSE>` | SQL-like WHERE clause to filter objects |
| `--no-limit` | Show all results (default limit is 100) |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Find all code units (no filter)
scai code find

# Find a specific object by name
scai code find --where "source.name = 'my_table'"

# Find all procedures in a schema
scai code find --where "source.schema = 'dbo' AND source.objectType = 'procedure'"

# Find objects that failed conversion
scai code find --where "codeStatus.conversion.status = 'failed'"

# Find objects not yet AI-verified
scai code find --where "codeStatus.aiVerification.status = 'pending'"
```

---

### `scai code convert --where`

Convert only a filtered subset of code units to Snowflake SQL. Objects that don’t match the filter are still parsed for dependency and symbol resolution, but only matched units produce converted output.

Copy code

```
scai code convert --where <WHERE_CLAUSE> [OPTIONS]
```

| Flag | Description |
| --- | --- |
| `--where <WHERE_CLAUSE>` | SQL-like filter to select which code units to convert |
| `--overwrite-working-directory` | Overwrite existing output files in the snowflake/ directory |
| `-x, --show-ewis` | Show detailed EWI table instead of summary |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Convert only procedures
scai code convert --where "source.objectType = 'procedure'"

# Convert objects in a single schema
scai code convert --where "source.schema = 'dbo'"

# Convert only tables and views
scai code convert --where "source.objectType IN ('table', 'view')"
```

> **Note:** Even when filtering, the converter still parses all source files for symbol resolution. This ensures that cross-object references (e.g., a procedure referencing a table) are resolved correctly, even if the referenced object is not in the `--where` filter.

---

### `scai code deploy --where`

Deploy a filtered subset of converted objects to Snowflake, instead of deploying everything.

Copy code

```
scai code deploy --where <WHERE_CLAUSE> [--include-dependencies] [OPTIONS]
```

| Flag | Description |
| --- | --- |
| `--where <WHERE_CLAUSE>` | SQL-like WHERE clause to filter objects to deploy |
| `--include-dependencies` | Also deploy the dependencies of the filtered code units. Has no effect without `--where`, since all code units are already included. |
| `-c, --connection <CONNECTION>` | Snowflake connection to use |
| `-d, --database` | Target database name for deployment |
| `-a, --all` | Deploy all successfully converted objects without selection prompt |
| `-r, --retry` | Number of retry attempts for failed deployments (default: 1) |
| `--continue-on-error` | Continue deploying remaining objects even if some fail (default: True) |
| `--warehouse <WAREHOUSE>` | Warehouse override (in-memory only, applied if connection has none) |
| `--schema <SCHEMA>` | Schema override (in-memory only) |
| `--role <ROLE>` | Role override (in-memory only) |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Deploy only tables
scai code deploy --where "target.objectType = 'table'"

# Deploy procedures and their dependencies (e.g. tables they reference)
scai code deploy --where "target.objectType = 'procedure'" --include-dependencies

# Deploy objects from a single schema
scai code deploy --where "source.schema = 'sales'"

# Deploy a specific object by name
scai code deploy --where "source.name = 'calculate_totals'"
```

**Why `--include-dependencies` matters:** When you filter with `--where`, you may select procedures that depend on tables or views. Without `--include-dependencies`, those dependent objects won’t be deployed, and the procedures may fail at runtime. Use this flag to automatically pull in everything the filtered objects need.

---

### `scai ai-convert start --where`

Send a filtered subset of objects for AI-powered conversion improvement, instead of processing everything.

Copy code

```
scai ai-convert start --where <WHERE_CLAUSE> [OPTIONS]
```

| Flag | Description |
| --- | --- |
| `--where <WHERE_CLAUSE>` | SQL-like WHERE clause to filter objects. Requires the code unit registry. |
| `-c, --connection <CONNECTION>` | Snowflake connection to use |
| `--selector <PATH>` | Path to object selector file (code-conversion-only projects). **Cannot be combined with `--where`.** |
| `-i, --instructions <PATH>` | Path to instructions file |
| `-w, --watch` | Wait for completion and show progress |
| `-y, --accept-disclaimers` | Skip disclaimer prompt |
| `--warehouse <WAREHOUSE>` | Warehouse override (in-memory only) |
| `--schema <SCHEMA>` | Schema override (in-memory only) |
| `--role <ROLE>` | Role override (in-memory only) |
| `--database <DATABASE>` | Database override (in-memory only) |

Expand

Show lessSee more

**Examples:**

Copy code

```
# AI-convert only tables
scai ai-convert start --where "target.objectType = 'table'"

# AI-convert objects from a specific schema
scai ai-convert start --where "source.schema = 'dbo'"

# AI-convert a single object by name
scai ai-convert start --where "source.name = 'calculate_totals'"

# Combine with other flags
scai ai-convert start --where "target.objectType = 'procedure'" -w -y
scai ai-convert start --where "source.schema = 'reporting'" -i config/instructions.yml
```

> **`--where` and `--selector` cannot be combined.** Use `--selector` when you have a selector file for a code-conversion-only project. Use `--where` for expressive filtering by type, schema, status, or any other registry field.

---

### `scai code accept --where`

Accept the latest artifact versions into the snowflake output folder for a filtered subset of objects. Without `--where`, all objects are accepted.

Copy code

```
scai code accept --where <WHERE_CLAUSE>
```

| Flag | Description |
| --- | --- |
| `--where <WHERE_CLAUSE>` | Filter expression to select which objects to accept |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Accept only tables
scai code accept --where "source.objectType = 'table'"

# Accept objects from a specific schema
scai code accept --where "source.schema = 'dbo'"

# Accept only successfully converted objects
scai code accept --where "codeStatus.conversion.status = 'completed'"
```

---

### `scai ai-convert accept --where`

Review and accept AI-suggested fixes for a filtered subset of objects, instead of reviewing everything.

Copy code

```
scai ai-convert accept [JOB_ID] --where <WHERE_CLAUSE> [OPTIONS]
```

| Flag | Description |
| --- | --- |
| `--where <WHERE_CLAUSE>` | SQL-like WHERE clause to filter which suggested fixes to accept. Full migration projects only. |
| `--all` | Accept all matching AI-suggested fixes without prompting |
| `-i, --interactive` | Review each matching code unit one by one |
| `--summary` | Preview affected code units without making changes (default) |
| `--json` | Output results in JSON format (for automation) |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Preview AI fixes for tables only
scai ai-convert accept --summary --where "source.objectType = 'table'"

# Accept all AI fixes for a specific schema
scai ai-convert accept --all --where "source.schema = 'sales'"

# Interactively review AI fixes for procedures
scai ai-convert accept -i --where "source.objectType = 'procedure'"
```

---

### `scai data migrate --where`

Migrate data from the source system to Snowflake for a filtered subset of tables. Available only for full migration projects (SQL Server, Redshift).

Copy code

```
scai data migrate --where <WHERE_CLAUSE> [OPTIONS]
```

| Flag | Description |
| --- | --- |
| `--where <WHERE_CLAUSE>` | SQL-like WHERE clause to filter tables from the Code Unit Registry |
| `-s, --source-connection <NAME>` | Source connection to extract data from |
| `-c, --connection <NAME>` | Snowflake connection to migrate data to |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Migrate only tables in the 'public' schema
scai data migrate --where "source.schema = 'public'"

# Migrate a specific table
scai data migrate --where "source.name = 'customers'"

# Migrate tables from a specific database
scai data migrate --where "source.database = 'retail_db'" --source-connection my-redshift
```

> **Note:** `--where` and `--selector` serve the same purpose (filtering tables) but for different project types. Use `--where` for full migration projects that have a Code Unit Registry. Use `--selector` for code-conversion-only projects.

---

### `scai data validate --where`

Compare data between source and Snowflake for a filtered subset of tables. Available only for full migration projects (SQL Server, Redshift).

Copy code

```
scai data validate --where <WHERE_CLAUSE> [OPTIONS]
```

| Flag | Description |
| --- | --- |
| `--where <WHERE_CLAUSE>` | SQL-like WHERE clause to filter tables from the Code Unit Registry |
| `-s, --source-connection <NAME>` | Source connection for validation |
| `-c, --connection <NAME>` | Snowflake connection for validation |
| `-d, --target-database <DATABASE>` | Target Snowflake database for validation |
| `-m, --db-mapping <MAPPING>` | Database name mapping (`source:target`) |
| `-e, --schema-mapping <MAPPING>` | Schema name mapping (`source:target`) |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Validate tables in the 'public' schema
scai data validate --where "source.schema = 'public'"

# Validate a specific table after migration
scai data validate --where "source.name = 'customers'"

# Validate with name mappings
scai data validate --where "source.schema = 'dbo'" --db-mapping "mydb:MY_DB" --schema-mapping "dbo:PUBLIC"
```

---

### Common `--where` scenarios

#### Re-process objects that failed conversion

After running `scai code convert`, some objects might have failed. Target just those for AI conversion:

Copy code

```
# First, see which objects failed
scai code find --where "codeStatus.conversion.status = 'failed'"

# Send only the failed ones for AI conversion
scai ai-convert start --where "codeStatus.conversion.status = 'failed'" -w
```

#### Run AI conversion on objects that haven’t been AI-verified yet

If you’ve already run AI conversion on some objects but not others, target the ones still pending:

Copy code

```
# Find objects that haven't gone through AI verification
scai code find --where "codeStatus.aiVerification.status = 'pending'"

# Convert just those
scai ai-convert start --where "codeStatus.aiVerification.status = 'pending'" -w
```

#### Focus on a specific object type in a specific schema

Copy code

```
# Preview: all procedures in the dbo schema
scai code find --where "source.schema = 'dbo' AND source.objectType = 'procedure'"

# Run AI conversion on them
scai ai-convert start --where "source.schema = 'dbo' AND source.objectType = 'procedure'" -w
```

#### Deploy only tables, then only procedures with dependencies

Copy code

```
# Deploy tables first
scai code deploy --where "target.objectType = 'table'"

# Then deploy procedures, pulling in any remaining dependencies
scai code deploy --where "target.objectType = 'procedure'" --include-dependencies
```

#### Incremental deployment of a single schema

Copy code

```
# Deploy everything in the 'sales' schema
scai code deploy --where "source.schema = 'sales'"
```

### Things to keep in mind

- **`--where` and `--selector` can’t be combined** (on `scai ai-convert start` and `scai ai-convert accept`). Use `--selector` for code-conversion-only projects with a short list, or `--where` for full migration projects with expressive filtering.
- **`--where` and `--selector` serve the same purpose** on `scai data migrate` and `scai data validate`. Use `--where` for full migration projects; use `--selector` for code-conversion-only projects.
- **The registry must exist.** You need to have run at least `scai code add` or `scai code extract` before `--where` will work. Otherwise you’ll get a “registry not found” error.
- **Use `scai code find` to preview.** Always test your filter with `scai code find --where "..."` before running a deployment or AI conversion job.
- **`scai code where` is the definitive reference.** The field list in this document covers the most common fields. Run `scai code where` for the full, always-up-to-date list of fields, operators, and examples.

---

## AI Convert Quick Guide

Use `scai ai-convert` to improve your converted code with AI. It uploads your converted SQL to Snowflake, analyzes it for functional equivalence issues, generates regression tests, and produces improved code.

**Supported languages:** SQL Server, Redshift, BigQuery, PostgreSQL

### Before you start

- A project initialized with `scai init`
- Code already converted with `scai code convert`
- A Snowflake connection configured via `snow connection add`
- `CREATE MIGRATION` privilege on your Snowflake account
- A warehouse set in the connection

### Basic usage

Copy code

```
# Convert all objects (default behavior)
scai ai-convert start

# Convert and wait for it to finish (can take minutes to hours depending on code size)
scai ai-convert start -w

# Skip the disclaimer prompt (handy for CI/CD)
scai ai-convert start -y -w

# Convert only specific objects by name
scai ai-convert start -o MY_PROC,MY_VIEW

# Use an instructions file for source system verification
scai ai-convert start -i config/instructions.yml
```

For filtering objects with `--where`, see the [Filtering Objects with the `--where` Clause](#filtering-objects-with-the---where-clause) section above.

### Managing jobs

Once a job is running, you’ve got a few commands to work with:

Copy code

```
# Check the last job's status
scai ai-convert status

# Check a specific job
scai ai-convert status JOB_20260310_ABC

# Wait for a job to finish and download results
scai ai-convert status -w

# List all jobs for this project
scai ai-convert list

# Cancel a running job
scai ai-convert cancel
```

### Accepting AI fixes

After a job completes, review what the AI suggested and decide what to keep:

Copy code

```
# Preview what changed (default -- no files modified)
scai ai-convert accept --summary

# Review each fix interactively (accept, skip, or diff)
scai ai-convert accept -i

# Accept everything at once
scai ai-convert accept --all

# JSON output for automation
scai ai-convert accept --summary --json
```

### Output structure

Results land in the `ai-converted/` directory inside your project:

Copy code

```
ai-converted/
  └── JOB_<timestamp>_<id>/
      ├── fixed/           AI-improved SQL files organized by object type/schema
      └── tests_sql/       Generated regression tests organized by database/schema
```

### All `ai-convert start` options

| Flag | Short | Description |
| --- | --- | --- |
| `--connection` | `-c` | Snowflake connection to use |
| `--objects` | `-o` | Comma-separated object names, or `'all'` (default). Cannot be combined with `--where`. |
| `--where` |  | SQL-like WHERE clause to filter objects (see [Filtering Objects](#filtering-objects-with-the---where-clause)) |
| `--instructions` | `-i` | Path to instructions file for custom config |
| `--watch` | `-w` | Wait for completion and show progress |
| `--accept-disclaimers` | `-y` | Skip disclaimer prompt |
| `--warehouse` |  | Override warehouse (in-memory only) |
| `--schema` |  | Override schema (in-memory only) |
| `--role` |  | Override role (in-memory only) |
| `--database` |  | Override database (in-memory only) |

Expand

Show lessSee more

---

## Workflow Examples

### Example 1: Migrate Oracle Stored Procedures

Copy code

```
# Create project
scai init oracle-migration -l Oracle
cd oracle-migration

# Add your PL/SQL files
scai code add -i ./oracle-procs/

# Convert
scai code convert

# Review converted code in snowflake/ folder, then deploy
scai code deploy --all
```

### Example 2: SQL Server End-to-End with Specific Schema

Copy code

```
# Create project
scai init sqlserver-migration -l SqlServer
cd sqlserver-migration

# Add connection
scai connection add-sql-server

# Extract only the 'sales' schema
scai code extract --schema sales

# Convert
scai code convert

# Deploy
scai code deploy
```

### Example 3: AI Convert After Code Conversion

Copy code

```
# Create project
scai init ai-convert-demo -l SqlServer
cd ai-convert-demo

# Add connection
scai connection add-sql-server

# Extract and convert
scai code extract
scai code convert

# Start AI code conversion and wait for completion
scai ai-convert start -w

# Review last executed job results
scai ai-convert status

# Review executed job list
scai ai-convert list
```

### Example 4: Selective Migration Using `--where`

Copy code

```
# Create project and convert
scai init selective-demo -l SqlServer
cd selective-demo
scai connection add-sql-server
scai code extract
scai code convert

# Preview what failed conversion
scai code find --where "issues IS NOT NULL AND issues != '[]'"

# Send failed objects through AI conversion
scai ai-convert start --where "issues IS NOT NULL AND issues != '[]'" -w -y

# Deploy only tables first
scai code deploy --where "target.objectType = 'table'"

# Deploy procedures with their dependencies
scai code deploy --where "target.objectType = 'procedure'" --include-dependencies
```

---

## Getting Help

Use –help with any command to see available options:

Copy code

```
scai --help
scai init --help
scai code convert --help
scai code where
scai connection add-redshift --help
```

## Troubleshooting

“Project file not found”
You must run commands from within a project directory. Navigate to your project folder (where the .scai/ directory exists) before running commands:

Copy code

```
cd <project-folder>
scai code convert
```

“Connection not found” (source database)

1. List your connections: `scai connection list -l <language>`
2. Add a connection if needed: `scai connection add-sql-server` or `scai connection add-redshift`
3. Or set a default: `scai connection set-default -l <language> --connection-name <name>`

“Authentication failed” for Snowflake

The SCAI CLI uses your Snowflake CLI configuration. Ensure your connection is working:

Make sure you have a default Snowflake connection configured in the Snowflake CLI (used when no connection name is specified).

Copy code

```
# List available Snowflake connections
snow connection list

# Test your connection
snow connection test

# Add a new connection if needed
snow connection add
```

“Registry not found” when using `--where`

The `--where` flag requires a Code Unit Registry, which is created when you run `scai code add` or `scai code extract`. Make sure you’ve run one of those commands before using `--where`:

Copy code

```
# For file-based projects
scai code add -i /path/to/source

# For SQL Server / Redshift extraction
scai code extract
```

## Supported Source Dialects

| Dialect | Extract | Convert | Deploy |
| --- | --- | --- | --- |
| SQL Server | X | X | X |
| Redshift | X | X | X |
| Oracle |  | X |  |
| Teradata |  | X |  |
| BigQuery |  | X |  |
| Databricks |  | X |  |
| Greenplum |  | X |  |
| Sybase |  | X |  |
| PostgreSQL |  | X |  |
| Netezza |  | X |  |
| Spark |  | X |  |
| Vertica |  | X |  |
| Hive |  | X |  |
| DB2 |  | X |  |

Expand

Show lessSee more

## Complete CLI Reference

For quick reference, here is every top-level command and subcommand available in the `scai` CLI:

| Command | Subcommands | Description |
| --- | --- | --- |
| `scai init` |  | Create a new migration project |
| `scai project` | `info`, `set-default-connection` | View and manage project configuration |
| `scai connection` | `add-sql-server`, `add-redshift`, `set-default`, `list`, `test` | Manage source database connections |
| `scai code` | `add`, `extract`, `convert`, `deploy`, `find`, `accept`, `where`, `resync` | Manage code migration operations |
| `scai ai-convert` | `start`, `status`, `cancel`, `list`, `accept` | AI-powered conversion improvement |
| `scai data` | `migrate`, `validate` | Data migration and validation |
| `scai test` | `seed`, `capture`, `validate` | Generate and run test cases for stored procedures |
| `scai object-selector` | `create` | Generate selector files for filtering objects |
| `scai query` |  | Execute SQL queries on source database systems |
| `scai license` | `install` | Manage offline license operations |
| `scai terms` | `accept` | View and accept terms and conditions |
| `scai logs` |  | Show log directory and recent log files |

Expand

Show lessSee more
